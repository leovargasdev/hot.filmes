from plone import api
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class footerViewlet(ViewletBase):
	index = ViewPageTemplateFile('../templates/footer_viewlet.pt')
