"""
Custom API response module.
"""

class APIResponse(dict):
    """
    APIResponse is a dict subclass that can be used to send API responses.
    """

    def __init__(self, code, data=None, **kwargs):
        """
        Initialize APIResponse.
        """
        result = {
            'code': code
        }
        if data is not None:
            if isinstance(data, str):
                result['message'] = data
            elif 'data' in data or 'message' in data:
                result.update(data)
            else:
                result['data'] = data

        kwargs.update(result)
        super().__init__(**kwargs)
