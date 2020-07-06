"""
    test_pyincept.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    Unit test cases for the :py:mod:`pyincept.pyincept` module.

    ~~~~~~~~~~~~~~~~~~~~~~~

    Unpublished Copyright (c) 2020 Andrew van Herick. All Rights Reserved.
"""

__author__ = 'Andrew van Herick'

import os
import shutil
from datetime import datetime
from unittest import mock

from click.testing import CliRunner
from hamcrest import assert_that, contains_string

from pyincept import pyincept
from tests.pyincept_test_base import PyinceptTestBase


class TestPyincept(PyinceptTestBase):
    """
    Unit test for class :py:mod:`pyincept`.
    """

    ##############################
    # Class attributes

    # See superclass declaration to understand the use of this attribute.
    _OVERWRITE_EXPECTED_FILE = False

    _PACKAGE_NAME = 'some_package_name'
    _AUTHOR = 'some_author'
    _AUTHOR_EMAIL = 'some_author_email'

    # Something earlier than the current year.
    _DATE = datetime(1900, 1, 1)

    ##############################
    # Class / static methods

    @classmethod
    def _get_resource_path(cls, resource_name):
        return os.path.abspath(
            os.path.join(
                __file__,
                os.pardir,
                '_resources',
                'test_pyincept',
                resource_name
            )
        )

    ##############################
    # Instance methods

    # Instance set up / tear down

    @mock.patch('pyincept.pyincept.datetime')
    def setup(self, mock_datetime):
        """
        Called before each method in this class with a name of the form
        test_*().
        """
        mock_datetime.now.return_value = self._DATE

        # The project root directory should not already exist.  If it does,
        # something unexpected has happened, so raise.
        self._validate_path_doesnt_exist(self._PACKAGE_NAME)

        runner = CliRunner()
        self.result = runner.invoke(
            pyincept.main,
            (self._PACKAGE_NAME, self._AUTHOR, self._AUTHOR_EMAIL)
        )

    def teardown(self):
        """
        Called after each method in this class with a name of the form
        test_*().
        """
        if os.path.exists(self._PACKAGE_NAME):
            shutil.rmtree(self._PACKAGE_NAME)

        self._validate_path_doesnt_exist(self._PACKAGE_NAME)

    # Test cases

    def test_main_maps_project_root(self):
        """
        Unit test case for :py:method:`pyincept.main`.
        """
        dir_path = self._PACKAGE_NAME
        assert_that(
            os.path.isdir(dir_path),
            'Directory not found: {}'.format(dir_path)
        )

    def test_main_maps_package_name(self):
        """
        Unit test case for :py:method:`pyincept.main`.
        """
        dir_path = os.path.join(self._PACKAGE_NAME, 'setup.py')
        content = self._get_file_content(dir_path)
        substring = 'Package distribution file for the {} library.'.format(
            self._PACKAGE_NAME
        )
        assert_that(content, contains_string(substring))

    def test_main_maps_author_name(self):
        """
        Unit test case for :py:method:`pyincept.main`.
        """
        dir_path = os.path.join(self._PACKAGE_NAME, 'setup.py')
        content = self._get_file_content(dir_path)
        substring = "author='{}'".format(self._AUTHOR)
        assert_that(content, contains_string(substring))

    def test_main_maps_author_email(self):
        """
        Unit test case for :py:method:`pyincept.main`.
        """
        dir_path = os.path.join(self._PACKAGE_NAME, 'setup.py')
        content = self._get_file_content(dir_path)
        substring = "author_email='{}'".format(self._AUTHOR_EMAIL)
        assert_that(content, contains_string(substring))

    def test_main_maps_date(self):
        """
        Unit test case for :py:method:`pyincept.main`.
        """
        dir_path = os.path.join(self._PACKAGE_NAME, 'setup.py')
        content = self._get_file_content(dir_path)
        substring = 'Copyright (c) {}'.format(self._DATE.year)
        assert_that(content, contains_string(substring))
