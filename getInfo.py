#<span data-value="2025-11-16 15:00:00" id="schedule-date"></span>

import sys
from datetime import datetime, timezone

from bs4 import BeautifulSoup
import requests as r



link: str = sys.argv[1]

# crude argument handling
if not ("https://hianime.to/watch/" in link):
    print("Make sure the provided link are as followed: https://hianime.to/watch/<your_show_here>\nexiting..")
    exit()

html = r.get(link).text
soup = BeautifulSoup(html, "html.parser")

span_schedule_date = soup.find("span", id="schedule-date")
if(span_schedule_date == None):
    print("This show is not being aired currently!\nexiting..")
    exit()

raw_time = span_schedule_date.get("data-value")
local_dt = datetime.strptime(raw_time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

print(local_dt.astimezone())