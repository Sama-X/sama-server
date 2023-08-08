"""
sama sdk.
"""

from pydantic import BaseModel
from base.config import get_settings
from base.request import RequestClient


class SamaSDK:
    """
    SamaSDK
    """

    API_DICT = {
        'platform.getBlockchains': '{}/ext/bc/P',
        'samavm.getNodes': '{}/ext/bc/{}/public'
    }
    SAMA_SERVER = get_settings().sama_server
    SAMA_ID = None

    @classmethod
    def get_sama_id_from_server(cls):
        """
        Get sama id from server.
        """
        url = cls.API_DICT['platform.getBlockchains'].format(cls.SAMA_SERVER)
        payload = {
            'jsonrpc': '2.0',
            'method': 'platform.getBlockchains',
            'params': {},
            'id': 1
        }
        resp = RequestClient.post(url, json=payload)
        if resp.status_code != 200:
            return None
        result = resp.json()
        blockchains = result.get('result', {}).get('blockchains', [])
        for blockchain in blockchains:
            if blockchain.get('name') == 'sama':
                return blockchain.get('id')

        return None

    @classmethod
    def get_sama_id(cls):
        """
        Get sama id.
        """
        if not cls.SAMA_ID:
            cls.SAMA_ID = cls.get_sama_id_from_server()
        return cls.SAMA_ID

    @classmethod
    def get_sama_nodes(cls):
        """
        Get sama nodes.
        """
        sama_id = cls.get_sama_id()
        url = cls.API_DICT['samavm.getNodes'].format(cls.SAMA_SERVER, sama_id)
        payload = {
            'jsonrpc': '2.0',
            'method': 'samavm.getNodes',
            'params': {
                'isActive': True
            },
            'id': 1
        }
        resp = RequestClient.post(url, json=payload)
        if resp.status_code != 200:
            return []
        result = resp.json()
        nodes = result.get('result', {}).get('nodes') or []

        return [Node(**node) for node in nodes]


class Node(BaseModel):
    """
    Node
    """
    txId: str
    stakerType: int
    stakerAddr: str
    country: str
    workKey: str
    localIP: str
    minPort: int
    maxPort: int
    publicIP: str
    checkPort: int
    workAddr: str
    isActive: bool
