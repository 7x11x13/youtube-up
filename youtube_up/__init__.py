# ruff: noqa
"""
# Installation

`pip install youtube-up`

## Installing certificates

On your first run you may get an error which says `Was not able to load https://youtube.com. Have you installed the certificate at {cert_path} ?`.
If this happens you should follow the instructions at https://docs.mitmproxy.org/stable/concepts-certificates/#installing-the-mitmproxy-ca-certificate-manually
to install the certificate at the given path.

# Examples

## Upload a video
```python
from youtube_up import AllowCommentsEnum, Metadata, PrivacyEnum, YTUploaderSession

uploader = YTUploaderSession.from_cookies_txt("cookies/cookies.txt")
metadata = Metadata(
    title="Video title",
    description="Video description",
    privacy=PrivacyEnum.PUBLIC,
    made_for_kids=False,
    allow_comments_mode=AllowCommentsEnum.HOLD_ALL,
)
uploader.upload("video.webm", metadata)
```
Note that for Enum-type parameters we can either pass the Enum itself (as shown above),
or the Enum value, or the Enum key, as a string. For example, instead of writing

`allow_comments_mode=AllowCommentsEnum.HOLD_ALL`

we could instead write `allow_comments_mode="HOLD_ALL"`
or `allow_comments_mode="APPROVED_COMMENTS"`

## Upload multiple videos
```python
from youtube_up import Metadata, YTUploaderSession

uploader = YTUploaderSession.from_cookies_txt("cookies/cookies.txt")
metadata_1 = Metadata(
    title="Video 1",
)
metadata_2 = Metadata(
    title="Video 2",
)
uploader.upload("video1.webm", metadata_1)
uploader.upload("video2.webm", metadata_2)
```

## Upload to a new or existing playlist
```python
from youtube_up import Metadata, YTUploaderSession, Playlist

uploader = YTUploaderSession.from_cookies_txt("cookies/cookies.txt")
metadata = Metadata(
    title="Video 1",
    playlists=[
        Playlist(
            "Songs by me",
            description="Playlist that will only be created if "
            "no playlist exists with the title 'Songs by me'",
            create_if_title_doesnt_exist=True,
            create_if_title_exists=False,
        ),
        Playlist(
            "test playlist",
            description="Playlist that video will be added to "
            "only if it exists already. This description does "
            "nothing.",
            create_if_title_doesnt_exist=False,
            create_if_title_exists=False,
        ),
        Playlist(
            "Album",
            description="Playlist will be created even if there"
            " is already a playlist with the name 'Album'"
            create_if_title_doesnt_exist=True,
            create_if_title_exists=True,
        ),
    ],
)
uploader.upload("video.webm", metadata)
```

## CLI
youtube-up comes with a CLI app for uploading videos. For example, if we wanted to
create a public video with the title "Video title", we would execute the following command:
`youtube-up video video.webm --title="Video title" --cookies_file="cookies/cookies.txt" --privacy="PUBLIC"`

The app can also take a JSON file as input. For example, the following JSON file would upload
one video to a new or existing playlist called "Music" and one video which is set to premiere
on December 25th, 2023 at 5 PM (local time).

```json
[
    {
        "file": "song.webm",
        "metadata": {
            "title": "New song",
            "privacy": "PUBLIC",
            "playlists": [
                {
                    "title": "Music"
                }
            ]
        }
    },
    {
        "file": "premiere.webm",
        "metadata": {
            "title": "Special Announcement",
            "scheduled_upload": "2023-12-25T17:00:00",
            "premiere_countdown_duration": "ONE_MIN",
            "premiere_theme": "BRIGHT"
        }
    }
]
```

If we wanted the video to premiere at 5 PM GMT, would could have written "2023-12-25T17:00:00+00:00"
instead. We then run

`youtube-up json metadata.json --cookies_file="cookies/cookies.txt"`

to upload these videos.
"""

from .metadata import *
from .metadata import __all__ as m_all
from .uploader import *
from .uploader import __all__ as u_all

__all__ = u_all + m_all
