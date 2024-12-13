import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
from modules.interview_analyzer.interview_summarize import VideoProcessor

class TestVideoProcessor(unittest.TestCase):

    @patch('moviepy.VideoFileClip')
    def test_extract_audio(self, MockVideoFileClip):
        """Test extracting audio from a video."""
        # Create a mock for video_clip.audio
        mock_audio = MagicMock()
        MockVideoFileClip.return_value.audio = mock_audio
        
        # Temporary mock video file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
            video_path = tmp_video.name
        
        processor = VideoProcessor()
        
        with patch("moviepy.editor.VideoFileClip.audio.write_audiofile") as mock_write_audiofile:
            audio_path = processor.extract_audio(video_path)
            mock_write_audiofile.assert_called_once()  # Ensure that the audio was written
            self.assertTrue(audio_path.endswith(".wav"))
        
        os.remove(video_path)  # Clean up the mock video file

    @patch('speech_recognition.Recognizer.recognize_google')
    def test_transcribe_audio(self, mock_recognize_google):
        """Test transcribing audio to text."""
        mock_recognize_google.return_value = "This is a test transcript."
        
        processor = VideoProcessor()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
            audio_path = tmp_audio.name
        
        transcript = processor.transcribe_audio(audio_path)
        self.assertEqual(transcript, "This is a test transcript.")
        
        os.remove(audio_path)

    @patch('sentence_transformers.SentenceTransformer.encode')
    def test_embed_text(self, mock_encode):
        """Test embedding text using SentenceTransformer."""
        mock_encode.return_value = [0.1] * 384  # Mock the embedding with a dummy value
        
        processor = VideoProcessor()
        
        text = "This is a sample text."
        embedding = processor.embed_text(text)
        
        self.assertEqual(len(embedding), 384)  # Ensure the embedding has the correct length
        self.assertEqual(embedding[0], 0.1)  # Ensure the mock value is returned

    @patch('transformers.AutoModelForSeq2SeqLM.generate')
    @patch('transformers.AutoTokenizer.encode')
    def test_generate_summary(self, mock_encode, mock_generate):
        """Test generating a summary."""
        mock_generate.return_value = [1, 2, 3]  # Mock generated summary ids
        mock_encode.return_value = [101]  # Mock tokenizer encoding
        
        processor = VideoProcessor()
        
        summary = processor.generate_summary("This is a long test text that needs to be summarized.")
        
        self.assertIn("summarized", summary)  # Check that the summary contains the expected word

    @patch.object(VideoProcessor, 'extract_audio')
    @patch.object(VideoProcessor, 'transcribe_audio')
    @patch.object(VideoProcessor, 'embed_text')
    @patch.object(VideoProcessor, 'generate_summary')
    def test_process_video(self, mock_generate_summary, mock_embed_text, mock_transcribe_audio, mock_extract_audio):
        """Test the full video processing pipeline."""
        
        # Mock all the methods used in the process
        mock_extract_audio.return_value = "mock_audio.wav"
        mock_transcribe_audio.return_value = "This is a mock transcript."
        mock_embed_text.return_value = [0.1] * 384
        mock_generate_summary.return_value = "This is the summary."
        
        processor = VideoProcessor()
        
        video_path = "mock_video.mp4"
        result = processor.process_video(video_path)
        
        self.assertEqual(result['transcript'], "This is a mock transcript.")
        self.assertEqual(result['summary'], "This is the summary.")
        self.assertIn("traits", result)
        self.assertEqual(result['traits']['Communication Style'], "Effective")
        
        # Check if FAISS index and document store were updated
        self.assertEqual(len(processor.faiss_index.ntotal), 1)
        self.assertEqual(len(processor.document_store), 1)

if __name__ == '__main__':
    unittest.main()
