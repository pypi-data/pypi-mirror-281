# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["OutfitRecommendationResponse"]


class OutfitRecommendationResponse(BaseModel):
    indices: List[str]

    time_spent: str
