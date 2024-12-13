import os
import logging
from flask import Flask, request, jsonify, render_template
import tempfile
from modules.interview_analyzer.interview_summarize import VideoProcessor
from modules.job_matching.text_extractor import extract_text_from_file
from modules.job_matching.matching import ResumeJobMatcher
from modules.job_matching.job_parser import JobDescriptionParser
from modules.job_matching.resume_parser import ResumeParser

# Initialize Flask app
app = Flask(__name__)

# Directories for uploads and ensuring they exist
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/uploads')
VIDEO_FOLDER = os.path.join(UPLOAD_FOLDER, 'videos')
RESUME_FOLDER = os.path.join(UPLOAD_FOLDER, 'resumes')
JOB_FOLDER = os.path.join(UPLOAD_FOLDER, 'jobs')
LOG_FOLDER = os.path.join(os.getcwd(), 'logs')
os.makedirs(VIDEO_FOLDER, exist_ok=True)
os.makedirs(RESUME_FOLDER, exist_ok=True)
os.makedirs(JOB_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# Set up logging configuration
log_file_path = os.path.join(LOG_FOLDER, 'app.log')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log_file_path),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger()

app.config['VIDEO_FOLDER'] = VIDEO_FOLDER
app.config['RESUME_FOLDER'] = RESUME_FOLDER
app.config['JOB_FOLDER'] = JOB_FOLDER

# Home page route
@app.route('/')
def home():
    return render_template('home.html')  # Template with options: Resume or Interview Analysis

# Resume analysis upload page
@app.route('/resume_job_upload')
def upload_resume_job_page():
    return render_template('resume_job_upload.html')  # Page to upload resume and job description

# Video upload page
@app.route('/upload_interview')
def upload_interview_page():
    return render_template('upload_interview.html')  # Page to upload videos

# Resume and Job Description Analysis route
@app.route('/resume_job_analysis', methods=['POST'])
def analyze_resume_job():
    if 'resume' not in request.files or 'job_description' not in request.files:
        logger.error("Both resume and job description files must be uploaded.")
        return jsonify({"error": "Both resume and job description files must be uploaded."}), 400

    resume = request.files['resume']
    job_description = request.files['job_description']

    if resume.filename == '' or job_description.filename == '':
        logger.error("Both resume and job description files must be selected.")
        return jsonify({"error": "Both resume and job description files must be selected."}), 400

    try:
        # Save resume and job description files
        resume_path = os.path.join(app.config['RESUME_FOLDER'], resume.filename)
        job_path = os.path.join(app.config['JOB_FOLDER'], job_description.filename)
        resume.save(resume_path)
        job_description.save(job_path)

        logger.info(f"Saved resume to {resume_path}")
        logger.info(f"Saved job description to {job_path}")

        # Extract text from files
        resume_text = extract_text_from_file(resume_path)
        job_text = extract_text_from_file(job_path)

        logger.debug(f"Extracted resume text: {resume_text[:100]}")  # Log the first 100 characters
        logger.debug(f"Extracted job description text: {job_text[:100]}")  # Log the first 100 characters

        # Analyze resume and job description
        skills = ["Python", "Machine Learning", "SQL", "Deep Learning"]
        resume_data = ResumeParser(resume_text).summarize(skills)
        job_data = JobDescriptionParser(job_text).summarize(skills)
        logger.info(f"Parsed resume data: {resume_data}")
        logger.info(f"Parsed job data: {job_data}")

        match_score = ResumeJobMatcher(resume_data, job_data).calculate_total_match_score()
        logger.info(f"Match score: {match_score}")

        return render_template('match_result.html', match_score=match_score)

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500


# Interview analysis route
@app.route('/interview_analysis', methods=['POST'])
def analyze_video():
    if 'video' not in request.files:
        logger.error("No video file uploaded.")
        return jsonify({"error": "No video file uploaded."}), 400

    video = request.files['video']
    if video.filename == '':
        logger.error("No video file selected.")
        return jsonify({"error": "No video file selected."}), 400

    temp_video = None
    try:
        # Save video file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(video.filename)[1]) as temp_file:
            video.save(temp_file.name)
            temp_video = temp_file.name

            # Process the video
            video_processor = VideoProcessor()
            response = video_processor.process_video(temp_video)

        # Render results page with analysis
        return render_template('interview_result.html', response=response)

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        if temp_video:
            try:
                os.remove(temp_video)
            except PermissionError:
                logger.warning(f"Could not remove file: {temp_video}. It may be in use.")


# Main function to run the app
if __name__ == "__main__":
    app.run(debug=True)
