# المسار: fallacy_analyzer_cloud/api/main.py

import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from fallacy_analyzer.nlp_pipeline import ArgumentNLPPipeline
from fallacy_analyzer.decision_tree import LogicalFallacyClassifier

app = FastAPI(
    title="محلل المغالطات المنطقية السحابي",
    description="تطبيق سحابي متكامل مع دعم PWA لتحليل المغالطات والبراهين المنطقية.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp_pipeline = ArgumentNLPPipeline()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class ArgumentRequest(BaseModel):
    text: str

class FallacyResponse(BaseModel):
    original_text: str
    raw_premises: List[str]
    implicit_premises: List[str]
    full_premises: List[str]
    extracted_conclusion: str
    detected_logical_form: Optional[str]
    classification_result: str

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "الخادم السحابي يعمل بنجاح"}

@app.get("/", include_in_schema=False)
async def serve_spa():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    raise HTTPException(status_code=404, detail="ملف واجهة المستخدم غير موجود")

@app.post("/analyze", response_model=FallacyResponse)
async def analyze_argument(request: ArgumentRequest) -> Dict[str, Any]:
    if not request.text or len(request.text.strip()) < 5:
        raise HTTPException(status_code=400, detail="النص المدخل قصير جداً أو غير صالح للاستدلال.")

    try:
        processed_data = nlp_pipeline.process_text(request.text)
        classifier = LogicalFallacyClassifier(processed_data)
        result_message = classifier.classify()

        return {
            "original_text": request.text,
            "raw_premises": processed_data.get("raw_premises", []),
            "implicit_premises": processed_data.get("implicit_premises", []),
            "full_premises": processed_data.get("premises", []),
            "extracted_conclusion": processed_data.get("conclusion", ""),
            "detected_logical_form": processed_data.get("logical_form"),
            "classification_result": result_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء معالجة الحجة: {str(e)}")
