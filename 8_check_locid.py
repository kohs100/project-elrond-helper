import pickle

from typing import Dict, List, Set
from circle_type import Circle


def main():
    with open("dict/id_dict.pkl", "rb") as f:
        id_dict: Dict[int, Circle] = pickle.load(f)

    locid_list: List[str] = []
    locid_set: Set[str] = set()
    for _, circle in id_dict.items():
        locid = circle.Day + circle.Hall + circle.Block

        if locid not in locid_set:
            locid_set.add(locid)
            locid_list.append(locid)

    for locid in locid_list:
        print(locid)

if __name__ == "__main__":
    main()
