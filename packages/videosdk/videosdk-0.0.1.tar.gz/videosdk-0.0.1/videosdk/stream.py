from vsaiortc.mediastreams import MediaStreamTrack
from av import AudioFrame, VideoFrame

class Stream:
  def __init__(self, track: MediaStreamTrack) -> None:
    self.track = track
    self.id = track.id
    self.kind = track.kind
    self.codecs = None 