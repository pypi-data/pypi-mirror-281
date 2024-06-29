# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List

from .._models import BaseModel

__all__ = ["GarmentDescriptionResponse"]


class GarmentDescriptionResponse(BaseModel):
    description_batch: List[Dict[str, str]]

    embedding_batch: List[List[float]]

    image_url_batch: List[str]

    time_spent_description_batch: str

    time_spent_embedding_batch: str
