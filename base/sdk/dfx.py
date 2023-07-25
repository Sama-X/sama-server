"""
DFX client.
"""

import logging
import os
import subprocess
from base.config import get_settings


logger = logging.getLogger(__name__)


class DFXClient:
    """
    DFX client.
    """

    SERVER = get_settings().dfx_server
    DFX_PATH = get_settings().dfx_path

    @classmethod
    def _check_env(cls):
        """
        Check the environment.
        """
        if not cls.SERVER:
            logger.error("DFX server is not set.")
            return False

        if not cls.DFX_PATH:
            logger.error("DFX path is not set.")
            return False

        if not os.path.exists(cls.DFX_PATH):
            logger.error("DFX path %s is not exists.", cls.DFX_PATH)
            return False

        return True

    @classmethod
    def _execute(cls, scripts):
        """
        Execute the scripts.
        """
        if not cls._check_env():
            return False

        print(scripts)
        result, error = None, None
        with subprocess.Popen(
            scripts, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ) as process:
            process.wait()
            result, error = process.communicate()
            result = result.decode("utf-8")

        print(result)
        if error:
            logger.error("【dfx error】 reason: %s", error)
            return None
        return result

    @classmethod
    def add(cls, name, description, data):
        """
        add a new record.
        """
        scripts = (
            f'{cls.DFX_PATH} canister --network ic call {cls.SERVER} add '
            f'\"(record name = "{name}"; description = "{description}";'
            f' keywords = vec {{"{data}"}})\"'
        )
        return cls._execute(scripts)

    @classmethod
    def get(cls, name):
        """
        Get the record.
        """
        scripts = (
            f'''{cls.DFX_PATH} canister --network ic call {cls.SERVER} get '(\"{name}\")' '''
        )
        return cls._execute(scripts)

    @classmethod
    def remove(cls, name):
        """
        Remove the record.
        """
        scripts = (
            f'''{cls.DFX_PATH} canister --network ic call {cls.SERVER} remove '(\"{name}\")' '''
        )
        return cls._execute(scripts)

    @classmethod
    def search(cls, keyword):
        """
        Search the record.
        """
        scripts = (
            f'''{cls.DFX_PATH} canister --network ic call {cls.SERVER} search '("{keyword}")' '''
        )
        return cls._execute(scripts)

    @classmethod
    def traverse(cls):
        """
        Traverse the record.
        """
        scripts = f'{cls.DFX_PATH} canister --network ic call {cls.SERVER} traverse'
        return cls._execute(scripts)

    @classmethod
    def update(cls, name, description, data):
        """
        Update the record.
        """
        scripts = (
            f'{cls.DFX_PATH} canister --network ic call {cls.SERVER} update '
            f'\"(record name = "{name}"; description = "{description}";'
            f' keywords = vec {{"{data}"}})\"'
        )
        return cls._execute(scripts)
