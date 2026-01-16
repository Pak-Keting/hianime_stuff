#<span data-value="2025-11-16 15:00:00" id="schedule-date"></span>

from bs4 import BeautifulSoup
from datetime import datetime, timezone
import requests as r



html: str = open("./samples/hianime/watch_gachiakuta-19785").read()

html = r.get("https://hianime.to/watch/jujutsu-kaisen-the-culling-game-part-1-20401").text
soup = BeautifulSoup(html, "html.parser")

raw_time = soup.find("span", id="schedule-date").get("data-value")
print(raw_time)
dt = datetime.strptime(raw_time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

print(dt.astimezone())