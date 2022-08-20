# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from enum import Enum
from typing import Optional

import httpx
from pydantic import BaseModel

from . import headers

__NEWS_URL__ = (
    "https://www.minecraft.net/content/minecraft-net/_jcr_content.articles.grid"
)

http_client = httpx.Client(headers=headers)


class _ArticleLang(str, Enum):
    en_us = "en-us"


class _BackgroundColor(str, Enum):
    bg_blue = "bg-blue"
    bg_green = "bg-green"
    bg_red = "bg-red"


class _ContentType(str, Enum):
    image = "image"
    outgoing_link = "outgoing-link"
    video = "video"


class _Image(BaseModel):
    content_type: _ContentType
    imageURL: str
    alt: Optional[str] = None
    videoURL: Optional[str] = None
    videoType: Optional[str] = None
    videoProvider: Optional[str] = None
    videoId: Optional[str] = None
    linkurl: Optional[str] = None
    background_color: Optional[_BackgroundColor] = None


class _TileSize(str, Enum):
    the1x1 = "1x1"
    the1x2 = "1x2"
    the2x1 = "2x1"
    the2x2 = "2x2"
    the4x2 = "4x2"


class _Tile(BaseModel):
    sub_header: str
    image: _Image
    tile_size: _TileSize
    title: str


class _Article(BaseModel):
    default_tile: _Tile
    articleLang: _ArticleLang
    primary_category: str
    categories: list[str]
    article_url: str
    publish_date: str
    tags: list[str]
    preferred_tile: Optional[_Tile] = None


class Articles(BaseModel):
    article_grid: list[_Article]
    article_count: int


def fetch(page_size: int = 20) -> Articles:
    """
    Get the news from minecraft.net
    """

    parameters = {"pageSize": page_size}
    response = http_client.get(__NEWS_URL__, params=parameters)
    articles = Articles.parse_raw(response.content)

    return articles
