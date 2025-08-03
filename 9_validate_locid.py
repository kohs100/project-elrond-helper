import json
from typing import Dict, List

def main():
    lst_ldict: Dict[str, str] = {}

    with open("locid.lst", "rt") as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            assert len(line) == 4

            jp = line[2]
            kr = line[3]

            lst_ldict[jp] = kr

    lst_rdict: Dict[str, List[str]] = {}
    with open("locid.json", "rt") as f:
        locid_dic: Dict[str, str] = json.load(f)

        for jp, kr in locid_dic.items():
            if jp in lst_ldict:
                assert lst_ldict[jp] == kr, f"{jp} - {kr} - {lst_ldict[jp]}"
            if kr not in lst_rdict:
                lst_rdict[kr] = []
            lst_rdict[kr].append(jp)
    with open("locid_rev.json", "wt") as f:
        json.dump(lst_rdict, f, ensure_ascii=False, indent=2)



if __name__ == "__main__":
    main()
