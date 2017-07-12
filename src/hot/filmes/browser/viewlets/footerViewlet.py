#!/opt/plone/zinstance/bin/python2.7
# -*- coding: utf-8 -*-
from plone import api
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class footerViewlet(ViewletBase):
    index = ViewPageTemplateFile('../templates/footer.pt')
