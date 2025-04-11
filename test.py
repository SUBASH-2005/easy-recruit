from jd_parser import read_job_description
from resume_extractor import extract_resume_text, extract_candidate_details
from match_score import calculate_match_score
from shortlist_agent import save_to_db
from email_generator import generate_email

# Step 1: JD
jd_data = read_job_description("job_description.csv")

# Step 2: Resume
resume_text = extract_resume_text("C1070.pdf")
candidate_data = extract_candidate_details(resume_text)

# Step 3: Match Score
score, skills, certs = calculate_match_score(jd_data, candidate_data)
print(f"Match Score: {score}%")
print("Matched Skills:", skills)
print("Matched Certifications:", certs)
print("JD Skills:", jd_data['skills'])
print("Candidate Keywords:", candidate_data['skills'] + candidate_data['tech_stack'] + candidate_data['certifications'])

# Step 4: Shortlist and Save
threshold = 60.0
shortlisted = score >= threshold
save_to_db(candidate_data, score, shortlisted)

# Step 5: Generate Interview Email
if shortlisted:
    email = generate_email(candidate_data['name'], candidate_data['email'], jd_data['title'])
    print(email)
else:
    print(f"{candidate_data['name']} is not shortlisted.")
