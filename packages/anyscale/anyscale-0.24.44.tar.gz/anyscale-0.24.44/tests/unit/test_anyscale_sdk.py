import click
import pytest

from anyscale.shared_anyscale_utils.headers import RequestHeaders
from frontend.cli.anyscale.__init__ import _validate_headers


@pytest.mark.parametrize(
    ("headers", "raise_exception"),
    [
        ({RequestHeaders.SOURCE: "astronomy-sdk"}, False),
        ({RequestHeaders.SOURCE: 1}, True),
    ],
)
def test_validate_api_client_headers(headers, raise_exception) -> None:
    """
    Test headers are validated correctly.
    """
    if raise_exception:
        with pytest.raises(click.ClickException):
            _validate_headers(headers=headers)

    else:
        _validate_headers(headers=headers)
