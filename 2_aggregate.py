import json
import pickle

from typing import Dict, List, Any
from circle_type import Circle, MAX_DICT

def main():
    id_dict: Dict[int, Circle] = {}
    cid_dict: Dict[int, Circle] = {}
    zero_cid_list: List[Circle] = []

    for day, max_page in MAX_DICT.items():
        for page in range(1, max_page + 1):
            with open(f"resp_json/day{day}-page{page}.json", "rt") as f:
                data = json.load(f)

            for circle in data["Circles"]:
                circle = Circle.model_validate(circle)
                if circle.Id in id_dict:
                    raise ValueError(f"Duplicate id: {circle.Name}")
                else:
                    id_dict[circle.Id] = circle

                if circle.CircleId == 0:
                    zero_cid_list.append(circle)
                elif circle.CircleId in cid_dict:
                    raise ValueError(f"Duplicate cid: {circle.Name}")
                else:
                    cid_dict[circle.CircleId] = circle


    with open("dict/id_dict.pkl", "wb") as f:
        pickle.dump(id_dict, f)

    with open("dict/id_dict.json", "wt") as f:
        id_dict_dump: Dict[int, Dict[str, Any]] = {
            id: obj.model_dump()
            for id, obj in id_dict.items()
        }
        json.dump(id_dict_dump, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
