import json
import requests
import time
from bs4 import BeautifulSoup
from bs4.filter import SoupStrainer
from circle_type import MAX_DICT

STRAINER = SoupStrainer(id="TheModel")

def get_data(session: requests.Session, day: int, page: int):
    url = f"https://webcatalog.circle.ms/Circle/List?day={day}&page={page}"

    resp = session.get(url)

    if resp.status_code == 200:
        with open(f"resp_raw/day{day}-page{page}.html", "wt") as f:
            f.write(resp.text)
        soup = BeautifulSoup(resp.text, "html.parser", parse_only=STRAINER)
        elem = soup.find(id="TheModel")

        if elem:
            content = elem.get_text(strip=True)
            data = json.loads(content)
            with open(f"resp_json/day{day}-page{page}.json", "wt") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            raise ValueError(f"Request with day{day}, page{page}: TheModel not found")
    else:
        raise ValueError(
            f"Request with day{day}, page{page} failed with {resp.status_code}"
        )

def main():
    session = requests.Session()
    with open("cookies.json", "rt") as f:
        cookies_list = json.load(f)

    for cookie in cookies_list:
        session.cookies.set(  # type: ignore
            cookie["name"],
            cookie["value"],
            domain=cookie["domain"],
            path=cookie["path"],
        )

    for day, max_page in MAX_DICT.items():
        for page in range(1, max_page + 1):
            get_data(session, day, page)
            time.sleep(0.5)


if __name__ == "__main__":
    main()
