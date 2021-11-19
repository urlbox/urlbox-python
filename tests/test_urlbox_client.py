from faker import Faker
from urlbox import UrlboxClient
import pytest

fake = Faker()

# Fixtures
@pytest.fixture
def api_key():
    return fake.pystr()


@pytest.fixture
def api_secret():
    return fake.pystr()


# Tests
# test_init()


def test_only_api_key_provided():
    urlbox_client = UrlboxClient(api_key=api_key)

    assert urlbox_client.api_key == api_key


def test_both_api_key_and_api_secret_provided():
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
