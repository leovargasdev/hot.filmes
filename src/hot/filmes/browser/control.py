#!/opt/plone/zinstance/bin/python2.7
# -*- coding: utf-8 -*-
import os
import re
import sys
import base64
import time
import datetime
import transaction
from plone import api
from unicodedata import normalize
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.interface import Interface
from z3c.relationfield import RelationValue
from z3c.relationfield import Relation
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
from plone.protect.auto import safeWrite
from plone.protect import CheckAuthenticator
from plone.uuid.interfaces import IUUID
from Products.ZCatalog import interfaces
from Products.ZCatalog.interfaces import IZCatalog
from plone.supermodel import model
from zope import schema
from zope.component.interfaces import IObjectEvent
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent import ObjectAddedEvent
from Products.AdvancedQuery import Eq, Between, Le
from five import grok


@grok.subscribe(ObjectModifiedEvent)
@grok.subscribe(ObjectAddedEvent)
def modifiedObject(event):
	type_obj = ''
	try:
		obj = event.object
		type_obj = str(obj.portal_type)
	except Exception as e:
		return

	if ('ato_normativo' == type_obj):
		setValues_ato_normativo(obj)
	elif ('ato_normativo_pasta_setor' == type_obj):
		setValues_ato_normativo_pasta_setor(obj)
	elif ('organograma' == type_obj):
		setValues_organograma(obj)
	elif ('pessoa' == type_obj):
		setValues_pessoa(obj)
	elif ('apresentacao_dinamica' == type_obj):
		setValues_apresentacao_dinamica(obj)
	obj.reindexObject()
	obj.setSubject("blabla")
	return
