class UrlboxClient:

    """
        The core client object used to interact with the Urlbox API

        :param api_key: Your API key found in your Urlbox Dashboard
        `https://urlbox.io/dashboard/api`

        :param api_secret: (Optional) Your API secret found in your Urlbox
        Dashboard`https://urlbox.io/dashboard/api`
        Required for authenticated requests.
    """

    def __init__(self, *, api_key, api_secret=None):
        self.api_key = api_key
        self.api_secret = api_secret

    def get():
        pass
