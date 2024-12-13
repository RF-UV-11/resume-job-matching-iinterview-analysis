class ResumeJobMatcher:
    def __init__(self, resume_data, job_data):
        """
        Initializes the ResumeJobMatcher with resume and job data.

        Args:
            resume_data (dict): Extracted data from the resume (skills, education, certifications, experience, etc.).
            job_data (dict): Parsed job description data (skills, education, certifications, experience requirements, etc.).
        """
        self.resume_data = resume_data
        self.job_data = job_data

    def calculate_skill_match(self):
        """
        Calculates the skill matching score between the resume and the job description.

        Returns:
            float: Skill match percentage.
        """
        resume_skills = set(self.resume_data.get("skills", []))
        job_skills = set(self.job_data.get("skills", []))

        # If either job or resume skills are missing or empty, return 0
        if not job_skills or not resume_skills:
            return 0.0

        matched_skills = resume_skills.intersection(job_skills)
        return len(matched_skills) / len(job_skills) * 100

    def calculate_education_match(self):
        """
        Checks if the education qualifications in the resume match the job requirements.

        Returns:
            bool: True if any required education is matched, otherwise False.
        """
        resume_education = set(self.resume_data.get("education", []))
        job_education = set(self.job_data.get("education", []))

        # If either the job or resume education is empty, return False
        if not resume_education or not job_education:
            return False

        return bool(resume_education.intersection(job_education))

    def calculate_certification_match(self):
        """
        Calculates the certification matching score between the resume and the job description.

        Returns:
            float: Certification match percentage.
        """
        resume_certifications = set(self.resume_data.get("certifications", []))
        job_certifications = set(self.job_data.get("certifications", []))

        # If either the job or resume certifications are missing or empty, return 0
        if not job_certifications or not resume_certifications:
            return 0.0

        matched_certifications = resume_certifications.intersection(job_certifications)
        return len(matched_certifications) / len(job_certifications) * 100

    def _parse_experience(self, experience):
        """
        Parses an experience string like "3+" and returns the number of years as an integer.

        Args:
            experience_str (str): The experience string to parse (e.g., "3+" or "5 years").

        Returns:
            int: The number of years (treated as the minimum years if experience is "X+").
        """
        # Default to "0" if the experience list is empty
        if not experience:
            return 0

        experience_str = experience[0] if isinstance(experience, list) else experience
        
        try:
            # If the string contains "+", we take the number before it
            if '+' in experience_str:
                return int(experience_str.split('+')[0])
            # If the string is in the format "X years"
            elif 'year' in experience_str.lower():
                return int(experience_str.split(' ')[0])
            else:
                return int(experience_str)
        except ValueError:
            return 0  # Return 0 if the format is invalid

    def calculate_experience_match(self):
        """
        Compares experience levels between the resume and the job description.

        Returns:
            bool: True if the resume meets or exceeds the required experience, otherwise False.
        """
        job_experience = self.job_data.get("experience", "0 years")
        resume_experience = self.resume_data.get("experience", ["0 years"])

        # Parse the job experience
        job_years = self._parse_experience(job_experience)

        # Parse all resume experience entries and find the maximum
        resume_years = max([self._parse_experience(exp) for exp in resume_experience], default=0)

        return resume_years >= job_years

    def calculate_total_match_score(self):
        """
        Calculates an overall match score based on skills, education, certifications, and experience.

        Returns:
            dict: A dictionary with detailed match scores and the total match percentage.
        """
        skill_match = self.calculate_skill_match()
        education_match = self.calculate_education_match()
        certification_match = self.calculate_certification_match()
        experience_match = self.calculate_experience_match()

        # Adjust total_weight to handle the importance of each match component
        total_weight = 4  # Adjust weights as needed
        match_score = (
            (skill_match / 100) * 2 +  # Skills weighted higher
            (education_match * 1) +
            (certification_match / 100) * 1 +
            (experience_match * 1)
        ) / total_weight * 100

        return {
            "skill_match": skill_match,
            "education_match": education_match,
            "certification_match": certification_match,
            "experience_match": experience_match,
            "total_match_score": match_score
        }
