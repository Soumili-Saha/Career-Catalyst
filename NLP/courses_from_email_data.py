import json
import re
from collections import Counter

# Load data from JSON file
def load_data_from_json(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []

# Preprocess keywords from email data
def preprocess_keywords(data):
    keywords = []
    for email in data:
        for key in ['subject', 'snippet']:
            if key in email:
                keywords.extend(email[key])
    # Clean and normalize the keywords (lowercase, remove punctuation)
    cleaned_keywords = [
        re.sub(r'[^\w\s]', '', keyword.lower()) for keyword in keywords
        if keyword.strip() and not keyword.isdigit()
    ]
    return cleaned_keywords

# Count the frequency of keywords
def count_keyword_frequency(keywords):
    return Counter(keywords).most_common()

# Recommend courses based on keywords, filtering out duplicates and missing links
def recommend_courses(ranked_keywords, keyword_to_courses):
    recommended_courses = []
    for keyword, _ in ranked_keywords:
        for category, data in keyword_to_courses.items():
            if keyword in data["keywords"]:
                recommended_courses.extend(data["courses"])
    
    # Filter out duplicate courses by course name and YouTube link
    seen = set()
    unique_courses = []
    for course in recommended_courses:
        # Use (course name, YouTube link) to identify duplicates
        course_name = course.get('course', '')
        youtube_link = course.get('link', '')
        
        if course_name and youtube_link:
            resource_tuple = (course_name, youtube_link)
            if resource_tuple not in seen:
                seen.add(resource_tuple)
                unique_courses.append(course)
    
    return unique_courses

if __name__ == "__main__":
    # File paths for input JSON (the user should provide these files)
    email_data_path = r'D:\python project\edtechwebsite\myenv\model\nlp\preprocessed_emails.json'  # Replace with actual file path
    keyword_to_courses_path = r'D:\python project\edtechwebsite\myenv\model\nlp\keywords_to_courses.json'  # Replace with actual file path
    
    # Load the JSON data
    email_data = load_data_from_json(email_data_path)
    keyword_to_courses = load_data_from_json(keyword_to_courses_path)
    
    if not email_data or not keyword_to_courses:
        print("Error: Missing or invalid input data.")
    else:
        # Preprocess the email data to extract keywords
        keywords = preprocess_keywords(email_data)
        ranked_keywords = count_keyword_frequency(keywords)

        # Recommend courses based on ranked keywords
        recommended_courses = recommend_courses(ranked_keywords, keyword_to_courses)
        
        # Output the introductory message and recommended courses
        if recommended_courses:
            print("Based on your email data, we have looked into these courses that may help you:")
            for course in recommended_courses:
                print(f"Course: {course['course']}, Link: {course.get('link', 'N/A')}")
        else:
            print("No relevant courses found based on your email data.")
