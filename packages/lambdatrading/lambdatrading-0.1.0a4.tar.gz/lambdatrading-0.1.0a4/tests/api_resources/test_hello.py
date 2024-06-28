# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from lambdatrading import LambdaTrading, AsyncLambdaTrading

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestHello:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_get(self, client: LambdaTrading) -> None:
        hello = client.hello.get()
        assert_matches_type(str, hello, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: LambdaTrading) -> None:
        response = client.hello.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        hello = response.parse()
        assert_matches_type(str, hello, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: LambdaTrading) -> None:
        with client.hello.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            hello = response.parse()
            assert_matches_type(str, hello, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncHello:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_get(self, async_client: AsyncLambdaTrading) -> None:
        hello = await async_client.hello.get()
        assert_matches_type(str, hello, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncLambdaTrading) -> None:
        response = await async_client.hello.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        hello = await response.parse()
        assert_matches_type(str, hello, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncLambdaTrading) -> None:
        async with async_client.hello.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            hello = await response.parse()
            assert_matches_type(str, hello, path=["response"])

        assert cast(Any, response.is_closed) is True
