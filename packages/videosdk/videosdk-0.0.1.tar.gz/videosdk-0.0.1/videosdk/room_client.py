import asyncio
from asyncio import (
    AbstractEventLoop,
    Future,
    Task,
    get_event_loop,
    new_event_loop,
    run,
    set_event_loop,
    wait_for,
    TimeoutError,
    sleep,
)
from dataclasses import dataclass
import json
import logging
import time
from ._events import Events
from typing import Any, Awaitable, Dict, Optional, Union, TypedDict, TypeVar
from random import random
from pyee import AsyncIOEventEmitter
from websockets import connect
from .exceptions import InternalServerError
from vsaiortc.mediastreams import AudioStreamTrack, MediaStreamTrack, VideoStreamTrack
from vsaiortc.rtcconfiguration import RTCIceServer
from .lib.pymediasoup.consumer import Consumer
from .lib.pymediasoup.device import Device
from .lib.pymediasoup.handlers.aiortc_handler import AiortcHandler
from .lib.pymediasoup.models.transport import DtlsParameters
from .lib.pymediasoup.producer import Producer
from .lib.pymediasoup.rtp_parameters import RtpParameters
from .lib.pymediasoup.transport import Transport
from .utils import ServerConfig, get_server_config


def generateRandomNumber():
    return round(random() * 10000000)


T = TypeVar("T")

# Tasks
TASK_INCOMING_MESSAGES = "TASK_INCOMING_MESSAGES"
TASK_JOIN = "TASK_JOIN"
TASK_LEAVE = "TASK_LEAVE"
TASK_CLOSE = "TASK_CLOSE"
TASK_SEND_MESSAGES = "TASK_SEND_MESSAGES"
TASK_ANY = "TASK_ANY"


@dataclass
class RoomClientConfig(TypedDict, total=False):
    room_id: str
    peer_id: str
    secret: str
    display_name: str
    mode: str
    produce: bool
    consume: bool
    use_sharing_simulcast: bool
    datachannel: bool
    mic_enabled: bool
    webcam_enabled: bool
    custom_camera_video_track: Optional[VideoStreamTrack]
    custom_microphone_audio_track: Optional[AudioStreamTrack]
    auto_consume: bool
    preferred_protocol: str
    signaling_base_url: str
    meta_data: Optional[Dict[str, Any]]
    default_camera_index: int
    debug_mode: bool
    loop: AbstractEventLoop


class RoomClient(AsyncIOEventEmitter):
    def __init__(self, **kwargs: Union[RoomClientConfig, Any]):
        """
        Initialize RoomClient with configuration parameters.
        """
        super(RoomClient, self).__init__(loop=kwargs.get("loop"))
        self.__loop: AbstractEventLoop = kwargs.get("loop") or asyncio.get_event_loop()
        if self.__loop is None:
            try:
                self.__loop = asyncio.get_event_loop()
            except RuntimeError as e:
                raise InternalServerError(e)
        self.__room_id: str = kwargs.get("room_id")
        self.__peer_id: str = kwargs.get("peer_id")
        self.__secret: str = kwargs.get("secret")
        self.__signaling_base_url: str = kwargs.get("signaling_base_url")
        self.__device: Device = None
        self.__mode: str = kwargs.get("mode")
        self.__produce: bool = kwargs.get("produce")
        self.__consume: bool = kwargs.get("consume")
        self.__use_sharing_simulcast: bool = kwargs.get("use_sharing_simulcast")
        self.__use_datachannel: bool = kwargs.get("datachannel")

        self.__auto_consume: bool = kwargs.get("auto_consume")
        self.__preferred_protocol: str = kwargs.get("preferred_protocol")
        self.__debug_mode: bool = kwargs.get("debug_mode")

        self.__generate_random_number = generateRandomNumber
        self.__websocket = None
        self.__tasks: dict[str, Task] = {}
        self.__answers: Dict[str, Future] = {}

        self.__send_transport: Optional[Transport] = None
        self.__recv_transport: Optional[Transport] = None
        self.__ice_servers: list[RTCIceServer] = []

        self.__custom_camera_video_track: Optional[VideoStreamTrack] = kwargs.get(
            "custom_camera_video_track"
        )
        self.__custom_microphone_audio_track: Optional[AudioStreamTrack] = kwargs.get(
            "custom_microphone_audio_track"
        )
        self.__audio_stream_track = (
            AudioStreamTrack()
            if self.__custom_microphone_audio_track is None
            else self.__custom_microphone_audio_track
        )
        self.__video_stream_track = (
            VideoStreamTrack()
            if self.__custom_camera_video_track is None
            else self.__custom_camera_video_track
        )

        self.__producers = []
        self.__consumers: dict[str, Consumer] = {}
        self.__audio_producer = None
        self.__video_producer = None

        self.display_name: str = kwargs.get("display_name")
        self.mic_enabled: bool = kwargs.get("mic_enabled")
        self.webcam_enabled: bool = kwargs.get("webcam_enabled")

        self.meta_data: Optional[Dict[str, Any]] = kwargs.get("meta_data")
        self.default_camera_index: int = kwargs.get("default_camera_index")
        self._closed = False
        self._joined = False

        logging.debug("mic_enabled: %s", self.mic_enabled)
        logging.debug("webcam_enabled: %s", self.webcam_enabled)
        logging.debug("consume: %s", self.__produce)
        logging.debug("produce: %s", self.__consume)
        logging.debug(f"Meeting Room Client initialized with room_id: {self.__room_id}")

    def join(self):
        """
        Join the meeting room.
        """
        try:
            self.__tasks[TASK_JOIN] = asyncio.ensure_future(self.async_join())
        except Exception as e:
            logging.error("Failed to Join", exc_info=True)
            self.__emit_error("Failed to Join in the Meeting")

    async def async_join(self):
        """
        Asynchronously join the meeting room.
        """
        try:
            if not self._joined:
                self._joined = True
                server_config: ServerConfig = get_server_config(
                    self.__room_id, self.__secret, self.__signaling_base_url
                )

                base_url = server_config["base_url"]
                signaling_url = server_config["signaling_url"]
                self.__ice_servers = server_config["ice_servers"]

                self.emit(Events.MEETING_STATE_CHANGED, {"state": "CONNECTING"})

                websocket_url = (
                    signaling_url
                    if signaling_url is not None
                    else f"wss://{base_url}/?roomId={self.__room_id}&peerId={self.__peer_id}&secret={self.__secret}&mode={self.__mode}"
                )

                self.__websocket = await connect(
                    websocket_url, subprotocols=["protoo"], ping_interval=2000
                )

                self.emit(Events.MEETING_STATE_CHANGED, {"state": "CONNECTED"})

                # create thread
                self.__tasks[TASK_INCOMING_MESSAGES] = asyncio.ensure_future(
                    self.__handle_incoming_messages()
                )

                await self.handle_device_load()
                await self.handle_send_transport()
                await self.handle_recv_transport()
                await self.handle_join()

                if self.__produce:
                    await self.handle_produce()

                logging.debug("Meeting joined")
                self.emit(Events.MEETING_JOINED)

        except Exception as e:
            logging.debug("ERROR", e)
            self.emit(Events.MEETING_STATE_CHANGED, {"state": "FAILED"})
            if self.__websocket:
                await self.__websocket.close()
            if self.__send_transport:
                await self.__send_transport.close()
            if self.__recv_transport:
                await self.__recv_transport.close()

            logging.error("Failed to Join", exc_info=True)
            self.__emit_error("Failed to Join in the Meeting")

    async def __send_request(self, request):
        self.__answers[request["id"]] = asyncio.get_event_loop().create_future()
        await self.__websocket.send(json.dumps(request))

    async def __wait_for(
        self, fut: Awaitable[T], timeout: Optional[float], **kwargs: Any
    ) -> T:
        try:
            return await wait_for(fut, timeout=timeout, **kwargs)
        except TimeoutError:
            logging.error("signal :: Timeout")
            self.__emit_error("Operation timed out")

    async def __handle_incoming_messages(self):
        try:
            async for Data in self.__websocket:
                message: Dict[str, Any] = json.loads(Data)
                if message.get("response"):
                    self.__handle_responses(message)
                elif message.get("request"):
                    await self.__handle_requests(message)
                elif message.get("notification"):
                    await self.__handle_notifications(message)
        except Exception as e:
            logging.error(
                "signal :: error while handling signal messages", exc_info=True
            )
            self.__emit_error("Internal socket Error")

    def __handle_responses(self, message: Dict[str, Any]):
        try:
            logging.debug(f"signal :: response message :: {message}")
            if message.get("id") is not None:
                self.__answers[message.get("id")].set_result(message)
        except Exception as e:
            logging.error(
                "signal :: error while handling signal messages", exc_info=True
            )
            self.__emit_error("Internal socket Error")

    async def __handle_requests(self, message: Dict[str, Any]):
        try:
            logging.debug(f"signal :: request message :: {message}")
            if message.get("method") == "close":
                self.leave()
            if message.get("method") == "newConsumer":
                if self.__consume:
                    await self.handleConsume(
                        id=message["data"]["id"],
                        producerId=message["data"]["producerId"],
                        kind=message["data"]["kind"],
                        rtpParameters=message["data"]["rtpParameters"],
                        peerId=message["data"]["peerId"],
                        appData=message["data"]["appData"],
                    )
                    await self.__accept(message=message)
                else:
                    logging.debug("I don't want to consume newConsumer event")
                    await self.__reject(
                        message=message["data"],
                        code=403,
                        reason="I don't want to consume",
                    )

            if message.get("method") == "newDataConsumer":
                if self.__consume:
                    await self.__accept(message=message)
                else:
                    logging.debug("I don't want to consume newDataConsumer event")
                    await self.__reject(
                        message=message["data"],
                        code=403,
                        reason="I don't want to consume",
                    )

            if message.get("method") == "enabledMic":
                logging.debug("signal :: enable mic received")
                self.emit(Events.MIC_REQUESTED, message["data"])
                await self.__accept(message=message)

            if message.get("method") == "disableMic":
                logging.debug("signal :: disable mic received")
                await self.async_disable_mic()
                await self.__accept(message=message)

            if message.get("method") == "enableWebcam":
                logging.debug("signal :: enable webcam received")
                self.emit(Events.WEBCAM_REQUESTED, message["data"])
                await self.__accept(message=message)

            if message.get("method") == "disableWebcam":
                logging.debug("signal :: disable webcam received")
                await self.async_disable_webcam()
                await self.__accept(message=message)
        except Exception as e:
            logging.error("signal :: Error while websocket request: ", e)
            self.__emit_error("Internal socket Error")

    async def __handle_notifications(self, message: Dict[str, Any]):
        try:
            logging.debug(f"signal :: notification message :: {message}")
            if message["method"] == "producerScore":
                producerId = message["data"]["producerId"]
                score = message["data"]["score"]
                logging.debug(f"signal :: producer score {producerId} :: {score}")

            if message["method"] == "newPeer":
                peerId = message["data"]["id"]
                logging.debug(f"signal :: peer connected {peerId}")
                self.emit(Events.ADD_PEER, message["data"])

            if message["method"] == "peerClosed":
                peerId = message["data"]["peerId"]
                logging.debug(f"signal :: peer disconnected {peerId}")
                self.emit(Events.REMOVE_PEER, message["data"])

            if message["method"] == "consumerClosed":
                consumerId = message["data"]["consumerId"]
                logging.debug(f"signal :: consumer closed {consumerId}")
                if consumerId in self.__consumers:
                    consumer = self.__consumers.pop(consumerId)
                    self.emit(Events.REMOVE_CONSUMER, consumer)
                    del consumer

            if message["method"] == "consumerPaused":
                consumerId = message["data"]["consumerId"]
                logging.debug(f"signal :: consumer paused {consumerId}")

            if message["method"] == "consumerResumed":
                consumerId = message["data"]["consumerId"]
                logging.debug(f"signal :: consumer resumed {consumerId}")

            if message["method"] == "consumerLayersChanged":
                consumerId = message["data"]["consumerId"]
                logging.debug(f"signal :: consumer layers changed {consumerId}")
                spatialLayer = message["data"]["spatialLayer"]
                temporalLayer = message["data"]["temporalLayer"]
                if consumerId in self.__consumers:
                    consumer: Consumer = self.__consumers.get(consumerId)
                    if len(consumer.appData["encodings"]) > 1:
                        self.emit(
                            Events.VIDEO_QUALITY_CHANGED,
                            {
                                "peerId": consumer.appData["peerId"],
                                "prevQuality": "HIGH",
                                "currentQuality": "HIGH",
                            },
                        )

            if message["method"] == "activeSpeaker":
                logging.debug(f"signal :: active speaker changed")
                self.emit(Events.SET_ROOM_ACTIVE_SPEAKER, message["data"])
            if message["method"] == "participantMediaStateChanged":
                logging.debug(
                    f"signal :: participant media state changed {message['data']}"
                )
                self.emit(Events.PARTICIPANT_MEDIA_STATE_CHANGED, message["data"])
        except Exception as e:
            logging.error(
                "signal :: Error processing websocket notification", exc_info=True
            )
            self.__emit_error("Internal socket Error")

    async def handle_device_load(self):
        try:
            # Init device
            self.__device = Device(
                handlerFactory=AiortcHandler.createFactory(
                    tracks=[self.__audio_stream_track, self.__video_stream_track]
                )
            )

            # Get Router RtpCapabilities
            reqId = self.__generate_random_number()
            req = {
                "request": True,
                "id": reqId,
                "method": "getRouterRtpCapabilities",
                "data": {},
            }
            await self.__send_request(req)
            ans = await self.__wait_for(self.__answers[reqId], timeout=15)

            # Load Router RtpCapabilities
            await self.__device.load(ans["data"])

            logging.debug(f"RTC :: device loaded at ::  {time.time()}")
        except Exception as e:
            logging.error("RTC :: error while device loading", exc_info=True)
            self.__emit_error("Error while Device Load")

    async def handle_send_transport(self):
        if self.__send_transport != None:
            logging.debug("RTC :: Send Transport is already created")
            return
        try:
            # Send create sendTransport request
            reqId = self.__generate_random_number()
            req = {
                "request": True,
                "id": reqId,
                "method": "createWebRtcTransport",
                "data": {
                    "preferredProtocol": self.__preferred_protocol,
                    "forceTcp": False,
                    "producing": True,
                    "consuming": False,
                    "sctpCapabilities": (
                        self.__device.sctpCapabilities.dict()
                        if self.__use_datachannel
                        else None
                    ),
                },
            }
            await self.__send_request(req)
            ans = await self.__wait_for(self.__answers[reqId], timeout=15)

            # Create sendTransport
            self.__send_transport = self.__device.createSendTransport(
                id=ans["data"]["id"],
                iceParameters=ans["data"]["iceParameters"],
                iceCandidates=ans["data"]["iceCandidates"],
                dtlsParameters=ans["data"]["dtlsParameters"],
                sctpParameters=ans["data"]["sctpParameters"],
                iceServers=self.__ice_servers,
            )
            logging.debug(f"RTC :: send transport created {time.time()}")
        except Exception as e:
            logging.error(
                "RTC :: error while send createWebRtcTransport()", exc_info=True
            )
            self.__emit_error("Error while Creating Send Transport")

        @self.__send_transport.on("connect")
        async def on_connect(dtlsParameters: DtlsParameters):
            try:
                logging.debug(f"RTC :: send transport connecting at ::  {time.time()}")
                reqId = self.__generate_random_number()
                req = {
                    "request": True,
                    "id": reqId,
                    "method": "connectWebRtcTransport",
                    "data": {
                        "transportId": self.__send_transport.id,
                        "dtlsParameters": dtlsParameters.dict(exclude_none=True),
                    },
                }
                await self.__send_request(req)
                ans = await self.__wait_for(self.__answers[reqId], timeout=15)
                logging.debug(f"RTC :: send transport connected at ::  {time.time()}")
            except Exception as e:
                logging.error(
                    "RTC :: error while send connectWebRtcTransport()", exc_info=True
                )
                self.__emit_error("Error while Connecting Send Transport")

        @self.__send_transport.on("produce")
        async def on_produce(kind: str, rtpParameters: RtpParameters, appData: dict):
            try:
                reqId = self.__generate_random_number()
                req = {
                    "id": reqId,
                    "method": "produce",
                    "request": True,
                    "data": {
                        "transportId": self.__send_transport.id,
                        "kind": kind,
                        "rtpParameters": rtpParameters.dict(exclude_none=True),
                        "appData": appData,
                    },
                }
                await self.__send_request(req)
                ans = await self.__wait_for(self.__answers[reqId], timeout=15)
                return ans["data"]["id"]
            except Exception as e:
                logging.error("RTC :: error while produce()", exc_info=True)
                self.__emit_error("Error while Producing Media")

        logging.debug(f"RTC :: send transport handled at ::  {time.time()}")

    async def handle_join(self):
        try:
            # Join room
            reqId = self.__generate_random_number()
            req = {
                "request": True,
                "id": reqId,
                "method": "join",
                "data": {
                    "autoConsume": self.__auto_consume,
                    "secret": self.__secret,
                    "displayName": self.display_name,
                    "device": "Unknown",
                    "deviceInfo": {
                        "sdkType": "prebuilt",
                        "sdkVersion": "0.3.37",
                        "platform": "desktop",
                    },
                    "rtpCapabilities": self.__device.rtpCapabilities.dict(
                        exclude_none=True
                    ),
                    "sctpCapabilities": self.__device.sctpCapabilities.dict(
                        exclude_none=True
                    ),
                },
            }
            await self.__send_request(req)
            ans = await self.__wait_for(self.__answers[reqId], timeout=15)
            logging.debug(f"RTC :: joined into meeting {time.time()}")
        except Exception as e:
            logging.error("RTC :: error while join()", exc_info=True)
            self.__emit_error("Error while Join")

    async def handle_produce(self):
        # produce
        try:
            await self.async_enable_webcam()
            logging.debug(
                "RTC :: sendtransport :: videoProducer created successfully..."
            )
        except Exception as e:
            logging.error("RTC :: error while create video producer", exc_info=True)
            self.__emit_error("Error while Producing Video")

        try:
            await self.async_enable_mic()
            logging.debug(
                "RTC :: sendtransport :: audioProducer created successfully..."
            )
        except Exception as e:
            logging.error("RTC :: error while creating audio producer", exc_info=True)
            self.__emit_error("Error while Producing Audio")

    async def handle_recv_transport(self):
        if self.__recv_transport != None:
            return
        try:
            # Send create recvTransport request
            reqId = self.__generate_random_number()
            req = {
                "request": True,
                "id": reqId,
                "method": "createWebRtcTransport",
                "data": {
                    "preferredProtocol": self.__preferred_protocol,
                    "forceTcp": False,
                    "producing": False,
                    "consuming": True,
                    "sctpCapabilities": (
                        self.__device.sctpCapabilities.dict()
                        if self.__use_datachannel
                        else None
                    ),
                },
            }
            await self.__send_request(req)
            ans = await self.__wait_for(self.__answers[reqId], timeout=15)

            # Create recvTransport
            self.__recv_transport = self.__device.createRecvTransport(
                id=ans["data"]["id"],
                iceParameters=ans["data"]["iceParameters"],
                iceCandidates=ans["data"]["iceCandidates"],
                dtlsParameters=ans["data"]["dtlsParameters"],
                sctpParameters=ans["data"]["sctpParameters"],
                iceServers=self.__ice_servers,
            )

            logging.debug(f"RTC :: recv transport created {time.time()}")
        except Exception as e:
            logging.error(
                "RTC :: error while recv createWebRtcTransport()", exc_info=True
            )
            self.__emit_error("Error while Creating Recv Transport")

        @self.__recv_transport.on("connect")
        async def on_connect(dtlsParameters: DtlsParameters):
            try:
                logging.debug(
                    f"RTC :: recv WebRtcTransport connectWebRtcTransport {time.time()}"
                )
                reqId = self.__generate_random_number()
                req = {
                    "request": True,
                    "id": reqId,
                    "method": "connectWebRtcTransport",
                    "data": {
                        "transportId": self.__recv_transport.id,
                        "dtlsParameters": dtlsParameters.dict(exclude_none=True),
                    },
                }
                await self.__send_request(req)
                ans = await self.__wait_for(self.__answers[reqId], timeout=15)
            except Exception as e:
                logging.error(
                    "RTC :: error while recv connectWebRtcTransport()", exc_info=True
                )
                self.__emit_error("Error while Connecting Recv Transport")

        logging.debug(f"RTC :: recv transport handled at ::  {time.time()}")

    async def handleConsume(
        self,
        id,
        producerId,
        kind,
        rtpParameters: Union[RtpParameters, dict],
        peerId,
        appData,
    ) -> Consumer:
        try:
            if self.__recv_transport == None:
                await self.handle_recv_transport()

            logging.debug(f"creating {kind} consumer for participant :: {peerId}")
            consumer: Consumer = await self.__recv_transport.consume(
                id=id,
                producerId=producerId,
                kind=kind,
                rtpParameters=rtpParameters,
                appData=appData,
            )

            @consumer.on("transportClose")
            def on_consumer_transport_closed():
                logging.debug(f"consumer transport closed {consumer.id}")

            @consumer.observer.on("close")
            def on_consumer_closed():
                logging.debug(f"consumer closed {consumer.id}")

            logging.debug(f"created {kind} consumer for participant :: {peerId}")

            self.__consumers[consumer.id] = consumer

            self.emit(Events.ADD_CONSUMER, consumer)

        except Exception as e:
            logging.error("RTC :: error while Creating Consumer", exc_info=True)
            self.__emit_error("Error while Consume")

    async def __accept(self, message):
        response = {
            "response": True,
            "id": message["id"],
            "ok": True,
            "data": {},
        }
        await self.__websocket.send(json.dumps(response))

    async def __reject(self, message, code, reason):
        response = {
            "response": True,
            "id": message["id"],
            "ok": False,
            "errorCode": code,
            "errorReason": reason,
        }
        await self.__websocket.send(json.dumps(response))

    def __emit_error(self, message: str):
        self.emit(Events.ERROR, message)

    def enable_webcam(self):
        logging.debug(f"RTC :: webcam_enabled {self.webcam_enabled}")
        if self.webcam_enabled:
            self.__tasks[f"{TASK_ANY}-enable-webcam"] = asyncio.ensure_future(
                self.async_enable_webcam()
            )

    async def async_enable_webcam(
        self, custom_track: Optional[MediaStreamTrack] = None
    ):
        try:
            logging.debug(f"RTC :: webcam_enabled {self.webcam_enabled}", time.time())
            if self.webcam_enabled or custom_track != None:
                if custom_track is not None:
                    self.__video_producer: Producer = (
                        await self.__send_transport.produce(
                            track=custom_track, stopTracks=False, appData={}
                        )
                    )
                else:
                    self.__video_producer: Producer = (
                        await self.__send_transport.produce(
                            track=self.__video_stream_track,
                            stopTracks=False,
                            appData={},
                        )
                    )
                logging.debug(f"RTC :: video producer created :: {time.time()}")

                @self.__video_producer.on("transportclose")
                def on_producer_transport_closed():
                    logging.debug(
                        f"video producer transport closed {self.__video_producer.id}"
                    )
                    self.emit(Events.REMOVE_PRODUCER, self.__video_producer)

                @self.__video_producer.observer.on("close")
                def on_producer_close():
                    logging.debug(f"video producer close :: {self.__video_producer.id}")

                @self.__video_producer.observer.on("pause")
                def on_producer_close():
                    logging.debug(f"video producer pause :: {self.__video_producer.id}")

                @self.__video_producer.observer.on("resume")
                def on_producer_close():
                    logging.debug(
                        f"video producer resume :: {self.__video_producer.id}"
                    )

                self.emit(Events.ADD_PRODUCER, self.__video_producer)
                self.__producers.append(self.__video_producer)
        except Exception as e:
            logging.error("MEDIA :: error while Enable Webcam", exc_info=True)
            self.__emit_error("Not Able to Enable Webcam")

    def disable_webcam(self):
        logging.debug(f"RTC :: webcam_enabled {self.webcam_enabled}")
        if self.webcam_enabled:
            self.__tasks[f"{TASK_ANY}-disable-webcam"] = asyncio.ensure_future(
                self.async_disable_webcam()
            )

    async def async_disable_webcam(self):
        try:
            reqId = self.__generate_random_number()
            req = {
                "request": True,
                "id": reqId,
                "method": "closeProducer",
                "data": {"producerId": self.__video_producer.id},
            }

            await self.__video_producer.close()
            await self.__send_request(req)
            await self.__wait_for(self.__answers[reqId], timeout=15)

            self.emit(Events.REMOVE_PRODUCER, self.__video_producer)
            self.__producers.remove(self.__video_producer)
        except Exception as e:
            logging.error("MEDIA :: error while Disable Webcam", exc_info=True)
            self.__emit_error("Not Able to Disbale Webcam")

    def enable_mic(self):
        logging.debug(f"RTC :: mic_enabled {self.mic_enabled}")
        if self.mic_enabled:
            self.__tasks[f"{TASK_ANY}-enable-mic"] = asyncio.ensure_future(
                self.async_enable_mic()
            )

    async def async_enable_mic(self):
        try:
            logging.debug(f"RTC :: mic_enabled {self.mic_enabled}")
            if self.mic_enabled:
                self.__audio_producer: Producer = await self.__send_transport.produce(
                    track=self.__audio_stream_track,
                    appData={},
                )
                logging.debug(f"RTC :: audio producer created :: {time.time()}")

                @self.__audio_producer.on("transportclose")
                def on_producer_transport_closed():
                    logging.debug(
                        f"audio producer transport closed {self.__audio_producer.id}"
                    )
                    self.emit(Events.REMOVE_PRODUCER, self.__audio_producer)

                @self.__audio_producer.observer.on("close")
                def on_producer_close():
                    logging.debug(f"audio producer close :: {self.__audio_producer.id}")

                @self.__audio_producer.observer.on("pause")
                def on_producer_close():
                    logging.debug(f"audio producer pause :: {self.__audio_producer.id}")

                @self.__audio_producer.observer.on("resume")
                def on_producer_close():
                    logging.debug(
                        f"audio producer resume :: {self.__audio_producer.id}"
                    )

                self.emit(Events.ADD_PRODUCER, self.__audio_producer)
                self.__producers.append(self.__audio_producer)
        except Exception as e:
            logging.error("MEDIA :: error while Enable Mic", exc_info=True)
            self.__emit_error("Not Able to Enable Mic")

    def disable_mic(self):
        logging.debug(f"RTC :: mic_enabled {self.mic_enabled}")
        if self.mic_enabled:
            self.__tasks[f"{TASK_ANY}-disable-mic"] = asyncio.ensure_future(
                self.async_disable_mic()
            )

    async def async_disable_mic(self):
        try:
            reqId = self.__generate_random_number()
            req = {
                "request": True,
                "id": reqId,
                "method": "closeProducer",
                "data": {"producerId": self.__audio_producer.id},
            }
            await self.__audio_producer.close()
            await self.__send_request(req)
            await self.__wait_for(self.__answers[reqId], timeout=15)

            self.emit(Events.REMOVE_PRODUCER, self.__audio_producer)
            self.__producers.remove(self.__audio_producer)
        except Exception as e:
            logging.error("MEDIA :: error while Disable Mic", exc_info=True)
            self.__emit_error("Not Able to Disable Mic")

    def leave(self):
        """
        Leave the meeting room.
        """
        try:
            self.__tasks[f"{TASK_ANY}-leave"] = asyncio.ensure_future(
                self.async_leave()
            )
        except Exception as e:
            logging.error("Failed to Leave", exc_info=True)
            self.__emit_error("Failed to Leave from the Meeting")

    async def async_leave(self):
        """
        Asynchronously leave the meeting room.
        """
        try:
            self.emit(Events.MEETING_STATE_CHANGED, {"state": "CLOSING"})

            if self._closed:
                return
            self._closed = True

            if self.__websocket:
                logging.debug("closing websocket")
                await self.__websocket.close()

            if self.__send_transport:
                logging.debug("---> closing send transport connection")
                await self.__send_transport.close()
                if self.__audio_producer is not None:
                    await self.__audio_producer.close()
                if self.__video_producer is not None:
                    await self.__video_producer.close()

            if self.__recv_transport:
                logging.debug("---> closing recv transport connection")
                await self.__recv_transport.close()

            self.__clean()

            self.emit(Events.MEETING_STATE_CHANGED, {"state": "CLOSED"})
            self.emit(Events.MEETING_LEFT)

        except Exception as e:
            logging.error("Failed to Leave", exc_info=True)
            self.__emit_error("Failed to Leave from the Meeting")

    def close(self):
        """
        Close the RoomClient instance.
        """
        try:
            self.__tasks[f"{TASK_ANY}-close"] = asyncio.ensure_future(
                self.async_close()
            )
        except Exception as e:
            logging.error("Failed to Close", exc_info=True)
            self.__emit_error("Failed to Close the Meeting")

    async def async_close(self):
        """
        Asynchronously close the RoomClient instance.
        """
        try:
            if self.__websocket:
                reqId = self.__generate_random_number()
                req = {
                    "request": True,
                    "id": reqId,
                    "method": "closeRoom",
                    "data": {},
                }
                await self.__send_request(req)
                await self.__wait_for(self.__answers[reqId], timeout=15)
        except Exception as e:
            logging.error("Failed to Close", exc_info=True)
            self.__emit_error("Failed to Close the Meeting")

    def enable_peer_mic(self, peerId):
        self.__tasks[f"{TASK_ANY}-enable-peer-mic"] = asyncio.ensure_future(
            self.async_enable_peer_mic(peerId)
        )

    async def async_enable_peer_mic(self, peerId):
        try:
            reqId = self.__generate_random_number()
            req = {
                "request": True,
                "id": reqId,
                "method": "enablePeerMic",
                "data": {"peerId": peerId},
            }
            await self.__send_request(req)
            await self.__wait_for(self.__answers[reqId], timeout=15)
        except Exception as e:
            logging.error("Signal :: Error while Enable Peer Mic", exc_info=True)
            self.__emit_error("Not Able to Enable Peer Mic")

    def disable_peer_mic(self, peerId):
        self.__tasks[f"{TASK_ANY}-disable-peer-mic"] = asyncio.ensure_future(
            self.async_disable_peer_mic(peerId)
        )

    async def async_disable_peer_mic(self, peerId):
        try:

            reqId = self.__generate_random_number()
            req = {
                "request": True,
                "id": reqId,
                "method": "disablePeerMic",
                "data": {"peerId": peerId},
            }

            await self.__send_request(req)
            await self.__wait_for(self.__answers[reqId], timeout=15)
        except Exception as e:
            logging.error("Signal :: Error while Disable Peer Mic", exc_info=True)
            self.__emit_error("Not Able to Disable Peer Mic")

    def enable_peer_webcam(self, peerId):
        self.__tasks[f"{TASK_ANY}-enable-peer-webcam"] = asyncio.ensure_future(
            self.async_enable_peer_webcam(peerId)
        )

    async def async_enable_peer_webcam(self, peerId):
        try:
            reqId = self.__generate_random_number()
            req = {
                "request": True,
                "id": reqId,
                "method": "enablePeerWebcam",
                "data": {"peerId": peerId},
            }
            await self.__send_request(req)
            await self.__wait_for(self.__answers[reqId], timeout=15)
        except Exception as e:
            logging.error("Signal :: Error while Enable Peer Webcam", exc_info=True)
            self.__emit_error("Not Able to Enable Peer Webcam")

    def disable_peer_webcam(self, peerId):
        self.__tasks[f"{TASK_ANY}-disable-peer-webcam"] = asyncio.ensure_future(
            self.async_disable_peer_webcam(peerId)
        )

    async def async_disable_peer_webcam(self, peerId):
        try:
            reqId = self.__generate_random_number()
            req = {
                "request": True,
                "id": reqId,
                "method": "disablePeerWebcam",
                "data": {"peerId": peerId},
            }
            await self.__send_request(req)
            await self.__wait_for(self.__answers[reqId], timeout=15)
        except Exception as e:
            logging.error("Signal :: Error while Disable Peer Webcam", exc_info=True)
            self.__emit_error("Not Able to Disable Peer Webcam")

    def remove_peer(self, peerId):
        self.__tasks[f"{TASK_ANY}-remove-peer"] = asyncio.ensure_future(
            self.async_remove_peer(peerId)
        )

    async def async_remove_peer(self, peerId):
        try:
            reqId = self.__generate_random_number()
            req = {
                "request": True,
                "id": reqId,
                "method": "removePeer",
                "data": {"peerId": peerId},
            }

            await self.__send_request(req)
            await self.__wait_for(self.__answers[reqId], timeout=15)
        except Exception as e:
            logging.error("Signal :: Error while Remove Peer", exc_info=True)
            self.__emit_error("Not Able to Remove Peer")

    def add_custom_video_track(self, track: MediaStreamTrack):
        self.__tasks[f"{TASK_ANY}-add-custom-video-track"] = asyncio.ensure_future(
            self.async_add_custom_video_track(track)
        )

    async def async_add_custom_video_track(self, track: MediaStreamTrack):
        try:
            logging.debug("custom video track adding...")
            await self.async_enable_webcam(custom_track=track)
            logging.debug("custom video track added")
            self.__video_stream_track = track
        except Exception as e:
            logging.error("RTC :: Error while Adding Custom Track", exc_info=True)
            self.__emit_error("Not Able to Add Custom Track")

    def release(self):
        self.__clean()

    def __clean(self):
        logging.debug("cleaning all running tasks")
        for task in self.__tasks.values():
            task.cancel()
