# ffmpeg -fflags +genpts -i local.m3u8 -c copy -avoid_negative_ts make_zero 

import argparse
import asyncio
import aiohttp
import hls_tools

# just a simple ansi terminal color here, it's rather crude
COLORS: dict = {
    "BLACK": "\033[0;30m",
    "RED": "\033[0;31m",
    "GREEN": "\033[0;32m",
    "BROWN": "\033[0;33m",
    "BLUE": "\033[0;34m",
    "PURPLE": "\033[0;35m",
    "CYAN": "\033[0;36m",
    "LIGHT_GRAY": "\033[0;37m",
    "DARK_GRAY": "\033[1;30m",
    "LIGHT_RED": "\033[1;31m",
    "LIGHT_GREEN": "\033[1;32m",
    "YELLOW": "\033[1;33m",
    "LIGHT_BLUE": "\033[1;34m",
    "LIGHT_PURPLE": "\033[1;35m",
    "LIGHT_CYAN": "\033[1;36m",
    "LIGHT_WHITE": "\033[1;37m",
    "BOLD": "\033[1m",
    "FAINT": "\033[2m",
    "ITALIC": "\033[3m",
    "UNDERLINE": "\033[4m",
    "BLINK": "\033[5m",
    "NEGATIVE": "\033[7m",
    "CROSSED": "\033[9m",
    "END": "\033[0m",
}

MAX_CONCURRENT_DOWNLOADS: int = 10
semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

MAX_RETRIES: int = 10
TIMEOUT_DURATION: int = 30

async def download_segment(session, url: str, filename: str) -> None:
    async with semaphore:
        for attempt in range(1, MAX_RETRIES+1):
            try:
                async with asyncio.timeout(TIMEOUT_DURATION):
                    async with session.get(url,
                                           timeout=aiohttp.ClientTimeout(total=TIMEOUT_DURATION),
                                           headers={"referer":"https://megacloud.blog/"}) as resp:
                        if resp.status != 200:
                            raise Exception(f"Server return bad status : {resp.status}")
                        data = await resp.read()
                        
                        # it's probably a good idea to separate this writing part and just return the data. we'll see.
                        try:
                            with open(filename, 'wb') as f:
                                f.write(data)
                            print(f"Done writing data to {filename}")
                            return
                        except OSError as e:
                            if e.errno == errno.ENOSPC:  # No space left on device
                                raise RuntimeError(f"Disk full! Cannot write {filename}") from e
                            else:
                                raise  # re-raise other OSErrors
                        
            except asyncio.TimeoutError:
                print(f"{COLORS['YELLOW']}[{attempt}/{MAX_RETRIES} Timeout] {filename}{COLORS['END']}")
            except Exception as err:
                print(f"{COLORS['YELLOW']}[{attempt}/{MAX_RETRIES} Retrying...] {filename}: {err}{COLORS['END']}")
    
                await asyncio.sleep(attempt) # crude backoff
                
        print(f"{COLORS['RED']}FAILED TO DOWNLOAD {filename}{COLORS['END']}")


import os
async def test() -> None:
    m3u8 = open("../samples/index-f3-v1-a1.m3u8").read()
    localized_m3u8 = hls_tools.localize_m3u8(m3u8, os.getcwd())
    with open("./local.m3u8",'w') as f:
        f.write(localized_m3u8)
        
    segment_links =  hls_tools.get_segment_links(m3u8)
    segment_filenames = hls_tools.get_segment_filenames_fixed_extension(m3u8)
    # async with aiohttp.ClientSession() as session:
    #     tasks = [download_segment(session, url, filename) for url, filename in zip(segment_links, segment_filenames)]
    #     await asyncio.gather(*tasks)

async def main() -> None:
    parser = argparse.ArgumentParser(prog="hianime-dl")
    parser.add_argument("link")
    parser.add_argument("-q", "--quality", type=int, default=2)

if __name__ == "__main__":
    asyncio.run(test())
