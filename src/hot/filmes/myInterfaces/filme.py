# encoding: utf-8
from hot.filmes import _
from zope import schema
from zope.interface import Interface

from collective import dexteritytextindexer
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel.model import Schema
from zope.interface import alsoProvides

class Ifilme(Schema):
    title = schema.TextLine(
        title       = _(u'Filme'),
        description = _(u'Título do filme'),
        required    = True
    )
    sinopse = schema.Text(
        title       = _(u'Sinopse'),
        description = _(u'Breve resumo do filme'),
        required    = False
    )
    dataLancamento = schema.Datetime(
        title       = _(u'Dia de Lançamento e Horário'),
        required    = True
    )
    atores = schema.TextLine(
        title       = _(u'Atores'),
        required    = True,
        readonly    = True
    )
    dexteritytextindexer.searchable('title', 'atores')

alsoProvides(Ifilme, IFormFieldProvider)
    # imagem = schema.NamedImage(
    #     title       = _(u'Imagem do Filme'),
    #     required    = True
    # )
