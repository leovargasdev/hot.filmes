#!/opt/plone/zinstance/bin/python2.7
# -*- coding: utf-8 -*-
import os
import sys
import base64
import time
import datetime
import transaction
from plone import api
from zope.interface import Interface
from z3c.relationfield import RelationValue
from Products.Five.browser import BrowserView
from plone.dexterity.browser.view import DefaultView
from plone.app.contentlisting.interfaces import IContentListing
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from OFS.interfaces import IOrderedContainer
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IFolderish
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from plone.app.relationfield.behavior import IRelatedItems
from Products.CMFPlone.utils import base_hasattr
from urlparse import urlparse
from datetime import datetime
from datetime import date
from transaction import commit
from plone.uuid.interfaces import IUUID

reload(sys)
sys.setdefaultencoding('utf8')

class filme(BrowserView):
	index = ViewPageTemplateFile("../templates/templateFilme.pt")

	def __call__(self):
		return self.index()

	def getSinopse(self):
		if not self.context.sinopse:
			return 'Não foi cadastrada sinopse para este filme'
		return self.context.sinopse
		
	def getData(self):
		return self.context.dataLancamento.date()

	def getHorario(self):
		return self.context.dataLancamento.time()
