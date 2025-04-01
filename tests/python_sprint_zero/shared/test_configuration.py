import os
from unittest.mock import patch, mock_open

import pytest
from assertpy import assert_that

from python_sprint_zero.shared.configuration import (
    ApplicationSettings,
    ApplicationSettingProvider,
    load_properties_file,
)


class TestLoadPropertiesFile:
    def test_should_load_properties_from_file(self):
        mock_file_content = "admin=testadmin\npassword=testpassword\n"

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = load_properties_file("dummy/path")

        assert_that(result).contains_entry({"admin": "testadmin"})

    def test_should_handle_empty_lines(self):
        mock_file_content = "admin=testadmin\n\npassword=testpassword\n"

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = load_properties_file("dummy/path")

        assert_that(result).is_length(2)

    def test_should_handle_comment_lines(self):
        mock_file_content = "admin=testadmin\n#comment line\npassword=testpassword\n"

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = load_properties_file("dummy/path")

        assert_that(result).is_length(2)


class TestApplicationSettings:
    @patch("python_sprint_zero.shared.configuration.get_resource_path")
    @patch("python_sprint_zero.shared.configuration.load_properties_file")
    def test_should_load_settings_from_properties_file(self, mock_load_properties, mock_get_resource_path):
        mock_get_resource_path.return_value = "dummy/path"
        mock_load_properties.return_value = {"admin": "coconuts", "password": "bunch"}

        with patch.dict(os.environ, {}, clear=True):
            settings = ApplicationSettings()

        assert_that(settings.admin).is_equal_to("coconuts")

    @patch("python_sprint_zero.shared.configuration.get_resource_path")
    @patch("python_sprint_zero.shared.configuration.load_properties_file")
    def test_should_use_environment_variables_over_properties(self, mock_load_properties, mock_get_resource_path):
        mock_get_resource_path.return_value = "dummy/path"
        mock_load_properties.return_value = {"admin": "coconuts", "password": "bunch"}

        with patch.dict(os.environ, {"APP_ADMIN": "envadmin"}, clear=True):
            settings = ApplicationSettings()

        assert_that(settings.admin).is_equal_to("envadmin")

    @patch("python_sprint_zero.shared.configuration.get_resource_path")
    def test_should_handle_missing_properties_file(self, mock_get_resource_path):
        mock_get_resource_path.side_effect = FileNotFoundError

        settings = ApplicationSettings()

        assert_that(settings.admin).is_equal_to("admin")


class TestApplicationSettingProvider:
    def test_should_get_setting_value(self):
        provider = ApplicationSettingProvider()

        result = provider.get("admin")

        assert_that(result).is_not_none()

    def test_should_allow_setting_override(self):
        provider = ApplicationSettingProvider()
        provider.override("admin", "overridden")

        result = provider.get("admin")

        assert_that(result).is_equal_to("overridden")

    def test_should_raise_error_for_nonexistent_setting(self):
        provider = ApplicationSettingProvider()

        with pytest.raises(ValueError) as excinfo:
            provider.get("nonexistent")

        assert_that(str(excinfo.value)).contains("not found")
