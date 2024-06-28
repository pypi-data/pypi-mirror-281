# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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

__all__ = ["HelloResource", "AsyncHelloResource"]


class HelloResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> HelloResourceWithRawResponse:
        return HelloResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> HelloResourceWithStreamingResponse:
        return HelloResourceWithStreamingResponse(self)

    def get(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """Returns a 'hello world' message"""
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return self._get(
            "/hello",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class AsyncHelloResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncHelloResourceWithRawResponse:
        return AsyncHelloResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncHelloResourceWithStreamingResponse:
        return AsyncHelloResourceWithStreamingResponse(self)

    async def get(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """Returns a 'hello world' message"""
        extra_headers = {"Accept": "text/plain", **(extra_headers or {})}
        return await self._get(
            "/hello",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=str,
        )


class HelloResourceWithRawResponse:
    def __init__(self, hello: HelloResource) -> None:
        self._hello = hello

        self.get = to_raw_response_wrapper(
            hello.get,
        )


class AsyncHelloResourceWithRawResponse:
    def __init__(self, hello: AsyncHelloResource) -> None:
        self._hello = hello

        self.get = async_to_raw_response_wrapper(
            hello.get,
        )


class HelloResourceWithStreamingResponse:
    def __init__(self, hello: HelloResource) -> None:
        self._hello = hello

        self.get = to_streamed_response_wrapper(
            hello.get,
        )


class AsyncHelloResourceWithStreamingResponse:
    def __init__(self, hello: AsyncHelloResource) -> None:
        self._hello = hello

        self.get = async_to_streamed_response_wrapper(
            hello.get,
        )
