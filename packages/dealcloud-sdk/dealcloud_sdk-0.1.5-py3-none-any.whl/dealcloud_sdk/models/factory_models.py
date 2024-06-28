from pydantic import BaseModel
from typing import Union


class DealCloudFactoryArgs(BaseModel):
    site_url: str
    client_id: Union[str, int]
    client_secret: str
