import json
from .logger import logger
from aiohttp import ClientSession, ClientResponseError


class HttpUtil:
    @staticmethod
    async def _http_request(method, url, data_map=None, params=None, **kwargs):
        try:
            async with ClientSession() as session:
                async with session.request(method, url, json=data_map, params=params, **kwargs) as response:
                    data = await response.text(encoding="utf-8")
                    response.raise_for_status()
        except ClientResponseError as e:
            logger.error(f"Network: HTTP error when requesting {url}. Error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Network: Unknown error when requesting {url}. Error: {str(e)}")
            return None

        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            logger.error(
                f"Network: requested {url} with data_map={data_map}, params={params}, response {data}, decode failed...")
            return None

    @staticmethod
    async def http_post(url, data_map=None, **kwargs):
        return await HttpUtil._http_request("POST", url, data_map=data_map, **kwargs)

    @staticmethod
    async def http_get(url, params=None, **kwargs):
        return await HttpUtil._http_request("GET", url, params=params, **kwargs)
