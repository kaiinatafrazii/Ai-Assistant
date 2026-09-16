import unittest
from unittest.mock import patch

import actions.browser_control as bc


class BrowserResolutionTests(unittest.TestCase):
    def test_windows_chrome_uses_registry_lookup_even_when_channel_is_set(self):
        with patch.object(bc, "_OS", "Windows"), patch.object(bc, "_find_exe_windows", return_value="C:/Program Files/Google/Chrome/Application/chrome.exe"):
            resolved = bc._resolve_browser("chrome")
            self.assertEqual(resolved["exe"], "C:/Program Files/Google/Chrome/Application/chrome.exe")

    def test_windows_edge_uses_registry_lookup_even_when_channel_is_set(self):
        with patch.object(bc, "_OS", "Windows"), patch.object(bc, "_find_exe_windows", return_value="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"):
            resolved = bc._resolve_browser("edge")
            self.assertEqual(resolved["exe"], "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")


if __name__ == "__main__":
    unittest.main()
