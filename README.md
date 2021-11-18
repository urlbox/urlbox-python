# UrlBox Python Library

The UrlBox Python library provides convenient access to the [UrlBox API](https://urlbox.io/) from your Python application.


## Documentation

See the [UrlBox API Docs](https://urlbox.io/docs/overview).

## Requirements

Python 3.x

## Installation

```pip install urlbox```


## Usage

First, grab your UrlBox API key (*and your API secret if you want to make authenticated requests*) found in your [UrlBox Dashboard](https://urlbox.io/dashboard/api) to initialise the UrlBoxClient instance.

```python

from urlbox import UrlBoxClient


urlbox_client = UrlBoxClient(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET") # YOUR_API_SECRET is optional

format = "png"  # can be either: png, jpg or jpeg, avif, webp ,pdf, svg, html
options = {"url": "http://example.com/", "full_page": True, "width": 300}
# See all available options here: https://urlbox.io/docs/options

# TODO: Break out the url from the options? That's different to the API, but makes sense as it's a different type of parameter.
response = urlbox_client.get(format=format, options=options)

# The urlbox API will return binary data as the response
# with the Content-Type header set to the relevant mime-type for the format requested.
# For example, if you requested png format, the Content-Type will be image/png
# and response body will be the actual PNG binary data.

# TODO: show processing the response

# TODO: Include further endpoints (head, post, etc), polling and webhook functionality.

# Authenticated requests JUST WORK when you supply YOUR_API_SECRET
# All requests will be authenticated when you supply YOUR_API_SECRET, unless you override: authenticated_request=False
```



## Feedback


Feel free to contact us if you have spot a bug or have any suggestion at chris`[at]`urlbox.com.