import unittest
from modules.job_matching.resume_parser import ResumeParser

class TestResumeParser(unittest.TestCase):
    def setUp(self):
        self.resume_text = """
        John Doe
        Email: johndoe@example.com
        Phone: (123) 456-7890
        Experienced Software Engineer with 7+ years of experience in Python, Java, and cloud technologies.
        Bachelor's degree in Computer Science.
        Certifications: AWS Certified Solutions Architect, PMP.
        Skills: Python, Java, Cloud Computing, Team Leadership, Agile Development.
        """
        self.parser = ResumeParser(self.resume_text)

    def test_extract_skills(self):
        skills = self.parser.extract_skills(["Python", "Java", "Cloud Computing", "Team Leadership", "Agile Development", "Machine Learning"])
        print(skills)
        self.assertIn("Python", skills)
        self.assertIn("Java", skills)
        self.assertIn("Cloud Computing", skills)

    def test_extract_education(self):
        education = self.parser.extract_education()
        print(education)
        self.assertIn("Bachelor's degree in Computer Science", education)

    def test_extract_certifications(self):
        certifications = self.parser.extract_certifications()
        print(certifications)
        self.assertIn("AWS Certified Solutions Architect", certifications)
        self.assertIn("PMP", certifications)

    def test_extract_experience(self):
        experience = self.parser.extract_experience()
        print(experience)
        self.assertIn("7+ years of experience", experience)

    def test_extract_contact_information(self):
        contact_info = self.parser.extract_contact_information()
        print(contact_info)
        self.assertIn("johndoe@example.com", contact_info["email"])
        self.assertIn("(123) 456-7890", contact_info["phone"])

    def test_summarize(self):
        summary = self.parser.summarize(["Python", "Java", "Cloud Computing", "Team Leadership", "Agile Development", "Machine Learning"])
        print(summary)
        self.assertIn("skills", summary)
        self.assertIn("education", summary)
        self.assertIn("certifications", summary)
        self.assertIn("experience", summary)
        self.assertIn("contact_information", summary)

if __name__ == "__main__":
    unittest.main()
