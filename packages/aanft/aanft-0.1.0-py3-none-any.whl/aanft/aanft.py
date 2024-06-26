import aiohttp
import asyncio
from loguru import logger
from typing_extensions import Self
from typing import List, Coroutine, Dict

ENDPOINTS_MAINNET = [
    "http://wax.eosusa.io/atomicassets", 
    "https://api.wax-aa.bountyblok.io/atomicassets", 
    "http://wax.blokcrafters.io/atomicassets", 
    "http://wax.blacklusion.io/atomicassets"
]
ENDPOINTS_TESTNET = [
    "https://test.wax.api.atomicassets.io",
    "https://wax-test.blokcrafters.io",
    "https://api.waxtest.waxgalaxy.io",
]
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

class AANFT:
    def __init__(self: Self, test: bool) -> None:
        """_summary_

        Args:
            test (bool): Testnet
        """
        self.network = "testnet" if test else "mainnet"
        self.endpoints =  ENDPOINTS_MAINNET if not test else ENDPOINTS_TESTNET
        self.prefered_endpoint = ENDPOINTS_MAINNET[0] if not test else ENDPOINTS_TESTNET[2]
        self.selected_endpoint = self.prefered_endpoint
        self.assets = "/v1/assets"
        self.headers = HEADERS
        self.max_tries = 3
        self.limit = 1000

    async def fetch_nfts(
        self: "AANFT", 
        account: str = "", 
        template: str = "", 
        schema: str = "", 
        collection: str = "") -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            resultcount = self.limit
            data = []
            page = 1
            n = 0
            endpoint = self.selected_endpoint + self.assets
            while resultcount == self.limit:
                n += 1
                logger.info(f"{n*1000} Assets Found so far...")
                params = {"limit": self.limit, "order": "asc", "page": page, "burned": "false"}
                if account:
                    params['owner'] = account
                if schema:
                    params['schema_name'] = schema
                if template:
                    params['template_id'] = template
                if collection:
                    params["collection_name"] = collection

                async with session.get(endpoint, params=params, headers=self.headers) as response:
                    assets = await response.json()
                if assets:
                    data += assets["data"]
                    resultcount = len(assets['data'])
                    page += 1
                else:
                    return data

            return data

    async def fetch_templates(
        self: Self,
        collection: str = "",
        template: str = ""
    ) -> List[Dict]:
        endpoint = self.selected_endpoint + "/v1/templates"
        async with aiohttp.ClientSession() as session:
            resultcount = self.limit
            data = []
            page = 1
            n = 0
            while resultcount == self.limit:
                n += 1
                params = {"limit": self.limit, "order": "asc", "page": page, "burned": "false"}
                if template:
                    params['template_id'] = template
                if collection:
                    params["collection_name"] = collection
                async with session.get(endpoint, params=params, headers=self.headers) as response:
                    templates = await response.json()
                if templates:
                    data += templates["data"]
                    resultcount = len(templates['data'])
                    page += 1
                else:
                    return data

            return data


    async def fetch_schemas(
        self: Self,
        collection: str = "",
        schema: str = ""
    ) -> List[Dict]:
        limit = 100
        resultcount = limit
        data = []
        page = 1
        n = 0
        endpoint = self.selected_endpoint + "/v1/schemas"
        async with aiohttp.ClientSession() as session:
            while resultcount == limit:
                n += 1
                params = {"limit": limit, "order": "asc", "page": page, "burned": "false"}
                if schema:
                    params['schema_name'] = schema
                if collection:
                    params["collection_name"] = collection
                async with session.get(endpoint, params=params, headers=self.headers) as response:
                    schemas = await response.json()
                    
                if schemas:
                    data += schemas["data"]
                    resultcount = len(schemas['data'])
                    page += 1
                else:
                    return data
            return data

    async def fetch_transactions(
        self: Self,
        sender: str = "",
        receiver: str = "",
        memo: str = ""
    ) -> List[Dict]:
        """_summary_

        Args:
            sender (str, optional): _sender account_. Defaults to "".
            receiver (str, optional): _receiver account_. Defaults to "".
            memo (str, optional): _memo_. Defaults to "".

        Returns:
            list: _List of transactions that fit criteria_
        """
        limit = 100
        resultcount = limit
        data = []
        page = 1
        n = 0
        endpoint = self.selected_endpoint + "/v1/transfers"
        async with aiohttp.ClientSession() as session:
            while resultcount == limit:
                n += 1
                params = {"limit": limit, "order": "asc", "page": page} #, "burned": "false"}
                if sender:
                    params['sender'] = sender
                if receiver:
                    params["receiver"] = receiver
                if memo:
                    params["memo"] = memo
                async with session.get(endpoint, params=params, headers=self.headers) as response:
                    transfers = await response.json()
                if transfers:
                    data += transfers["data"]
                    resultcount = len(transfers['data'])
                    page += 1
                else:
                    return data
            return data
                    

        



async def main():
    n = AANFT(False)
    nfts = await n.fetch_nfts(account="dl1rm.wam")
    schemas = await n.fetch_transactions(receiver="pixeltycoons", sender="dl1rm.wam", memo="ca")
    #print(len(schemas))
    #n.fetch_schemas

asyncio.run(main())