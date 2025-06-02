import pandas as pd
import re

# Load dataset
jobs_df = pd.read_csv(r'D:\python project\edtechwebsite\myenv\datasets\Jobs_usable.csv')

# Function to clean text
def clean_text(text):
    if isinstance(text, str):
        text = text.lower()  # Convert to lowercase
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
        text = ' '.join(text.split())  # Remove extra spaces
        return text
    return ''

# Preprocess experience column
def preprocess_experience(experience):
    if isinstance(experience, str):
        numbers = re.findall(r'\d+', experience)
        if len(numbers) == 2:
            return (float(numbers[0]) + float(numbers[1])) / 2  # Average for ranges like "2 to 10 Years"
        elif len(numbers) == 1:
            return float(numbers[0])
    return 0.0  # Default if no valid number is found

# Apply preprocessing steps
jobs_df['skills'] = jobs_df['skills'].apply(clean_text)
jobs_df['Experience'] = jobs_df['Experience'].apply(preprocess_experience)
jobs_df['Qualifications'] = jobs_df['Qualifications'].apply(clean_text)
jobs_df['Work Type'] = jobs_df['Work Type'].apply(clean_text)
jobs_df['Responsibilities'] = jobs_df['Responsibilities'].apply(clean_text)

# Function to recommend jobs based on user input
def recommend_jobs(qualification, experience, top_skills):
    # Normalize user input
    qualification = clean_text(qualification)
    top_skills = [clean_text(skill) for skill in top_skills]

    recommendations = []

    for _, job in jobs_df.iterrows():
        job_skills = set(job['skills'].split())

        # Calculate skill match scores with weights for top skills
        skill_match_score = (
            (1 if top_skills[0] in job_skills else 0) * 0.5 +
            (1 if top_skills[1] in job_skills else 0) * 0.3 +
            (1 if top_skills[2] in job_skills else 0) * 0.2
        )

        # Check if the qualification matches (normalized)
        qualification_match = qualification in job['Qualifications']

        # Check if the experience requirement is met
        experience_match = experience >= job['Experience']

        # Calculate overall priority
        if skill_match_score > 0:  # Prioritize skills
            overall_score = (
                skill_match_score * 0.7 +
                (1 if qualification_match else 0) * 0.2 +
                (1 if experience_match else 0) * 0.1
            )
            recommendations.append((job['Job Title'], job['Role'], overall_score))

    # Normalize scores to ensure a minimum of 70%
    if recommendations:
        scores = [rec[2] for rec in recommendations]
        min_score, max_score = min(scores), max(scores)

        # Scale and adjust scores to the range 70-100
        adjusted_recommendations = []
        for job_title, role, score in recommendations:
            scaled_score = 70 + (score - min_score) / (max_score - min_score) * 30 if max_score > min_score else 100
            adjusted_recommendations.append((job_title, role, scaled_score))

        # Sort recommendations by adjusted scores in descending order
        adjusted_recommendations = sorted(adjusted_recommendations, key=lambda x: x[2], reverse=True)

        # Remove duplicates
        unique_recommendations = []
        seen_jobs = set()
        for job_title, role, scaled_score in adjusted_recommendations:
            if (job_title, role) not in seen_jobs:
                seen_jobs.add((job_title, role))
                unique_recommendations.append((job_title, role, scaled_score))

        return unique_recommendations[:5]  # Top 5 unique job recommendations
    return []

# Get user input
user_qualification = input("Enter your highest qualification (e.g., bca, m.tech): ").lower()
user_experience = float(input("Enter your total years of experience: "))

print("Enter your top 3 skills:")
user_top_skills = [
    input("Enter your first top skill: "),
    input("Enter your second top skill: "),
    input("Enter your third top skill: ")
]

# Recommend jobs
recommended_jobs = recommend_jobs(user_qualification, user_experience, user_top_skills)

print("\nRecommended Job Roles:")
print("-----------------------")
for i, (job_title, role, score) in enumerate(recommended_jobs, 1):
    print(f"{i}. Job Title: {job_title}")
    print(f"   Role: {role}")
    print(f"   Match Score: {score:.2f}")
