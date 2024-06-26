from dataclasses import dataclass
import logging
from typing import Any, Callable, Dict, Optional, TypedDict
from ._events import Events, VideoSDKEvents
from .event_handler import BaseEvent
from .lib.pymediasoup.consumer import Consumer
from .lib.pymediasoup.producer import Producer
from .room_client import RoomClient
from .stream import Stream


@dataclass
class ParticipantConfig(TypedDict, total=False):
    id: str
    display_name: str
    local: bool
    mode: str
    meta_data: Optional[Dict[str, Any]]
    room_client: RoomClient


class Participant:
    def __init__(
        self,
        id: str,
        display_name=str,
        local=bool,
        mode=str,
        meta_data=Any,
        room_client: RoomClient = None,
    ):
        self.__id = id
        self.__display_name = display_name
        self.__local = local
        self.__mode = mode
        self.__meta_data = meta_data
        self.__streams: dict[str, Stream] = {}
        self.__mic_on: bool = False
        self.__webcam_on: bool = False
        self.__room_client = room_client
        self.__listeners: list[BaseEvent] = []
        self.__internal_event_listeners: dict[str, Callable] = {}
        self.__listen()
        logging.debug(f"Meeting Participant initialized with ID: {id}")

    def __del__(self):
        logging.debug("Meeting :: participant deleted %s", self.__id)

    def __emit(self, event_name, data=None):
        for _listener in self.__listeners:
            logging.debug(f"{self.id} :: Emitting Event: {event_name}")
            _listener.handle_event(event_name, data)

    def add_event_listener(self, event_handler: BaseEvent):
        self.__listeners.append(event_handler)

    def remove_event_listener(self, event_handler: BaseEvent):
        self.__listeners.remove(event_handler)

    def remove_all_listeners(self):
        logging.debug("removing all event listner for %s", self.__id)
        self.__listeners.clear()

    def _cleanup(self):
        for k, v in self.__internal_event_listeners.items():
            self.__room_client.remove_listener(k, v)

    def __listen(self):
        @self.__room_client.on(Events.ADD_CONSUMER)
        def on_stream_enabled(consumer: Consumer):
            if consumer.appData["peerId"] == self.__id:
                stream = Stream(track=consumer.track)
                self.__streams[consumer.id] = stream
                logging.debug(
                    f"Partcipant :: {self.id} :: stream-enabled {stream.kind}"
                )
                self.__emit(VideoSDKEvents.EV_STREAM_ENABLED.value, stream)

        self.__internal_event_listeners[Events.ADD_CONSUMER] = on_stream_enabled

        @self.__room_client.on(Events.REMOVE_CONSUMER)
        def on_stream_disabled(consumer: Consumer):
            if consumer.appData["peeId"] == self.__id:
                if consumer.id in self.__streams:
                    stream = self.__streams.pop(consumer.id)
                    stream.track.stop()
                    logging.debug(
                        f"Partcipant :: {self.id} :: stream-disabled {stream.kind}"
                    )
                    self.__emit(VideoSDKEvents.EV_STREAM_DISABLED.value, stream)

        self.__internal_event_listeners[Events.REMOVE_CONSUMER] = on_stream_disabled

        @self.__room_client.on(Events.PARTICIPANT_MEDIA_STATE_CHANGED)
        def on_media_status_changed(data):
            if data["peerId"] == self.__id:
                new_state = data["newState"]
                kind = data["kind"]
                if kind == "audio":
                    self.__mic_on = new_state
                elif kind == "video":
                    self.__webcam_on = new_state
                logging.debug(f"Partcipant :: {self.id} :: media-status-changed")
                self.__emit(
                    VideoSDKEvents.EV_MEDIA_STATUS_CHANGED.value,
                    {
                        "peerId": data["peerId"],
                        "kind": data["kind"],
                        "newState": data["newState"],
                    },
                )

        self.__internal_event_listeners[Events.PARTICIPANT_MEDIA_STATE_CHANGED] = (
            on_media_status_changed
        )

        @self.__room_client.on(Events.VIDEO_QUALITY_CHANGED)
        def on_video_quality_changed(data):
            if data["peerId"] == self.__id:
                logging.debug(f"Partcipant :: {self.id} :: video-quality-changed")
                self.__emit(
                    VideoSDKEvents.EV_VIDEO_QUALITY_CHANGED.value,
                    {
                        "peerId": data["peerId"],
                        "prevQuality": data["prevQuality"],
                        "currentQuality": data["currentQuality"],
                    },
                )

        self.__internal_event_listeners[Events.VIDEO_QUALITY_CHANGED] = (
            on_video_quality_changed
        )

    def remove(self):
        self.__room_client.remove_peer(self.__id)

    def enable_mic(self):
        self.__room_client.enable_peer_mic(self.__id)

    def disable_mic(self):
        self.__room_client.disable_peer_mic(self.__id)

    def enable_webcam(self):
        self.__room_client.enable_peer_webcam(self.__id)

    def disable_webcam(self):
        self.__room_client.disable_peer_webcam(self.__id)

    def _add_stream(self, producer: Producer):
        stream = Stream(track=producer.track)

        self.__emit(VideoSDKEvents.EV_STREAM_ENABLED.value, stream)
        self.__streams[producer.id] = stream

    def _remove_stream(self, producer: Producer):
        if producer.id in self.__streams:
            stream = self.__streams.pop(producer.id)
            self.__emit(VideoSDKEvents.EV_STREAM_DISABLED.value, stream)
            stream.track.stop()

    def _update_stream(self, producer: Producer):
        self.streams[producer.id] = producer.track

    @property
    def id(self):
        return self.__id

    @property
    def display_name(self):
        return self.__display_name

    @property
    def local(self):
        return self.__local

    @property
    def mode(self):
        return self.__mode

    @property
    def meta_data(self):
        return self.__meta_data

    @property
    def listeners(self):
        return self.__listeners

    @property
    def mic_on(self):
        return self.__mic_on

    @property
    def webcam_on(self):
        return self.__webcam_on

    @property
    def streams(self):
        return self.__streams
