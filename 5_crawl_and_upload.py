import json

import os
import boto3
from botocore.exceptions import ClientError
import requests
import tqdm

from mypy_boto3_s3 import S3Client
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from typing import List
from PIL import Image

req_session = requests.Session()
with open("cookies.json", "rt") as f:
    cookies_list = json.load(f)

for cookie in cookies_list:
    req_session.cookies.set(  # type: ignore
        cookie["name"],
        cookie["value"],
        domain=cookie["domain"],
        path=cookie["path"],
    )

COOKIE_JAR = req_session.cookies

load_dotenv()

CF_R2_ENDPOINT = os.getenv("CF_R2_ENDPOINT", default="")
CF_R2_BUCKET = os.getenv("CF_R2_BUCKET", default="")
CF_R2_ACCESS_KEY = os.getenv("CF_R2_ACCESS_KEY", default="")
CF_R2_SECRET_KEY = os.getenv("CF_R2_SECRET_KEY", default="")

session = boto3.session.Session()
s3: S3Client = session.client(  # type: ignore
    "s3",
    endpoint_url=CF_R2_ENDPOINT,
    aws_access_key_id=CF_R2_ACCESS_KEY,
    aws_secret_access_key=CF_R2_SECRET_KEY,
)

SAVE_AT = "downloaded"

def is_valid_webp_full(file_path: str) -> bool:
    try:
        with Image.open(file_path) as img:
            return img.format == "WEBP"
    except Exception:
        return False

def download_image(url: str):
    file_path = f"{SAVE_AT}/{url}"
    save_at = "/".join(file_path.split("/")[:-1])
    if os.path.isfile(f"{SAVE_AT}/{url}"):
        if is_valid_webp_full(file_path):
            return
    os.makedirs(save_at, exist_ok=True)

    # Download image
    url_from = f"https://webcatalog.circle.ms/{url}"
    resp = requests.get(url_from, stream=True, cookies=COOKIE_JAR)
    resp.raise_for_status()

    ctype = resp.headers["content-type"]
    if ctype != "application/octet-stream":
        raise ValueError(f"Invalid content-type: {ctype}")

    with open(f"{SAVE_AT}/{url}", "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

def upload_image(url: str):
    file_path = f"{SAVE_AT}/{url}"

    try:
        resp = s3.head_object(Bucket=CF_R2_BUCKET, Key=url)
    except ClientError as e:
        if e.response["Error"]["Code"] == "404": # type: ignore
            # No image -> upload
            s3.upload_file(file_path, CF_R2_BUCKET, url)
            return
        else:
            raise e
    if resp.get("ContentType") != "image/webp":
        # Object exists but not image
        s3.upload_file(file_path, CF_R2_BUCKET, url)
        return

def process_image(url: str):
    assert url.startswith("/Spa/")
    url = url[1:]
    download_image(url)
    upload_image(url)

def main():
    with open("dict/image_list.json", "rt") as f:
        urls_list: List[str] = json.load(f)

    with ThreadPoolExecutor(max_workers=10) as executor:
        list(tqdm.tqdm(executor.map(process_image, urls_list), total=len(urls_list)))


if __name__ == "__main__":
    main()
