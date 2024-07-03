import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import marshmallow.fields as mm_field
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
    NOT_APPLICABLE = "zxx"
    ABKHAZIAN = "ab"
    AFAR = "aa"
    AFRIKAANS = "af"
    AKAN = "ak"
    AKKADIAN = "akk"
    ALBANIAN = "sq"
    AMERICAN_SIGN_LANGUAGE = "ase"
    AMHARIC = "am"
    ARABIC = "ar"
    ARAMAIC = "arc"
    ARMENIAN = "hy"
    ASSAMESE = "as"
    AYMARA = "ay"
    AZERBAIJANI = "az"
    BAMBARA = "bm"
    BANGLA = "bn"
    BANGLA_INDIA = "bn-IN"
    BASHKIR = "ba"
    BASQUE = "eu"
    BELARUSIAN = "be"
    BHOJPURI = "bho"
    BISLAMA = "bi"
    BODO = "brx"
    BOSNIAN = "bs"
    BRETON = "br"
    BULGARIAN = "bg"
    BURMESE = "my"
    CANTONESE = "yue"
    CANTONESE_HONG_KONG = "yue-HK"
    CATALAN = "ca"
    CHEROKEE = "chr"
    CHINESE = "zh"
    CHINESE_CHINA = "zh-CN"
    CHINESE_HONG_KONG = "zh-HK"
    CHINESE_SIMPLIFIED = "zh-Hans"
    CHINESE_SINGAPORE = "zh-SG"
    CHINESE_TAIWAN = "zh-TW"
    CHINESE_TRADITIONAL = "zh-Hant"
    CHOCTAW = "cho"
    COPTIC = "cop"
    CORSICAN = "co"
    CREE = "cr"
    CROATIAN = "hr"
    CZECH = "cs"
    DANISH = "da"
    DOGRI = "doi"
    DUTCH = "nl"
    DUTCH_BELGIUM = "nl-BE"
    DUTCH_NETHERLANDS = "nl-NL"
    DZONGKHA = "dz"
    ENGLISH = "en"
    ENGLISH_AUSTRALIA = "en-AU"
    ENGLISH_CANADA = "en-CA"
    ENGLISH_INDIA = "en-IN"
    ENGLISH_IRELAND = "en-IE"
    ENGLISH_UNITED_KINGDOM = "en-GB"
    ENGLISH_UNITED_STATES = "en-US"
    ESPERANTO = "eo"
    ESTONIAN = "et"
    EWE = "ee"
    FAROESE = "fo"
    FIJIAN = "fj"
    FILIPINO = "fil"
    FINNISH = "fi"
    FRENCH = "fr"
    FRENCH_BELGIUM = "fr-BE"
    FRENCH_CANADA = "fr-CA"
    FRENCH_FRANCE = "fr-FR"
    FRENCH_SWITZERLAND = "fr-CH"
    FULA = "ff"
    GALICIAN = "gl"
    GANDA = "lg"
    GEORGIAN = "ka"
    GERMAN = "de"
    GERMAN_AUSTRIA = "de-AT"
    GERMAN_GERMANY = "de-DE"
    GERMAN_SWITZERLAND = "de-CH"
    GREEK = "el"
    GUARANI = "gn"
    GUJARATI = "gu"
    GUSII = "guz"
    HAITIAN_CREOLE = "ht"
    HAKKA_CHINESE = "hak"
    HAKKA_CHINESE_TAIWAN = "hak-TW"
    HARYANVI = "bgc"
    HAUSA = "ha"
    HAWAIIAN = "haw"
    HEBREW = "he"
    HINDI = "hi"
    HINDI_LATIN = "hi-Latn"
    HIRI_MOTU = "ho"
    HUNGARIAN = "hu"
    ICELANDIC = "is"
    IGBO = "ig"
    INDONESIAN = "id"
    INTERLINGUA = "ia"
    INTERLINGUE = "ie"
    INUKTITUT = "iu"
    INUPIAQ = "ik"
    IRISH = "ga"
    ITALIAN = "it"
    JAPANESE = "ja"
    JAVANESE = "jv"
    KALAALLISUT = "kl"
    KALENJIN = "kln"
    KAMBA = "kam"
    KANNADA = "kn"
    KASHMIRI = "ks"
    KAZAKH = "kk"
    KHMER = "km"
    KIKUYU = "ki"
    KINYARWANDA = "rw"
    KLINGON = "tlh"
    KONKANI = "kok"
    KOREAN = "ko"
    KURDISH = "ku"
    KYRGYZ = "ky"
    LADINO = "lad"
    LAO = "lo"
    LATIN = "la"
    LATVIAN = "lv"
    LINGALA = "ln"
    LITHUANIAN = "lt"
    LUBA_KATANGA = "lu"
    LUO = "luo"
    LUXEMBOURGISH = "lb"
    LUYIA = "luy"
    MACEDONIAN = "mk"
    MAITHILI = "mai"
    MALAGASY = "mg"
    MALAY = "ms"
    MALAY_SINGAPORE = "ms-SG"
    MALAYALAM = "ml"
    MALTESE = "mt"
    MANIPURI = "mni"
    MAORI = "mi"
    MARATHI = "mr"
    MASAI = "mas"
    MERU = "mer"
    MIN_NAN_CHINESE = "nan"
    MIN_NAN_CHINESE_TAIWAN = "nan-TW"
    MIXE = "mco"
    MIZO = "lus"
    MONGOLIAN = "mn"
    MONGOLIAN_MONGOLIAN = "mn-M"
    NAURU = "na"
    NAVAJO = "nv"
    NEPALI = "ne"
    NIGERIAN_PIDGIN = "pcm"
    NORTH_NDEBELE = "nd"
    NORTHERN_SOTHO = "nso"
    NORWEGIAN = "no"
    OCCITAN = "oc"
    ODIA = "or"
    OROMO = "om"
    PAPIAMENTO = "pap"
    PASHTO = "ps"
    PERSIAN = "fa"
    PERSIAN_AFGHANISTAN = "fa-AF"
    PERSIAN_IRAN = "fa-IR"
    POLISH = "pl"
    PORTUGUESE = "pt"
    PORTUGUESE_BRAZIL = "pt-BR"
    PORTUGUESE_PORTUGAL = "pt-PT"
    PUNJABI = "pa"
    QUECHUA = "qu"
    ROMANIAN = "ro"
    ROMANIAN_MOLDOVA = "ro-MD"
    ROMANSH = "rm"
    RUNDI = "rn"
    RUSSIAN = "ru"
    RUSSIAN_LATIN = "ru-Latn"
    SAMOAN = "sm"
    SANGO = "sg"
    SANSKRIT = "sa"
    SANTALI = "sat"
    SARDINIAN = "sc"
    SCOTTISH_GAELIC = "gd"
    SERBIAN = "sr"
    SERBIAN_CYRILLIC = "hr-Cyrl"
    SERBIAN_LATIN = "sr-Latn"
    SERBO_CROATIAN = "sh"
    SHERDUKPEN = "sdp"
    SHONA = "sn"
    SICILIAN = "scn"
    SINDHI = "sd"
    SINHALA = "si"
    SLOVAK = "sk"
    SLOVENIAN = "sl"
    SOMALI = "so"
    SOUTH_NDEBELE = "nr"
    SOUTHERN_SOTHO = "st"
    SPANISH = "es"
    SPANISH_LATIN_AMERICA = "es-419"
    SPANISH_MEXICO = "es-MX"
    SPANISH_SPAIN = "es-ES"
    SPANISH_UNITED_STATES = "es-US"
    SUNDANESE = "su"
    SWAHILI = "sw"
    SWATI = "ss"
    SWEDISH = "sv"
    TAGALOG = "tl"
    TAJIK = "tg"
    TAMIL = "ta"
    TATAR = "tt"
    TELUGU = "te"
    THAI = "th"
    TIBETAN = "bo"
    TIGRINYA = "ti"
    TOK_PISIN = "tpi"
    TOKI_PONA = "tok"
    TONGAN = "to"
    TSONGA = "ts"
    TSWANA = "tn"
    TURKISH = "tr"
    TURKMEN = "tk"
    TWI = "tw"
    UKRAINIAN = "uk"
    URDU = "ur"
    UYGHUR = "ug"
    UZBEK = "uz"
    VENDA = "ve"
    VIETNAMESE = "vi"
    VOLAPÜK = "vo"
    VÕRO = "vro"
    WELSH = "cy"
    WESTERN_FRISIAN = "fy"
    WOLAYTTA = "wal"
    WOLOF = "wo"
    XHOSA = "xh"
    YIDDISH = "yi"
    YORUBA = "yo"
    ZULU = "zu"


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
        try:
            value = getattr(cls, value)
            return Enum.__new__(cls, value)
        except (AttributeError, TypeError):
            raise ValueError(f"{cls.__name__} has no key or value '{value}'")


for enum_class in enum_classes:
    setattr(enum_class, "__new__", enum_allow_key__new__)


@dataclass_json
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
class CaptionsFile:
    """Subtitles file"""

    path: str
    """Path to .srt file"""

    language: Optional[LanguageEnum] = None
    """Language of captions. If None, language will default to audio language"""


@dataclass_json
@dataclass
class Metadata:
    """Metadata of video to upload"""

    title: str
    """Title. Max length 100. Cannot contain < or > characters"""

    description: str = ""
    """Description. Max length 5000. Cannot contain < or > characters"""

    privacy: PrivacyEnum = PrivacyEnum.PRIVATE
    """Privacy. Possible values: PUBLIC, UNLISTED, PRIVATE"""

    made_for_kids: bool = False
    """Made for kids. If true comments will be disabled"""

    tags: tuple[str, ...] = ()
    """List of tags"""

    # optional metadata for update_metadata
    scheduled_upload: Optional[datetime.datetime] = field(
        default=None,
        metadata=config(
            decoder=lambda x: (
                datetime.datetime.fromisoformat(x) if x is not None else None
            ),
            encoder=lambda x: datetime.datetime.isoformat(x) if x is not None else None,
            mm_field=mm_field.DateTime("iso", allow_none=True),
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
            decoder=lambda x: datetime.date.fromisoformat(x) if x is not None else None,
            encoder=lambda x: datetime.date.isoformat(x) if x is not None else None,
            mm_field=mm_field.Date("iso", allow_none=True),
        ),
    )
    """Day, month, and year that video was recorded"""

    restricted_to_over_18: Optional[bool] = None
    """Whether video is age restricted"""

    audio_language: Optional[LanguageEnum] = None
    """Language of audio"""

    captions_files: Optional[list[CaptionsFile]] = None
    """Path to captions files (.srt)"""

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

    def validate(self):
        """Raises error if metadata is invalid"""
        if (
            self.premiere_countdown_duration is not None
            or self.premiere_theme is not None
        ):
            if None in (
                self.premiere_countdown_duration,
                self.premiere_theme,
                self.scheduled_upload,
            ):
                raise ValueError(
                    "If trying to upload a premiere, premiere_countdown_duration, "
                    "premiere_theme, and scheduled_upload must be set"
                )

        if self.captions_files is not None:
            for caption_file in self.captions_files:
                if caption_file.language is None and self.audio_language is None:
                    raise ValueError(
                        "Must either specify captions file language or audio_language"
                    )

        if self.restricted_to_over_18 and self.made_for_kids:
            raise ValueError(
                "Video cannot be made for kids and also restricted to over 18"
            )

        if len(self.title) > 100:
            raise ValueError("Title must be at most 100 characters long")

        if len(self.description) > 5000:
            raise ValueError("Description must be at most 5000 characters long")

        to_check = [self.title, self.description] + list(self.tags)
        if self.playlists:
            for p in self.playlists:
                to_check += [p.title, p.description]

        if any(c in s for c in "<>" for s in to_check):
            raise ValueError(
                "Titles, descriptions, and tags cannot contain angled brackets"
            )

        errors = self.schema().validate(self.to_dict())
        if errors:
            raise ValueError(f"{errors}")


__all__ = [
    "Metadata",
    "Playlist",
    "CaptionsFile",
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
