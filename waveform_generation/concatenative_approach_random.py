import os
import numpy as np
import soundfile as sf
import librosa
import scipy.signal

class ConcatenativeSynthesizer:
    def __init__(self, phoneme_audio_dir):
        """
        Initialize the concatenative synthesizer
        
        :param phoneme_audio_dir: Directory containing pre-recorded phoneme WAV files
        """
        self.phoneme_audio_dir = phoneme_audio_dir
        self.phoneme_map = {
            'k': 'Svar_K',
            'a': 'Svar_A',
            'm': 'Svar_M',
            'l': 'Svar_L'
        }
        self.sr = 22050  # Standard sample rate
    
    def _load_phoneme_audio(self, phoneme):
        """
        Load audio for a specific phoneme
        
        :param phoneme: Phoneme character
        :return: Audio time series and sample rate
        """
        filename = self.phoneme_map.get(phoneme.lower())
        if not filename:
            raise ValueError(f"No audio found for phoneme {phoneme}")
        
        filepath = os.path.join(self.phoneme_audio_dir, filename + '.wav')
        
        try:
            audio, sr = librosa.load(filepath, sr=self.sr)
            return audio, sr
        except Exception as e:
            raise IOError(f"Error loading audio for {phoneme}: {e}")
    
    def _pitch_shift(self, audio, semitones=0):
        """
        Pitch shift audio using librosa
        
        :param audio: Input audio signal
        :param semitones: Number of semitones to shift (can be positive or negative)
        :return: Pitch-shifted audio
        """
        return librosa.effects.pitch_shift(audio, sr=self.sr, n_steps=semitones)
    
    def _apply_prosody_modifications(self, audio):
        """
        Apply prosody modifications to make speech sound more natural
        
        :param audio: Input audio signal
        :return: Modified audio with improved prosody
        """
        # Add slight pitch variation
        pitch_variation = np.random.uniform(-0.5, 0.5)  # Random pitch shift between -0.5 and 0.5 semitones
        audio = self._pitch_shift(audio, semitones=pitch_variation)
        
        # Apply soft envelope to reduce roboticness
        envelope = np.hanning(len(audio))  # Use numpy's hanning instead of scipy.signal
        audio = audio * envelope
        
        return audio
    
    def _apply_advanced_crossfade(self, audio1, audio2, crossfade_duration=0.05):
        """
        Apply advanced crossfade between two audio segments
        
        :param audio1: First audio segment
        :param audio2: Second audio segment
        :param crossfade_duration: Duration of crossfade in seconds
        :return: Crossfaded audio
        """
        crossfade_samples = int(crossfade_duration * self.sr)
        
        # Create Hann window for smoother crossfade using numpy
        fade_in = np.hanning(2 * crossfade_samples)[:crossfade_samples]
        fade_out = np.hanning(2 * crossfade_samples)[crossfade_samples:]
        
        # Trim or pad to ensure consistent crossfade
        min_length = min(len(audio1), len(audio2), crossfade_samples)
        
        # Apply crossfade
        crossfaded = np.zeros(len(audio1) + len(audio2) - min_length)
        crossfaded[:len(audio1)-min_length] = audio1[:len(audio1)-min_length]
        crossfaded[len(audio1)-min_length:len(audio1)-min_length+min_length] = (
            audio1[len(audio1)-min_length:] * fade_out[:min_length] + 
            audio2[:min_length] * fade_in[:min_length]
        )
        crossfaded[len(audio1)-min_length+min_length:] = audio2[min_length:]
        
        return crossfaded
    
    def synthesize_word(self, word):
        """
        Synthesize a word using concatenative synthesis with improved naturalness
        
        :param word: Word to synthesize
        :return: Synthesized audio
        """
        # Breakdown word into phonemes
        phonemes = list(word.lower())
        
        # Collect audio for each phoneme with prosody modifications
        phoneme_audios = []
        for phoneme in phonemes:
            audio, _ = self._load_phoneme_audio(phoneme)
            modified_audio = self._apply_prosody_modifications(audio)
            phoneme_audios.append(modified_audio)
        
        # Concatenate with advanced crossfading
        synthesized_audio = phoneme_audios[0]
        for next_audio in phoneme_audios[1:]:
            synthesized_audio = self._apply_advanced_crossfade(synthesized_audio, next_audio)
        
        return synthesized_audio
    
    def save_synthesized_audio(self, word, output_path):
        """
        Synthesize and save audio for a word
        
        :param word: Word to synthesize
        :param output_path: Path to save synthesized audio
        """
        synthesized_audio = self.synthesize_word(word)
        
        # Normalize audio to prevent clipping
        synthesized_audio = librosa.util.normalize(synthesized_audio)
        
        sf.write(output_path, synthesized_audio, self.sr)
        print(f"Synthesized audio for '{word}' saved to {output_path}")

# Usage example
def main():
    # Replace with the actual path to your phoneme audio files
    phoneme_dir = r'C:\Users\prach\Desktop\Svar-Text-to-Speech\phonemes_yash'
    synthesizer = ConcatenativeSynthesizer(phoneme_dir)
    
    # Synthesize the word "Kamal"
    synthesizer.save_synthesized_audio('kamal', 'synthesized_kamal3.wav')

if __name__ == "__main__":
    main()