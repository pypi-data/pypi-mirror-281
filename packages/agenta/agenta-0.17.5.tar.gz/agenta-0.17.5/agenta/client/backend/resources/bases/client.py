# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

from ...core.api_error import ApiError
from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.remove_none_from_dict import remove_none_from_dict
from ...errors.unprocessable_entity_error import UnprocessableEntityError
from ...types.base_output import BaseOutput
from ...types.http_validation_error import HttpValidationError

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class BasesClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def list_bases(
        self,
        *,
        app_id: typing.Optional[str] = None,
        base_name: typing.Optional[str] = None,
    ) -> typing.List[BaseOutput]:
        """
        Retrieve a list of bases filtered by app_id and base_name.

        Args:
        request (Request): The incoming request.
        app_id (Optional[str], optional): The ID of the app to filter by. Defaults to None.
        base_name (Optional[str], optional): The name of the base to filter by. Defaults to None.

        Returns:
        List[BaseOutput]: A list of BaseOutput objects representing the filtered bases.

        Raises:
        HTTPException: If there was an error retrieving the bases.

        Parameters:
            - app_id: typing.Optional[str].

            - base_name: typing.Optional[str].
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.bases.list_bases()
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "bases"),
            params=remove_none_from_dict({"app_id": app_id, "base_name": base_name}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[BaseOutput], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncBasesClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def list_bases(
        self,
        *,
        app_id: typing.Optional[str] = None,
        base_name: typing.Optional[str] = None,
    ) -> typing.List[BaseOutput]:
        """
        Retrieve a list of bases filtered by app_id and base_name.

        Args:
        request (Request): The incoming request.
        app_id (Optional[str], optional): The ID of the app to filter by. Defaults to None.
        base_name (Optional[str], optional): The name of the base to filter by. Defaults to None.

        Returns:
        List[BaseOutput]: A list of BaseOutput objects representing the filtered bases.

        Raises:
        HTTPException: If there was an error retrieving the bases.

        Parameters:
            - app_id: typing.Optional[str].

            - base_name: typing.Optional[str].
        ---
        from agenta.client import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.bases.list_bases()
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "bases"),
            params=remove_none_from_dict({"app_id": app_id, "base_name": base_name}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[BaseOutput], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
