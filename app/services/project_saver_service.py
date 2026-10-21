import tempfile
from pathlib import Path

from app.data.schemas import Project
from app.services.storage_service import StorageService
from app.services.project_conv_service import ProjectConvService
from app.services.project_service import ProjectService


class ProjectSaverService:
    def __init__(
            self,
            project_conv_service: ProjectConvService,
            project_service: ProjectService,
            storage_service: StorageService,
    ):
        self.project_conv_service = project_conv_service
        self.project_service = project_service
        self.storage_service = storage_service


    def save_project(self, user_id: int, project_name: str):
        self._save_project(
            user_id,
            Project.model_validate(self.project_service.get(user_id, project_name))
        )


    def _save_project(self, user_id: int, project: Project):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir)

            midi_path = out_dir / f"{project.name}.mid"
            wav_path = out_dir / f"{project.name}.wav"
            mp3_path = out_dir / f"{project.name}.mp3"
            preview_path = out_dir / f"{project.name}.preview.mp3"

            with open(midi_path, "wb") as f_midi:
                self.project_conv_service.conv2midi(project, f_midi)

            self.storage_service.save_file(midi_path, str(Path(str(user_id)) / midi_path.name))

            self.project_conv_service.conv_midi2wav(midi_path, wav_path)
            self.storage_service.save_file(wav_path, str(Path(str(user_id)) / wav_path.name))

            self.project_conv_service.conv_wav2mp3(wav_path, mp3_path)
            self.storage_service.save_file(mp3_path, str(Path(str(user_id)) / mp3_path.name))

            self.project_conv_service.conv_wav2mp3(wav_path, preview_path)
            self.storage_service.save_file(preview_path, str(Path(str(user_id)) / preview_path.name))
