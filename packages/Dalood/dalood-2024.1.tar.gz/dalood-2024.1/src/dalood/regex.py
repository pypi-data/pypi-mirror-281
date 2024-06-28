#!/usr/bin/env python3
"""
Regular expression types and functions.
"""

import enum
import fnmatch
import logging
import re


LOGGER = logging.getLogger(__name__)


@enum.unique
class PatternType(enum.Enum):
    """
    Recognized pattern types.
    """

    REGEX = enum.auto()
    GLOB = enum.auto()
    LITERAL = enum.auto()

    @classmethod
    def from_str(cls, arg):
        """
        Convert a string to a PatternType.
        """
        arg = str(arg).upper()
        for ptype in cls:
            if ptype.name == arg:
                return ptype
        raise ValueError(f"Unrecognized pattern type: {arg}")


def get_regex(pattern, pattern_type=PatternType.REGEX):
    """
    Get the regular expression corresponding to the given pattern.

    Args:
        pattern:
            A string containing a pattern of the specified type that should be
            converted to a regular expression.

        pattern_type:
            An instance of PatternType or an equivalent string.

    Returns:
        An re.Pattern regular expression object.
    """
    if isinstance(pattern, re.Pattern):
        LOGGER.debug("Ignoring pattern type for pre-compiled re.Pattern")
        return pattern

    if isinstance(pattern_type, str):
        pattern_type = PatternType.from_str(pattern_type)

    if pattern_type is PatternType.LITERAL:
        regex = re.escape(pattern)
    elif pattern_type is PatternType.GLOB:
        regex = fnmatch.translate(pattern)
    elif pattern_type is PatternType.REGEX:
        regex = pattern
    else:
        raise ValueError(f"Unrecogznied pattern type: {pattern_type}")

    return re.compile(regex)


def get_extension_pattern_for_filepath(ext, escape=True):
    r"""
    Get a regular expression pattern for filepaths that end with the given
    extension. This will exclude URIs, including file URIs.

    Args:
        ext:
            The extention to recognize, e.g. ".txt".

        escape:
            If True, escape the extension for the pattern. This can be set to
            false whena pre-escaped pattern is passed in, e.g. r"\.[tc]sv".

    Returns:
        A 2-tuple with the pattern and pattern type.
    """
    if escape:
        ext = re.escape(ext)
    pattern = rf"^(?!\w+://).*{ext}$"
    return pattern, PatternType.REGEX
