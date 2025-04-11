def generate_email(name, email, job_title):
    return f"""
To: {email}
Subject: Interview Invitation for {job_title}

Hi {name},

Congratulations! You’ve been shortlisted for the role of {job_title}.
We'd love to move ahead with the next round of interviews.

Please respond to schedule a suitable time.

Best regards,  
Team RecruitAI
"""
