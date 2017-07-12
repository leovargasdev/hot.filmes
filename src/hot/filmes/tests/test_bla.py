# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from hot.filmes.interfaces import Ibla
from hot.filmes.testing import HOT_FILMES_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class blaIntegrationTest(unittest.TestCase):

    layer = HOT_FILMES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='bla')
        schema = fti.lookupSchema()
        self.assertEqual(Ibla, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='bla')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='bla')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(Ibla.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='bla',
            id='bla',
        )
        self.assertTrue(Ibla.providedBy(obj))
