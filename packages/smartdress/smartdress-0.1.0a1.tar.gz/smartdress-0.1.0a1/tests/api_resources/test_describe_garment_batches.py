# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from smartdress import Smartdress, AsyncSmartdress
from tests.utils import assert_matches_type
from smartdress.types import GarmentDescriptionResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDescribeGarmentBatches:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Smartdress) -> None:
        describe_garment_batch = client.describe_garment_batches.create(
            image_url_batch=["string", "string", "string"],
        )
        assert_matches_type(GarmentDescriptionResponse, describe_garment_batch, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Smartdress) -> None:
        response = client.describe_garment_batches.with_raw_response.create(
            image_url_batch=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        describe_garment_batch = response.parse()
        assert_matches_type(GarmentDescriptionResponse, describe_garment_batch, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Smartdress) -> None:
        with client.describe_garment_batches.with_streaming_response.create(
            image_url_batch=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            describe_garment_batch = response.parse()
            assert_matches_type(GarmentDescriptionResponse, describe_garment_batch, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDescribeGarmentBatches:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSmartdress) -> None:
        describe_garment_batch = await async_client.describe_garment_batches.create(
            image_url_batch=["string", "string", "string"],
        )
        assert_matches_type(GarmentDescriptionResponse, describe_garment_batch, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSmartdress) -> None:
        response = await async_client.describe_garment_batches.with_raw_response.create(
            image_url_batch=["string", "string", "string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        describe_garment_batch = await response.parse()
        assert_matches_type(GarmentDescriptionResponse, describe_garment_batch, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSmartdress) -> None:
        async with async_client.describe_garment_batches.with_streaming_response.create(
            image_url_batch=["string", "string", "string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            describe_garment_batch = await response.parse()
            assert_matches_type(GarmentDescriptionResponse, describe_garment_batch, path=["response"])

        assert cast(Any, response.is_closed) is True
