import unittest

from pelican import signals
from pelican.tests.support import get_settings

from minchin.pelican.readers import commonmark


class TestMarkdownTakeover(unittest.TestCase):
    """Test taking over the extensions"""

    def setUp(self) -> None:
        self.settings = get_settings()

    def test_register(self):
        self.assertFalse(signals.readers_init.has_receivers_for("md"))
        commonmark.register()
        self.assertTrue(signals.readers_init.has_receivers_for("md"))
