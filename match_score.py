import re

def clean_and_tokenize(keywords):
    tokens = set()
    for item in keywords:
        words = re.findall(r'\b[a-zA-Z]+\b', item.lower())
        tokens.update(words)
    return tokens

def calculate_match_score(jd_data, candidate_data):
    jd_skills = set(jd_data.get('skills', []))
    jd_certs = set(jd_data.get('certifications', []))

    candidate_skills = set(candidate_data.get('skills', []) + candidate_data.get('tech_stack', []))
    candidate_certs = set(candidate_data.get('certifications', []))

    matched_skills = jd_skills.intersection(candidate_skills)
    matched_certs = jd_certs.intersection(candidate_certs)

    total_possible = len(jd_skills) + len(jd_certs)
    total_matched = len(matched_skills) + len(matched_certs)

    score = (total_matched / total_possible) * 100 if total_possible > 0 else 0

    return round(score, 2), matched_skills, matched_certs