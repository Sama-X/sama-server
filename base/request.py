"""
request client.
"""

import logging
import requests


logger = logging.getLogger(__name__)


class RequestClient:
    """
    request client.
    """

    @classmethod
    def _request(cls, _method, url, **kwargs):
        """
        request
        """
        logger.info('【request client】start url: %s method: %s, params: %s', url, _method, kwargs)
        _method_func = getattr(requests, _method, requests.get)
        try:
            resp = _method_func(url, **kwargs)
        except Exception as error:
            logger.info('【request error url: %s method: %s error: %s', url, _method, error)
            raise error

        logger.info('【request client】end url: %s method: %s result: %s', url, _method, resp.text)

        return resp

    @classmethod
    def get(cls, url, **kwargs):
        """
        GET method.
        """
        return cls._request('get', url, **kwargs)

    @classmethod
    def post(cls, url, **kwargs):
        """
        post method.
        """
        return cls._request('post', url, **kwargs)

    @classmethod
    def put(cls, url, **kwargs):
        """
        put method.
        """
        return cls._request('put', url, **kwargs)

    @classmethod
    def delete(cls, url, **kwargs):
        """
        delete method.
        """
        return cls._request('delete', url, **kwargs)
