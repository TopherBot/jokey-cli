import json
from unittest import mock

import pytest

from jokey.main import fetch_joke, format_joke, main


def test_format_joke():
    joke = {
        "setup": "Why did the chicken cross the road?",
        "punchline": "To get to the other side!",
    }
    assert format_joke(joke) == "Why did the chicken cross the road?\nTo get to the other side!"


@mock.patch("urllib.request.urlopen")
def test_fetch_joke_success(mock_urlopen):
    dummy_resp = mock.Mock()
    dummy_resp.__enter__.return_value = dummy_resp
    dummy_resp.status = 200
    dummy_resp.read.return_value = json.dumps({"setup": "a", "punchline": "b"}).encode()
    mock_urlopen.return_value = dummy_resp

    joke = fetch_joke()
    assert joke == {"setup": "a", "punchline": "b"}


@mock.patch("urllib.request.urlopen")
def test_fetch_joke_error(mock_urlopen):
    dummy_resp = mock.Mock()
    dummy_resp.__enter__.return_value = dummy_resp
    dummy_resp.status = 500
    dummy_resp.read.return_value = b"{}"
    mock_urlopen.return_value = dummy_resp

    with pytest.raises(RuntimeError) as excinfo:
        fetch_joke()
    assert "API returned 500" in str(excinfo.value)


def test_main_success(capsys):
    with mock.patch("jokey.main.fetch_joke", return_value={"setup": "s", "punchline": "p"}):
        exit_code = main()
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "s\np\n"


def test_main_failure(capsys):
    with mock.patch("jokey.main.fetch_joke", side_effect=Exception("boom")):
        exit_code = main()
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error: boom" in captured.err
