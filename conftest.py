from pytest_socket import disable_socket

# hooks
def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    disable_socket()  # prevent any real http requests being made by the API
