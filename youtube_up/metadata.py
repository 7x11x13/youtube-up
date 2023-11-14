import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PrivacyEnum(str, Enum):
    PRIVATE = "PRIVATE"
    UNLISTED = "UNLISTED"
    PUBLIC = "PUBLIC"


class CategoryEnum(int, Enum):
    FILM_ANIMATION = 1
    AUTOS_VEHICLES = 2
    MUSIC = 10
    PETS_ANIMALS = 15
    SPORTS = 17
    TRAVEL_EVENTS = 19
    GAMING = 20
    PEOPLE_BLOGS = 22
    COMEDY = 23
    ENTERTAINMENT = 24
    NEWS_POLITICS = 25
    HOWTO_STYLE = 26
    EDUCATION = 27
    SCIENCE_TECH = 28
    NONPROFITS_ACTIVISM = 29


class LanguageEnum(str, Enum):
    ENGLISH = "en"
    # todo


class LicenseEnum(str, Enum):
    STANDARD = "standard"
    CREATIVE_COMMONS = "creative_commons"


class AllowCommentsEnum(str, Enum):
    ALL_COMMENTS = "ALL_COMMENTS"
    HOLD_INAPPROPRIATE = "AUTOMATED_COMMENTS"
    HOLD_INAPPROPRIATE_STRICT = "AUTO_MODERATED_COMMENTS_HOLD_MORE"
    HOLD_ALL = "APPROVED_COMMENTS"


class CommentsSortOrderEnum(str, Enum):
    LATEST = "MDE_COMMENT_SORT_ORDER_LATEST"
    TOP = "MDE_COMMENT_SORT_ORDER_TOP"


class ThumbnailFormatEnum(str, Enum):
    PNG = "CUSTOM_THUMBNAIL_IMAGE_FORMAT_PNG"
    JPG = "CUSTOM_THUMBNAIL_IMAGE_FORMAT_JPEG"


class PremiereDurationEnum(str, Enum):
    ONE_MIN = "60"
    TWO_MIN = "120"
    THREE_MIN = "180"
    FOUR_MIN = "240"
    FIVE_MIN = "300"


class PremiereThemeEnum(str, Enum):
    CLASSIC = "VIDEO_PREMIERE_INTRO_THEME_DEFAULT"
    ALTERNATIVE = "VIDEO_PREMIERE_INTRO_THEME_ALTERNATIVE"
    AMBIENT = "VIDEO_PREMIERE_INTRO_THEME_AMBIENT"
    BRIGHT = "VIDEO_PREMIERE_INTRO_THEME_BRIGHT"
    CALM = "VIDEO_PREMIERE_INTRO_THEME_CALM"
    CINEMATIC = "VIDEO_PREMIERE_INTRO_THEME_CINEMATIC"
    CONTEMPORARY = "VIDEO_PREMIERE_INTRO_THEME_CONTEMPORARY"
    DRAMATIC = "VIDEO_PREMIERE_INTRO_THEME_DRAMATIC"
    FUNKY = "VIDEO_PREMIERE_INTRO_THEME_FUNKY"
    GENTLE = "VIDEO_PREMIERE_INTRO_THEME_GENTLE"
    HAPPY = "VIDEO_PREMIERE_INTRO_THEME_HAPPY"
    INSPIRATIONAL = "VIDEO_PREMIERE_INTRO_THEME_INSPIRATIONAL"
    KIDS = "VIDEO_PREMIERE_INTRO_THEME_KIDS"
    SCI_FI = "VIDEO_PREMIERE_INTRO_THEME_SCI_FI"
    SPORTS = "VIDEO_PREMIERE_INTRO_THEME_SPORTS"


@dataclass
class Playlist:
    title: str
    description: str = ""
    privacy: PrivacyEnum = PrivacyEnum.PUBLIC
    create_if_title_exists: bool = False
    create_if_title_doesnt_exist: bool = True


@dataclass
class Metadata:
    title: str
    description: str
    privacy: PrivacyEnum
    made_for_kids: bool = False
    tags: list[str] = ()
    # optional metadata for update_metadata
    scheduled_upload: Optional[datetime.datetime] = None
    premiere_countdown_duration: Optional[PremiereDurationEnum] = None
    premiere_theme: Optional[PremiereThemeEnum] = None
    playlist_ids: Optional[list[str]] = None
    playlists: Optional[list[Playlist]] = None
    thumbnail: Optional[str] = None
    publish_to_feed: Optional[bool] = None
    category: Optional[CategoryEnum] = None
    auto_chapter: Optional[bool] = None
    auto_places: Optional[bool] = None
    auto_concepts: Optional[bool] = None
    has_product_placement: Optional[bool] = None
    show_product_placement_overlay: Optional[bool] = None
    recorded_date: Optional[datetime.date] = None
    restriced_to_over_18: Optional[bool] = None
    audio_language: Optional[LanguageEnum] = None
    license: Optional[LicenseEnum] = None
    allow_comments: Optional[bool] = None
    allow_comments_mode: Optional[AllowCommentsEnum] = None
    can_view_ratings: Optional[bool] = None
    comments_sort_order: Optional[CommentsSortOrderEnum] = None
    allow_embedding: Optional[bool] = None


__all__ = [
    "Metadata",
    "Playlist",
    "PremiereThemeEnum",
    "PremiereDurationEnum",
    "ThumbnailFormatEnum",
    "CommentsSortOrderEnum",
    "AllowCommentsEnum",
    "LicenseEnum",
    "LanguageEnum",
    "CategoryEnum",
    "PrivacyEnum",
]
