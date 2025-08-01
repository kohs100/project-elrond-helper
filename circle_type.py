from typing import Literal, List, Optional
import json
from pydantic import BaseModel, Field, AliasChoices

MAX_DICT = {1: 168, 2: 159}

class Image(BaseModel):
    Id: str
    OfficialCircleId: int = Field(validation_alias=AliasChoices('OfficialCircleId', '公開サークルId'))
    ThumbnailUrl: str = Field(validation_alias=AliasChoices('ThumbnailUrl', 'サムネイル画像'))
    BigimageUrl: str = Field(validation_alias=AliasChoices('BigimageUrl', '既定表示画像'))
    R18: bool
    imageCode: int
    UpdatedAt: int

class Circle(BaseModel):
    Id: int
    CircleId: int
    Name: str
    Author: str
    IsReject: bool
    Hall: Literal['東','南', '西']
    Day: Literal['土', '日']
    Block: str
    Space: str
    HaichiStr: str
    Is2SP: bool
    IsMain: bool
    Loc: int
    Genre: str
    CircleCutUrls: List[str]
    WebCircleCutUrls: List[str]
    MovieCutUrls: List[Optional[str]]
    Image1: Optional[Image]
    Image2: Optional[Image]
    BookImage: Optional[Image]
    IsNew: bool
    IsOnlineBooksRegistered: bool
    IsPixivRegistered: bool
    PixivUrl: str
    IsTwitterRegistered: bool
    TwitterUrl: str
    IsNiconicoRegistered: bool
    NiconicoUrl: str
    IsClipstudioRegistered: bool
    ClipstudioUrl: str
    HasKokutiImage: bool
    HasHanpuImage: bool
    WebSite: str
    CanCashless: bool
    CashlessTypes: str
    Description: str

if __name__ == "__main__":
    with open("circle.schema.json", "wt") as f:
        json.dump(Circle.model_json_schema(), f, ensure_ascii=False, indent=2)