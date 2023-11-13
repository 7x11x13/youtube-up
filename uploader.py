import copy
import json
import math
import re
import time
import uuid
from hashlib import sha1
from http.cookiejar import Cookie, CookieJar, FileCookieJar, MozillaCookieJar

import requests
from seleniumwire import webdriver
from seleniumwire.utils import decode

from schema import *


class YTUploaderException(Exception):
    pass


class YTUploaderSession:
    innertube_api_key_regex = re.compile(r'"INNERTUBE_API_KEY":"([^"]*)"')
    channel_id_regex = re.compile(r"https://studio.youtube.com/channel/([^/]*)/*")

    def __init__(self, cookie_jar: FileCookieJar):
        self.channel_id: str = ""
        self.innertube_api_key: str = ""
        self.session_token: str = ""
        self.front_end_upload_id: str = ""

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

    def upload(self, file_path: str, metadata: Metadata):
        self._get_session_data()
        url = self._get_upload_url()
        scotty_resource_id = self._upload_file(url, file_path)
        try:
            encrypted_video_id = self._create_video(scotty_resource_id, metadata)
        except requests.HTTPError as ex:
            if ex.response.status_code == 400:
                # could be bad session token, try to get new one
                self._get_session_token()
                encrypted_video_id = self._create_video(scotty_resource_id, metadata)
        self._update_metadata(encrypted_video_id, metadata)

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

    def _get_session_data(self):
        r = self.session.get("https://youtube.com/upload")

        if "studio.youtube.com/channel" not in r.url:
            raise YTUploaderException(
                "Could not log in to YouTube account. Try getting new cookies"
            )

        self.channel_id = self.channel_id_regex.match(r.url).group(1)
        self.innertube_api_key = self.innertube_api_key_regex.search(r.text).group(1)

    def _get_creator_channels(self) -> list[str]:
        params = {"key": self.innertube_api_key, "alt": "json"}
        data = {
            "channelIds": [self.channel_id],
            "context": APIContext.from_session_data(
                self.channel_id, self.session_token
            ).to_dict(),
        }
        r = self.session.post(
            "https://studio.youtube.com/youtubei/v1/creator/get_creator_channels",
            params=params,
            json=data,
        )
        r.raise_for_status()
        return r.json()

    def _get_upload_url(self) -> str:
        params = {"authuser": 0}
        headers = {
            "x-goog-upload-command": "start",
            "x-goog-upload-protocol": "resumable",
        }
        self.front_end_upload_id = f"innertube_studio:{self._generateUUID()}:0"
        r = self.session.post(
            "https://upload.youtube.com/upload/studio",
            headers=headers,
            params=params,
            data=f'{{"frontendUploadId":"{self.front_end_upload_id}"}}',
        )
        r.raise_for_status()
        upload_url = r.headers["x-goog-upload-url"]
        return upload_url

    def _upload_file(self, upload_url: str, file_path: str):
        params = {"authuser": 0}
        headers = {
            "x-goog-upload-command": "upload, finalize",
            "x-goog-upload-offset": "0",
        }
        with open(file_path, "rb") as f:
            r = self.session.post(upload_url, headers=headers, params=params, data=f)

        r.raise_for_status()
        return r.json()["scottyResourceId"]

    def _create_video(self, scotty_resource_id: str, metadata: Metadata) -> str:
        params = {"key": self.innertube_api_key, "alt": "json"}
        """
        data = {
            "channelId": self.channel_id,
            "context": APIContext.from_session_data(
                self.channel_id, self.session_token
            ).to_dict(),
            "delegationContext": APIDelegationContext(self.channel_id).to_dict(),
            "frontendUploadId": self.front_end_upload_id,
            "initialMetadata": APIInitialMetadata.from_metadata(metadata).to_dict(),
            "presumedShort": False,
            "resourceId": {"scottyResourceId": {"id": scotty_resource_id}},
        }
        """
        data = APIRequestCreateVideo.from_session_data(
            self.channel_id,
            self.session_token,
            self.front_end_upload_id,
            metadata,
            False,
            scotty_resource_id,
        ).to_dict()
        print(data)
        r = self.session.post(
            "https://studio.youtube.com/youtubei/v1/upload/createvideo",
            params=params,
            json=data,
        )
        r.raise_for_status()
        return r.json()["videoId"]

    def _update_metadata(self, encrypted_video_id: str, metadata: Metadata):
        params = {"key": self.innertube_api_key, "alt": "json"}
        data = APIRequestUpdateMetadata.from_session_data(
            self.channel_id, self.session_token, encrypted_video_id, metadata
        ).to_dict()
        print(data)
        r = self.session.post(
            "https://studio.youtube.com/youtubei/v1/video_manager/metadata_update",
            params=params,
            json=data,
        )
        r.raise_for_status()


if __name__ == "__main__":
    uploader = YTUploaderSession.from_cookies_txt("cookies.txt")
    file_path = "test.mp4"
    metadata = Metadata(
        "test title",
        "test description",
        PrivacyEnum.UNLISTED,
        tags=["Music", "test tag lol"],
        allow_comments=False,
    )
    uploader.upload(file_path, metadata)
