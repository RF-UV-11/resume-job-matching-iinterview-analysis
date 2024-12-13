import unittest
from modules.job_matching.matching import ResumeJobMatcher

class TestResumeJobMatcher(unittest.TestCase):

    def setUp(self):
        """
        Setup method to initialize the resume_data and job_data for testing.
        """
        self.resume_data = {
            'skills': ['Python', 'Machine Learning', 'SQL'],
            'education': ["bachelor's"],
            'certifications': ['AWS Certified Solutions Architect'],
            'experience': ['5+ years'],
            'contact_information': {'email': ['johndoe@example.com'], 'phone': ['(123) 456-7890']}
        }
        
        self.job_data = {
            'skills': ['Python', 'Machine Learning', 'SQL'],
            'education': ["master's"],
            'certifications': ['AWS Certified Solutions Architect'],
            'experience': ["3+ years"]
        }

    def test_calculate_skill_match(self):
        """
        Test skill matching calculation.
        """
        matcher = ResumeJobMatcher(self.resume_data, self.job_data)
        result = matcher.calculate_skill_match()
        # The skills in both resume and job are identical, so result should be 100%
        self.assertEqual(result, 100.0)

    def test_calculate_education_match(self):
        """
        Test education matching calculation.
        """
        matcher = ResumeJobMatcher(self.resume_data, self.job_data)
        result = matcher.calculate_education_match()
        # The resume has a bachelor's and the job requires a master's, so match is 0%
        self.assertEqual(result, False)

    def test_calculate_certification_match(self):
        """
        Test certification matching calculation.
        """
        matcher = ResumeJobMatcher(self.resume_data, self.job_data)
        result = matcher.calculate_certification_match()
        # Both resume and job require the same certification, so match is 100%
        self.assertEqual(result, 100.0)

    def test_calculate_experience_match(self):
        """
        Test experience matching calculation.
        """
        matcher = ResumeJobMatcher(self.resume_data, self.job_data)
        result = matcher.calculate_experience_match()
        # Resume has 5+ years, job requires 3+ years, so experience should match
        self.assertTrue(result)

    def test_calculate_total_match_score(self):
        """
        Test the total match score calculation.
        """
        matcher = ResumeJobMatcher(self.resume_data, self.job_data)
        result = matcher.calculate_total_match_score()
        
        expected_score = {
            "skill_match": 100.0,
            "education_match": False,
            "certification_match": 100.0,
            "experience_match": True,
            "total_match_score": 75.0
        }
        self.assertEqual(result, expected_score)

    def test_invalid_experience_format(self):
        """
        Test that invalid experience format returns 0 experience years.
        """
        invalid_experience_data = {
            'skills': ['Python'],
            'education': ['bachelor\'s'],
            'certifications': ['AWS Certified'],
            'experience': ['invalid experience']
        }
        matcher = ResumeJobMatcher(invalid_experience_data, self.job_data)
        result = matcher.calculate_experience_match()
        self.assertEqual(result, False)  # Invalid experience format should be treated as 0 years.

    def test_empty_job_experience(self):
        """
        Test that if job experience is empty or missing, it is handled properly.
        """
        job_data_no_experience = {
            'skills': ['Python'],
            'education': ['bachelor\'s'],
            'certifications': ['AWS Certified'],
            'experience': []
        }
        matcher = ResumeJobMatcher(self.resume_data, job_data_no_experience)
        result = matcher.calculate_experience_match()
        self.assertEqual(result, True)  # No experience requirement means match by default

if __name__ == '__main__':
    unittest.main()
