import hmac
import requests
import urllib.parse
import validators
from hashlib import sha1
from urlbox import InvalidUrlException


class UrlboxClient:

    """
        The core client object used to interact with the Urlbox API

        :param api_key: Your API key found in your Urlbox Dashboard
        `https://urlbox.io/dashboard/api`

        :param api_secret: (Optional) Your API secret found in your Urlbox
        Dashboard`https://urlbox.io/dashboard/api`
        Required for authenticated requests.
    """

    BASE_API_URL = "https://api.urlbox.io/v1/"

    def __init__(self, *, api_key, api_secret=None, api_host_name=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_api_url = self._init_base_api_url(api_host_name)

    def get(self, options):
        """
            Make simple get request to Urlbox API

            :param options: dictionary containing all of the options you want to set.
            eg: {"url": "http://example.com/", "format": "png", "full_page": True, "width": 300}

            format: can be either "png", "jpg", "jpeg", "avif", "webp", "pdf", "svg", "html".

            Example: urlbox_client.get({"url": "http://example.com/", "format": "png", "full_page": True, "width": 300})
            API example: https://urlbox.io/docs/getting-started
            Full options reference: https://urlbox.io/docs/options
        """

        format = options["format"]
        url = options["url"]

        url_stripped = url.strip()
        options["url"] = url_stripped
        url_encoded_options = urllib.parse.urlencode(options)

        if not self._valid_url(url_stripped):
            raise InvalidUrlException(url_stripped)

        if self.api_secret is None:
            return self._get_unauthenticated(format, url_encoded_options)
        else:
            return self._get_authenticated(format, url_encoded_options)

    # private

    def _get_authenticated(self, format, url_encoded_options):
        return requests.get(
            (
                f"{self.base_api_url}"
                f"{self.api_key}/{self._token(url_encoded_options)}/{format}"
                f"?{url_encoded_options}"
            )
        )

    def _get_unauthenticated(self, format, url_encoded_options):
        return requests.get(
            (
                f"{self.base_api_url}"
                f"{self.api_key}/{format}"
                f"?{url_encoded_options}"
            )
        )

    # private

    def _init_base_api_url(self, api_host_name):
        if api_host_name is None:
            return self.BASE_API_URL
        else:
            return f"https://{api_host_name}/"

    def _parsed_url(self, url):
        # TODO: if not url.startswith("http"): url = "http://" + url
        pass

    def _token(self, url_encoded_options):
        return (
            hmac.new(
                str.encode(self.api_secret),
                str.encode(url_encoded_options),
                sha1,
            )
            .hexdigest()
            .rstrip("\n")
        )

    def _valid_url(self, url):
        return validators.url(url) == True
