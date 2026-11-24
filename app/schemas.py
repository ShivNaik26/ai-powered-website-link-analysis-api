
from typing import Any

from pydantic import BaseModel, Field, ConfigDict


class LinkAnalysisRequest(BaseModel):
    url: str = Field(
        ...,
        description="Public website URL to analyze",
        examples=["https://example.com"]
    )


class BrandInfo(BaseModel):
    name: str = ""
    category: str = ""
    summary: str = ""


class CompetitorAnalysis(BaseModel):
    brand_overview: str = ""
    business_category: str = ""
    main_products_services: list[str] = Field(default_factory=list)
    competitors: list[dict[str, Any] | str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    competitive_advantages: list[str] = Field(default_factory=list)
    opportunities: list[str] = Field(default_factory=list)


class SEOImprovements(BaseModel):
    primary_keyword: str = ""
    secondary_keywords: list[str] = Field(default_factory=list)
    long_tail_keywords: list[str] = Field(default_factory=list)
    business_keywords: list[str] = Field(default_factory=list)
    recommended_title: str = ""
    meta_description: str = ""
    supporting_content: list[str] = Field(default_factory=list)


class TargetAudience(BaseModel):
    primary_audience: list[str] = Field(default_factory=list)
    secondary_audience: list[str] = Field(default_factory=list)
    industries: list[str] = Field(default_factory=list)
    business_types: list[str] = Field(default_factory=list)
    customer_profiles: list[str] = Field(default_factory=list)
    geographical_focus: list[str] = Field(default_factory=list)
    customer_needs: list[str] = Field(default_factory=list)
    customer_interests: list[str] = Field(default_factory=list)
    marketing_segments: list[str] = Field(default_factory=list)


class WebsiteAnalysis(BaseModel):
    competitor_analysis: CompetitorAnalysis
    target_search_queries: list[dict[str, Any] | str] = Field(default_factory=list)
    seo_improvements: SEOImprovements
    top_services: list[dict[str, Any]] = Field(default_factory=list)
    target_audience: TargetAudience


class TokenUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


class LinkAnalysisResponse(BaseModel):
    success: bool = True
    website: dict[str, Any]
    brand: BrandInfo
    analysis: WebsiteAnalysis
    usage: TokenUsage = Field(default_factory=TokenUsage)
