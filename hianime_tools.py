from bs4 import BeautifulSoup

def parse_episode_list(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    
    episodes: list = []
    
    # find all the <a> tags with class 'ssl-item ep-item'
    for a in soup.find_all("a", class_="ep-item"):
        title: str = a.get("title")
        data_number: str = a.get("data-number")
        data_id: str = a.get("data-id")
        href: str = a.get("href")
    
        episodes.append({
            "title": title,
            "episode": data_number,
            "episodeId": data_id,
            "link": href
        })

    return episodes


def parse_servers(html: str) -> list:
    results: dict = {} # example: results["SUB"] = [{HD-1:dataId}]
    soup = BeautifulSoup(html, "html.parser")
    for block in soup.select("div.ps_-block-sub"):
        title_div = block.select_one(".ps__-title")
        language: str = title_div.get_text().replace(':','')
        
        server_dict: dict = {}
        for item in block.select(".server-item"):
            server: str = item.select_one("a").get_text()
            server_dict[server] = item.get("data-id")
        results[language] = server_dict

    return results


def parse_season_data(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    os_item = soup.select("a.os-item")

    season_data: dict = {}
    for i in os_item:
        season_data[i.select_one("div.title").get_text()] = i.get("href")
    return season_data



# get the embed link that then can be fed to megacloud.py to extract the m3u8 and sub links
def get_sources(sourceId: int) -> str:
    pass




def test() -> None:
    import requests as r
    html: str = r.get("https://hianime.to/ajax/v2/episode/list/552").json().get("html")
    episodes: list = parse_episode_list(html)
    for ep in episodes:
        print(ep)
    
    
    epId = episodes[3].get("episodeId")
    html = r.get("https://hianime.to/ajax/v2/episode/servers?episodeId="+epId).json().get("html")
    servers = parse_servers(html)
    print(servers)

if __name__ == "__main__":
    test()
