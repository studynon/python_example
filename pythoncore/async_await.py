# %%
import asyncio
async def hello():
    print("Hello world!")
    r = await asyncio.sleep(2)
    print("Hello again!")

loop = asyncio.get_event_loop()
loop.run_until_complete(hello())

# %%
import asyncio
import time

async def f1():
    await asyncio.sleep(1)
    print("111111")
    await asyncio.sleep(1)
    print("222222")
    return 1

async def hello():
    print("Hello world!")
    r1 = await f1()
    print(r1)

loop = asyncio.get_event_loop()
loop.run_until_complete(hello())

# %%
# 生成器协程 or 原生协程
'''
其中 generator_coroutine 函数里因为用到了 yield 表达式，所以只能定义成基于生成器的协程；
native_coroutine 函数由于自身是协程,可以直接用 await 表达式调用其他协程；main 函数由于不是协程，
因而需要用 native_coroutine().send(None) 这种方式来调用协程。
'''
import types
@types.coroutine
def generator_coroutine():
    print(2)
    yield 1

async def native_coroutine():
    await generator_coroutine()
    print(3)

def main():
    native_coroutine().send(None)

main()

# %%
import asyncio
import requests
import aiohttp
import time

async def download(url): # 通过async def定义的函数是原生的协程对象
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            r1 = await resp.text()
            return r1

async def wait_download(url):
    t1 = time.time()
    r1 = await download(url) # 这里download(url)就是一个原生的协程对象
    print(f"get {url} data complete in {time.time()-t1} s")

start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([wait_download("http://www.163.com"),
                                        wait_download("http://www.jd.com"),
                                        wait_download("http://www.sina.com"),
                                        wait_download("http://www.taobao.com"),
                                        wait_download("http://www.sohu.com")]))
end = time.time()
print("Complete in {} seconds".format(end - start))

# %%
import asyncio
import requests

async def main():
    loop = asyncio.get_event_loop()
    future1 = loop.run_in_executor(None, requests.get, 'http://www.163.com')
    future2 = loop.run_in_executor(None, requests.get, 'http://www.taobao.com')
    future3 = loop.run_in_executor(None, requests.get, 'http://www.sina.com')
    future4 = loop.run_in_executor(None, requests.get, 'http://www.sohu.com')
    response1 = await future1
    response2 = await future2
    response3 = await future3
    response4 = await future4
    # print(response1.text)
    # print(response2.text)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
