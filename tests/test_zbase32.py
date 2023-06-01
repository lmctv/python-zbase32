"""
Tests for :mod:`zbase32`.
"""

import hypothesis
import hypothesis.strategies
import pytest

import zbase32


@pytest.mark.parametrize(
    ["decoded", "encoded"],
    [
        (b"asdasd", "cf3seamuco"),
        (b"\xF0\xBF\xC7", "6n9hq"),
        (b"\xD4\x7A\x04", "4t7ye"),
        (b"\xff", "9h"),
        (b"\xb5", "sw"),
        (b"\x34\x5a", "gtpy"),
        (b"\xff\xff\xff\xff\xff", "99999999"),
        (b"\xff\xff\xff\xff\xff\xff", "999999999h"),
        (
            b"\xc0\x73\x62\x4a\xaf\x39\x78\x51\x4e\xf8\x44\x3b\xb2\xa8\x59"
            b"\xc7\x5f\xc3\xcc\x6a\xf2\x6d\x5a\xaa",
            "ab3sr1ix8fhfnuzaeo75fkn3a7xh8udk6jsiiko",
        ),
    ],
)
def test_it_should_support_encoding_and_decoding(decoded: bytes, encoded: str) -> None:
    """
    it should support encoding and decoding.
    """
    assert zbase32.encode(decoded) == encoded
    assert zbase32.decode(encoded) == decoded


def test_it_should_error_on_invalid_zbase32_strings() -> None:
    """
    it should error on invalid zbase32 strings.
    """
    with pytest.raises(zbase32.DecodeError):
        zbase32.decode("bar#")
    with pytest.raises(zbase32.DecodeError):
        zbase32.decode_rspamd("bar#")


@hypothesis.given(value=hypothesis.strategies.binary())
def test_it_should_be_able_to_decode_encoded_values(value: bytes) -> None:
    """
    it should be able to decode encoded values.
    """
    assert zbase32.decode(zbase32.encode(value)) == value


@pytest.mark.parametrize(
    ["decoded", "encoded"],
    [
        (b"test123", "wm3g84fg13cy"),
        (b"TEST123", "wktgfkfg13cy"),
        (b"hello", "em3ags7p"),
        (b"HELLO", "ektarg7j"),
        (b"!HELLO~", "bb1krgtjx19y"),
        (b"~hello!", "6d4kgstpxmey"),
        (b"\x00\x00\x00\x00\x00", "yyyyyyyy"),  # 0b00000
        (b"!\x84\x10B\x08", "bbbbbbbb"),  # 0b00001
        (b"B\x08!\x84\x10", "nnnnnnnn"),  # 0b00010
        (b"\x84\x10B\x08!", "rrrrrrrr"),  # 0b00100
        (b"\x08!\x84\x10B", "eeeeeeee"),  # 0b01000
        (b"\x10B\x08!\x84", "oooooooo"),  # 0b10000
        (b"\xB5\xD6Zk\xAD", "iiiiiiii"),  # 0b10101
        (b"J)\xA5\x94R", "kkkkkkkk"),  # 0b01010
        (b"\xFF\xFF\xFF\xFF\xFF", "99999999"),  # 0b11111
    ],
)
def test_should_support_rspamd_encoding_and_decoding(
    decoded: bytes, encoded: str
) -> None:
    """
    it should support encoding and decoding conforming to rspamd variant.
    """
    assert zbase32.encode_rspamd(decoded) == encoded
    assert zbase32.decode_rspamd(encoded) == decoded


@hypothesis.given(value=hypothesis.strategies.binary())
def test_it_should_be_able_to_decode_rspamd_encoded_values(value: bytes) -> None:
    """
    it should be able to decode values encoded according to rspamd variant.
    """
    assert zbase32.decode_rspamd(zbase32.encode_rspamd(value)) == value
