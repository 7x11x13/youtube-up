import argparse
import json
from argparse import BooleanOptionalAction

import tqdm

from youtube_up.metadata import (
    AllowCommentsEnum,
    CaptionsFile,
    CategoryEnum,
    CommentsSortOrderEnum,
    LicenseEnum,
    Metadata,
    PremiereDurationEnum,
    PremiereThemeEnum,
    PrivacyEnum,
)

from .uploader import YTUploaderSession


def main():
    parser = argparse.ArgumentParser(
        prog="youtube-up",
        description="Upload videos to YouTube using the internal YouTube API",
    )
    subparsers = parser.add_subparsers(help="commands", dest="command", required=True)

    json_parser = subparsers.add_parser("json")
    json_parser.add_argument(
        "filename",
        help="JSON file specifying videos to upload. File should"
        "be an array of objects with 'file' and 'metadata' keys where 'file' "
        "is a path to a video file and 'metadata' is structured as the Metadata"
        "class",
    )
    json_parser.add_argument(
        "--cookies_file", help="Path to Netscape cookies.txt file", required=True
    )

    video_parser = subparsers.add_parser("video")
    video_parser.add_argument("filename", help="Video file to upload")
    video_parser.add_argument(
        "--cookies_file", help="Path to Netscape cookies.txt file", required=True
    )
    video_parser.add_argument("--title", help="Title. Max length 100", required=True)
    video_parser.add_argument(
        "--description", help="Description. Max length 5000", default=""
    )
    video_parser.add_argument(
        "--privacy", help="Privacy", type=PrivacyEnum, default=PrivacyEnum.PRIVATE
    )
    video_parser.add_argument(
        "--made_for_kids",
        help="Made for kids. If true comments will be disabled",
        action=BooleanOptionalAction,
        default=False,
    )
    video_parser.add_argument("--tags", nargs="+", help="List of tags", default=[])
    video_parser.add_argument(
        "--scheduled_upload",
        help="Date to make upload public, in ISO format (local time, unless timezone is specified)."
        " If set, video will be set to private until the date, unless video is a premiere in which "
        "case it will be set to public. Video will not be a premiere unless both "
        "premiere_countdown_duration and premiere_theme are set",
    )
    video_parser.add_argument(
        "--premiere_countdown_duration",
        help="Duration of premiere countdown in seconds",
        type=PremiereDurationEnum,
    )
    video_parser.add_argument(
        "--premiere_theme",
        help="Theme of premiere countdown",
        type=PremiereThemeEnum,
    )
    video_parser.add_argument(
        "--playlist_ids",
        nargs="+",
        help="List of existing playlist IDs to add video to",
    )
    video_parser.add_argument("--thumbnail", help="Path to thumbnail file to upload")
    video_parser.add_argument(
        "--publish_to_feed",
        help="Whether to notify subscribers",
        action=BooleanOptionalAction,
    )
    video_parser.add_argument(
        "--category",
        help="Category. Category-specific metadata is not supported yet",
        type=CategoryEnum,
    )
    video_parser.add_argument(
        "--auto_chapter",
        help="Whether to use automatic video chapters",
        action=BooleanOptionalAction,
    )
    video_parser.add_argument(
        "--auto_places",
        help="Whether to use automatic places",
        action=BooleanOptionalAction,
    )
    video_parser.add_argument(
        "--auto_concepts",
        help="Whether to use automatic concepts",
        action=BooleanOptionalAction,
    )
    video_parser.add_argument(
        "--has_product_placement",
        help="Whether video has product placement",
        action=BooleanOptionalAction,
    )
    video_parser.add_argument(
        "--show_product_placement_overlay",
        help="Whether to show product placement overlay",
        action=BooleanOptionalAction,
    )
    video_parser.add_argument(
        "--recorded_date",
        help="Day, month, and year that video was recorded, in ISO format",
    )
    video_parser.add_argument(
        "--restricted_to_over_18",
        help="Whether video is age restricted",
        action=BooleanOptionalAction,
    )
    video_parser.add_argument(
        "--audio_language",
        help="Language of audio. If uploading captions this must be set",
    )
    video_parser.add_argument(
        "--captions_file",
        help="Path to captions file (.srt) with language audio_language",
        type=CaptionsFile,
    )
    video_parser.add_argument(
        "--license",
        help="License",
        type=LicenseEnum,
    )
    video_parser.add_argument(
        "--allow_comments",
        help="Whether to allow comments",
        action=BooleanOptionalAction,
    )
    video_parser.add_argument(
        "--allow_comments_mode",
        help="Comment filtering mode",
        type=AllowCommentsEnum,
    )
    video_parser.add_argument(
        "--can_view_ratings",
        help="Whether video likes/dislikes can be seen",
        action=BooleanOptionalAction,
    )
    video_parser.add_argument(
        "--comments_sort_order",
        help="Default comment sort order",
        type=CommentsSortOrderEnum,
    )
    video_parser.add_argument(
        "--allow_embedding",
        help="Whether to allow embedding on 3rd party sites",
        action=BooleanOptionalAction,
    )

    args = parser.parse_args()

    uploader = YTUploaderSession.from_cookies_txt(args.cookies_file)

    if args.command == "json":
        with open(args.filename, "r") as f:
            data = json.load(f)
        with tqdm.tqdm(total=100 * len(data)) as pbar:
            for i, video in enumerate(data):

                def callback(step: str, prog: int):
                    pbar.n = 100 * i + prog
                    pbar.update()

                video_id = uploader.upload(
                    video["file"], Metadata.from_dict(video["metadata"]), callback
                )
                tqdm.tqdm.write(
                    f"Uploaded video: https://youtube.com/watch?v={video_id}"
                )
    else:
        args_dict = vars(args)
        args_dict.pop("cookies_file")
        args_dict.pop("command")
        video_file = args_dict.pop("filename")
        captions_file = args_dict.pop("captions_file")
        if captions_file is None:
            args_dict["captions_files"] = None
        else:
            args_dict["captions_files"] = [captions_file]
        metadata = Metadata.from_dict(args_dict)
        with tqdm.tqdm(total=100) as pbar:

            def callback(step: str, prog: int):
                pbar.n = prog
                pbar.update()

            video_id = uploader.upload(video_file, metadata, callback)
            tqdm.tqdm.write(f"Uploaded video: https://youtube.com/watch?v={video_id}")


if __name__ == "__main__":
    main()
    main()


if __name__ == "__main__":
    main()
    main()
