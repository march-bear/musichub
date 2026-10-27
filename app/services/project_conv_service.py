from midi2audio import FluidSynth
from midiutil import MIDIFile
from pydub import AudioSegment

from app.db.schemas import Project


class ProjectConvService:
    def __init__(self, soundfont):
        self.fs = FluidSynth(soundfont)

    def conv2midi(self, project: Project, out_file):
        payload = project.payload
        tempo = payload.tempo
        parts = payload.parts

        midi = MIDIFile(len(parts))
        for track, project_part in enumerate(parts):
            channel = track
            instrument = project_part.instrument

            midi.addTempo(track, 0, tempo)
            midi.addProgramChange(track, channel,0, instrument)

            for note in project_part.part:
                midi.addNote(track, channel, note.note, note.time, note.duration, note.velocity)

        midi.writeFile(out_file)

    def conv_midi2wav(self, midi_filename, wav_filename):
        self.fs.midi_to_audio(midi_filename, wav_filename)

    def conv_wav2mp3(self, wav_filename, mp3_filename, bitrate="192k"):
        AudioSegment.from_wav(wav_filename).export(mp3_filename, format="mp3", bitrate=bitrate)
