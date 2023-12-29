import base64
import copy
import json
import math
import os
import re
import time
import uuid
from hashlib import sha1
from http.cookiejar import Cookie, FileCookieJar
from typing import Callable, Dict

import requests
import tqdm
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from seleniumwire import webdriver
from seleniumwire.utils import decode
from tqdm.utils import CallbackIOWrapper

from .metadata import *
from .metadata import CaptionsFile
from .schema import *

try:
    from http.cookiejar import HTTPONLY_ATTR, MozillaCookieJar
except ImportError:
    from .polyfills import HTTPONLY_ATTR, MozillaCookieJar
    
    


class YTUploaderException(Exception):
    """YouTube uploader exception"""


@dataclass
class YTUploaderVideoData:
    authuser: str = None
    channel_id: str = None
    innertube_api_key: str = None
    delegated_session_id: str = None
    front_end_upload_id: str = None
    encrypted_video_id: str = None
    thumbnail_scotty_id: str = None
    thumbnail_format: str = None


class YTUploaderSession:
    """
    Class for uploading YouTube videos to a single channel
    """

    _delegated_session_id_regex = re.compile(r'"DELEGATED_SESSION_ID":"([^"]*)"')
    _innertube_api_key_regex = re.compile(r'"INNERTUBE_API_KEY":"([^"]*)"')
    _session_index_regex = re.compile(r'"SESSION_INDEX":"([^"]*)"')
    _channel_id_regex = re.compile(r"https://studio.youtube.com/channel/([^/]*)/*")
    _progress_steps = {
        "start": 0,
        "get_session_data": 10,
        "get_upload_url": 20,
        "upload_video": 70,
        "get_session_token": 80,
        "create_video": 90,
        "upload_thumbnail": 95,
        "finish": 100,
    }

    _session_token: str
    _cookies: FileCookieJar
    _session: requests.Session

    def __init__(self, cookie_jar: FileCookieJar, webdriver_path: Optional[str] = None):
        """Create YTUploaderSession from generic FileCookieJar

        Args:
            cookie_jar (FileCookieJar): FileCookieJar. Must have save(), load(),
                and set_cookie(http.cookiejar.Cookie) methods
            webdriver_path (str, optional): Optional path to geckodriver or chromedriver executable
        """
        self._session_token = ""
        self._webdriver_path = webdriver_path

        # load cookies and init session
        self._cookies = cookie_jar
        self._cookies.load(ignore_discard=True, ignore_expires=True)
        self._session = requests.Session()
        for cookie in self._cookies:
            if cookie.name == "SESSION_TOKEN":
                self._session_token = cookie.value
            else:
                self._session.cookies.set_cookie(copy.copy(cookie))
        self._session.headers = {
            "Authorization": f"SAPISIDHASH {self._generateSAPISIDHASH(self._session.cookies['SAPISID'])}",
            "x-origin": "https://studio.youtube.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        }

    @classmethod
    def from_cookies_txt(cls, cookies_txt_path: str, webdriver_path: Optional[str] = None):
        """Create YTUploaderSession from cookies.txt file

        Args:
            cookies_txt_path (str): Path to Netscape cookies format file
            webdriver_path (str, optional): Optional path to geckodriver or chromedriver executable
        """
        cj = MozillaCookieJar(cookies_txt_path)
        return cls(cj, webdriver_path)

    def upload(
        self,
        file_path: str,
        metadata: Metadata,
        progress_callback: Callable[[str, float], None] = lambda step, percent: None,
    ) -> str:
        """Upload a video

        Args:
            file_path (str): Path to video file
            metadata (Metadata): Metadata of video to set when uploaded
            progress_callback (Callable[[str, float], None], optional): Optional progress callback.
                Callback receives what step uploader is on and what the total percentage of the upload
                progress is (defined by YTUploaderSession._progress_steps).
        
        Returns:
            str: ID of video uploaded
        """
        try:
            metadata.validate()
        except ValueError as ex:
            raise YTUploaderException(f"Validation error: {ex}") from ex
        progress_callback("start", self._progress_steps["start"])
        data = YTUploaderVideoData()
        self._get_session_data(data)
        progress_callback("get_session_data", self._progress_steps["get_session_data"])
        url = self._get_video_upload_url(data)
        progress_callback("get_upload_url", self._progress_steps["get_upload_url"])
        scotty_resource_id = self._upload_file(
            url, file_path, progress_callback, "get_upload_url", "upload_video"
        )
        progress_callback("upload_video", self._progress_steps["upload_video"])
        try:
            data.encrypted_video_id = self._create_video(
                scotty_resource_id, metadata, data
            )
        except requests.HTTPError as ex:
            if ex.response.status_code == 400:
                # could be bad session token, try to get new one
                self._get_session_token()
                progress_callback(
                    "get_session_token", self._progress_steps["get_session_token"]
                )
                data.encrypted_video_id = self._create_video(
                    scotty_resource_id, metadata, data
                )
        progress_callback("create_video", self._progress_steps["create_video"])

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
        # captions
        if metadata.captions_files:
            for caption_file in metadata.captions_files:
                if caption_file.language is None:
                    caption_file.language = metadata.audio_language
                self._update_captions(
                    caption_file,
                    data
                )
            
        self._update_metadata(metadata, data)
        # save cookies
        for cookie in self._session.cookies:
            self._cookies.set_cookie(cookie)
        self._cookies.save()
        progress_callback("finish", self._progress_steps["finish"])
        return data.encrypted_video_id

    def has_valid_cookies(self) -> bool:
        """Check if cookies are valid

        Returns:
            bool: True if we are able to log in to YouTube with the given cookies
        """
        r = self._session.get("https://youtube.com/upload")

        return "studio.youtube.com/channel" in r.url

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
            if self._webdriver_path:
                service = FirefoxService(self._webdriver_path)
                driver = webdriver.Firefox(options=options, service=service)
            else:
                driver = webdriver.Firefox(options=options)
        except Exception:
            try:
                # try chrome
                options = webdriver.ChromeOptions()
                options.add_argument("--headless=new")
                if self._webdriver_path:
                    service = ChromeService(self._webdriver_path)
                    driver = webdriver.Chrome(options=options, service=service)
                else:
                    driver = webdriver.Chrome(options=options)
            except Exception:
                raise YTUploaderException(
                    "Could not launch Firefox or Chrome. Make sure geckodriver or chromedriver is installed"
                )

        driver.get("https://youtube.com")

        for cookie in self._cookies:
            if cookie.name != "SESSION_TOKEN":
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
        self._session_token = r_json["sessionToken"]
        self._cookies.set_cookie(
            Cookie(
                None,
                "SESSION_TOKEN",
                self._session_token,
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
        self._cookies.save()
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
        r = self._session.get("https://youtube.com/upload")

        if "studio.youtube.com/channel" not in r.url:
            raise YTUploaderException(
                "Could not log in to YouTube account. Try getting new cookies"
            )

        data.channel_id = self._channel_id_regex.match(r.url).group(1)
        data.innertube_api_key = self._innertube_api_key_regex.search(r.text).group(1)
        m = self._delegated_session_id_regex.search(r.text)
        data.delegated_session_id = m and m.group(1)
        data.authuser = self._session_index_regex.search(r.text).group(1)
        self._session.headers["X-Goog-AuthUser"] = data.authuser

    def _get_upload_url(self, api_url: str, authuser: str, data: dict) -> str:
        params = {"authuser": authuser}
        headers = {
            "x-goog-upload-command": "start",
            "x-goog-upload-protocol": "resumable",
        }
        r = self._session.post(
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

    def _get_creator_playlists(self, data: YTUploaderVideoData) -> Dict[str, str]:
        params = {"key": data.innertube_api_key, "alt": "json"}
        data = APIRequestListPlaylists.from_session_data(
            data.channel_id,
            self._session_token,
            data.delegated_session_id
        ).to_dict()
        r = self._session.post(
            "https://studio.youtube.com/youtubei/v1/creator/list_creator_playlists",
            params=params,
            json=data,
        )
        r.raise_for_status()
        return {
            playlist["title"]: playlist["playlistId"]
            for playlist in r.json().get("playlists", [])
        }

    def _create_playlist(
        self,
        playlist: Playlist,
        data: YTUploaderVideoData,
    ) -> str:
        params = {"key": data.innertube_api_key, "alt": "json"}
        data = APIRequestCreatePlaylist.from_session_data(
            data.channel_id, self._session_token, data.delegated_session_id, playlist
        ).to_dict()
        r = self._session.post(
            "https://studio.youtube.com/youtubei/v1/playlist/create",
            params=params,
            json=data,
        )
        r.raise_for_status()
        return r.json()["playlistId"]

    def _update_captions(
        self,
        caption_file: CaptionsFile,
        data: YTUploaderVideoData,
    ):
        params = {"key": data.innertube_api_key, "alt": "json"}
        with open(caption_file.path, "rb") as f:
            captions_b64 = "data:application/octet-stream;base64," + base64.b64encode(f.read()).decode("utf-8")
        timestamp = str(time.time_ns())
        data = APIRequestUpdateCaptions.from_session_data(
            data.channel_id,
            self._session_token,
            data.delegated_session_id,
            data.encrypted_video_id,
            caption_file.path,
            captions_b64,
            caption_file.language,
            timestamp
        ).to_dict()
        r = self._session.post(
            "https://studio.youtube.com/youtubei/v1/globalization/update_captions",
            params=params,
            json=data,
        )
        r.raise_for_status()

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
                start_prog = self._progress_steps[prev_progress_step]
                end_prog = self._progress_steps[cur_progress_step]
                cur_prog = start_prog + (end_prog - start_prog) * (bytes_sent / size)
                cur_prog = round(cur_prog, 1)
                progress_callback(cur_progress_step, cur_prog)

            wrapped_file = CallbackIOWrapper(upload_callback, f)
            r = self._session.post(upload_url, headers=headers, data=wrapped_file)

        r.raise_for_status()
        return r.json()["scottyResourceId"]

    def _create_video(
        self, scotty_resource_id: str, metadata: Metadata, data: YTUploaderVideoData
    ) -> str:
        params = {"key": data.innertube_api_key, "alt": "json"}
        data = APIRequestCreateVideo.from_session_data(
            data.channel_id,
            self._session_token,
            data.delegated_session_id,
            data.front_end_upload_id,
            metadata,
            scotty_resource_id,
        ).to_dict()
        r = self._session.post(
            "https://studio.youtube.com/youtubei/v1/upload/createvideo",
            params=params,
            json=data,
        )
        r.raise_for_status()
        r = r.json()
        if "videoId" not in r:
            raise YTUploaderException(
                f"Could not upload. Daily limit may have been reached. Response: {r}"
            )
        return r["videoId"]

    def _update_metadata(self, metadata: Metadata, data: YTUploaderVideoData):
        params = {"key": data.innertube_api_key, "alt": "json"}
        data = APIRequestUpdateMetadata.from_session_data(
            data.channel_id,
            self._session_token,
            data.delegated_session_id,
            data.encrypted_video_id,
            metadata,
            data.thumbnail_scotty_id,
            data.thumbnail_format,
        ).to_dict()
        r = self._session.post(
            "https://studio.youtube.com/youtubei/v1/video_manager/metadata_update",
            params=params,
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
        PrivacyEnum.UNLISTED,
        tags=["Music", "test tag lol"],
        allow_comments=False,
        thumbnail="test/thumb.jpg",
    )
    with tqdm.tqdm(total=100) as pbar:

        def callback(step: str, prog: int):
            pbar.n = prog
            pbar.update()

        uploader.upload(file_path, metadata, callback)
