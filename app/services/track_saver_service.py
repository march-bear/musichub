from pathlib import Path

from app.data.schemas import Track
from app.services.track_conv_service import TrackConvService
from app.services.track_service import TrackService


class TrackSaverService:
    def __init__(
            self,
            track_conv_service: TrackConvService,
            track_service: TrackService,
    ):
        self.track_conv_service = track_conv_service
        self.track_service = track_service


    def save_track(self, user_id: int, track_name: str):
        self._save_track(
            user_id,
            Track.model_validate(self.track_service.get(user_id, track_name))
        )


    def _save_track(self, user_id: int, track: Track):
        out_dir = Path(str(user_id))
        out_dir.mkdir(parents=True, exist_ok=True)

        midi_path = out_dir / f"{track.name}.mid"
        wav_path = out_dir / f"{track.name}.wav"
        mp3_path = out_dir / f"{track.name}.mp3"
        preview_path =out_dir / f"{track.name}.preview.mp3"

        with open(midi_path, "wb") as f_midi:
            self.track_conv_service.conv2midi(track, f_midi)

        self.track_conv_service.conv_midi2wav(midi_path, wav_path)
        self.track_conv_service.conv_wav2mp3(wav_path, mp3_path)
        self.track_conv_service.conv_wav2mp3(wav_path, preview_path)
