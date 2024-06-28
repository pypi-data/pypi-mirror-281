from typing import Union, Dict, Any
import os
from dotenv import load_dotenv
load_dotenv()

Scope = {
    'PUBLIC': 'public',
    'ACCOUNT': 'account',
    'ADMIN': 'admin',
    'GLOBAL': 'global',
    'ORGANIZATION': 'organization',
    'STUDY': 'study',
}

RecordSchemaType = Union[str, str, str]

APIID = Union[int, str]

class APIOption:
    def __init__(self, header: Dict[str, str] = None, param: Dict[str, str] = None):
        self.header = header if header else {}
        self.param = param if param else {}

from typing import TypeVar, Generic
T = TypeVar('T')

class APIResponse(Generic[T]):
    def __init__(self, data: T):
        self.data = data

class GetRecordPayload(Generic[T]):
    def __init__(self, record: T):
        self.record = record
        
class Config:
    HOST_URL = os.getenv("HOST_URL")
    AUTH_TOKEN = os.getenv("AUTH_TOKEN")

    @staticmethod
    def validate():
        if not Config.HOST_URL or not Config.AUTH_TOKEN:
            raise ValueError("Please set the HOST_URL and AUTH_TOKEN environment variables.")