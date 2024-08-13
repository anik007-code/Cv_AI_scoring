from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from main import extract_text, assess_langauge_quality, experience_score, assess_structure, language_score, word_count

app = FastAPI()


@app.post('/score')
async def cv_score(request: Request):
    form_data = await request.form()
    file: UploadFile = form_data.get('file')
    if file is None or file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    pdf_content = await file.read()

    # Now extract text from the PDF content
    pdf_text = extract_text(pdf_content)
    score1 = assess_langauge_quality(pdf_text)
    score2 = assess_structure(pdf_text)
    score3 = experience_score(pdf_text)
    score4 = language_score(pdf_text)
    score5 = word_count(pdf_text)

    total_score = score1 + score2 + score3 + score4 + score5
    if total_score >= 100:
        total_score = 99

    score = {"cv_score": total_score}

    return JSONResponse(score)
