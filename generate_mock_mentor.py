import csv
from faker import Faker
import random 


# Initialize Faker for generating random user data
fake = Faker()

# Sample job titles and skills
job_titles = [
    "Software Engineer", "Data Scientist", "Product Manager", 
    "UX Designer", "Machine Learning Engineer", "DevOps Engineer", 
    "Full Stack Developer", "Backend Developer", "Frontend Developer", 
    "AI Specialist"
]
skills_pool = [
    "Python", "Java", "C++", "SQL", "AWS", "TensorFlow", "PyTorch", "React",
    "Node.js", "Docker", "Kubernetes", "Machine Learning", "Deep Learning",
    "Data Analysis", "Agile", "Team Leadership", "Communication",
    "Problem Solving", "Project Management", "Cloud Computing", "Software Architecture",
    "C#", "C", "HTML", "CSS", "Software Design", "Srum", "Program management", "User Interface Design"
    "Software Development"
]
educations = [
    "B.S. in Computer Science", "M.S. in Data Science",
    "B.A. in Information Technology", "Ph.D. in Artificial Intelligence",
    "B.S. in Electrical Engineering", "B.A. in Computer Science", "M.S. in Computer Science",
    "M.S. in Computer Engineering", "B.S. in Computer Engineering"
]
locations = [
    "New York, NY", "San Francisco, CA", "Seattle, WA", "Austin, TX",
    "London, UK", "Berlin, Germany", "Toronto, Canada", "Sydney, Australia",
    "Singapore", "Paris, France", "Los Angeles, CA", "San Diego, CA", "Seoul, South Korea",
    "Atlanta, GA", "Chicago, IL", 
]

def generate_mentor_profile():
    """
    Generate a single mock mentor profile with consistent keys
    matching the CSV column names.
    """
    job_title = random.choice(job_titles)
    location = random.choice(locations)
    education_level = random.choice(educations)
    
    # Choose 5 random skills
    chosen_skills = random.sample(skills_pool, k=5)
    
    # Convert the Python list to a string, e.g.: "Python, AWS, React, ..."
    skills_str = ", ".join(chosen_skills)
    
    years_of_experience = random.randint(5, 40)  # 5 to 20 years
    # Generate a random summary (not saved to CSV, just an example)
    summary = fake.paragraph(nb_sentences=3)
    
    return {
        # These keys match the fieldnames in the CSV
        "Name": fake.name(),
        "Job Title": job_title,
        "Location": location,
        "Education": education_level,
        "Years of Experience": years_of_experience,
        "Skills": skills_str,
        "LinkedIn Profile": fake.url(),
    }

def main():
    """
    Generate a CSV of mock mentor profiles.
    """
    number_of_profiles = 100  # Adjust as needed

    # Generate mock data
    profiles = [generate_mentor_profile() for _ in range(number_of_profiles)]

    # Define the CSV columns (they must match the dictionary keys exactly)
    fieldnames = [
        "Name",
        "Job Title",
        "Location",
        "Education",
        "Years of Experience",
        "Skills",
        "LinkedIn Profile",
    ]

    # Write to CSV and generate
    output_filename = "mock_profiles.csv"
    with open(output_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(profiles)

    print(f"Generated {number_of_profiles} mock profiles in {output_filename}")

if __name__ == "__main__":
    main()