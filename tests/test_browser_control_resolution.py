import unittest
from pathlib import Path
from unittest.mock import patch

import actions.browser_control as bc
import core.user_paths as user_paths


class BrowserResolutionTests(unittest.TestCase):
    def test_windows_chrome_uses_registry_lookup_even_when_channel_is_set(self):
        with patch.object(bc, "_OS", "Windows"), patch.object(bc, "_find_exe_windows", return_value="C:/Program Files/Google/Chrome/Application/chrome.exe"):
            resolved = bc._resolve_browser("chrome")
            self.assertEqual(resolved["exe"], "C:/Program Files/Google/Chrome/Application/chrome.exe")

    def test_windows_edge_uses_registry_lookup_even_when_channel_is_set(self):
        with patch.object(bc, "_OS", "Windows"), patch.object(bc, "_find_exe_windows", return_value="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"):
            resolved = bc._resolve_browser("edge")
            self.assertEqual(resolved["exe"], "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")

    def test_windows_uses_real_desktop_from_user_shell_folders(self):
        user_paths._lookup.cache_clear()
        with patch.object(user_paths, "_OS", "Windows"), \
             patch.object(user_paths.os.path, "expandvars", side_effect=lambda p: p.replace("%USERPROFILE%", "C:/Users/test")), \
             patch.object(user_paths.Path, "home", return_value=Path("C:/Users/test")):
            with patch("winreg.OpenKey") as open_key, patch("winreg.QueryValueEx", return_value=(r"%USERPROFILE%\OneDrive\Desktop", "")):
                self.assertEqual(user_paths.desktop(), Path("C:/Users/test/OneDrive/Desktop"))
        user_paths._lookup.cache_clear()


if __name__ == "__main__":
    unittest.main()
