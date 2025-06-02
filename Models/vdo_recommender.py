import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from bs4 import BeautifulSoup
import requests
import lxml


def clean_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = ' '.join(text.split())
        return text
    return ''


def youtube_search(query, api_key, max_results=3):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": "AIzaSyAex-XVQ4AmXetNrgREc8C9hHU4ZdEvwxc"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()
        videos = []
        for item in results.get("items", []):
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            videos.append({"title": title, "url": f"https://www.youtube.com/watch?v={video_id}"})
        return videos
    else:
        print("YouTube API Error:", response.json())
        return []


jobs_df = pd.read_csv(r'D:\python project\edtechwebsite\myenv\datasets\Jobs_usable.csv')
courses_df = pd.read_csv(r'D:\python project\edtechwebsite\myenv\datasets\coursera_course_dataset_v3.csv')


jobs_df['skills'] = jobs_df['skills'].apply(clean_text)
courses_df['Skills'] = courses_df['Skills'].apply(clean_text)


skills_vectorizer = TfidfVectorizer(stop_words='english')
job_skills_matrix = skills_vectorizer.fit_transform(jobs_df['skills'])
course_skills_matrix = skills_vectorizer.transform(courses_df['Skills'])

# Take user input for skills
user_skills = input("Enter your skills (comma-separated): ")
user_skills = clean_text(user_skills)

# # Vectorize user skills
user_skills_vector = skills_vectorizer.transform([user_skills])


job_similarities = cosine_similarity(user_skills_vector, job_skills_matrix)
n_jobs = 5
top_job_indices = job_similarities[0].argsort()[-n_jobs:][::-1]

print("Recommended Jobs:")
print("-------------------------------")
for i, idx in enumerate(top_job_indices, 1):
    print(f"\n{i}. Job Title: {jobs_df.iloc[idx]['Job Title']}")
    print(f"Role: {jobs_df.iloc[idx]['Role']}")
    print(f"Required Experience: {jobs_df.iloc[idx]['Experience']}")
    print(f"Required Skills: {jobs_df.iloc[idx]['skills']}")
    print(f"Similarity Score: {job_similarities[0][idx]:.2f}")


html = "https://www.timesjobs.com/candidate/job-search.html"
query_params = {
    "searchType": "personalizedSearch",
    "from": "submit",
    "txtKeywords": user_skills,
    "txtLocation": ""
}

# page = 1
# for _ in range(1, 3):
#     query_params["sequence"] = page
response = requests.get(html, params=query_params)
soup = BeautifulSoup(response.text, 'lxml')

jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

for job in jobs:
    comp_name = job.find('h3', class_='joblist-comp-name').text.strip()
    skills_data = job.find('div', class_='more-skills-sections').text.splitlines()
    skills = [item.strip() for item in skills_data if item.strip()]
    job_location = job.find('li', class_='srp-zindex location-tru').text.strip()

    print(f"Company Name: {comp_name}")
    print(f"Job Location: {job_location}")
    print(f"Skills Required: {skills}")
    print('-' * 50)

    # page += 1

# Skill gap analysis and course recommendations
api_key = "AIzaSyAex-XVQ4AmXetNrgREc8C9hHU4ZdEvwxc"
target_job = input("\nEnter the job title to analyze skill gaps (e.g., Data Scientist): ").lower()
target_jobs = jobs_df[jobs_df['Job Title'].str.lower() == target_job]

if len(target_jobs) > 0:
    target_skills = set(target_jobs.iloc[0]['skills'].split())
    user_skills_set = set(user_skills.split())
    missing_skills = target_skills - user_skills_set

    print(f"\nSkill Gaps for {target_job.capitalize()}:")
    print("----------------------------------------")
    if missing_skills:
        print("\nSkills you might want to learn:")
        for skill in missing_skills:
            print(f"- {skill}")

        # Find courses specifically for missing skills
        missing_skills_text = " ".join(missing_skills)
        missing_skills_vector = skills_vectorizer.transform([missing_skills_text])
        gap_course_similarities = cosine_similarity(missing_skills_vector, course_skills_matrix)
        top_gap_course_indices = gap_course_similarities[0].argsort()[-3:][::-1]

        print("\nRecommended Courses for Skill Gaps:")
        print("----------------------------------")
        for i, idx in enumerate(top_gap_course_indices, 1):
            print(f"\n{i}. Course Title: {courses_df.iloc[idx]['Title']}")
            print(f"Organization: {courses_df.iloc[idx]['Organization']}")
            print(f"Duration: {courses_df.iloc[idx]['Duration']}")
            print(f"Difficulty: {courses_df.iloc[idx]['Difficulty']}")
            print(f"Course URL: {courses_df.iloc[idx]['course_url']}")

        # Recommend YouTube videos for missing skills
        print("\nRecommended YouTube Videos for Skill Gaps:")
        print("------------------------------------------")
        youtube_videos = youtube_search(missing_skills_text, api_key)
        for i, video in enumerate(youtube_videos, 1):
            print(f"\n{i}. Title: {video['title']}")
            print(f"URL: {video['url']}")
    else:
        print("You already have all the common skills required for this position!")
