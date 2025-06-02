import requests
from bs4 import BeautifulSoup
import re


def clean_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = ' '.join(text.split())
        return text
    return ''


# # Take user input for skills
user_skills = input("Enter your skills (comma-separated): ")
# user_skills = clean_text(user_skills)

# # Perform web scraping from TimesJobs
html = "https://www.naukri.com/python-development-jobs"
query_params = {
    "k": user_skills,  # Job keywords (e.g., skills like Python, Java)
    "qproductJobSource": "2",  # Source ID for job filtering
    "naukriCampus": "true",  # Whether the job is a campus job
    "experience": "0",  # Experience level (0 for freshers)
    "nignbevent_src": "jobsearchDeskGNB",  # Event source ID
}


response = requests.get(html, params=query_params)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('div', class_='srp-jobtuple-wrapper')

    print("\nRecommended Jobs:")
    print("-" * 50)

    for job in jobs:
        # job_title = job.find('a').text.strip() if job.find('a') else "N/A"
        # job_link = job.find('a')['href'] if job.find('a') else "N/A"
        comp_name = job.find('span', class_='comp-dtls-wrap').text.strip() if job.find('span', class_='comp-dtls-wrap') else "N/A"
        # skills_data = job.find('span', class_='srp-skills').text.strip() if job.find('span', class_='srp-skills') else "N/A"
        # job_location = job.find('ul', class_='top-jd-dtl clearfix').find('li').text.strip() if job.find('ul', class_='top-jd-dtl clearfix') else "N/A"
        # posted_date = job.find('span', class_='sim-posted').text.strip() if job.find('span', class_='sim-posted') else "N/A"

        # print(f"Job Title: {job_title}")
        print(f"Company Name: {comp_name}")
        # print(f"Location: {job_location}")
        # print(f"Skills Required: {skills_data}")
        # print(f"Posted Date: {posted_date}")
        # print(f"Job Link: {job_link}")
        # print("-" * 50)
else:
    print("Failed to fetch job data from TimesJobs.")
















from urllib.parse import urlencode

final_url = f"{html}?{urlencode(query_params)}"
print(final_url)
