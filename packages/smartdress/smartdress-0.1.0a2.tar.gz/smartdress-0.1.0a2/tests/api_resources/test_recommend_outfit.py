# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from smartdress import Smartdress, AsyncSmartdress
from tests.utils import assert_matches_type
from smartdress.types import OutfitRecommendationResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRecommendOutfit:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Smartdress) -> None:
        recommend_outfit = client.recommend_outfit.create(
            descriptions={"foo": {"foo": "string"}},
            query="string",
        )
        assert_matches_type(OutfitRecommendationResponse, recommend_outfit, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Smartdress) -> None:
        response = client.recommend_outfit.with_raw_response.create(
            descriptions={"foo": {"foo": "string"}},
            query="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        recommend_outfit = response.parse()
        assert_matches_type(OutfitRecommendationResponse, recommend_outfit, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Smartdress) -> None:
        with client.recommend_outfit.with_streaming_response.create(
            descriptions={"foo": {"foo": "string"}},
            query="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            recommend_outfit = response.parse()
            assert_matches_type(OutfitRecommendationResponse, recommend_outfit, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncRecommendOutfit:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSmartdress) -> None:
        recommend_outfit = await async_client.recommend_outfit.create(
            descriptions={"foo": {"foo": "string"}},
            query="string",
        )
        assert_matches_type(OutfitRecommendationResponse, recommend_outfit, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSmartdress) -> None:
        response = await async_client.recommend_outfit.with_raw_response.create(
            descriptions={"foo": {"foo": "string"}},
            query="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        recommend_outfit = await response.parse()
        assert_matches_type(OutfitRecommendationResponse, recommend_outfit, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSmartdress) -> None:
        async with async_client.recommend_outfit.with_streaming_response.create(
            descriptions={"foo": {"foo": "string"}},
            query="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            recommend_outfit = await response.parse()
            assert_matches_type(OutfitRecommendationResponse, recommend_outfit, path=["response"])

        assert cast(Any, response.is_closed) is True
