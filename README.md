# UrlBox Python Library

The UrlBox Python library provides convenient access to the <a href="https://urlbox.io/" target="_blank">UrlBox API</a> from your Python application.


## Documentation

See the <a href=https://urlbox.io/docs/overview target="_blank">UrlBox API Docs</a>.

## Requirements

Python 3.x

## Installation

```pip install urlbox```


## Usage

First, grab your UrlBox API key* found in your <a  href="https://urlbox.io/dashboard/api" target="_blank">UrlBox Dashboard</a>, used to initialise the UrlBoxClient instance.

*\* and grab your API secret - if you want to make authenticated requests.*

```python

from urlbox import UrlBoxClient

# Initialise the UrlBoxClient (YOUR_API_SECRET is optional)
urlbox_client = UrlBoxClient(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")

format = "png"  # can be either: png, jpg or jpeg, avif, webp ,pdf, svg, html

# See all available options here: https://urlbox.io/docs/options
options = {"url": "http://example.com/", "full_page": True, "width": 300}

# TODO: Break out the url from the options? That's different to the API,
# but makes sense as it's a different type of parameter.
# eg: response = urlbox_client.get(url, format=format, options=options)
response = urlbox_client.get(format=format, options=options)

# The urlbox API will return binary data as the response with the
# Content-Type header set to the relevant mime-type for the format requested.
# For example, if you requested png format, the Content-Type will be image/png
# and response body will be the actual PNG binary data.

# TODO: show processing the response

# TODO: Include further endpoints (head, post, etc), polling and webhook functionality.

# Authenticated requests JUST WORK when you supply YOUR_API_SECRET
# All requests will be authenticated when you supply YOUR_API_SECRET,
# unless you override: authenticated_request=False
```



## Feedback


Feel free to contact us if you have spot a bug or have any suggestion at chris`[at]`urlbox.com.
