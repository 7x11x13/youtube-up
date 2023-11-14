import copy
import json
import math
import os
import re
import time
import uuid
from hashlib import sha1
from http.cookiejar import Cookie, FileCookieJar, MozillaCookieJar
from typing import Callable

import requests
import tqdm
from seleniumwire import webdriver
from seleniumwire.utils import decode
from tqdm.utils import CallbackIOWrapper

from .metadata import *
from .schema import *


class YTUploaderException(Exception):
    pass


@dataclass
class YTUploaderVideoData:
    authuser: str = None
    channel_id: str = None
    innertube_api_key: str = None
    front_end_upload_id: str = None
    encrypted_video_id: str = None
    thumbnail_scotty_id: str = None
    thumbnail_format: str = None


class YTUploaderSession:
    innertube_api_key_regex = re.compile(r'"INNERTUBE_API_KEY":"([^"]*)"')
    session_index_regex = re.compile(r'"SESSION_INDEX":"([^"]*)"')
    channel_id_regex = re.compile(r"https://studio.youtube.com/channel/([^/]*)/*")
    progress_steps = {
        "start": 0,
        "get_session_data": 10,
        "get_upload_url": 20,
        "upload_video": 70,
        "get_session_token": 80,
        "create_video": 90,
        "upload_thumbnail": 95,
        "finish": 100,
    }

    def __init__(self, cookie_jar: FileCookieJar):
        self.session_token: str = ""

        # load cookies and init session
        self.cookies = cookie_jar
        self.cookies.load(ignore_discard=True)
        self.session = requests.Session()
        for cookie in self.cookies:
            if cookie.name == "YT_UPLOADER_SESSION_ID":
                self.session_token = cookie.value
            else:
                self.session.cookies.set_cookie(copy.copy(cookie))
        self.session.headers = {
            "Authorization": f"SAPISIDHASH {self._generateSAPISIDHASH(self.session.cookies['SAPISID'])}",
            "x-origin": "https://studio.youtube.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        }

    @classmethod
    def from_cookies_txt(cls, cookies_txt_path: str):
        cj = MozillaCookieJar(cookies_txt_path)
        return cls(cj)

    def upload(
        self,
        file_path: str,
        metadata: Metadata,
        progress_callback: Callable[[str, float], None] = lambda step, percent: None,
    ):
        progress_callback("start", self.progress_steps["start"])
        data = YTUploaderVideoData()
        self._get_session_data(data)
        progress_callback("get_session_data", self.progress_steps["get_session_data"])
        url = self._get_video_upload_url(data)
        progress_callback("get_upload_url", self.progress_steps["get_upload_url"])
        scotty_resource_id = self._upload_file(
            url, file_path, progress_callback, "get_upload_url", "upload_video"
        )
        progress_callback("upload_video", self.progress_steps["upload_video"])
        try:
            data.encrypted_video_id = self._create_video(
                scotty_resource_id, metadata, data
            )
        except requests.HTTPError as ex:
            if ex.response.status_code == 400:
                # could be bad session token, try to get new one
                self._get_session_token()
                progress_callback(
                    "get_session_token", self.progress_steps["get_session_token"]
                )
                data.encrypted_video_id = self._create_video(
                    scotty_resource_id, metadata, data
                )
        progress_callback("create_video", self.progress_steps["create_video"])

        # set thumbnail
        if metadata.thumbnail is not None:
            url = self._get_upload_url_thumbnail(data)
            data.thumbnail_scotty_id = self._upload_file(
                url,
                metadata.thumbnail,
                progress_callback,
                "create_video",
                "upload_thumbnail",
            )
            data.thumbnail_format = self._get_thumbnail_format(metadata.thumbnail)

        # playlists
        if metadata.playlists:
            playlists = self._get_creator_playlists(data)
            if metadata.playlist_ids is None:
                metadata.playlist_ids = []
            for playlist in metadata.playlists:
                exists = playlist.title in playlists
                if (playlist.create_if_title_exists and exists) or (
                    playlist.create_if_title_doesnt_exist and not exists
                ):
                    playlist_id = self._create_playlist(playlist, data)
                    metadata.playlist_ids.append(playlist_id)
                elif exists:
                    metadata.playlist_ids.append(playlists[playlist.title])

        self._update_metadata(metadata, data)
        progress_callback("finish", self.progress_steps["finish"])

    def _get_thumbnail_format(self, filename: str) -> ThumbnailFormatEnum:
        ext = filename.split(".")[-1]
        if ext in ("jpg", "jpeg", "jfif", "pjpeg", "pjp"):
            return ThumbnailFormatEnum.JPG
        if ext in ("png",):
            return ThumbnailFormatEnum.PNG
        raise YTUploaderException(
            f"Unknown format for thumbnail with extension '{ext}'. Only JPEG and PNG allowed"
        )

    def _get_session_token(self):
        try:
            # try firefox
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
        except Exception:
            try:
                # try chrome
                options = webdriver.ChromeOptions()
                options.add_argument("--headless=new")
                driver = webdriver.Chrome(options=options)
            except Exception:
                raise YTUploaderException(
                    "Could not launch Firefox or Chrome. Make sure geckodriver or chromedriver is installed"
                )

        driver.get("https://youtube.com")

        for cookie in self.cookies:
            if cookie.name != "YT_UPLOADER_SESSION_ID":
                driver.add_cookie(cookie.__dict__)

        driver.get("https://youtube.com/upload")

        if "studio.youtube.com/channel" not in driver.current_url:
            driver.quit()
            raise YTUploaderException(
                "Could not log in to YouTube account. Try getting new cookies"
            )

        r = driver.wait_for_request("studio.youtube.com/youtubei/v1/ars/grst")
        response = r.response
        r_json = json.loads(
            decode(response.body, response.headers.get("Content-Encoding"))
        )
        self.session_token = r_json["sessionToken"]
        self.cookies.set_cookie(
            Cookie(
                None,
                "YT_UPLOADER_SESSION_ID",
                self.session_token,
                None,
                False,
                "",
                False,
                False,
                "",
                False,
                False,
                None,
                False,
                None,
                None,
                {},
            )
        )
        self.cookies.save()
        driver.quit()

    @staticmethod
    def _generateUUID() -> str:
        return str(uuid.uuid4()).upper()

    @staticmethod
    def _generateSAPISIDHASH(SAPISID) -> str:
        timestamp = math.floor(time.time())
        msg = f"{timestamp} {SAPISID} {'https://studio.youtube.com'}"
        hash = sha1(msg.encode("utf-8")).hexdigest()
        return f"{timestamp}_{hash}"

    def _get_session_data(self, data: YTUploaderVideoData):
        r = self.session.get("https://youtube.com/upload")

        if "studio.youtube.com/channel" not in r.url:
            raise YTUploaderException(
                "Could not log in to YouTube account. Try getting new cookies"
            )

        data.channel_id = self.channel_id_regex.match(r.url).group(1)
        data.innertube_api_key = self.innertube_api_key_regex.search(r.text).group(1)
        data.authuser = self.session_index_regex.search(r.text).group(1)

    def _get_upload_url(self, api_url: str, authuser: str, data: dict) -> str:
        params = {"authuser": authuser}
        headers = {
            "x-goog-upload-command": "start",
            "x-goog-upload-protocol": "resumable",
        }
        r = self.session.post(
            api_url,
            headers=headers,
            params=params,
            json=data,
        )
        r.raise_for_status()
        upload_url = r.headers["x-goog-upload-url"]
        return upload_url

    def _get_video_upload_url(self, data: YTUploaderVideoData) -> str:
        data.front_end_upload_id = f"innertube_studio:{self._generateUUID()}:0"
        return self._get_upload_url(
            "https://upload.youtube.com/upload/studio",
            data.authuser,
            {"frontendUploadId": data.front_end_upload_id},
        )

    def _get_upload_url_thumbnail(self, data: YTUploaderVideoData) -> str:
        return self._get_upload_url(
            "https://upload.youtube.com/upload/studiothumbnail", data.authuser, {}
        )

    def _get_creator_playlists(self, data: YTUploaderVideoData) -> dict[str, str]:
        params = {"key": data.innertube_api_key, "alt": "json"}
        data = APIRequestListPlaylists.from_session_data(
            data.channel_id,
            self.session_token,
        ).to_dict()
        r = self.session.post(
            "https://studio.youtube.com/youtubei/v1/creator/list_creator_playlists",
            params=params,
            json=data,
        )
        r.raise_for_status()
        return {
            playlist["title"]: playlist["playlistId"]
            for playlist in r.json()["playlists"]
        }

    def _create_playlist(
        self,
        playlist: Playlist,
        data: YTUploaderVideoData,
    ) -> str:
        params = {"key": data.innertube_api_key, "alt": "json"}
        data = APIRequestCreatePlaylist.from_session_data(
            data.channel_id, self.session_token, playlist
        ).to_dict()
        r = self.session.post(
            "https://studio.youtube.com/youtubei/v1/playlist/create",
            params=params,
            json=data,
        )
        r.raise_for_status()
        return r.json()["playlistId"]

    def _upload_file(
        self,
        upload_url: str,
        file_path: str,
        progress_callback: Callable[[str, float], None],
        prev_progress_step: str,
        cur_progress_step: str,
    ):
        headers = {
            "x-goog-upload-command": "upload, finalize",
            "x-goog-upload-offset": "0",
        }

        with open(file_path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(0)
            bytes_sent = 0

            def upload_callback(bytes: int):
                nonlocal bytes_sent
                bytes_sent += bytes
                start_prog = self.progress_steps[prev_progress_step]
                end_prog = self.progress_steps[cur_progress_step]
                cur_prog = start_prog + (end_prog - start_prog) * (bytes_sent / size)
                cur_prog = round(cur_prog, 1)
                progress_callback(cur_progress_step, cur_prog)

            wrapped_file = CallbackIOWrapper(upload_callback, f)
            r = self.session.post(upload_url, headers=headers, data=wrapped_file)

        r.raise_for_status()
        return r.json()["scottyResourceId"]

    def _create_video(
        self, scotty_resource_id: str, metadata: Metadata, data: YTUploaderVideoData
    ) -> str:
        params = {"key": data.innertube_api_key, "alt": "json"}
        headers = {"X-Goog-AuthUser": data.authuser}
        data = APIRequestCreateVideo.from_session_data(
            data.channel_id,
            self.session_token,
            data.front_end_upload_id,
            metadata,
            scotty_resource_id,
        ).to_dict()
        r = self.session.post(
            "https://studio.youtube.com/youtubei/v1/upload/createvideo",
            params=params,
            headers=headers,
            json=data,
        )
        r.raise_for_status()
        return r.json()["videoId"]

    def _update_metadata(self, metadata: Metadata, data: YTUploaderVideoData):
        params = {"key": data.innertube_api_key, "alt": "json"}
        headers = {"X-Goog-AuthUser": data.authuser}
        data = APIRequestUpdateMetadata.from_session_data(
            data.channel_id,
            self.session_token,
            data.encrypted_video_id,
            metadata,
            data.thumbnail_scotty_id,
            data.thumbnail_format,
        ).to_dict()
        r = self.session.post(
            "https://studio.youtube.com/youtubei/v1/video_manager/metadata_update",
            params=params,
            headers=headers,
            json=data,
        )
        r.raise_for_status()


__all__ = ["YTUploaderSession", "YTUploaderException"]

if __name__ == "__main__":
    uploader = YTUploaderSession.from_cookies_txt("test/cookies.txt")
    file_path = "test/short.webm"
    metadata = Metadata(
        "test title not short",
        "test description",
        PrivacyEnum.PUBLIC,
        tags=["Music", "test tag lol"],
        allow_comments=False,
        thumbnail="test/thumb.jpg",
    )
    with tqdm.tqdm(total=100) as pbar:

        def callback(step: str, prog: int):
            pbar.n = prog
            pbar.update()

        uploader.upload(file_path, metadata, callback)
