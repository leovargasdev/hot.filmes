# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from hot.filmes.testing import HOT_FILMES_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that hot.filmes is properly installed."""

    layer = HOT_FILMES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if hot.filmes is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'hot.filmes'))

    def test_browserlayer(self):
        """Test that IHotFilmesLayer is registered."""
        from hot.filmes.interfaces import (
            IHotFilmesLayer)
        from plone.browserlayer import utils
        self.assertIn(IHotFilmesLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = HOT_FILMES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['hot.filmes'])

    def test_product_uninstalled(self):
        """Test if hot.filmes is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'hot.filmes'))

    def test_browserlayer_removed(self):
        """Test that IHotFilmesLayer is removed."""
        from hot.filmes.interfaces import \
            IHotFilmesLayer
        from plone.browserlayer import utils
        self.assertNotIn(IHotFilmesLayer, utils.registered_layers())
