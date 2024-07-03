import datetime
from dataclasses import dataclass, field
from typing import Any, Optional

from dataclasses_json import config, dataclass_json

from youtube_up.metadata import Metadata, Playlist, PrivacyEnum


def _x_is_not_none(x: Optional[Any]):
    return x is not None


@dataclass_json
@dataclass(frozen=True)
class APIClient:
    clientName: int = 62
    clientVersion: str = "1.20231215.01.00"
    experimentsToken: str = ""
    gl: str = "US"
    hl: str = "en"
    utcOffsetMinutes: int = -300
    userInterfaceTheme: str = "USER_INTERFACE_THEME_DARK"
    screenWidthPoints: int = 1920
    screenHeightPoints: int = 529
    screenPixelDensity: int = 1
    screenDensityFloat: int = 1


@dataclass_json
@dataclass(frozen=True)
class APISessionInfo:
    token: str = ""


@dataclass_json
@dataclass(frozen=True)
class APIRequest:
    internalExperimentFlags: tuple[str, ...] = ()
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
    onBehalfOfUser: Optional[str] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )


@dataclass_json
@dataclass(frozen=True)
class APIContext:
    client: APIClient
    request: APIRequest
    user: APIUser

    @classmethod
    def from_session_data(
        cls, channel_id: str, session_token: str, delegated_session_id: Optional[str]
    ):
        return cls(
            APIClient(),
            APIRequest(sessionInfo=APISessionInfo(session_token)),
            APIUser(
                APIDelegationContext(channel_id), onBehalfOfUser=delegated_session_id
            ),
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
    newTags: tuple[str, ...]


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
        default=None,
        metadata=config(exclude=_x_is_not_none),
    )
    newAllowCommentsMode: Optional[str] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    newCanViewRatings: Optional[bool] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    newDefaultSortOrder: Optional[str] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
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
    def from_date(cls, date: Optional[datetime.date]):
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
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    newShowPaidProductPlacementOverlay: Optional[bool] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
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
    addToPlaylistIds: tuple[str, ...]
    deleteFromPlaylistIds: tuple[str, ...] = ()


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataSchedule(UpdateMetadataBase):
    timeSec: str
    privacy: str = "PUBLIC"

    @classmethod
    def from_date(cls, date: Optional[datetime.datetime]):
        if date is None:
            return None
        else:
            return cls(str(round(date.timestamp())))


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataScheduledPublishing(UpdateMetadataBase):
    set: APIUpdateMetadataSchedule


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataPremiere(UpdateMetadataBase):
    scheduledStartTimeSec: str
    operation: str = "MDE_PREMIERE_UPDATE_OPERATION_SCHEDULE"

    @classmethod
    def from_date(cls, date: Optional[datetime.datetime]):
        if date is None:
            return None
        else:
            return cls(str(round(date.timestamp())))


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataCountdown(UpdateMetadataBase):
    seconds: str


@dataclass_json
@dataclass(frozen=True)
class APIUpdateMetadataPremiereIntro(UpdateMetadataBase):
    countdownDuration: APIUpdateMetadataCountdown
    theme: str
    operation: str = "MDE_PREMIERE_INTRO_UPDATE_OPERATION_SET"


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
        delegated_session_id: Optional[str],
        front_end_upload_id: str,
        metadata: Metadata,
        scotty_resource_id: str,
    ):
        return cls(
            channel_id,
            APIContext.from_session_data(
                channel_id, session_token, delegated_session_id
            ),
            APIDelegationContext(channel_id),
            front_end_upload_id,
            APIInitialMetadata.from_metadata(metadata),
            False,  # apparently does nothing; will be a short if video meets short requirements regardless
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
    memberVideoIds: tuple[str, ...] = ()
    pageSize: int = 500

    @classmethod
    def from_session_data(
        cls, channel_id: str, session_token: str, delegated_session_id: Optional[str]
    ):
        return cls(
            channel_id,
            APIContext.from_session_data(
                channel_id, session_token, delegated_session_id
            ),
            APIDelegationContext(channel_id),
        )


@dataclass_json
@dataclass(frozen=True)
class APICaptionsFile:
    dataUri: str
    fileName: str


@dataclass_json
@dataclass(frozen=True)
class APICaptionsTrackData:
    lang: str
    kind: str = ""
    name: str = ""


@dataclass_json
@dataclass(frozen=True)
class APIOperationUpdateCaptions:
    captionsFile: APICaptionsFile
    ttsTrackId: APICaptionsTrackData
    contentUpdateTime: str
    isContentEdited: bool = False
    userIntent: str = "USER_INTENT_EDIT_LATEST_DRAFT"
    vote: str = "VOTE_PUBLISH"


@dataclass_json
@dataclass(frozen=True)
class APIRequestUpdateCaptions:
    channelId: str
    context: APIContext
    operations: tuple[APIOperationUpdateCaptions, ...]
    videoId: str

    @classmethod
    def from_session_data(
        cls,
        channel_id: str,
        session_token: str,
        delegated_session_id: Optional[str],
        video_id: str,
        caption_file: str,
        caption_file_base64: str,
        caption_language: str,
        nanosecond_timestamp: str,
    ):
        return cls(
            channel_id,
            APIContext.from_session_data(
                channel_id, session_token, delegated_session_id
            ),
            (
                APIOperationUpdateCaptions(
                    APICaptionsFile(caption_file_base64, caption_file),
                    APICaptionsTrackData(caption_language),
                    nanosecond_timestamp,
                ),
            ),
            video_id,
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
    def from_session_data(
        cls,
        channel_id: str,
        session_token: str,
        delegated_session_id: Optional[str],
        playlist: Playlist,
    ):
        return cls(
            APIContext.from_session_data(
                channel_id, session_token, delegated_session_id
            ),
            APIDelegationContext(channel_id),
            playlist.title,
            playlist.description,
            playlist.privacy,
        )


RacyDict = {
    True: "MDE_RACY_TYPE_RESTRICTED",
    False: "MDE_RACY_TYPE_NOT_RESTRICTED",
    None: None,
}
MFKDict = {True: "MDE_MADE_FOR_KIDS_TYPE_MFK", False: "MDE_MADE_FOR_KIDS_TYPE_NOT_MFK"}


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
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    autoPlaces: Optional[APIUpdateMetadataAutoPlaces] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    learningConcepts: Optional[APIUpdateMetadataAutoLearningConcepts] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    productPlacement: Optional[APIUpdateMetadataProductPlacement] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    racy: Optional[APIUpdateMetadataRacy] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    audioLanguage: Optional[APIUpdateMetadataAudioLanguage] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    recordedDate: Optional[APIUpdateMetadataRecordedDate] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    category: Optional[APIUpdateMetadataCategory] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    commentOptions: Optional[APIUpdateMetadataCommentOptions] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    distributionOptions: Optional[APIUpdateMetadataDistributionOptions] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    license: Optional[APIUpdateMetadataLicense] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    publishingOptions: Optional[APIUpdateMetadataPublishingOptions] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    videoStill: Optional[APIUpdateMetadataThumbnail] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    addToPlaylist: Optional[APIUpdateMetadataPlaylists] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    scheduledPublishing: Optional[APIUpdateMetadataScheduledPublishing] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    premiere: Optional[APIUpdateMetadataPremiere] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )
    premiereIntro: Optional[APIUpdateMetadataPremiereIntro] = field(
        default=None, metadata=config(exclude=_x_is_not_none)
    )

    @classmethod
    def from_session_data(
        cls,
        channel_id: str,
        session_token: str,
        delegated_session_id: Optional[str],
        encrypted_video_id: str,
        metadata: Metadata,
        thumbnail_scotty_id: Optional[str] = None,
        thumbnail_format: Optional[str] = None,
    ):
        if (
            metadata.premiere_countdown_duration is not None
            and metadata.premiere_theme is not None
        ):
            # premiere, not scheduled upload
            premier_upload_time = metadata.scheduled_upload
            scheduled_upload_time = None
            metadata.privacy = PrivacyEnum.PUBLIC
        elif metadata.scheduled_upload is not None:
            # scheduled upload
            premier_upload_time = None
            scheduled_upload_time = metadata.scheduled_upload
            metadata.privacy = PrivacyEnum.PRIVATE
        else:
            # neither scheduled upload nor premiere
            premier_upload_time = None
            scheduled_upload_time = None

        return cls(
            APIContext.from_session_data(
                channel_id, session_token, delegated_session_id
            ),
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
                RacyDict[metadata.restricted_to_over_18]
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
            APIUpdateMetadataScheduledPublishing.from_metadata_args(
                APIUpdateMetadataSchedule.from_date(scheduled_upload_time)
            ),
            APIUpdateMetadataPremiere.from_date(premier_upload_time),
            APIUpdateMetadataPremiereIntro.from_metadata_args(
                APIUpdateMetadataCountdown.from_metadata_args(
                    metadata.premiere_countdown_duration
                ),
                metadata.premiere_theme,
            ),
        )
