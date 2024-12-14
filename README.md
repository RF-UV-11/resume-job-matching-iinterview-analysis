---

# Interview Analysis and Job Matching System 🎥📄

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-NLP-yellow?style=for-the-badge&logo=huggingface)](https://huggingface.co/)
[![FAISS](https://img.shields.io/badge/FAISS-Embeddings-green?style=for-the-badge)](https://github.com/facebookresearch/faiss)
[![MoviePy](https://img.shields.io/badge/MoviePy-Video%20Processing-lightblue?style=for-the-badge)](https://zulko.github.io/moviepy/)
![Logging](https://img.shields.io/badge/Logging-Debugging-lightblue?style=flat-square&logo=files)
[![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)](LICENSE)

This project provides an **Interview Analysis and Job Matching System**, which processes interview videos to extract meaningful insights and matches candidates' profiles with job descriptions. It utilizes **machine learning models**, **natural language processing (NLP)**, and **FAISS** for efficient embeddings storage and retrieval.

---

## 🎥 Demo Video

Check out how the system works in action:

[!Demo Video](https://github.com/RF-UV-11/resume-job-matching-iinterview-analysis/tree/main/assets/videos/demo.mp4)

---

## 🔍 Features

1. **Interview Analysis**:
   - Extract audio from video files.
   - Transcribe audio to text using Speech Recognition.
   - Generate contextual summaries of transcripts.
   - Analyze candidate traits such as communication style, active listening, and engagement.

2. **Job Matching**:
   - Parse job descriptions and resumes.
   - Extract and compare key skills and qualifications.
   - Match resumes with job descriptions based on text embeddings and similarity scoring.

3. **Efficient Embedding Storage**:
   - Uses FAISS for storing and retrieving embeddings for transcripts and job data.

---

## 📂 Project Structure

```
├── README.md                      # Documentation for the project
├── app.py                         # Main application script
├── assets/                        # Assets used in the project
│   └── images/                    # Placeholder for images or UI assets
├── demo/                          # Demo video files
│   └── demo_video.mp4             # Demo video for showcasing the project
├── data/                          # Sample data files
│   └── interview_video.mp4        # Example video for testing
├── logs/                          # Log files for debugging and analysis
│   └── app.log                    # Application log file
├── modules/                       # Core project modules
│   ├── __init__.py                # Module initialization
│   ├── interview_analyzer/        # Interview analysis module
│   │   ├── __init__.py
│   │   └── interview_summarize.py # Core functions for summarizing and analyzing interviews
│   └── job_matching/              # Job matching module
│       ├── __init__.py
│       ├── job_parser.py          # Parse job descriptions
│       ├── matching.py            # Perform job matching logic
│       ├── resume_parser.py       # Parse and analyze resumes
│       └── text_extractor.py      # Extract relevant text from documents
```

---

## ⚙️ Technologies Used

- **Python**: Core programming language.
- **MoviePy**: Video processing and audio extraction.
- **SpeechRecognition**: Audio-to-text transcription.
- **Transformers**: BART model for summarization.
- **Sentence Transformers**: For generating embeddings.
- **FAISS**: Efficient similarity search and retrieval.
- **Numpy**: Numerical operations and data handling.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Install required dependencies using:
  ```bash
  pip install -r requirements.txt
  ```

### Running the Application
1. Place the video file in the `data/` directory.
2. Run the `app.py` script:
   ```bash
   python app.py
   ```

---

## 📦 Modules Overview

### 1. Interview Analyzer
Located in `modules/interview_analyzer/`:
- **Core Functions**:
  - `extract_audio()`: Extracts audio from video files.
  - `transcribe_audio()`: Converts audio to text.
  - `generate_summary()`: Generates a summary of the transcript.
  - `process_video()`: Orchestrates the video processing pipeline.

### 2. Job Matching
Located in `modules/job_matching/`:
- **Core Functions**:
  - `job_parser.py`: Parses job descriptions into structured data.
  - `resume_parser.py`: Parses candidate resumes.
  - `matching.py`: Compares resumes and job descriptions for compatibility.
  - `text_extractor.py`: Extracts key skills and qualifications from documents.

---

---

## 🛠️ Future Improvements

- Add a user-friendly web interface for uploading videos and resumes.
- Enhance job matching algorithms with machine learning models.
- Support for multiple languages in transcription and summarization.

---

## 👩‍💻 Contributing

1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Commit and push your changes.
4. Submit a pull request.

---

## ✨ Acknowledgments

- [Hugging Face](https://huggingface.co/) for their pre-trained transformer models.
- [FAISS](https://faiss.ai/) for efficient similarity search.
- [MoviePy](https://zulko.github.io/moviepy/) for video and audio processing.
---
