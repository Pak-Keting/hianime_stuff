import sys

import requests as r

import hianime_tools


# crude argument detection
if(len(sys.argv) != 2):
    print(sys.argv[0] + " requires 1 argument!\nexiting.")
    exit(1)

html: str = r.get(
    hianime_tools.BASE_LINK + "/ajax/search/suggest",
    params={"keyword": sys.argv[1]}
).json().get("html")
search_results = hianime_tools.parse_search_result(html)
max_len = max(len(title) for title in search_results)

for title, link in search_results.items():
    print(f"{title:<{max_len + 2}}{hianime_tools.BASE_LINK}/watch{link}")
print()