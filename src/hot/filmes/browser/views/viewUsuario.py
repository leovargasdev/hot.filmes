#!/opt/plone/zinstance/bin/python2.7
# -*- coding: utf-8 -*-
import os
import sys
from plone import api
from operator import itemgetter
from zope.interface import Interface
from Products.Five.browser import BrowserView
from plone.dexterity.browser.view import DefaultView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

reload(sys)
sys.setdefaultencoding('utf8')

class usuario(BrowserView):
	index = ViewPageTemplateFile("../templates/templateUsuario.pt")

	def __call__(self):
		return self.index()

	def getNome(self):
		if not self.context.description: #caso não tenha preenchido o campo sobrenome
			return self.context.title
		return self.context.title + " " + self.context.description

	def getFilmesFavoritos(self):
		filmes = self.context.filmesFavoritos
		result = []
		for i in filmes:
			result.append(i.to_object.title)
		if not result:
			result.append('Não tem nenhum filme como favorito')
		return result

	def getCPF(self):
		cpf = self.context.cpf
		return (cpf[0:3] + "." + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:11])

	def getSexo(self):
		s = self.context.sexo
		if s == 'f':
			return "Feminino"
		elif s == 'm':
			return "Masculino"
		else:
			return "Indefinido"

	def getEndereco(self):
		# results = ["bla", "blu", "blo"]
		results = []
		localizacoes = api.content.find(portal_type='localizacao')
		for loc in localizacoes:
			if(self.context.endereco == loc.getObject().title):
				results.append({'pais': loc.getObject().title, 'cidade': loc.getObject().cidade, 'sigla': loc.getObject().sigla})
		return results

	def getEnderecoALL(self):
		# results = ["bla", "blu", "blo"]
		results = []
		localizacoes = api.content.find(portal_type='localizacao')
		for loc in localizacoes:
			# results.append(loc.getObject().title)
			results.append({'pais': loc.getObject().title, 'cidade': loc.getObject().cidade, 'sigla': loc.getObject().sigla})
		return results
