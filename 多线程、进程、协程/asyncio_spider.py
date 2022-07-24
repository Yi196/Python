import asyncio
import aiohttp
import blog_spider

#定义协程
async def async_craw(url):
    print('craw url:',url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.text()
            print(f'craw url:{url}', {len(result)})

#定义主事件循环
loop = asyncio.get_event_loop()

#定义tasks
tasks = [
    loop.create_task(async_craw(url))
    for url in blog_spider.urls
]

import time

start = time.time()
loop.run_until_complete(asyncio.wait(tasks))
end = time.time()
print('Time:',end-start, 'Seconds')