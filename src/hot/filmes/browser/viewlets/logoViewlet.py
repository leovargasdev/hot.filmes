from plone import api
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class logoViewlet(ViewletBase):
	index = ViewPageTemplateFile('../templates/logo.pt')

	def getPortal(self):
		return api.portal.get()
