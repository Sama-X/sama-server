"""
DFX client.
"""

import base64
import json
import logging
import os
import re
import subprocess
from typing import Optional
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

        if error:
            logger.error("【dfx error】 reason: %s", error)
            return None
        return result

    @classmethod
    def add(cls, name, data):
        """
        add a new record.
        """
        data = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        scripts = (
            f'{cls.DFX_PATH} canister --network ic call {cls.SERVER} add '
            f'\'("{name}", "{data}")\''
        )
        return Record("add", cls._execute(scripts))

    @classmethod
    def get(cls, name):
        """
        Get the record.
        """
        scripts = (
            f'''{cls.DFX_PATH} canister --network ic call {cls.SERVER} get '(\"{name}\")' '''
        )
        return Record(name, cls._execute(scripts))

    @classmethod
    def remove(cls, name):
        """
        Remove the record.
        """
        scripts = (
            f'''{cls.DFX_PATH} canister --network ic call {cls.SERVER} remove '(\"{name}\")' '''
        )
        return Record("remove", cls._execute(scripts))

    @classmethod
    def list(cls):
        """
        list the record.
        """
        scripts = f'{cls.DFX_PATH} canister --network ic call {cls.SERVER} get_all'
        return Record('list', cls._execute(scripts))

    @classmethod
    def update(cls, name, data):
        """
        Update the record.
        """
        data = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        scripts = (
            f'{cls.DFX_PATH} canister --network ic call {cls.SERVER} update '
            f'\'("{name}", "{data}")\''
        )
        return Record("update", cls._execute(scripts))


class Record:
    """
    Record.
    """
    data: Optional[dict | list | str]
    error: Optional[str]

    def __init__(self, name, data):
        self.name = name
        print("data = ", data)
        self.parse(data)

    def parse(self, data):
        """
        Parse the data.
        """
        new_data = data.replace('\n', '')
        if not new_data or new_data == '(null)':
            self.data = None
            return
        if new_data.replace(' ', '').startswith('(opt"'):
            self.data = self.prase_text(new_data)
            return
        if new_data.replace(' ', '').startswith('(optvec{'):
            self.data = self.prase_list(new_data)
            return

    def prase_text(self, data):
        """
        Parse the text.
        such as: '(opt "Ok.")'
        """
        result = re.match(r'\(.*opt "(?P<data>.*?)".*\)', data)
        if not result:
            return None
        value = result.group('data')
        try:
            return json.loads(base64.b64decode(value).decode("utf-8"))
        except Exception as error:  # pylint: disable=broad-exception-caught
            self.error = str(error)
            return value

    def prase_list(self, data):
        """
        Parse the list.
        such as:'(  opt vec {
                        record {
                            5_343_647 = "test3";
                            834_174_833 = "eyJuYW1lIjogImxhZ2VsIiwgImFnZSI6IDIwfQ==";
                        };
                        record {
                            5_343_647 = "111"; 834_174_833 = "data1"
                        };
                    },
                )'
        """
        reg = re.compile(r'(?:5_343_647 = "(?P<name>.*?)".*?834_174_833 = "(?P<data>.*?)")+')
        items = reg.findall(data)
        if not items:
            return None

        result = []
        for name, value in items:
            try:
                value = base64.b64decode(value).decode("utf-8")
                value = json.loads(value)
            except ValueError:
                pass
            except Exception:  # pylint: disable=broad-exception-caught
                pass
            result.append({
                name: value
            })
        return result

    def __str__(self):
        """
        String.
        """
        return f"Record(name={self.name})"

    def __repr__(self):
        """
        Representation.
        """
        return self.__str__()
