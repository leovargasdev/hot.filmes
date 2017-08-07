from plone import api
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class homeViewlet(ViewletBase):
	index = ViewPageTemplateFile('../templates/home_viewlet.pt')
