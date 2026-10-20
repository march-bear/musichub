from midi2audio import FluidSynth
from midiutil import MIDIFile
from pydub import AudioSegment

from app.data.schemas import Track


class TrackConvService:
    def __init__(self, soundfont):
        self.fs = FluidSynth(soundfont)

    def conv2midi(self, track: Track, out_file):
        payload = track.payload
        tempo = payload.tempo
        parts = payload.parts

        midi = MIDIFile(len(parts))
        for track_num, track_part in enumerate(parts):
            channel = track_num
            instrument = track_part.instrument

            midi.addTempo(track_num, 0, tempo)
            midi.addProgramChange(track_num, channel,0, instrument)

            for note in track_part.part:
                midi.addNote(track_num, channel, note.note, note.time, note.duration, note.velocity)

        midi.writeFile(out_file)

    def conv_midi2wav(self, midi_filename, wav_filename):
        self.fs.midi_to_audio(midi_filename, wav_filename)

    def conv_wav2mp3(self, wav_filename, mp3_filename, bitrate="192k"):
        AudioSegment.from_wav(wav_filename).export(mp3_filename, format="mp3", bitrate=bitrate)
