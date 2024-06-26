import aiohttp, asyncio, aiofiles, uuid, mimetypes, os, requests, json
from traceback import format_exc

class AsyncAniPlease:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "accept": "application/json",
            "api-key": self.api_key,
        }
        self.api_url = requests.get("https://gist.githubusercontent.com/1Me-Noob/2a1804b571dbbe80a1fdc453e52773e9/raw/link.txt").text
        self.loop = asyncio.get_event_loop()

    async def upload_file_request(self, headers: dict, data: dict) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.api_url}/UploadFile", headers=headers, data=data) as response:
                    return await response.json()
        except BaseException:
            raise aiohttp.ClientError(str(format_exc()))

    async def upload_file(self, filepath: str, anime_type: int, description: str, block: bool=True):
        filepath = os.path.join('./', filepath)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{filepath} not found!")
        boundary = uuid.uuid4().hex
        async with aiofiles.open(filepath, 'rb') as file:
            file_data = await file.read()
        filename = filepath.split('/')[-1]
        content_type = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
        data = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="data"\r\n'
            f'Content-Type: application/json\r\n\r\n'
            f'{{"category_id": {anime_type}, "description": "{description}"}}\r\n'
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f'Content-Type: {content_type}\r\n\r\n'
            f'{file_data.decode("ISO-8859-1")}\r\n'
            f'--{boundary}--\r\n'
        ).encode('ISO-8859-1')
        headers = dict(self.headers)
        headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'
        if block:
            return await self.upload_file_request(headers, data)
        return asyncio.ensure_future(self.upload_file_request(headers, data))

    def run(self):
        self.loop.run_forever()

class SyncAniPlease:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'accept': 'application/json',
            'api-key': api_key
        }
        self.api_url = requests.get("https://gist.githubusercontent.com/1Me-Noob/2a1804b571dbbe80a1fdc453e52773e9/raw/link.txt").text

    def upload_file(self, filepath: str, anime_type: int, description: str):
        filepath = os.path.join('./', filepath)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{filepath} not found!")
        with open(filepath, 'rb') as file:
            file_content = file.read()
        filename = filepath.split('/')[-1]
        content_type = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
        files = {'file': (filename, file_content, content_type)}
        try:
            response = requests.post(f"{self.api_url}/UploadFile", headers=self.headers, files=files, data={'data': json.dumps({"category_id": anime_type, "description": description})})
            return response.json()
        except BaseException:
            raise requests.RequestException(str(format_exc()))