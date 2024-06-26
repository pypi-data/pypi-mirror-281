import logging
from typing import final

class BaseEvent:
  """
  VideoSDK BaseEvent Class
  """
  
  @final
  def handle_event(self, action, data):
    method_name = {
      # Base Event Handlers
      "error": "on_error",
      
      # Meeting Event Handlers
      "meeting-joined": "on_meeting_joined",
      "meeting-left": "on_meeting_left",
      "participant-mode-changed": "on_participant_mode_changed",
      "participant-joined": "on_participant_joined",
      "participant-left": "on_participant_left",
      "speaker-changed": "on_speaker_changed",
      "presenter-changed": "on_presenter_changed",
      "main-participant-changed": "on_main_participant_changed",
      "chat-message": "on_chat_message",
      "entry-requested": "on_entry_requested",
      "entry-responded": "on_entry_responded",
      "recording-state-changed": "on_recording_state_changed",
      "recording-started": "on_recording_started",
      "recording-stopped": "on_recording_stopped",
      "livestream-state-changed": "on_livestream_state_changed",
      "livestream-started": "on_livestream_started",
      "livestream-stopped": "on_livestream_stopped",
      "hls-state-changed": "on_hls_state_changed",
      "hls-started": "on_hls_started",
      "hls-stopped": "on_hls_stopped",
      "whiteboard-started": "on_whiteboard_started",
      "whiteboard-stopped": "on_whiteboard_stopped",
      "video-state-changed": "on_video_state_changed",
      "video-seeked": "on_video_seeked",
      "mic-requested": "on_mic_requested",
      "webcam-requested": "on_webcam_requested",
      "pin-state-changed": "on_pin_state_changed",
      "connection-open": "on_connection_open",
      "connection-close": "on_connection_close",
      "switch-meeting": "on_switch_meeting",
      "meeting-state-changed": "on_meeting_state_change",
      "transcription-state-changed": "on_transcription_state_changed",
      "transcription-text": "on_transcription_text",

      # Participant Event Handlers
      "stream-enabled": "on_stream_enabled",
      "stream-disabled": "on_stream_disabled",
      "media-status-changed": "on_media_status_changed",
      "video-quality-changed": "on_video_quality_changed"
    }.get(action, None)

    if method_name is None:
        logging.debug(f"unimplemented event handler {action}")
        return

    method = getattr(self, method_name, None)
    if method:
        method(data)
    else:
        logging.debug(f"No method found for {method_name}")

  
class MeetingEventHandler(BaseEvent):
  def on_error(self, data):
      """
      Handle error event.
      """

  def on_meeting_joined(self, data):
      """
      Handle meeting joined event.
      """

  def on_meeting_left(self, data):
      """
      Handle meeting left event.
      """

  def on_participant_mode_changed(self, data):
      """
      Handle participant mode changed event.
      """

  def on_participant_joined(self, data):
      """
      Handle participant joined event.
      """

  def on_participant_left(self, data):
      """
      Handle participant left event.
      """

  def on_speaker_changed(self, data):
      """
      Handle speaker changed event.
      """

  def on_presenter_changed(self, data):
      """
      Handle presenter changed event.
      """

  def on_main_participant_changed(self, data):
      """
      Handle main participant changed event.
      """

  def on_chat_message(self, data):
      """
      Handle chat message event.
      """

  def on_entry_requested(self, data):
      """
      Handle entry requested event.
      """

  def on_entry_responded(self, data):
      """
      Handle entry responded event.
      """

  def on_recording_state_changed(self, data):
      """
      Handle recording state changed event.
      """

  def on_recording_started(self, data):
      """
      Handle recording started event.
      """

  def on_recording_stopped(self, data):
      """
      Handle recording stopped event.
      """

  def on_livestream_state_changed(self, data):
      """
      Handle livestream state changed event.
      """

  def on_livestream_started(self, data):
      """
      Handle livestream started event.
      """

  def on_livestream_stopped(self, data):
      """
      Handle livestream stopped event.
      """

  def on_hls_state_changed(self, data):
      """
      Handle HLS state changed event.
      """

  def on_hls_started(self, data):
      """
      Handle HLS started event.
      """

  def on_hls_stopped(self, data):
      """
      Handle HLS stopped event.
      """

  def on_whiteboard_started(self, data):
      """
      Handle whiteboard started event.
      """

  def on_whiteboard_stopped(self, data):
      """
      Handle whiteboard stopped event.
      """

  def on_video_state_changed(self, data):
      """
      Handle video state changed event.
      """

  def on_video_seeked(self, data):
      """
      Handle video seeked event.
      """

  def on_mic_requested(self, data):
      """
      Handle microphone requested event.
      """

  def on_webcam_requested(self, data):
      """
      Handle webcam requested event.
      """

  def on_pin_state_changed(self, data):
      """
      Handle pin state changed event.
      """

  def on_connection_open(self, data):
      """
      Handle connection open event.
      """

  def on_connection_close(self, data):
      """
      Handle connection close event.
      """

  def on_switch_meeting(self, data):
      """
      Handle switch meeting event.
      """

  def on_meeting_state_change(self, data):
      """
      Handle meeting state change event.
      """

  def on_transcription_state_changed(self, data):
      """
      Handle transcription state changed event.
      """

  def on_transcription_text(self, data):
      """
      Handle transcription text event.
      """


class ParticipantEventHandler(BaseEvent):
  def on_stream_enabled(self, data)->None:
    """
    Handle Participant stream enabled event.
    """
  def on_stream_disabled(self, data)->None:
    """
    Handle Participant stream enabled event.
    """
  def on_media_status_changed(self, data)->None:
    """
    Handle Participant stream enabled event.
    """
  def on_video_quality_changed(self, data)->None:
    """
    Handle Participant stream enabled event.
    """