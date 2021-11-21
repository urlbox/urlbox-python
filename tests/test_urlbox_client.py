from faker import Faker
from urlbox import InvalidUrlException, UrlboxClient
import pytest
import random
import requests
import requests_mock
import urllib.parse


fake = Faker()

# test_init()
def test_only_api_key_provided():
    api_key = fake.pystr()
    urlbox_client = UrlboxClient(api_key=api_key)

    assert urlbox_client.api_key == api_key


def test_both_api_key_and_api_secret_provided():
    api_key = fake.pystr()
    api_secret = fake.pystr()
    urlbox_client = UrlboxClient(api_key=api_key, api_secret=api_secret)

    assert (
        urlbox_client.api_key == api_key
        and urlbox_client.api_secret == api_secret
    )


def test_api_key_not_provided():
    with pytest.raises(TypeError) as type_error:
        UrlboxClient()

    assert (
        str(type_error.value)
        == "__init__() missing 1 required keyword-only argument: 'api_key'"
    )


# Test get()
# valid api key
# valid url, format and options
def test_get_successful():
    api_key = fake.pystr()

    format = random.choice(
        ["png", "jpg", "jpeg", "avif", "webp", "pdf", "svg", "html"]
    )
    options = {
        "full_page": random.choice([True, False]),
        "width": fake.random_int(),
    }
    url = fake.url()

    urlbox_request_url = (
        f"{UrlboxClient.URLBOX_BASE_API_URL}"
        f"{api_key}/{format}"
        f"?url={urllib.parse.quote(url)}"
        f"&{urllib.parse.urlencode(options)}"
    )

    urlbox_client = UrlboxClient(api_key=api_key)

    with requests_mock.Mocker() as requests_mocker:
        with open(
            "tests/files/urlbox_screenshot.png", "rb"
        ) as urlbox_screenshot:
            requests_mocker.get(
                urlbox_request_url,
                content=urlbox_screenshot.read(),
                headers={"content-type": f"image/{format}"},
            )

            response = urlbox_client.get(url, format=format, options=options)

            assert response.status_code == 200
            assert format in response.headers["Content-Type"]
            assert isinstance(response, requests.models.Response)
            assert isinstance(response.content, bytes)


# valid url but with white spaces before and after
def test_get_successful():
    api_key = fake.pystr()

    format = random.choice(
        ["png", "jpg", "jpeg", "avif", "webp", "pdf", "svg", "html"]
    )
    options = {
        "full_page": random.choice([True, False]),
        "width": fake.random_int(),
    }
    url = fake.url()
    url_with_white_spaces = f"  {url}   "

    print("!!! - url ", url)

    urlbox_request_url = (
        f"{UrlboxClient.URLBOX_BASE_API_URL}"
        f"{api_key}/{format}"
        f"?url={urllib.parse.quote(url)}"
        f"&{urllib.parse.urlencode(options)}"
    )

    urlbox_client = UrlboxClient(api_key=api_key)

    with requests_mock.Mocker() as requests_mocker:
        with open(
            "tests/files/urlbox_screenshot.png", "rb"
        ) as urlbox_screenshot:
            requests_mocker.get(
                urlbox_request_url,
                content=urlbox_screenshot.read(),
                headers={"content-type": f"image/{format}"},
            )

            response = urlbox_client.get(
                url_with_white_spaces, format=format, options=options
            )

            assert response.status_code == 200
            assert format in response.headers["Content-Type"]
            assert isinstance(response, requests.models.Response)
            assert isinstance(response.content, bytes)


def test_get_invalid_url():
    api_key = fake.pystr()

    format = random.choice(
        ["png", "jpg", "jpeg", "avif", "webp", "pdf", "svg", "html"]
    )
    options = {
        "full_page": random.choice([True, False]),
        "width": fake.random_int(),
    }
    url = fake.address()

    urlbox_client = UrlboxClient(api_key=api_key)

    with pytest.raises(InvalidUrlException) as invalid_url_exception:
        urlbox_client.get(url, format=format, options=options)

    assert url in str(invalid_url_exception.value)


# TODO:
# Test invalid API key
# Test with api_secret - authenticated request
