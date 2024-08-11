# this will be changed day by day.
import PyPDF2
from collections import Counter
import spacy

nlp = spacy.load("en_core_web_sm")


def extract_text(pdf):
    with open(pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


def count_keywords(cv_text, keywords):
    words = cv_text.lower().split()
    word_count = Counter(words)
    return sum(word_count[keyword] for keyword in keywords if keyword in word_count)


def assess_structure(cv_text):
    sections = ["education", "experience", "skills", "projects", "certifications", "contact", "summary"]
    score = 0
    for section in sections:
        if section in cv_text.lower():
            score += 5
    return score


# Function to assess language quality
def assess_language_quality(cv_text):
    doc = nlp(cv_text)
    spelling_score = 10

    action_verbs = ["manage", "lead", "develop", "design", "implement", "analyze", "collaborate", "create"]
    action_verb_count = sum(1 for token in doc if token.lemma_ in action_verbs and token.pos_ == "VERB")
    action_verb_score = min(10, action_verb_count)

    return spelling_score + action_verb_score


# Advanced CV scoring function
def advanced_score_cv(cv_text):
    score = 0
    # Weighted criteria
    criteria = {
        "education": (["bachelor", "master", "phd", "degree", "university", "college"], 20),
        "experience": (["experience", "years", "worked", "managed", "project", "internship"], 25),
        "skills": (["python", "java", "excel", "sql", "data analysis", "communication", "leadership"], 25),
        "structure": ([], 20),
        "language_quality": ([], 10)
    }
    # Score for keyword-based criteria
    for key, (keywords, weight) in criteria.items():
        if key in ["structure", "language_quality"]:
            continue
        keyword_count = count_keywords(cv_text, keywords)
        score += min(weight, (keyword_count / len(keywords)) * weight)
    score += assess_structure(cv_text)
    score += assess_language_quality(cv_text)
    return score


# Example usage
pdf_file = 'Md_Arifur_Rahman_Anik_1716448919903.pdf'
cv_text = extract_text(pdf_file)
# print(cv_text)
cv_score = advanced_score_cv(cv_text)

print(f"Advanced CV Score: {cv_score}/100")
