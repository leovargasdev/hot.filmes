# #!/opt/plone/zinstance/bin/python2.7
# # -*- coding: utf-8 -*-
# import sys
# import base64
# from five import grok
# from zope.schema.interfaces import IContextSourceBinder
# from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
#
# @grok.provider(IContextSourceBinder)
# def listaDePaises(context):
#     terms = []
#     result = []
#     res = context.portal_catalog(portal_type="localizacao")
#     for i in res:
#         pais = i.getObject().title #pega o camplo title da classe localizacao
#         if pais not in [t for t in result]:
#             result.append(pais)
#             terms.append(SimpleVocabulary.createTerm(pais))
#     return SimpleVocabulary(terms)
