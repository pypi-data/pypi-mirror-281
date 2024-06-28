from __future__ import annotations

import pytest

from typing import Optional

from remotecall.endpoint import Endpoint
from remotecall.codecs import Codec, Codecs
from remotecall.codecs import APPLICATION_INT
from remotecall.codecs import APPLICATION_FLOAT


@pytest.fixture
def endpoint():
    def foo(a: int, b: float = 1.0) -> bool:
        """Foo"""
        return True

    return Endpoint("foo", foo)


def test_setup(endpoint):
    codecs = Codecs(Codec.subclasses)
    endpoint.setup(codecs)

    endpoint.parameters["a"].get_codec_by_content_type(APPLICATION_INT)
    endpoint.parameters["b"].get_codec_by_content_type(APPLICATION_FLOAT)

    with pytest.raises(ValueError):
        endpoint.parameters["a"].get_codec_by_content_type(APPLICATION_FLOAT)


def test_doc(endpoint):
    assert endpoint.doc == "Foo", "Expecting 'Foo'."
