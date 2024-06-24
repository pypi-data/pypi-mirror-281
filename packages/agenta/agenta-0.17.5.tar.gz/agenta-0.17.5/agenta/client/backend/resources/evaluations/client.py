# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

from ...core.api_error import ApiError
from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.jsonable_encoder import jsonable_encoder
from ...core.remove_none_from_dict import remove_none_from_dict
from ...errors.unprocessable_entity_error import UnprocessableEntityError
from ...types.evaluation import Evaluation
from ...types.evaluation_scenario import EvaluationScenario
from ...types.evaluation_webhook import EvaluationWebhook
from ...types.http_validation_error import HttpValidationError
from ...types.llm_run_rate_limit import LlmRunRateLimit

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class EvaluationsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def fetch_evaluation_ids(
        self,
        *,
        app_id: str,
        resource_type: str,
        resource_ids: typing.Optional[typing.Union[str, typing.List[str]]] = None,
    ) -> typing.List[str]:
        """
        Fetches evaluation ids for a given resource type and id.

        Arguments:
        app_id (str): The ID of the app for which to fetch evaluations.
        resource_type (str): The type of resource for which to fetch evaluations.
        resource_ids List[ObjectId]: The IDs of resource for which to fetch evaluations.

        Raises:
        HTTPException: If the resource_type is invalid or access is denied.

        Returns:
        List[str]: A list of evaluation ids.

        Parameters:
            - app_id: str.

            - resource_type: str.

            - resource_ids: typing.Optional[typing.Union[str, typing.List[str]]].
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.evaluations.fetch_evaluation_ids(
            app_id="app_id",
            resource_type="resource_type",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "evaluations/by_resource"
            ),
            params=remove_none_from_dict(
                {
                    "app_id": app_id,
                    "resource_type": resource_type,
                    "resource_ids": resource_ids,
                }
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[str], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def fetch_list_evaluations(self, *, app_id: str) -> typing.List[Evaluation]:
        """
        Fetches a list of evaluations, optionally filtered by an app ID.

        Args:
        app_id (Optional[str]): An optional app ID to filter the evaluations.

        Returns:
        List[Evaluation]: A list of evaluations.

        Parameters:
            - app_id: str.
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.evaluations.fetch_list_evaluations(
            app_id="app_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "evaluations"
            ),
            params=remove_none_from_dict({"app_id": app_id}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[Evaluation], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_evaluation(
        self,
        *,
        app_id: str,
        variant_ids: typing.List[str],
        evaluators_configs: typing.List[str],
        testset_id: str,
        rate_limit: LlmRunRateLimit,
        lm_providers_keys: typing.Optional[typing.Dict[str, str]] = OMIT,
        correct_answer_column: typing.Optional[str] = OMIT,
    ) -> typing.List[Evaluation]:
        """
        Creates a new comparison table document
        Raises:
        HTTPException: _description_
        Returns:
        _description_

        Parameters:
            - app_id: str.

            - variant_ids: typing.List[str].

            - evaluators_configs: typing.List[str].

            - testset_id: str.

            - rate_limit: LlmRunRateLimit.

            - lm_providers_keys: typing.Optional[typing.Dict[str, str]].

            - correct_answer_column: typing.Optional[str].
        ---
        from agenta import LlmRunRateLimit
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.evaluations.create_evaluation(
            app_id="app_id",
            variant_ids=["variant_ids"],
            evaluators_configs=["evaluators_configs"],
            testset_id="testset_id",
            rate_limit=LlmRunRateLimit(
                batch_size=1,
                max_retries=1,
                retry_delay=1,
                delay_between_batches=1,
            ),
        )
        """
        _request: typing.Dict[str, typing.Any] = {
            "app_id": app_id,
            "variant_ids": variant_ids,
            "evaluators_configs": evaluators_configs,
            "testset_id": testset_id,
            "rate_limit": rate_limit,
        }
        if lm_providers_keys is not OMIT:
            _request["lm_providers_keys"] = lm_providers_keys
        if correct_answer_column is not OMIT:
            _request["correct_answer_column"] = correct_answer_column
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "evaluations"
            ),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[Evaluation], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete_evaluations(
        self, *, evaluations_ids: typing.List[str]
    ) -> typing.List[str]:
        """
        Delete specific comparison tables based on their unique IDs.

        Args:
        delete_evaluations (List[str]): The unique identifiers of the comparison tables to delete.

        Returns:
        A list of the deleted comparison tables' IDs.

        Parameters:
            - evaluations_ids: typing.List[str].
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.evaluations.delete_evaluations(
            evaluations_ids=["evaluations_ids"],
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "DELETE",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "evaluations"
            ),
            json=jsonable_encoder({"evaluations_ids": evaluations_ids}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[str], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def fetch_evaluation_status(self, evaluation_id: str) -> typing.Any:
        """
        Fetches the status of the evaluation.

        Args:
        evaluation_id (str): the evaluation id
        request (Request): the request object

        Returns:
        (str): the evaluation status

        Parameters:
            - evaluation_id: str.
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.evaluations.fetch_evaluation_status(
            evaluation_id="evaluation_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"evaluations/{evaluation_id}/status",
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.Any, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def fetch_evaluation_results(self, evaluation_id: str) -> typing.Any:
        """
        Fetches the results of the evaluation

        Args:
        evaluation_id (str): the evaluation id
        request (Request): the request object

        Returns:
        _type_: _description_

        Parameters:
            - evaluation_id: str.
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.evaluations.fetch_evaluation_results(
            evaluation_id="evaluation_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"evaluations/{evaluation_id}/results",
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.Any, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def fetch_evaluation_scenarios(
        self, evaluation_id: str
    ) -> typing.List[EvaluationScenario]:
        """
        Fetches evaluation scenarios for a given evaluation ID.

        Arguments:
        evaluation_id (str): The ID of the evaluation for which to fetch scenarios.

        Raises:
        HTTPException: If the evaluation is not found or access is denied.

        Returns:
        List[EvaluationScenario]: A list of evaluation scenarios.

        Parameters:
            - evaluation_id: str.
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.evaluations.fetch_evaluation_scenarios(
            evaluation_id="evaluation_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"evaluations/{evaluation_id}/evaluation_scenarios",
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[EvaluationScenario], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def fetch_evaluation(self, evaluation_id: str) -> Evaluation:
        """
        Fetches a single evaluation based on its ID.

        Args:
        evaluation_id (str): The ID of the evaluation to fetch.

        Returns:
        Evaluation: The fetched evaluation.

        Parameters:
            - evaluation_id: str.
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.evaluations.fetch_evaluation(
            evaluation_id="evaluation_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"evaluations/{evaluation_id}",
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(Evaluation, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def webhook_example_fake(self) -> EvaluationWebhook:
        """
        Returns a fake score response for example webhook evaluation

        Returns:
        _description_

        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.evaluations.webhook_example_fake()
        """
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                "evaluations/webhook_example_fake",
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(EvaluationWebhook, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def fetch_evaluation_scenarios(self, *, evaluations_ids: str) -> typing.Any:
        """
        Fetches evaluation scenarios for a given evaluation ID.

        Arguments:
        evaluation_id (str): The ID of the evaluation for which to fetch scenarios.

        Raises:
        HTTPException: If the evaluation is not found or access is denied.

        Returns:
        List[EvaluationScenario]: A list of evaluation scenarios.

        Parameters:
            - evaluations_ids: str.
        ---
        from agenta.client import AgentaApi

        client = AgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        client.evaluations.fetch_evaluation_scenarios(
            evaluations_ids="evaluations_ids",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                "evaluations/evaluation_scenarios/comparison-results",
            ),
            params=remove_none_from_dict({"evaluations_ids": evaluations_ids}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.Any, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncEvaluationsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def fetch_evaluation_ids(
        self,
        *,
        app_id: str,
        resource_type: str,
        resource_ids: typing.Optional[typing.Union[str, typing.List[str]]] = None,
    ) -> typing.List[str]:
        """
        Fetches evaluation ids for a given resource type and id.

        Arguments:
        app_id (str): The ID of the app for which to fetch evaluations.
        resource_type (str): The type of resource for which to fetch evaluations.
        resource_ids List[ObjectId]: The IDs of resource for which to fetch evaluations.

        Raises:
        HTTPException: If the resource_type is invalid or access is denied.

        Returns:
        List[str]: A list of evaluation ids.

        Parameters:
            - app_id: str.

            - resource_type: str.

            - resource_ids: typing.Optional[typing.Union[str, typing.List[str]]].
        ---
        from agenta.client import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.evaluations.fetch_evaluation_ids(
            app_id="app_id",
            resource_type="resource_type",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "evaluations/by_resource"
            ),
            params=remove_none_from_dict(
                {
                    "app_id": app_id,
                    "resource_type": resource_type,
                    "resource_ids": resource_ids,
                }
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[str], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def fetch_list_evaluations(self, *, app_id: str) -> typing.List[Evaluation]:
        """
        Fetches a list of evaluations, optionally filtered by an app ID.

        Args:
        app_id (Optional[str]): An optional app ID to filter the evaluations.

        Returns:
        List[Evaluation]: A list of evaluations.

        Parameters:
            - app_id: str.
        ---
        from agenta.client import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.evaluations.fetch_list_evaluations(
            app_id="app_id",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "evaluations"
            ),
            params=remove_none_from_dict({"app_id": app_id}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[Evaluation], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_evaluation(
        self,
        *,
        app_id: str,
        variant_ids: typing.List[str],
        evaluators_configs: typing.List[str],
        testset_id: str,
        rate_limit: LlmRunRateLimit,
        lm_providers_keys: typing.Optional[typing.Dict[str, str]] = OMIT,
        correct_answer_column: typing.Optional[str] = OMIT,
    ) -> typing.List[Evaluation]:
        """
        Creates a new comparison table document
        Raises:
        HTTPException: _description_
        Returns:
        _description_

        Parameters:
            - app_id: str.

            - variant_ids: typing.List[str].

            - evaluators_configs: typing.List[str].

            - testset_id: str.

            - rate_limit: LlmRunRateLimit.

            - lm_providers_keys: typing.Optional[typing.Dict[str, str]].

            - correct_answer_column: typing.Optional[str].
        ---
        from agenta import LlmRunRateLimit
        from agenta.client import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.evaluations.create_evaluation(
            app_id="app_id",
            variant_ids=["variant_ids"],
            evaluators_configs=["evaluators_configs"],
            testset_id="testset_id",
            rate_limit=LlmRunRateLimit(
                batch_size=1,
                max_retries=1,
                retry_delay=1,
                delay_between_batches=1,
            ),
        )
        """
        _request: typing.Dict[str, typing.Any] = {
            "app_id": app_id,
            "variant_ids": variant_ids,
            "evaluators_configs": evaluators_configs,
            "testset_id": testset_id,
            "rate_limit": rate_limit,
        }
        if lm_providers_keys is not OMIT:
            _request["lm_providers_keys"] = lm_providers_keys
        if correct_answer_column is not OMIT:
            _request["correct_answer_column"] = correct_answer_column
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "evaluations"
            ),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[Evaluation], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete_evaluations(
        self, *, evaluations_ids: typing.List[str]
    ) -> typing.List[str]:
        """
        Delete specific comparison tables based on their unique IDs.

        Args:
        delete_evaluations (List[str]): The unique identifiers of the comparison tables to delete.

        Returns:
        A list of the deleted comparison tables' IDs.

        Parameters:
            - evaluations_ids: typing.List[str].
        ---
        from agenta.client import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.evaluations.delete_evaluations(
            evaluations_ids=["evaluations_ids"],
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "DELETE",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", "evaluations"
            ),
            json=jsonable_encoder({"evaluations_ids": evaluations_ids}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[str], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def fetch_evaluation_status(self, evaluation_id: str) -> typing.Any:
        """
        Fetches the status of the evaluation.

        Args:
        evaluation_id (str): the evaluation id
        request (Request): the request object

        Returns:
        (str): the evaluation status

        Parameters:
            - evaluation_id: str.
        ---
        from agenta.client import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.evaluations.fetch_evaluation_status(
            evaluation_id="evaluation_id",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"evaluations/{evaluation_id}/status",
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.Any, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def fetch_evaluation_results(self, evaluation_id: str) -> typing.Any:
        """
        Fetches the results of the evaluation

        Args:
        evaluation_id (str): the evaluation id
        request (Request): the request object

        Returns:
        _type_: _description_

        Parameters:
            - evaluation_id: str.
        ---
        from agenta.client import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.evaluations.fetch_evaluation_results(
            evaluation_id="evaluation_id",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"evaluations/{evaluation_id}/results",
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.Any, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def fetch_evaluation_scenarios(
        self, evaluation_id: str
    ) -> typing.List[EvaluationScenario]:
        """
        Fetches evaluation scenarios for a given evaluation ID.

        Arguments:
        evaluation_id (str): The ID of the evaluation for which to fetch scenarios.

        Raises:
        HTTPException: If the evaluation is not found or access is denied.

        Returns:
        List[EvaluationScenario]: A list of evaluation scenarios.

        Parameters:
            - evaluation_id: str.
        ---
        from agenta.client import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.evaluations.fetch_evaluation_scenarios(
            evaluation_id="evaluation_id",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"evaluations/{evaluation_id}/evaluation_scenarios",
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[EvaluationScenario], _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def fetch_evaluation(self, evaluation_id: str) -> Evaluation:
        """
        Fetches a single evaluation based on its ID.

        Args:
        evaluation_id (str): The ID of the evaluation to fetch.

        Returns:
        Evaluation: The fetched evaluation.

        Parameters:
            - evaluation_id: str.
        ---
        from agenta.client import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.evaluations.fetch_evaluation(
            evaluation_id="evaluation_id",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                f"evaluations/{evaluation_id}",
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(Evaluation, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def webhook_example_fake(self) -> EvaluationWebhook:
        """
        Returns a fake score response for example webhook evaluation

        Returns:
        _description_

        ---
        from agenta.client import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.evaluations.webhook_example_fake()
        """
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                "evaluations/webhook_example_fake",
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(EvaluationWebhook, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def fetch_evaluation_scenarios(self, *, evaluations_ids: str) -> typing.Any:
        """
        Fetches evaluation scenarios for a given evaluation ID.

        Arguments:
        evaluation_id (str): The ID of the evaluation for which to fetch scenarios.

        Raises:
        HTTPException: If the evaluation is not found or access is denied.

        Returns:
        List[EvaluationScenario]: A list of evaluation scenarios.

        Parameters:
            - evaluations_ids: str.
        ---
        from agenta.client import AsyncAgentaApi

        client = AsyncAgentaApi(
            api_key="YOUR_API_KEY",
            base_url="https://yourhost.com/path/to/api",
        )
        await client.evaluations.fetch_evaluation_scenarios(
            evaluations_ids="evaluations_ids",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/",
                "evaluations/evaluation_scenarios/comparison-results",
            ),
            params=remove_none_from_dict({"evaluations_ids": evaluations_ids}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.Any, _response.json())  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(pydantic.parse_obj_as(HttpValidationError, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
