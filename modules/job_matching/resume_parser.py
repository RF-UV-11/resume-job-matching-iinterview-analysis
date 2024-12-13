import re
import spacy

class ResumeParser:
    def __init__(self, resume_text):
        """
        Initializes the ResumeParser with the resume text.

        Args:
            resume_text (str): The text of the resume.
        """
        self.resume_text = resume_text
        self.nlp = spacy.load("en_core_web_sm")
        self.doc = self.nlp(resume_text)

    def extract_skills(self, skills_list):
        """
        Extracts skills mentioned in the resume based on a predefined list.

        Args:
            skills_list (list): A list of skills to look for in the resume.

        Returns:
            list: A list of skills found in the resume.
        """
        found_skills = [skill for skill in skills_list if skill.lower() in self.resume_text.lower()]
        return found_skills

    def extract_education(self):
        """
        Extracts education qualifications mentioned in the resume.

        Returns:
            list: A list of education qualifications found.
        """
        education_keywords = ["bachelor's", "master's", "phd", "high school diploma", "associate degree"]
        found_education = [edu for edu in education_keywords if edu.lower() in self.resume_text.lower()]
        return found_education

    def extract_certifications(self):
        """
        Extracts certifications mentioned in the resume.

        Returns:
            list: A list of certifications found.
        """
        certification_pattern = r'(certified [\w ]+|\b(?:cisco|aws|pmp|cpa|scrum|google)[\w ]* certification\b)'
        certifications = re.findall(certification_pattern, self.resume_text, re.IGNORECASE)
        return [cert.strip() for cert in certifications]

    def extract_experience(self):
        """
        Extracts experience details mentioned in the resume.

        Returns:
            list: A list of experience details found.
        """
        experience_pattern = r'\b(\d+\+? years? of experience)\b'
        experience_matches = re.findall(experience_pattern, self.resume_text, re.IGNORECASE)
        return experience_matches

    def extract_contact_information(self):
        """
        Extracts contact information such as email and phone number from the resume.

        Returns:
            dict: A dictionary containing email and phone number.
        """
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_pattern = r'\b\d{10}\b|\(\d{3}\) \d{3}-\d{4}'
        email_matches = re.findall(email_pattern, self.resume_text)
        phone_matches = re.findall(phone_pattern, self.resume_text)
        return {
            "email": email_matches,
            "phone": phone_matches
        }

    def summarize(self, skills_list):
        """
        Summarizes all extracted information from the resume.

        Args:
            skills_list (list): A list of skills to look for in the resume.

        Returns:
            dict: A dictionary containing extracted data.
        """
        return {
            "skills": self.extract_skills(skills_list),
            "education": self.extract_education(),
            "certifications": self.extract_certifications(),
            "experience": self.extract_experience(),
            "contact_information": self.extract_contact_information()
        }

