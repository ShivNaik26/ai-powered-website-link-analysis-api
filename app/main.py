
from fastapi import FastAPI, HTTPException
from app.config import APP_NAME, APP_VERSION
from app.schemas import LinkAnalysisRequest, LinkAnalysisResponse
from app.services.analysis_service import analyze_link
from app.utils.validators import validate_website_url

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="AI-powered website link analysis API using Gemini."
)


@app.get("/")
async def home():
    return {
        "message": "AI-Powered Website Link Analysis API is running",
        "version": APP_VERSION
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post(
    "/link-analysis",
    response_model=LinkAnalysisResponse
)
async def link_analysis(request: LinkAnalysisRequest):
    try:
        validated_url = validate_website_url(request.url)
        result = await analyze_link(validated_url)
        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during website analysis."
        ) from exc
