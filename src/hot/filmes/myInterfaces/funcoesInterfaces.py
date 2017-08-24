#!/opt/plone/zinstance/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import base64
from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


"""
 	CORRIGIR A IMPLEMENTACAO DOS VOCABULARIOS E DAS CONDIÇÕES NAS TEMPLATES A PARTIR DE:

			items = [ ("value1", u"This is label for item"), ("value2", u"This is label for value 2")]

			terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]

			vocabulary = SimpleVocabulary(terms)

	NO FORMATO ACIMA É POSSIVEL DESIGNAR O VALOR QUE É SALVO NO CAMPO E O VALOR QUE É APRESENTADO AO USUÁRIO (LABEL)
	OU SEJA, É POSSIVEL DEFINIR CHAVE-VALOR
"""


@grok.provider(IContextSourceBinder)
def estadoAto(context):
	"""
		Vocabulário para o campo estado_do_ato do tipo ato_normativo
	"""
	result = []
	result.append(SimpleVocabulary.createTerm("Alterado/Alterada"))
	result.append(SimpleVocabulary.createTerm("Alterado e Retificado"))
	result.append(SimpleVocabulary.createTerm("Anulado/Anulada"))
	result.append(SimpleVocabulary.createTerm("Retificado/Retificada"))
	result.append(SimpleVocabulary.createTerm("Revogado/Revogada"))
	result.append(SimpleVocabulary.createTerm("Tornado sem efeito/Tornada sem efeito"))
	return SimpleVocabulary(result)

@grok.provider(IContextSourceBinder)
def acaoAto(context):
	"""
		Vocabulário para o campo acao_do_ato do tipo ato_normativo
	"""
	result = []
	result.append(SimpleVocabulary.createTerm("Altera"))
	result.append(SimpleVocabulary.createTerm("Altera e Retifica"))
	result.append(SimpleVocabulary.createTerm("Anula"))
	result.append(SimpleVocabulary.createTerm("Retifica"))
	result.append(SimpleVocabulary.createTerm("Revoga"))
	result.append(SimpleVocabulary.createTerm("Torna sem efeito"))
	return SimpleVocabulary(result)

