from flask import Flask, request, jsonify
from flask_cors import CORS
from jd_parser import read_job_description
from resume_extractor import extract_resume_text, extract_candidate_details
from match_score import calculate_match_score
from shortlist_agent import save_to_db
from email_generator import generate_email
import os

app = Flask(__name__)
CORS(app)

jd_data_global = {}

@app.route('/upload-jd', methods=['POST'])
def upload_jd():
    file = request.files['jd']
    if file:
        global jd_data_global
        jd_data_global = read_job_description(file)
        return jsonify({"message": "JD processed", "jd": jd_data_global}), 200
    return jsonify({"error": "No file provided"}), 400

@app.route('/manual-jd', methods=['POST'])
def manual_jd():
    jd_text = request.json.get('jd_text', '')
    if not jd_text:
        return jsonify({"error": "No JD text provided"}), 400

    # Manually wrap the input to simulate CSV row
    jd_data = {
        "Job Title": "Manual Entry",
        "Job Description": jd_text
    }

    # Convert to same format as read_job_description()
    skill_bank = [
        'python', 'sql', 'tensorflow', 'pytorch', 'docker',
        'kubernetes', 'git', 'rest apis', 'django', 'flask',
        'nlp', 'machine learning', 'deep learning', 'linux',
        'cybersecurity', 'communication', 'agile'
    ]
    cert_bank = ['ceh', 'aws certified', 'pmp', 'cissp']

    extracted_skills = [skill for skill in skill_bank if skill in jd_text.lower()]
    extracted_certs = [cert for cert in cert_bank if cert in jd_text.lower()]

    jd_result = {
        "title": jd_data["Job Title"],
        "skills": extracted_skills,
        "certifications": extracted_certs
    }

    # Store to global for rest of flow
    global jd_data_global
    jd_data_global = jd_result

    return jsonify({"jd": jd_result})
@app.route('/upload-resumes', methods=['POST'])
def upload_resumes():
    if not jd_data_global:
        return jsonify({"error": "No JD uploaded"}), 400

    files = request.files.getlist('resumes')
    results = []

    for pdf in files:
        try:
            resume_text = extract_resume_text(pdf)
            candidate = extract_candidate_details(resume_text)
            score, skills, certs = calculate_match_score(jd_data_global, candidate)
            is_shortlisted = score >= 50.0
            save_to_db(candidate, score, is_shortlisted)
            email = generate_email(candidate['name'], candidate['email'], jd_data_global['title']) if is_shortlisted else "Not shortlisted"

            results.append({
                "name": candidate['name'],
                "email": candidate['email'],
                "score": score,
                "shortlisted": is_shortlisted,
                "email_invite": email if is_shortlisted else None
            })
        except Exception as e:
            results.append({
                "error": f"Error processing {pdf.filename}: {str(e)}"
            })

    return jsonify({"results": results}), 200

if __name__ == '__main__':
    app.run(debug=True)
