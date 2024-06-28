#!/usr/bin/env python3
"""
File manager class.
"""

import datetime
import logging
from collections import OrderedDict

from .data_wrapper import DataWrapper
from .exception import LoaderValueError  # pylint: disable=no-name-in-module
from .regex import PatternType, get_regex


LOGGER = logging.getLogger(__name__)


class Manager:
    """
    File manager for loading files on demand and managing memory.

    Attributes:
        loaders:
            An OrderedDict mapping argument regular expressions to loaders.
    """

    def __init__(self):
        self.loaders = OrderedDict()
        self._cache = {}

    def register_loader(
        self, pattern, loader, *, prioritize=False, pattern_type=PatternType.REGEX
    ):
        """
        Register a loader to handle a pattern.

        Args:
            pattern:
                A pattern that can be converted to a regular expression.

            loader:
                A subclass of the base loader.

            prioritize:
                If True, insert this regex at the start of the list of registred
                regexes, otherwise it will be inserted at the end.

            pattern_type:
                The pattern type, as an instance of PatternType.
        """
        regex = get_regex(pattern, pattern_type=pattern_type)
        LOGGER.debug("Registering loader %s with regex %s", loader, regex)
        self.loaders[regex] = loader
        if prioritize:
            self.loaders.move_to_end(regex, last=False)

    def get_loader(self, src):
        """
        Get the loader that matches the source.

        Args:
            src:
                The data source (e.g. a file or URI, or whatever else the
                matching loader can handle).

        Raises:
            ValueError:
                The given source is not matched by any registered regular
                expressions.
        """
        src = str(src)
        try:
            return self._cache[src].loader
        except KeyError:
            pass
        for regex, loader in self.loaders.items():
            if regex.fullmatch(src):
                return loader
        raise LoaderValueError(
            f'None of the registered regular expressions match the source "{src}": '
            "unable to find a corresponding data loader"
        )

    def clear_cache(
        self,
        pattern=None,
        age=None,
        by_access_time=False,
        pattern_type=PatternType.REGEX,
    ):
        """
        Clear cached data from memory.

        Args:
            pattern:
                A pattern that can be converted to a regular expression. If
                given, only cached items matching this regular expression will
                be cleared.

            pattern_type:
                The pattern type, as an instance of PatternType.

            age:
                An optional datetime.timedelta object (or a dict of keyword
                arguments that can be passed to datetime.timedelta(). If the
                data has been loaded for longer than this time, it will be
                cleared.

            by_access_time:
                If True, clear data by last access time when clearing by age,
                otherwise clear by load time.
        """
        if isinstance(age, dict):
            age = datetime.timedelta(**age)
        elif not (isinstance(age, datetime.timedelta) or age is None):
            raise ValueError(f"Invalid argument type for age: {type(age)}")

        time_attr = "access_time" if by_access_time else "load_time"

        if pattern is None:
            if age is None:
                self._cache.clear()
            else:
                now = datetime.datetime.now(datetime.UTC)
                for src, item in list(self._cache.items()):
                    if (now - getattr(item, time_attr)) > age:
                        del self._cache[src]
            return

        regex = get_regex(pattern, pattern_type=pattern_type)
        for src, item in list(self._cache.items()):
            if regex.fullmatch(src):
                if age is None or (now - getattr(item, time_attr)) > age:
                    del self._cache[src]

    def refresh(self, pattern=None, pattern_type=PatternType.REGEX):
        """
        Refresh data for which the loader reports a source modification since
        the time the data was loaded.

        Args:
            pattern:
                A pattern that can be converted to a regular expression. If
                given, only cached items matching this regular expression will
                be cleared.

            pattern_type:
                The pattern type, as an instance of PatternType.
        """
        wrappers = self._cache.values()
        if pattern is not None:
            regex = get_regex(pattern, pattern_type=pattern_type)
            wrappers = (
                wrapper for wrapper in wrappers if regex.fullmatch(str(wrapper.src))
            )
        for wrapper in wrappers:
            wrapper.refresh()

    def _get_wrapper(self, src):
        """
        Get the wrapper for the given source.

        Args:
            src:
                The data source.

        Returns:
            The wrapper for this source.
        """
        str_src = str(src)
        try:
            wrapper = self._cache[str_src]
        except KeyError:
            LOGGER.debug("%s is not in cache.", str_src)
            loader = self.get_loader(src)
            wrapper = DataWrapper(loader, src)
            self._cache[str(src)] = wrapper
            return wrapper
        LOGGER.debug("Found %s in cache.", str_src)
        return wrapper

    def get(self, src, refresh=False, reload=False):
        """
        Get the data from the given source. The data will be loaded via the
        loader if necessary.

        Args:
            src:
                The data source.

            refresh:
                If True, reload data if the reported modification time is newer
                than the loaded data.

            reload:
                If True, force a reload.

        Returns:
            The data.
        """
        wrapper = self._get_wrapper(src)
        if reload:
            LOGGER.debug("Forcing reload of %s.", src)
            wrapper.load()
        elif refresh:
            wrapper.refresh()
        return wrapper.access()

    def get_mtime(self, src):
        """
        Get the modification time of a source.

        Args:
            src:
                The data source.

        Returns:
            The modification time as a datetime.datetime object, or None.
        """
        str_src = str(src)
        try:
            loader = self._cache[str_src].loader
        except KeyError:
            loader = self.get_loader(src)
        return loader.get_mtime(src)

    def __iter__(self):
        """
        Iterator over cached sources.
        """
        yield from self._cache.keys()
