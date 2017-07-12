# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import hot.filmes


class HotFilmesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=hot.filmes)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'hot.filmes:default')


HOT_FILMES_FIXTURE = HotFilmesLayer()


HOT_FILMES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(HOT_FILMES_FIXTURE,),
    name='HotFilmesLayer:IntegrationTesting'
)


HOT_FILMES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(HOT_FILMES_FIXTURE,),
    name='HotFilmesLayer:FunctionalTesting'
)


HOT_FILMES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        HOT_FILMES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='HotFilmesLayer:AcceptanceTesting'
)
