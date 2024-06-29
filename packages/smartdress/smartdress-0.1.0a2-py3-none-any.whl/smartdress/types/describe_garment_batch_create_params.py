# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["DescribeGarmentBatchCreateParams"]


class DescribeGarmentBatchCreateParams(TypedDict, total=False):
    image_url_batch: Required[List[str]]
