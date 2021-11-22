from faker import Faker
from hashlib import sha1
from urlbox import InvalidUrlException, UrlboxClient
import hmac
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
    url = fake.url()

    options = {
        "url": url,
        "format": format,
        "full_page": random.choice([True, False]),
        "width": fake.random_int(),
    }

    urlbox_request_url = (
        f"{UrlboxClient.BASE_API_URL}"
        f"{api_key}/{format}"
        f"?{urllib.parse.urlencode(options)}"
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

            response = urlbox_client.get(options)

            assert response.status_code == 200
            assert format in response.headers["Content-Type"]
            assert isinstance(response, requests.models.Response)
            assert isinstance(response.content, bytes)


# providing just the api_key
def test_get_successful_as_str():
    api_key = fake.pystr()

    format = random.choice(
        ["png", "jpg", "jpeg", "avif", "webp", "pdf", "svg", "html"]
    )
    url = fake.url()

    options = {
        "url": url,
        "format": format,
        "full_page": random.choice([True, False]),
        "width": fake.random_int(),
    }

    urlbox_client = UrlboxClient(api_key=api_key)

    response = urlbox_client.get(options, to_string=True)

    assert isinstance(response, str)


def test_get_successful_as_str_with_api_secret():
    api_key = fake.pystr()
    api_secret = fake.pystr()

    format = random.choice(
        ["png", "jpg", "jpeg", "avif", "webp", "pdf", "svg", "html"]
    )
    url = fake.url()

    options = {
        "url": url,
        "format": format,
        "full_page": random.choice([True, False]),
        "width": fake.random_int(),
    }

    urlbox_client = UrlboxClient(api_key=api_key, api_secret=api_secret)

    response = urlbox_client.get(options, to_string=True)

    assert isinstance(response, str)
    # It still returns the unautenticated get url
    assert api_secret not in response


# valid url but with white spaces before and after
def test_get_successful_white_space_url():
    api_key = fake.pystr()

    format = random.choice(
        ["png", "jpg", "jpeg", "avif", "webp", "pdf", "svg", "html"]
    )

    url = fake.url()
    url_with_white_spaces = f"  {url}   "

    options = {
        "url": url_with_white_spaces,
        "format": format,
        "full_page": random.choice([True, False]),
        "width": fake.random_int(),
    }

    options_parsed = options.copy()
    options_parsed["url"] = url

    urlbox_request_url = (
        f"{UrlboxClient.BASE_API_URL}"
        f"{api_key}/{format}"
        f"?{urllib.parse.urlencode(options_parsed)}"
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

            response = urlbox_client.get(options)

            assert response.status_code == 200
            assert format in response.headers["Content-Type"]
            assert isinstance(response, requests.models.Response)
            assert isinstance(response.content, bytes)


def test_get_successful_missing_schema_url():
    api_key = fake.pystr()

    format = random.choice(
        ["png", "jpg", "jpeg", "avif", "webp", "pdf", "svg", "html"]
    )

    url_original = "twitter.com"
    url_with_schema = f"http://{url_original}"

    options = {
        "url": url_original,
        "format": format,
        "full_page": random.choice([True, False]),
        "width": fake.random_int(),
    }

    options_parsed = options.copy()
    options_parsed["url"] = url_with_schema

    urlbox_request_url = (
        f"{UrlboxClient.BASE_API_URL}"
        f"{api_key}/{format}"
        f"?{urllib.parse.urlencode(options_parsed)}"
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

            response = urlbox_client.get(options)

            assert response.status_code == 200
            assert format in response.headers["Content-Type"]
            assert isinstance(response, requests.models.Response)
            assert isinstance(response.content, bytes)


def test_get_invalid_url():
    format = random.choice(
        ["png", "jpg", "jpeg", "avif", "webp", "pdf", "svg", "html"]
    )
    url = fake.address()

    options = {
        "url": url,
        "format": format,
        "full_page": random.choice([True, False]),
        "width": fake.random_int(),
    }

    urlbox_client = UrlboxClient(api_key=fake.pystr())

    with pytest.raises(InvalidUrlException) as invalid_url_exception:
        urlbox_client.get(options)

    assert url in str(invalid_url_exception.value)


def test_get_with_different_host_name():
    api_host_name = random.choice(["api-eu.urlbox.io", "api-direct.urlbox.io"])
    api_key = fake.pystr()

    format = random.choice(
        ["png", "jpg", "jpeg", "avif", "webp", "pdf", "svg", "html"]
    )
    url = fake.url()

    options = {
        "url": url,
        "format": format,
        "full_page": random.choice([True, False]),
        "width": fake.random_int(),
    }

    urlbox_request_url = (
        f"https://{api_host_name}/"
        f"{api_key}/{format}"
        f"?{urllib.parse.urlencode(options)}"
    )

    urlbox_client = UrlboxClient(api_key=api_key, api_host_name=api_host_name)

    with requests_mock.Mocker() as requests_mocker:
        with open(
            "tests/files/urlbox_screenshot.png", "rb"
        ) as urlbox_screenshot:
            requests_mocker.get(
                urlbox_request_url,
                content=urlbox_screenshot.read(),
                headers={"content-type": f"image/{format}"},
            )

            response = urlbox_client.get(options)

            assert response.status_code == 200
            assert format in response.headers["Content-Type"]
            assert isinstance(response, requests.models.Response)
            assert isinstance(response.content, bytes)


def test_head_request():
    api_key = fake.pystr()

    format = random.choice(
        ["png", "jpg", "jpeg", "avif", "webp", "pdf", "svg", "html"]
    )
    url = fake.url()

    options = {
        "url": url,
        "format": format,
        "full_page": random.choice([True, False]),
        "width": fake.random_int(),
    }

    urlbox_request_url = (
        f"{UrlboxClient.BASE_API_URL}"
        f"{api_key}/{format}"
        f"?{urllib.parse.urlencode(options)}"
    )

    urlbox_client = UrlboxClient(api_key=api_key)

    with requests_mock.Mocker() as requests_mocker:
        requests_mocker.head(
            urlbox_request_url,
            content=b"",
            headers={"content-type": f"image/{format}"},
        )

        response = urlbox_client.head(options)

        assert response.status_code == 200
        assert format in response.headers["Content-Type"]
        assert isinstance(response, requests.models.Response)
        assert isinstance(response.content, bytes)
        assert len(response.content) == 0

