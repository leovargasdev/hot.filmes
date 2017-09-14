#!/opt/plone/zinstance/bin/python2.7
# -*- coding: utf-8 -*-
from five import grok
from zope.app.content import queryContentType
from zope.schema import getFieldsInOrder
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

"""
	Usado para o tipo: apresentacao_dinamica
	Este python retorna elements para um tipo descrito em xml (objeto do plone)
	Modo de chamada (no xml): 
		# <source>uffs.site.browser.xml_elements.vocabularyDynamic</source>
"""

GLOBAL_NIVEL = 10

@grok.provider(IContextSourceBinder)
def vocabularyDynamic(context):
	terms = []
	"""
	DESCRIÇÃO:
		Atribui os termos criados no xml (ex: <element> term </element>)
		Os termos são os campos do objeto selecionado para apresentação

	MELHORIA:
		Apresentar termos com o valor do "title" (xml) de cada campo.

	"""

	if(str(context.portal_type).lower() == "apresentacao_dinamica"):
		if((0 != len(context.tipo))):
			obj = context.tipo[0] # primeiro campo da lista define o tipo permitido
			obj = obj.to_object
			obj_name = obj.portal_type
			nivel = int(context.nivel) if (str(context.portal_type).lower() == "apresentacao_dinamica") else GLOBAL_NIVEL
			all_names = obterCampos(obj, "", nivel)

			for name in all_names:
				if context.vocabulario is None:
					context.vocabulario = ["--CONTEUDO-DE-PASTA--","--SEPARADOR1--","--SEPARADOR2--","--SEPARADOR3--"]
				if name not in [termo for termo in context.vocabulario]:
					context.vocabulario.append(name)

			for termo in context.vocabulario:
				terms.append(SimpleVocabulary.createTerm(termo))
		else:
			terms.append(SimpleVocabulary.createTerm("--CONTEUDO-DE-PASTA--"))
	else:
			terms.append(SimpleVocabulary.createTerm("--CONTEUDO-DE-PASTA--"))

	return SimpleVocabulary(terms)


def obterAtributo(context, field_name):
	field = field_name

	"""
	DECRIÇÃO:
		Retorna o atributo "field_name"
	
	CARACTERÍSTICA
		Essa função só pega campos preenchidos
		Um campo de relação vazio não terá os atributos apresentados;
	"""

	if hasattr(context, 'REQUEST'):
		REQUEST=context.REQUEST
		if REQUEST.has_key(field_name):
			return REQUEST[field_name]
		if hasattr(context, field_name):
			field = getattr(context, field_name)
			return field

	if hasattr(context, field_name):
		field = getattr(context, field_name)

	return field


def obterCampos(context, term, nivel):

	results = []

	"""
	DESCRIÇÃO: 
		Retorna todos os campos em context
		e os campos dos objetos referenciados
		até o nivel de parâmetro.

	ISSUES:  
		Relações estáticas tem campo vazio por definição (modelo base?);
		
		Campos ocultos não podem ser apresentados;

	"""

	schema = queryContentType(context)
	all_fields = getFieldsInOrder(schema)

	fix_term = ''
	if (len(term) > 0):
		fix_term = term+'/'

	for f in all_fields:
		field_name = str(f[0])

		if (field_name.lower().find('oculto') != -1): # campos de controle ocultos não são apresentados
			continue

		field_type = str(f[1]).lower()
		term = fix_term+field_name

		if len(term) > 0:
			results.append(term)

		try:
			if (nivel > 1):
				rel = ""
				if (field_type.find("relationchoice") != -1):
					rel = obterAtributo(context, field_name)
					rel = rel.to_object
				elif (field_type.find("relationlist") != -1):
					rel = obterAtributo(context, field_name)
					rel = rel[0].to_object

				if(len(str(rel)) > 0):
					res = obterCampos(rel, term, nivel-1)
					for r in res:
						results.append(r)
		except Exception, e:
			pass

	return results
