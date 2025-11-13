from bs4 import BeautifulSoup

def parse_episode_list(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    
    episodes: list = []
    
    # find all the <a> tags with class 'ssl-item ep-item'
    for a in soup.find_all("a", class_="ep-item"):
        title = a.get("title")
        data_number = a.get("data-number")
        data_id = a.get("data-id")
        href = a.get("href")
    
        episodes.append({
            "title": title,
            "episode": data_number,
            "episodeId": data_id,
            "link": href
        })

    return episodes


def parse_servers(html: str) -> list:
    results = {}
    soup = BeautifulSoup(html, "html.parser")
    for block in soup.select("div.ps_-block-sub"):
        title_div = block.select_one(".ps__-title")
        language = title_div.get_text().replace(':','')
        results[language] = [] # results["SUB"] = [{HD-1:dataId}]
    
        
        
        server_dict = {}
        for item in block.select(".server-item"):
            server = item.select_one("a").get_text()
            server_dict[server] = item.get("data-id")
        results[language].append(server_dict)

    return results




if __name__ == "__main__":
    import requests as r
    html: str = r.get("https://hianime.to/ajax/v2/episode/list/504").json().get("html")
    episodes: list = parse_episode_list(html)
    for ep in episodes:
        print(ep)
    
    
    epId = episodes[3].get("episodeId")
    html = r.get("https://hianime.to/ajax/v2/episode/servers?episodeId="+epId).json().get("html")
    servers = parse_servers(html)
    print(servers)