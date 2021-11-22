import requests
import urllib.parse
import validators
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

    URLBOX_BASE_API_URL = "https://api.urlbox.io/v1/"

    def __init__(self, *, api_key, api_secret=None):
        self.api_key = api_key
        self.api_secret = api_secret

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

        if not self._valid_url(url_stripped):
            raise InvalidUrlException(url_stripped)

        return requests.get(
            (
                f"{self.URLBOX_BASE_API_URL}"
                f"{self.api_key}/{format}"
                f"?{urllib.parse.urlencode(options)}"
            )
        )

    # private
    def _parsed_url(self, url):
        return urllib.parse.quote(url)

    def _valid_url(self, url):
        return validators.url(url) == True
