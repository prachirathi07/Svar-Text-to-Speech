import os
import re
import string
import numpy as np
import librosa
import soundfile as sf
import scipy.signal
from prosody.prosody import process_gujarati_text  

class ConcatenativeSynthesizer:
    def __init__(self, phoneme_audio_dir):
        """
        Initialize the concatenative synthesizer.
        
        :param phoneme_audio_dir: Directory containing pre-recorded phoneme WAV files.
        """
        self.phoneme_audio_dir = phoneme_audio_dir
        self.phoneme_map = {
            'ક': 'Svar_K',
            'મ': 'Svar_M',
            'લ': 'Svar_L'
        }
        self.sr = 22050  

    def _apply_schwa_deletion(self, letters):
        """
        Delete schwa (represented by 'a') if it is in a medial position flanked by consonants.
        
        :param letters: List of letters (phoneme labels).
        :return: Modified list after schwa deletion.
        """
        result = []
        for i, letter in enumerate(letters):
            if letter == 'a':
                if i > 0 and i < len(letters) - 1:
                    prev, next_ = letters[i-1], letters[i+1]
                    if prev in self.phoneme_map and next_ in self.phoneme_map and prev != 'a' and next_ != 'a':
                        continue
            result.append(letter)
        return result

    def _load_phoneme_audio(self, phoneme):
        """
        Load audio for a specific phoneme.
        
        :param phoneme: Phoneme character (Gujarati).
        :return: Audio time series and sample rate.
        """
        filename = self.phoneme_map.get(phoneme)
        if not filename:
            raise ValueError(f"No audio found for phoneme '{phoneme}'")
        
        filepath = os.path.join(self.phoneme_audio_dir, filename + '.wav')
        try:
            audio, sr = librosa.load(filepath, sr=self.sr)
            return audio, sr
        except Exception as e:
            raise IOError(f"Error loading audio for '{phoneme}': {e}")

    def _apply_prosody(self, audio, target_pitch, duration_factor):
        """
        Modify the audio segment using prosody parameters (pitch shift and time stretch).
        
        :param audio: Input audio signal.
        :param target_pitch: Desired pitch multiplier.
        :param duration_factor: Duration modifier.
        :return: Modified audio segment.
        """
        semitone_shift = 12 * np.log2(target_pitch) if target_pitch > 0 else 0
        pitched_audio = librosa.effects.pitch_shift(audio, sr=self.sr, n_steps=semitone_shift)
        rate = 1 / duration_factor if duration_factor != 0 else 1.0
        stretched_audio = librosa.effects.time_stretch(pitched_audio, rate=rate)
        envelope = np.hanning(len(stretched_audio))
        modified_audio = stretched_audio * envelope
        return modified_audio

    def _apply_advanced_crossfade(self, audio1, audio2, crossfade_duration=0.05):
        """
        Apply advanced crossfade between two audio segments.
        
        :param audio1: First audio segment.
        :param audio2: Second audio segment.
        :param crossfade_duration: Duration of crossfade in seconds.
        :return: Crossfaded audio.
        """
        crossfade_samples = int(crossfade_duration * self.sr)
        fade_in = np.hanning(2 * crossfade_samples)[:crossfade_samples]
        fade_out = np.hanning(2 * crossfade_samples)[crossfade_samples:]
        min_length = min(len(audio1), len(audio2), crossfade_samples)
        combined = np.zeros(len(audio1) + len(audio2) - min_length)
        combined[:len(audio1)-min_length] = audio1[:len(audio1)-min_length]
        combined[len(audio1)-min_length:len(audio1)-min_length+min_length] = (
            audio1[len(audio1)-min_length:] * fade_out[:min_length] +
            audio2[:min_length] * fade_in[:min_length]
        )
        combined[len(audio1)-min_length+min_length:] = audio2[min_length:]
        return combined

    def _post_process_audio(self, audio):
        """
        Apply post-processing effects to add naturalness.
        This example adds a simple reverb effect, amplitude modulation,
        and a low-pass filter.
        """
        ir_duration = 0.1  
        ir_length = int(self.sr * ir_duration)
        impulse_response = np.zeros(ir_length)
        impulse_response[0] = 1.0
        impulse_response[int(ir_length * 0.3)] = 0.5
        impulse_response[int(ir_length * 0.6)] = 0.3

        reverbed = np.convolve(audio, impulse_response, mode='same')

        t = np.linspace(0, len(reverbed) / self.sr, num=len(reverbed))
        modulation = 1.0 + 0.02 * np.sin(2 * np.pi * 5 * t)  # 5 Hz vibrato, 2% variation
        modulated = reverbed * modulation

        nyquist = self.sr / 2.0
        cutoff = nyquist * 0.9  
        b, a = scipy.signal.butter(4, cutoff / nyquist, btype='low')
        smooth_audio = scipy.signal.filtfilt(b, a, modulated)

        return smooth_audio

    def synthesize_word(self, word, sentence_type='statement'):
        """
        Synthesize a word using concatenative synthesis with prosody parameters.
        
        :param word: Word to synthesize.
        :param sentence_type: Sentence type (for intonation).
        :return: Synthesized audio signal.
        """
        prosody_data = process_gujarati_text(word, sentence_type)
        enhanced_phonemes = prosody_data['prosody']['phonemes']
        
        letters = [p['grapheme'] for p in enhanced_phonemes]
        processed_letters = self._apply_schwa_deletion(letters)
        print("Final phoneme sequence after schwa deletion:", processed_letters)
        
        if not processed_letters:
            raise ValueError("No phonemes generated after schwa deletion; check input mapping.")
        
        phoneme_audios = []
        idx = 0
        for letter in processed_letters:
            lookup = letter  
            audio, _ = self._load_phoneme_audio(lookup)
            if idx < len(enhanced_phonemes):
                prosody_info = enhanced_phonemes[idx]
            else:
                prosody_info = {'pitch': 1.0, 'duration': 1.0}
            target_pitch = prosody_info.get('pitch', 1.0)
            duration_factor = prosody_info.get('duration', 1.0)
            modified_audio = self._apply_prosody(audio, target_pitch, duration_factor)
            phoneme_audios.append(modified_audio)
            idx += 1
        
        synthesized_audio = phoneme_audios[0]
        for next_audio in phoneme_audios[1:]:
            synthesized_audio = self._apply_advanced_crossfade(synthesized_audio, next_audio)
        
        final_audio = self._post_process_audio(synthesized_audio)
        return final_audio

    def save_synthesized_audio(self, word, output_path, sentence_type='statement'):
        """
        Synthesize and save audio for a word.
        
        :param word: Word to synthesize.
        :param output_path: File path to save synthesized audio.
        :param sentence_type: Sentence type for prosody.
        """
        synthesized_audio = self.synthesize_word(word, sentence_type)
        synthesized_audio = librosa.util.normalize(synthesized_audio)
        sf.write(output_path, synthesized_audio, self.sr)
        print(f"Synthesized audio for '{word}' saved to {output_path}")

def main():
    phoneme_dir = r'C:\Users\prach\Desktop\Svar-Text-to-Speech\resources\base_phonemes'
    synthesizer = ConcatenativeSynthesizer(phoneme_dir)
    synthesizer.save_synthesized_audio('કમલ', 'synthesized_kamal_with_prosody4.wav')

if __name__ == "__main__":
    main()
