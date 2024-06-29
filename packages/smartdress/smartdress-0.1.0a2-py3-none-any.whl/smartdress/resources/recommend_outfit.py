# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict

import httpx

from ..types import recommend_outfit_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import (
    make_request_options,
)
from ..types.outfit_recommendation_response import OutfitRecommendationResponse

__all__ = ["RecommendOutfitResource", "AsyncRecommendOutfitResource"]


class RecommendOutfitResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RecommendOutfitResourceWithRawResponse:
        return RecommendOutfitResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RecommendOutfitResourceWithStreamingResponse:
        return RecommendOutfitResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        descriptions: Dict[str, Dict[str, str]],
        query: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OutfitRecommendationResponse:
        """
        Get Outfit Recommendation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/recommend_outfit/",
            body=maybe_transform(
                {
                    "descriptions": descriptions,
                    "query": query,
                },
                recommend_outfit_create_params.RecommendOutfitCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OutfitRecommendationResponse,
        )


class AsyncRecommendOutfitResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRecommendOutfitResourceWithRawResponse:
        return AsyncRecommendOutfitResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRecommendOutfitResourceWithStreamingResponse:
        return AsyncRecommendOutfitResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        descriptions: Dict[str, Dict[str, str]],
        query: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OutfitRecommendationResponse:
        """
        Get Outfit Recommendation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/recommend_outfit/",
            body=await async_maybe_transform(
                {
                    "descriptions": descriptions,
                    "query": query,
                },
                recommend_outfit_create_params.RecommendOutfitCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OutfitRecommendationResponse,
        )


class RecommendOutfitResourceWithRawResponse:
    def __init__(self, recommend_outfit: RecommendOutfitResource) -> None:
        self._recommend_outfit = recommend_outfit

        self.create = to_raw_response_wrapper(
            recommend_outfit.create,
        )


class AsyncRecommendOutfitResourceWithRawResponse:
    def __init__(self, recommend_outfit: AsyncRecommendOutfitResource) -> None:
        self._recommend_outfit = recommend_outfit

        self.create = async_to_raw_response_wrapper(
            recommend_outfit.create,
        )


class RecommendOutfitResourceWithStreamingResponse:
    def __init__(self, recommend_outfit: RecommendOutfitResource) -> None:
        self._recommend_outfit = recommend_outfit

        self.create = to_streamed_response_wrapper(
            recommend_outfit.create,
        )


class AsyncRecommendOutfitResourceWithStreamingResponse:
    def __init__(self, recommend_outfit: AsyncRecommendOutfitResource) -> None:
        self._recommend_outfit = recommend_outfit

        self.create = async_to_streamed_response_wrapper(
            recommend_outfit.create,
        )
