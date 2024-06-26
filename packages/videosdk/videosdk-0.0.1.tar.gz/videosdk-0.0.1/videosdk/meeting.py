import gc
import logging
from typing import Callable
from ._events import Events, VideoSDKEvents
from .event_handler import BaseEvent
from .lib.pymediasoup.producer import Producer
from .participant import Participant
from .room_client import RoomClient


class Meeting:
    def __init__(
        self, meeting_id: str, local_participant: Participant, room_client: RoomClient
    ):
        self.__id = meeting_id
        self.__local_participant = local_participant
        self.__room_client = room_client
        self.__listeners: list[BaseEvent] = []
        self.__participants: dict[str, Participant] = {}
        self.__active_speaker_id: str = None
        self.__internal_event_listeners: dict[str, Callable] = {}
        logging.debug(f"Meeting initialized with ID: {meeting_id}")
        self.__listen()

    def __del__(self):
        logging.debug("Meeting :: instance deleted %s", self.__id)

    def join(self):
        logging.debug(f"Starting meeting {self.__id}")
        self.__room_client.join()

    def leave(self):
        logging.debug(f"Leaving meeting {self.__id}")
        self.__room_client.leave()

    def end(self):
        logging.debug(f"Ending/Closing running meeting {self.__id}")
        self.__room_client.close()

    def enable_mic(self):
        logging.debug(f"Unmute mic {self.__id}")
        self.__room_client.enable_mic()

    def disable_mic(self):
        logging.debug(f"Mute mic {self.__id}")
        self.__room_client.disable_mic()

    def enable_webcam(self):
        logging.debug(f"Webcam on {self.__id}")
        self.__room_client.enable_webcam()

    def disable_webcam(self):
        logging.debug(f"Webcam off {self.__id}")
        self.__room_client.disable_webcam()

    def release(self):
        logging.debug(f"releasing meeting")
        self.__room_client.release()

    def add_custom_video_track(self, track):
        self.__room_client.add_custom_video_track(track)

    def __reject_mic_request(self):
        # Implementation for rejecting the microphone request
        pass

    def __reject_webcam_request(self):
        # Implementation for rejecting the webcam request
        pass

    def add_event_listener(self, event_listener: BaseEvent):
        self.__listeners.append(event_listener)

    def remove_event_listener(self, event_listener: BaseEvent):
        self.__listeners.remove(event_listener)

    def remove_all_listeners(self):
        self.__listeners.clear()

    def _cleanup(self):
        for k, v in self.__internal_event_listeners.items():
            self.__room_client.remove_listener(k, v)

    def __emit(self, event_name, data=None):
        for _listener in self.__listeners:
            _listener.handle_event(event_name, data)

    def __listen(self):
        @self.__room_client.on(Events.ERROR)
        def on_error(data):
            self.__emit(VideoSDKEvents.EV_ERROR.value, data)

        # meeting
        @self.__room_client.on(Events.MEETING_JOINED)
        def on_meeting_joined():
            self.__emit(VideoSDKEvents.EV_MEETING_JOINED.value)

        @self.__room_client.on(Events.MEETING_LEFT)
        def on_meeting_left():
            self.__emit(VideoSDKEvents.EV_MEETING_LEFT.value)

        @self.__room_client.on(Events.MEETING_STATE_CHANGED)
        def on_meeting_state_change(data):
            self.__emit(VideoSDKEvents.EV_MEETING_STATE_CHANGE.value, data)

        @self.__room_client.on(Events.MIC_REQUESTED)
        def on_mic_requested(data):
            self.__emit(
                VideoSDKEvents.EV_MIC_REQUESTED,
                data={
                    "participantId": data["peerId"],
                    "accept": self.unmute,
                    "reject": self.__reject_mic_request,
                },
            )

        @self.__room_client.on(Events.WEBCAM_REQUESTED)
        def on_webcam_requested(data):
            self.__emit(
                VideoSDKEvents.EV_WEBCAM_REQUESTED,
                data={
                    "participantId": data["peerId"],
                    "accept": self.enable_webcam,
                    "reject": self.__reject_webcam_request,
                },
            )

        # active speaker
        @self.__room_client.on(Events.SET_ROOM_ACTIVE_SPEAKER)
        def on_speaker_changed(data):
            self.__emit(VideoSDKEvents.EV_SPEAKER_CHANGED.value, data)

        # participant
        @self.__room_client.on(Events.ADD_PEER)
        def on_participant_joined(data):
            id = data["id"]
            display_name = data["displayName"]
            device = data["device"]
            mode = data["mode"]
            meta_data = data["metaData"] if "metaData" in data else None

            participant = Participant(
                id=id,
                display_name=display_name,
                local=False,
                mode=mode,
                meta_data=meta_data,
                room_client=self.__room_client,
            )
            self.__participants[id] = participant
            self.__emit(VideoSDKEvents.EV_PARTICIPANT_JOINED.value, participant)

        @self.__room_client.on(Events.REMOVE_PEER)
        def on_participant_left(data):
            id = data["peerId"]
            if id in self.__participants:
                participant = self.__participants.pop(id)
                self.__emit(VideoSDKEvents.EV_PARTICIPANT_LEFT.value, participant)

                # remove all event listeners
                participant.remove_all_listeners()
                participant._cleanup()
                # delete participant object
                del participant

                gc.collect()

        @self.__room_client.on(Events.ADD_PRODUCER)
        def on_stream_enabled(data: Producer):
            if self.__local_participant:
                self.__local_participant._add_stream(data)

        @self.__room_client.on(Events.REMOVE_PRODUCER)
        def on_stream_disabled(data: Producer):
            if self.__local_participant:
                self.__local_participant._remove_stream(data)

    @property
    def listeners(self):
        return self.__listeners

    @property
    def id(self):
        return self.__id

    @property
    def local_participant(self):
        return self.__local_participant

    @property
    def participants(self):
        return self.__participants

    @property
    def active_speaker_id(self):
        return self.__active_speaker_id
