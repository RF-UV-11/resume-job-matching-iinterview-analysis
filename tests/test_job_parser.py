import unittest
from modules.job_matching.job_parser import JobDescriptionParser

class TestJobDescriptionParser(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment with sample job description text.
        """
        self.job_description = """
        We are looking for a skilled Data Scientist with experience in Python, Machine Learning, and SQL.
        The candidate should have a Master's degree in Computer Science or a related field.
        certified in as AWS or Azure are a plus.
        At least 3+ years of experience in data analysis is required.
        """
        self.parser = JobDescriptionParser(self.job_description)

    def test_extract_skills(self):
        """
        Test the extraction of skills from the job description.
        """
        expected_skills = ["Python", "Machine Learning", "SQL"]
        extracted_skills = self.parser.extract_skills(["Python", "Machine Learning", "SQL", "Deep Learning"])
        print("***",extracted_skills)
        self.assertCountEqual(extracted_skills, expected_skills)

    def test_extract_education(self):
        """
        Test the extraction of education qualifications from the job description.
        """
        expected_education = ["master's"]
        extracted_education = self.parser.extract_education()
        print(extracted_education)
        self.assertCountEqual(extracted_education, expected_education)

    def test_extract_certifications(self):
        """
        Test the extraction of certifications from the job description.
        """
        expected_certifications = ["AWS", "Azure"]
        extracted_certifications = self.parser.extract_certifications()
        print("///",extracted_certifications)
        self.assertCountEqual(extracted_certifications, expected_certifications)

    def test_extract_experience(self):
        """
        Test the extraction of experience requirements from the job description.
        """
        expected_experience = ["3+ years of experience"]
        extracted_experience = self.parser.extract_experience()
        print("]]]",extracted_experience)
        self.assertCountEqual(extracted_experience, expected_experience)

if __name__ == "__main__":
    unittest.main()
