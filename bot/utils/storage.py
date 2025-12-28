import json
import aiofiles
import os

async def read_json(file_path, default=[]):
    if not os.path.exists(file_path):
        return default
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
        content = await f.read()
        if not content:
            return default
        return json.loads(content)

async def write_json(file_path, data):
    async with aiofiles.open(file_path, mode='w', encoding='utf-8') as f:
        await f.write(json.dumps(data, indent=4, ensure_ascii=False))


