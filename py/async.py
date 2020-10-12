import asyncio
import aiohttp


async def main():
    async for r in f():
        print(r)


async def f():
    urls = [
        'https://raw.githubusercontent.com/yuki-mt/scripts/master/cp_link.sh',
        'https://raw.githubusercontent.com/yuki-mt/scripts/master/py/find_huge_vars.py',
        'https://raw.githubusercontent.com/yuki-mt/scripts/master/video.sh'
    ]
    session = aiohttp.ClientSession()
    res = await asyncio.gather(*[request(session, url) for url in urls])
    for r in res:
        yield r
    await session.close()


async def request(session, url):
    async with session.get(url) as res:
        res = await res.text()
        return res.split('\n')[1]

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
