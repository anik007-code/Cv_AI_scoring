import PyPDF2
from collections import Counter
import spacy
import re
from datetime import datetime
from configs.config import programming_languages, pdf_path

nlp = spacy.load("en_core_web_sm")


def extract_text(pdf):
    with open(pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


def word_count(text):
    doc = nlp(text)
    token = [token.text for token in doc]
    words = [word for word in token if word.isalpha()]
    return len(Counter(words)) / 2 * 0.1


# print(word_count(extract_text(path)))

def assess_langauge_quality(text):
    doc = nlp(text)
    action_verbs = ["manage", "lead", "develop", "design", "implement", "analyze", "collaborate", "create",
                    "internship"]
    for token in doc:
        if token.pos_ == "VERB" and token.lemma_ in action_verbs:
            return len(token)


# print(assess_langauge_quality(extract_text(path)))


def assess_structure(cv_text):
    score = 0
    sections = ["education", "skills", "projects", "certifications", "contact", "summary"]
    for section in sections:
        if section in cv_text.lower():
            score += 5
    return score


# print(assess_structure(extract_text(path)))


def parse_date(date_str):
    """Parse various date formats into a datetime object."""
    formats = [
        '%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y',  # Common formats
        '%b %Y', '%B %Y',  # Short and full month names with year
        '%d %b %Y', '%d %B %Y',  # Full day and month names
        '%Y-%m', '%Y/%m',  # Year and month formats
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format for '{date_str}' is not recognized.")


def calculate_total_experience(cv_text):
    date_pattern = (r'(\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep('
                    r'?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) \d{4}|\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{'
                    r'4}|\d{2}/\d{2}/\d{2}|\d{2}-\d{2}-\d{2}|\b\d{4}[-/]\d{2})\s*[-to]*\s*(\b(?:Jan(?:uary)?|Feb('
                    r'?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct('
                    r'?:ober)?|Nov(?:ember)?|Dec(?:ember)?) \d{4}|\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4}|\d{2}/\d{2}/\d{'
                    r'2}|\d{2}-\d{2}-\d{2}|\b\d{4}[-/]\d{2}|Present)')

    dates = []
    matches = re.findall(date_pattern, cv_text)
    for match in matches:
        if not match:
            continue
        start_date_str = match[0].strip()
        end_date_str = match[1].strip() if len(match) > 1 else "Present"

        try:
            start_date_obj = parse_date(start_date_str)
        except ValueError:
            continue  # Skip invalid dates
        if end_date_str.lower() == 'present':
            end_date_obj = datetime.now()
        else:
            try:
                end_date_obj = parse_date(end_date_str)
            except ValueError:
                continue
        dates.append((start_date_obj, end_date_obj))

    total_experience = 0
    for start_date, end_date in dates:
        experience = (end_date - start_date).days / 365.25
        total_experience += experience
    return total_experience


def experience_score(text):
    total_experience = calculate_total_experience(text)
    if total_experience >= 5:
        return 20
    elif 3 <= total_experience < 5:
        return 15
    elif 1 <= total_experience < 3:
        return 10
    elif 0.5 <= total_experience < 1:
        return 5
    else:
        return 1


# print(experience_score(extract_text(path)))


def language_score(text):
    score = 0
    for language in programming_languages:
        if language in text:
            score += 2

    return score


# print(language_score(extract_text(pdf_path)))


def ai_cv_score():
    score1 = assess_langauge_quality(extract_text(pdf_path))
    score2 = assess_structure(extract_text(pdf_path))
    score3 = experience_score(extract_text(pdf_path))
    score4 = language_score(extract_text(pdf_path))
    score5 = word_count(extract_text(pdf_path))
    score = score1 + score2 + score3 + score4 + score5
    if score >= 100:
        return 99
    return score


print(ai_cv_score())
