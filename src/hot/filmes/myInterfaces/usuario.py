#!/opt/plone/zinstance/bin/python2.7
# -*- coding: utf-8 -*-
from hot.filmes import _
from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.app.vocabularies.catalog import CatalogSource
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import directlyProvides

from collective import dexteritytextindexer
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel.model import Schema
from zope.interface import alsoProvides

sexos = [["m", "Masculino"], ["f", "Feminino"]]
opSexos = SimpleVocabulary([SimpleTerm(value=sexos[0][0], title=sexos[0][1]),
                            SimpleTerm(value=sexos[1][0], title=sexos[1][1])])

# def possibleOrganizers(context):
#     terms = []
#     result = []
#     res = context.portal_catalog(portal_type="localizacao")
#     for i in res:
#         pais = i.getObject().title #pega o camplo title da classe localizacao
#         if pais not in [t for t in result]:
#             result.append(pais)
#             terms.append(SimpleVocabulary.createTerm(pais))
#     return SimpleVocabulary(terms)
# directlyProvides(possibleOrganizers, IContextSourceBinder)

class Iusuario(Schema):
    title = schema.TextLine(
        title       = _(u'Nome'),
        required    = True
    )
    description = schema.TextLine(
        title       = _(u'Sobrenome'),
        required    = False
    )
    apelido = schema.TextLine(
        title       = _(u'Apelido'),
        required    = False
    )
    cpf = schema.TextLine(
        title       = _(u'CPF'),
        description = _(u'Deve ter 11 digitos'),
        required    = True,
        min_length  = 0,
        max_length  = 11
    )
    sexo = schema.Choice(
        title       = _(u'sexo'),
        vocabulary  = opSexos,
        required    = False
    )
    #Add varios elementos na lista
    filmesFavoritos = RelationList(
        title       = _(u'Filmes Favoritos'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'filme')),
        description = _(u'Dos filmes que estao no sistema, dizer quais declara favorito'),
        required    = False
    )
    #Add um elemento
    # filmesFavoritos = RelationChoice(
    #     title       = _(u'Filmes Favoritos'),
    #     source      = CatalogSource(portal_type = 'filme'),
    #     required    = False,
    # )
    # endereco = schema.Choice(
    #     title       = _(u'Endereco'),
    #     source      = possibleOrganizers,
    #     required    = False
    # )
    aniversario = schema.Date(
        title       = (u'Data de Nascimento'),
        required    = False
    )
    dexteritytextindexer.searchable('title', 'description', 'apelido')

alsoProvides(Iusuario, IFormFieldProvider)
