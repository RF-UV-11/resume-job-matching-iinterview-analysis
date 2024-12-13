import re
import spacy

class JobDescriptionParser:
    def __init__(self, job_description):
        """
        Initializes the JobDescriptionParser with the job description text.

        Args:
            job_description (str): The text of the job description.
        """
        self.job_description = job_description
        self.nlp = spacy.load("en_core_web_sm")
        self.doc = self.nlp(job_description)

    def extract_skills(self, skills_list):
        """
        Extracts skills mentioned in the job description based on a predefined list.

        Args:
            skills_list (list): A list of skills to look for in the job description.

        Returns:
            list: A list of skills found in the job description.
        """
        found_skills = [skill for skill in skills_list if skill.lower() in self.job_description.lower()]
        return found_skills

    def extract_education(self):
        """
        Extracts education qualifications mentioned in the job description.

        Returns:
            list: A list of education qualifications found.
        """
        education_keywords = ["bachelor's", "master's", "phd", "high school diploma", "associate degree"]
        found_education = [edu for edu in education_keywords if edu.lower() in self.job_description.lower()]
        return found_education

    def extract_certifications(self):
        """
        Extracts certifications mentioned in the job description.

        Returns:
            list: A list of certifications found.
        """
        certification_pattern = r'(certified [\w ]+|\b(?:cisco|aws|pmp|cpa|scrum|google)[\w ]* certification\b)'
        certifications = re.findall(certification_pattern, self.job_description, re.IGNORECASE)
        return [cert.strip() for cert in certifications]

    def extract_experience(self):
        """
        Extracts experience requirements mentioned in the job description.

        Returns:
            list: A list of experience details found.
        """
        experience_pattern = r'\b(\d+\+? years? of experience)\b'
        experience_matches = re.findall(experience_pattern, self.job_description, re.IGNORECASE)
        return experience_matches

    def summarize(self, skills_list):
        """
        Summarizes all extracted information from the job description.

        Args:
            skills_list (list): A list of skills to look for in the job description.

        Returns:
            dict: A dictionary containing extracted data.
        """
        return {
            "skills": self.extract_skills(skills_list),
            "education": self.extract_education(),
            "certifications": self.extract_certifications(),
            "experience": self.extract_experience(),
        }


