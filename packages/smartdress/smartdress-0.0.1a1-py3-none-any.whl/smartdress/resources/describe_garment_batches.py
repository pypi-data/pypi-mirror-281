# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ..types import describe_garment_batch_create_params
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
from ..types.garment_description_response import GarmentDescriptionResponse

__all__ = ["DescribeGarmentBatchesResource", "AsyncDescribeGarmentBatchesResource"]


class DescribeGarmentBatchesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DescribeGarmentBatchesResourceWithRawResponse:
        return DescribeGarmentBatchesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DescribeGarmentBatchesResourceWithStreamingResponse:
        return DescribeGarmentBatchesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        image_url_batch: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GarmentDescriptionResponse:
        """
        Get Garment Descriptions

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1/describe_garment_batch/",
            body=maybe_transform(
                {"image_url_batch": image_url_batch},
                describe_garment_batch_create_params.DescribeGarmentBatchCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GarmentDescriptionResponse,
        )


class AsyncDescribeGarmentBatchesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDescribeGarmentBatchesResourceWithRawResponse:
        return AsyncDescribeGarmentBatchesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDescribeGarmentBatchesResourceWithStreamingResponse:
        return AsyncDescribeGarmentBatchesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        image_url_batch: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GarmentDescriptionResponse:
        """
        Get Garment Descriptions

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1/describe_garment_batch/",
            body=await async_maybe_transform(
                {"image_url_batch": image_url_batch},
                describe_garment_batch_create_params.DescribeGarmentBatchCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GarmentDescriptionResponse,
        )


class DescribeGarmentBatchesResourceWithRawResponse:
    def __init__(self, describe_garment_batches: DescribeGarmentBatchesResource) -> None:
        self._describe_garment_batches = describe_garment_batches

        self.create = to_raw_response_wrapper(
            describe_garment_batches.create,
        )


class AsyncDescribeGarmentBatchesResourceWithRawResponse:
    def __init__(self, describe_garment_batches: AsyncDescribeGarmentBatchesResource) -> None:
        self._describe_garment_batches = describe_garment_batches

        self.create = async_to_raw_response_wrapper(
            describe_garment_batches.create,
        )


class DescribeGarmentBatchesResourceWithStreamingResponse:
    def __init__(self, describe_garment_batches: DescribeGarmentBatchesResource) -> None:
        self._describe_garment_batches = describe_garment_batches

        self.create = to_streamed_response_wrapper(
            describe_garment_batches.create,
        )


class AsyncDescribeGarmentBatchesResourceWithStreamingResponse:
    def __init__(self, describe_garment_batches: AsyncDescribeGarmentBatchesResource) -> None:
        self._describe_garment_batches = describe_garment_batches

        self.create = async_to_streamed_response_wrapper(
            describe_garment_batches.create,
        )
