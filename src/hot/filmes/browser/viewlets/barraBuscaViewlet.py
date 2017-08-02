from plone import api
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class barraBuscaViewlet(ViewletBase):
	index = ViewPageTemplateFile('../templates/barraBusca_viewlet.pt')
