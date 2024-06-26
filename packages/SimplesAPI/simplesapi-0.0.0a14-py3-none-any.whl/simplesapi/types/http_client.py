import simplesapi.types.logger as logger
from typing import List
import httpx
from simplesapi.types import Cache, Cipher


class EncryptionRequiredError(Exception): ...

class HTTPClient:
    def __init__(
        self,
        cache: Cache = None,
        cipher: Cipher = None,
        log_requests: bool = False,
        log_responses: bool = False,
        unsafe_all_logs: bool = False,
        unsafe_request_keys: List[str] = [],
        unsafe_response_keys: List[str] = [],
    ):
        if not unsafe_all_logs and not cipher and (log_requests or log_responses):
            raise EncryptionRequiredError(
                "Encryption is required to log. Unsafe all logs must be set to True when logging requests."
            )
        self.cache = cache
        self.cipher = cipher
        self.log_requests = log_requests
        self.log_responses = log_responses
        self.unsafe_all_logs = unsafe_all_logs
        self.unsafe_request_keys = unsafe_request_keys
        self.unsafe_response_keys = unsafe_response_keys
        self.client = httpx.AsyncClient()

    async def get(self, url, headers=None):
        if self.log_requests:
            self._log_request(url, headers)
        response = await self.client.get(url, headers=headers)
        if self.log_responses:
            self._log_response(url, response)
        return response

    async def post(self, url, data, headers=None):
        if self.log_requests:
            self._log_request(url, headers, data)
        response = await self.client.post(url, data=data, headers=headers)
        if self.log_responses:
            self._log_response(url, response)
        return response

    async def put(self, url, data, headers=None):
        if self.log_requests:
            self._log_request(url, headers, data)
        response = await self.client.put(url, data=data, headers=headers)
        if self.log_responses:
            self._log_response(url, response)
        return response

    async def delete(self, url, headers=None):
        if self.log_requests:
            self._log_request(url, headers)
        response = await self.client.delete(url, headers=headers)
        if self.log_responses:
            self._log_response(url, response)
        return response

    def _log_request(self, url, headers=None, data=None):
        if headers:
            headers = self.cipher.encrypt(str(headers))
        if data:
            data = self.cipher.encrypt(str(data))
        logger.log.info(f"Request to {url}", context={"headers": headers, "data": data})

    def _log_response(self, url, response):
        if response:
            headers = self.cipher.encrypt({**response.headers})
            data = self.cipher.encrypt(response.text)
        logger.log.info(
            f"Response from {url}",
            context={
                "headers": headers,
                "data": data,
                "status_code": response.status_code,
            },
        )
