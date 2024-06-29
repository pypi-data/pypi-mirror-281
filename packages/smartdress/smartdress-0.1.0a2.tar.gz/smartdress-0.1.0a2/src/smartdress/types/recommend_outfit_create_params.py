# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["RecommendOutfitCreateParams"]


class RecommendOutfitCreateParams(TypedDict, total=False):
    descriptions: Required[Dict[str, Dict[str, str]]]

    query: Required[str]
