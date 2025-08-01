import pickle
import json

from typing import Dict, List, Set
from circle_type import Circle


def main():
    with open("dict/id_dict.pkl", "rb") as f:
        id_dict: Dict[int, Circle] = pickle.load(f)

    urls_total_list: List[str] = []
    for _id, circle in id_dict.items():
        urls_total_list.extend(circle.CircleCutUrls)
        urls_total_list.extend(circle.WebCircleCutUrls)

        # if circle.Image1 is not None:
        #     turl = circle.Image1.ThumbnailUrl
        #     burl = circle.Image1.BigimageUrl
        #     urls_dict[id].append(turl)
        #     urls_dict[id].append(burl)

        # if circle.Image2 is not None:
        #     turl = circle.Image2.ThumbnailUrl
        #     burl = circle.Image2.BigimageUrl
        #     urls_dict[id].append(turl)
        #     urls_dict[id].append(burl)

    urls_set: Set[str] = set(urls_total_list)
    print(f"Duplicate circlecut urls: {len(urls_set)} / {len(urls_total_list)}")
    print(len(urls_set))
    urls_list: List[str] = list(urls_set)

    with open("dict/image_list.json", "wt") as f:
        json.dump(urls_list, f)

if __name__ == "__main__":
    main()
