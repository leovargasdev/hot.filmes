# import Image
from plone import api
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class logoViewlet(ViewletBase):
	index = ViewPageTemplateFile('../templates/logo.pt')

	def getPortal(self):
		return api.portal.get()

	def logo_title(self):
		return "Hot Filmes - Video Locadora"

	def logo_alt(self):
		return "Imagem logotipo do hot filmes"

	# def logo_img(self):
	# 	return Image.open(icon.png)
