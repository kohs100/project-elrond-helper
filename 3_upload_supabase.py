from dotenv import load_dotenv
from unicodedata import normalize

import os
import pickle

from typing import Dict, Any, List
from circle_type import Circle
from supabase import create_client, Client, ClientOptions
from tqdm import trange

load_dotenv()

DAY_EVENT={
    "土": 1,
    "日": 2
}
CIRCLE_TYPE=1
BATCH_SIZE=64

def batch_insert(supabase: Client, rows: List[Dict[str, Any]], table: str):
    num_batch = len(rows) // BATCH_SIZE + 1

    for batch_idx in trange(num_batch):
        idx_begin = batch_idx * BATCH_SIZE
        idx_end = idx_begin + BATCH_SIZE
        if len(rows) < idx_end:
            idx_end = len(rows)
        try:
            supabase.table(table).upsert(rows[idx_begin:idx_end]).execute() # type: ignore
        except Exception as e:
            print(e)

def main():
    url: str = os.getenv("SUPABASE_URL", default="")
    key: str = os.getenv("SUPABASE_SERV_KEY", default="")
    options = ClientOptions(postgrest_client_timeout=600, storage_client_timeout=600)

    supabase: Client = create_client(url, key, options=options)

    with open("dict/id_dict.pkl", "rb") as f:
        id_dict: Dict[int, Circle] = pickle.load(f)

    circles: Dict[int, str] = {}

    rows_booth: List[Dict[str, Any]] = []
    for _id, circle in id_dict.items():
        cid = circle.CircleId
        if circle.CircleId > 0:
            assert cid not in circles
            circles[cid] = circle.Name

        space = normalize('NFKC', circle.Space)
        assert space == circle.Space

        space_num = space[:2]
        assert int(space_num) >= 0
        space_subsec = space[2:]
        assert space_subsec == 'a' or space_subsec == 'b'

        if circle.Is2SP:
            space_subsec = 'ab'
        locstr = f'{circle.Block}{space_num}{space_subsec}'

        row: Dict[str, Any] = {
            "event_id": DAY_EVENT[circle.Day],
            "location_top": circle.Hall,
            "location": locstr,
            "jname": circle.Name,
            "data": circle.model_dump(),
            "circle_id": circle.CircleId,
            "circle_type": CIRCLE_TYPE
        }
        rows_booth.append(row)

    rows_circle:List[ Dict[str, Any]] = []
    for cid, name in circles.items():
        rows_circle.append({
            "circleid": cid,
            "circle_type": CIRCLE_TYPE,
            "name": name
        })

    print("# of circles:", len(rows_booth))
    print("# of booths:", len(rows_circle))

    # batch_insert(supabase, rows_circle, "circle")
    batch_insert(supabase, rows_booth, "booth")

if __name__ == "__main__":
    main()

