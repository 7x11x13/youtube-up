import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from dataclasses_json import config, dataclass_json


@dataclass_json
@dataclass(frozen=True)
class APIClient:
    clientName: int = 62
    clientVersion: str = "1.20231103.02.01"
    experimentsToken: str = ""
    gl: str = "US"
    hl: str = "en"
    utcOffsetMinutes: int = -300


@dataclass_json
@dataclass(frozen=True)
class APISessionInfo:
    token: str = ""


@dataclass_json
@dataclass(frozen=True)
class APIRequest:
    internalExperimentFlags: list = ()
    returnLogEntry: bool = True
    sessionInfo: APISessionInfo = APISessionInfo()


@dataclass_json
@dataclass(frozen=True)
class APIRoleType:
    channelRoleType: str = "CREATOR_CHANNEL_ROLE_TYPE_OWNER"


@dataclass_json
@dataclass(frozen=True)
class APIDelegationContext:
    externalChannelId: str
    roleType: APIRoleType = APIRoleType()


@dataclass_json
@dataclass(frozen=True)
class APIUser:
    delegationContext: APIDelegationContext


@dataclass_json
@dataclass(frozen=True)
class APIContext:
    client: APIClient
    request: APIRequest
    user: APIUser

    @classmethod
    def from_session_data(cls, channel_id: str, session_token: str):
        return cls(
            APIClient(),
            APIRequest(sessionInfo=APISessionInfo(session_token)),
            APIUser(APIDelegationContext(channel_id)),
        )


@dataclass_json
@dataclass(frozen=True)
class APIID:
    id: str


@dataclass_json
@dataclass(frozen=True)
class APIScottyResourceID:
    scottyResourceId: APIID


@dataclass_json
@dataclass(frozen=True)
class APIMetadataTitle:
    newTitle: str


@dataclass_json
@dataclass(frozen=True)
class APIMetadataDescription:
    newDescription: str
    shouldSegment: bool = True


@dataclass_json
@dataclass(frozen=True)
class APIMetadataPrivacy:
    newPrivacy: str


@dataclass_json
@dataclass(frozen=True)
class APIMetadataDraftState:
    isDraft: bool


@dataclass_json
@dataclass(frozen=True)
class APIMetadataTags:
    newTags: list[str]


class UpdateMetadataBase:
    @classmethod
    def from_metadata_args(cls, *args):
        if all(a is None for a in args):
            return None
        else:
            return cls(*args)


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataMadeForKids(UpdateMetadataBase):
    newMfk: str
    operation: str = "MDE_MADE_FOR_KIDS_UPDATE_OPERATION_SET"


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataPrivacy(UpdateMetadataBase):
    newPrivacy: str


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataCategory(UpdateMetadataBase):
    newCategoryId: int


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataCommentOptions(UpdateMetadataBase):
    newAllowComments: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    newAllowCommentsMode: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    newCanViewRatings: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    newDefaultSortOrder: Optional[str] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataDistributionOptions(UpdateMetadataBase):
    newAllowEmbedding: bool


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataLicense(UpdateMetadataBase):
    newLicenseId: str


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataPublishingOptions(UpdateMetadataBase):
    newPostToFeed: bool


@dataclass_json
@dataclass(frozen=True)
class APIDate:
    day: int
    month: int
    year: int

    @classmethod
    def from_date(cls, date: datetime.datetime):
        if date is None:
            return None
        else:
            return cls(date.day, date.month, date.year)


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataRecordedDate(UpdateMetadataBase):
    newRecordedDate: APIDate
    operation: str = "MDE_RECORDED_DATE_UPDATE_OPERATION_SET"


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataAudioLanguage(UpdateMetadataBase):
    newAudioLanguage: str


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataAutoChapter(UpdateMetadataBase):
    creatorOptOut: bool


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataAutoPlaces(UpdateMetadataBase):
    creatorOptOut: bool


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataAutoLearningConcepts(UpdateMetadataBase):
    autoConceptsCreatorOptOut: bool


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataProductPlacement(UpdateMetadataBase):
    newHasPaidProductPlacement: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    newShowPaidProductPlacementOverlay: Optional[bool] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataRacy(UpdateMetadataBase):
    newRacy: str
    operation: str = "MDE_RACY_UPDATE_OPERATION_SET"


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataRemoveDraftState(UpdateMetadataBase):
    operation: str = "MDE_DRAFT_STATE_UPDATE_OPERATION_REMOVE_DRAFT_STATE"


@dataclass_json
@dataclass(frozen=True)
class APIImage(UpdateMetadataBase):
    encryptedScottyResourceId: str
    format: str
    name: str = "CUSTOM_THUMBNAIL_IMAGE_NAME_DEFAULT"


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataThumbnail(UpdateMetadataBase):
    image: APIImage
    operation: str = "UPLOAD_CUSTOM_THUMBNAIL"


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataPlaylists(UpdateMetadataBase):
    addToPlaylistIds: list[str]
    deleteFromPlaylistIds: list[str] = ()


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


RacyDict = {
    True: "MDE_RACY_TYPE_RESTRICTED",
    False: "MDE_RACY_TYPE_NOT_RESTRICTED",
    None: None,
}
MFKDict = {True: "MDE_MADE_FOR_KIDS_TYPE_MFK", False: "MDE_MADE_FOR_KIDS_TYPE_NOT_MFK"}


@dataclass(frozen=True)
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


@dataclass_json
@dataclass(frozen=True)
class APIInitialMetadata:
    title: APIMetadataTitle
    description: APIMetadataDescription
    privacy: APIMetadataPrivacy
    draftState: APIMetadataDraftState
    tags: APIMetadataTags

    @classmethod
    def from_metadata(cls, metadata: Metadata):
        return cls(
            APIMetadataTitle(metadata.title),
            APIMetadataDescription(metadata.description),
            APIMetadataPrivacy(PrivacyEnum.PRIVATE),
            APIMetadataDraftState(True),
            APIMetadataTags(metadata.tags),
        )


@dataclass_json
@dataclass(frozen=True)
class APIRequestCreateVideo:
    channelId: str
    context: APIContext
    delegationContext: APIDelegationContext
    frontendUploadId: str
    initialMetadata: APIInitialMetadata
    presumedShort: bool
    resourceId: APIScottyResourceID

    @classmethod
    def from_session_data(
        cls,
        channel_id: str,
        session_token: str,
        front_end_upload_id: str,
        metadata: Metadata,
        presumed_short: bool,
        scotty_resource_id: str,
    ):
        return cls(
            channel_id,
            APIContext.from_session_data(channel_id, session_token),
            APIDelegationContext(channel_id),
            front_end_upload_id,
            APIInitialMetadata.from_metadata(metadata),
            presumed_short,
            APIScottyResourceID(APIID(scotty_resource_id)),
        )


@dataclass_json
@dataclass(frozen=True)
class APIRequestListPlaylistsMask:
    playlistId: bool = True
    title: bool = True


@dataclass_json
@dataclass(frozen=True)
class APIRequestListPlaylists:
    channelId: str
    context: APIContext
    delegationContext: APIDelegationContext
    mask: APIRequestListPlaylistsMask = APIRequestListPlaylistsMask()
    memberVideoIds: list[str] = ()
    pageSize: int = 500

    @classmethod
    def from_session_data(cls, channel_id: str, session_token: str):
        return cls(
            channel_id,
            APIContext.from_session_data(channel_id, session_token),
            APIDelegationContext(channel_id),
        )


@dataclass_json
@dataclass(frozen=True)
class APIPlaylistCourseMetadata:
    isCourse: bool = False


@dataclass_json
@dataclass(frozen=True)
class APIPlaylistPodcastMetadata:
    isPodcast: bool = False


@dataclass_json
@dataclass(frozen=True)
class APIRequestCreatePlaylist:
    context: APIContext
    delegationContext: APIDelegationContext
    title: str
    description: str
    privacyStatus: str
    courseMetadata: APIPlaylistCourseMetadata = APIPlaylistCourseMetadata()
    podcastMetadata: APIPlaylistPodcastMetadata = APIPlaylistPodcastMetadata()

    @classmethod
    def from_session_data(cls, channel_id: str, session_token: str, playlist: Playlist):
        return cls(
            APIContext.from_session_data(channel_id, session_token),
            APIDelegationContext(channel_id),
            playlist.title,
            playlist.description,
            playlist.privacy,
        )


@dataclass_json
@dataclass(frozen=True)
class APIRequestUpdateMetadata:
    context: APIContext
    delegationContext: APIDelegationContext
    encryptedVideoId: str
    # mandatory updates
    madeForKids: APIUpdateMetadataMadeForKids
    draftState: APIUpdateMetadataRemoveDraftState
    privacyState: APIUpdateMetadataPrivacy
    # optional updates
    autoChapter: Optional[APIUpdateMetadataAutoChapter] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    autoPlaces: Optional[APIUpdateMetadataAutoPlaces] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    learningConcepts: Optional[APIUpdateMetadataAutoLearningConcepts] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    productPlacement: Optional[APIUpdateMetadataProductPlacement] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    racy: Optional[APIUpdateMetadataRacy] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    audioLanguage: Optional[APIUpdateMetadataAudioLanguage] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    recordedDate: Optional[APIUpdateMetadataRecordedDate] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    category: Optional[APIUpdateMetadataCategory] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    commentOptions: Optional[APIUpdateMetadataCommentOptions] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    distributionOptions: Optional[APIUpdateMetadataDistributionOptions] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    license: Optional[APIUpdateMetadataLicense] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    publishingOptions: Optional[APIUpdateMetadataPublishingOptions] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    videoStill: Optional[APIUpdateMetadataThumbnail] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )
    addToPlaylist: Optional[APIUpdateMetadataPlaylists] = field(
        default=None, metadata=config(exclude=lambda x: x is None)
    )

    @classmethod
    def from_session_data(
        cls,
        channel_id: str,
        session_token: str,
        encrypted_video_id: str,
        metadata: Metadata,
        thumbnail_scotty_id: Optional[str] = None,
        thumbnail_format: Optional[str] = None,
    ):
        return cls(
            APIContext.from_session_data(channel_id, session_token),
            APIDelegationContext(channel_id),
            encrypted_video_id,
            APIUpdateMetadataMadeForKids(MFKDict[metadata.made_for_kids]),
            APIUpdateMetadataRemoveDraftState(),
            APIUpdateMetadataPrivacy(metadata.privacy),
            APIUpdateMetadataAutoChapter.from_metadata_args(metadata.auto_chapter),
            APIUpdateMetadataAutoPlaces.from_metadata_args(metadata.auto_places),
            APIUpdateMetadataAutoLearningConcepts.from_metadata_args(
                metadata.auto_concepts
            ),
            APIUpdateMetadataProductPlacement.from_metadata_args(
                metadata.has_product_placement, metadata.show_product_placement_overlay
            ),
            APIUpdateMetadataRacy.from_metadata_args(
                RacyDict[metadata.restriced_to_over_18]
            ),
            APIUpdateMetadataAudioLanguage.from_metadata_args(metadata.audio_language),
            APIUpdateMetadataRecordedDate.from_metadata_args(
                APIDate.from_date(metadata.recorded_date)
            ),
            APIUpdateMetadataCategory.from_metadata_args(metadata.category),
            APIUpdateMetadataCommentOptions.from_metadata_args(
                metadata.allow_comments,
                metadata.allow_comments_mode,
                metadata.can_view_ratings,
                metadata.comments_sort_order,
            ),
            APIUpdateMetadataDistributionOptions.from_metadata_args(
                metadata.allow_embedding
            ),
            APIUpdateMetadataLicense.from_metadata_args(metadata.license),
            APIUpdateMetadataPublishingOptions.from_metadata_args(
                metadata.publish_to_feed
            ),
            APIUpdateMetadataThumbnail.from_metadata_args(
                APIImage.from_metadata_args(thumbnail_scotty_id, thumbnail_format)
            ),
            APIUpdateMetadataPlaylists.from_metadata_args(metadata.playlist_ids),
        )
