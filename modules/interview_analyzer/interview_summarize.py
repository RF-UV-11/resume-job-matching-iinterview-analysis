import os
import tempfile
from moviepy import VideoFileClip
import speech_recognition as sr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class VideoProcessor:
    def __init__(self):
        """Initialize models and FAISS setup."""
        # Load models
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # FAISS setup
        self.embedding_dim = 384  # Dimension of embeddings
        self.faiss_index = faiss.IndexFlatL2(self.embedding_dim)
        self.document_store = []  # To store metadata associated with embeddings

    def extract_audio(self, video_path):
        """Extracts audio from the video file using moviepy."""
        audio_path = tempfile.mktemp(suffix=".wav")
        video_clip = VideoFileClip(video_path)
        audio = video_clip.audio
        audio.write_audiofile(audio_path)
        return audio_path

    def transcribe_audio(self, audio_path):
        """Transcribes audio to text."""
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data)
        except Exception as e:
            raise RuntimeError(f"Transcription error: {e}")

    def embed_text(self, text):
        """Generates embeddings for text using a sentence transformer model."""
        return self.embedder.encode([text])[0]

    def generate_summary(self, text):
        """Generates a contextual summary using a transformer model."""
        inputs = self.tokenizer.encode("summarize: " + text, return_tensors="pt", truncation=True, max_length=512)
        summary_ids = self.model.generate(
            inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True
        )
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    def process_video(self, video_path):
        """Processes the video, extracting audio, transcribing, summarizing, and generating embeddings."""
        # Extract audio
        audio_path = self.extract_audio(video_path)

        try:
            # Transcribe audio
            transcript = self.transcribe_audio(audio_path)

            if not transcript:
                raise ValueError("Could not process the audio.")

            # Generate embedding and store in FAISS
            embedding = self.embed_text(transcript)
            self.faiss_index.add(np.array([embedding]))
            self.document_store.append({"filename": video_path, "transcript": transcript})

            # Generate summary
            summary = self.generate_summary(transcript)

            # Key trait analysis (rudimentary example)
            traits = {
                "Communication Style": "Effective",
                "Active Listening": "Good",
                "Engagement": "Moderate",
            }

            return {
                "transcript": transcript,
                "summary": summary,
                "traits": traits
            }

        finally:
            # Clean up
            os.remove(audio_path)
