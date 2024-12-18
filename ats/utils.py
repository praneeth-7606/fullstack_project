import pdfplumber

def parse_resume(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def call_llama_api(resume_text, job_description):
    # Mock API call
    import requests
    api_url = "http://llama-api-endpoint/"
    payload = {'resume': resume_text, 'jd': job_description}
    response = requests.post(api_url, json=payload)
    return response.json().get('score', 0)
