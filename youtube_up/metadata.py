import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from dataclasses_json import config, dataclass_json


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


enum_classes = [
    PrivacyEnum,
    CategoryEnum,
    LanguageEnum,
    LicenseEnum,
    AllowCommentsEnum,
    CommentsSortOrderEnum,
    ThumbnailFormatEnum,
    PremiereDurationEnum,
    PremiereThemeEnum,
]


def enum_allow_key__new__(cls, value):
    try:
        return Enum.__new__(cls, value)
    except ValueError:
        # maybe key was specified instead of value?
        value = getattr(cls, value)
        return Enum.__new__(cls, value)


for enum_class in enum_classes:
    setattr(enum_class, "__new__", enum_allow_key__new__)


@dataclass
class Playlist:
    """Metadata of playlist to create and/or add video to"""

    title: str
    """Title. Max length 150"""

    description: str = ""
    """Description. Max length 5000"""

    privacy: PrivacyEnum = PrivacyEnum.PUBLIC
    """Privacy. Possible values: PUBLIC, UNLISTED, PRIVATE"""

    create_if_title_exists: bool = False
    """Whether to create playlist if a playlist with the same
    title already exists on the channel"""

    create_if_title_doesnt_exist: bool = True
    """Whether to create playlist if there is no playlist with the same title"""


@dataclass_json
@dataclass
class Metadata:
    """Metadata of video to upload"""

    title: str
    """Title. Max length 100"""

    description: str = ""
    """Description. Max length 5000"""

    privacy: PrivacyEnum = PrivacyEnum.PRIVATE
    """Privacy. Possible values: PUBLIC, UNLISTED, PRIVATE"""

    made_for_kids: bool = False
    """Made for kids. If true comments will be disabled"""

    tags: list[str] = ()
    """List of tags"""

    # optional metadata for update_metadata
    scheduled_upload: Optional[datetime.datetime] = field(
        default=None,
        metadata=config(
            decoder=datetime.datetime.fromisoformat,
            encoder=datetime.datetime.isoformat,
        ),
    )
    """
    Date to make upload public. If set, video will be set to private until the date, unless video
    is a premiere in which case it will be set to public. Video will not be a premiere unless both
    premiere_countdown_duration and premiere_theme are set
    """

    premiere_countdown_duration: Optional[PremiereDurationEnum] = None
    """Duration of premiere countdown in seconds. Possible values: 60, 120, 180, 240, 300"""

    premiere_theme: Optional[PremiereThemeEnum] = None
    """
    Theme of premiere countdown. Possible values: CLASSIC, ALTERNATIVE, AMBIENT, BRIGHT, CALM,
    CINEMATIC, CONTEMPORARY, DRAMATIC, FUNKY, GENTLE, HAPPY, INSPIRATIONAL, KIDS, SCI_FI, SPORTS
    """

    playlist_ids: Optional[list[str]] = None
    """List of existing playlist IDs to add video to"""

    playlists: Optional[list[Playlist]] = None
    """List of playlists to create and/or add video to"""

    thumbnail: Optional[str] = None
    """Path to thumbnail file to upload"""

    publish_to_feed: Optional[bool] = None
    """Whether to notify subscribers"""

    category: Optional[CategoryEnum] = None
    """Category. Category-specific metadata is not supported yet. Possible values: FILM_ANIMATION,
    AUTOS_VEHICLES, MUSIC, PETS_ANIMALS, SPORTS, TRAVEL_EVENTS, GAMING, PEOPLE_BLOGS, COMEDY,
    ENTERTAINMENT, NEWS_POLITICS, HOWTO_STYLE, EDUCATION, SCIENCE_TECH, NONPROFITS_ACTIVISM"""

    auto_chapter: Optional[bool] = None
    """Whether to use automatic video chapters"""

    auto_places: Optional[bool] = None
    """Whether to use automatic places"""

    auto_concepts: Optional[bool] = None
    """Whether to use automatic concepts"""

    has_product_placement: Optional[bool] = None
    """Whether video has product placement"""

    show_product_placement_overlay: Optional[bool] = None
    """Whether to show product placement overlay"""

    recorded_date: Optional[datetime.date] = field(
        default=None,
        metadata=config(
            decoder=datetime.date.fromisoformat,
            encoder=datetime.date.isoformat,
        ),
    )
    """Day, month, and year that video was recorded"""

    restricted_to_over_18: Optional[bool] = None
    """Whether video is age restricted"""

    audio_language: Optional[LanguageEnum] = None
    """Language of audio. If uploading captions this must be set"""

    license: Optional[LicenseEnum] = None
    """License. Possible values: STANDARD, CREATIVE_COMMONS"""

    allow_comments: Optional[bool] = None
    """Whether to allow comments"""

    allow_comments_mode: Optional[AllowCommentsEnum] = None
    """Comment filtering mode. Possible values: ALL_COMMENTS, HOLD_INAPPROPRIATE,
    HOLD_INAPPROPRIATE_STRICT, HOLD_ALL"""

    can_view_ratings: Optional[bool] = None
    """Whether video likes/dislikes can be seen"""

    comments_sort_order: Optional[CommentsSortOrderEnum] = None
    """Default comment sort order. Possible values: LATEST, TOP"""

    allow_embedding: Optional[bool] = None
    """Whether to allow embedding on 3rd party sites"""


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
