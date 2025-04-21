from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from .service import SchemeService
from .models import SchemeResponse
from typing import List, Optional
from pathlib import Path

app = FastAPI(
    title="Agricultural Schemes API",
    description="API for accessing agricultural schemes in multiple languages"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

# Templates
templates = Jinja2Templates(directory="src/frontend/templates")

scheme_service = SchemeService()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/schemes/", response_model=List[SchemeResponse])
async def get_schemes(
    lang: str = Query("en", description="Language code (en/hi/mr)"),
    level: Optional[str] = Query(None, description="Scheme level (central/state)")
):
    try:
        return scheme_service.get_all_schemes(lang, level)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/schemes/{scheme_id}", response_model=SchemeResponse)
async def get_scheme(
    scheme_id: str,
    lang: str = Query("en", description="Language code (en/hi/mr)")
):
    try:
        scheme = scheme_service.get_scheme_by_id(scheme_id, lang)
        if not scheme:
            raise HTTPException(status_code=404, detail="Scheme not found")
        return scheme
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 