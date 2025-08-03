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
BATCH_SIZE=32

def main():
    url: str = os.getenv("SUPABASE_URL", default="")
    key: str = os.getenv("SUPABASE_SERV_KEY", default="")
    options = ClientOptions(postgrest_client_timeout=600, storage_client_timeout=600)

    supabase: Client = create_client(url, key, options=options)

    with open("dict/id_dict.pkl", "rb") as f:
        id_dict: Dict[int, Circle] = pickle.load(f)

    rows: List[Dict[str, Any]] = []
    for _id, circle in id_dict.items():
        row: Dict[str, Any] = {
            "event_id": DAY_EVENT[circle.Day],
            "location_top": circle.Hall,
            "location": normalize('NFKC', circle.Block + circle.Space),
            "jname": circle.Name,
            "data": circle.model_dump(),
        }
        rows.append(row)

    print(len(rows))

    num_batch = len(rows) // BATCH_SIZE + 1

    for batch_idx in trange(num_batch):
        idx_begin = batch_idx * BATCH_SIZE
        idx_end = idx_begin + BATCH_SIZE
        if len(rows) < idx_end:
            idx_end = len(rows)
        try:
            supabase.table("booth").insert(rows[idx_begin:idx_end]).execute() # type: ignore
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()

