from hot.filmes import _
from zope import schema
from zope.interface import Interface

class Ifilme(Interface):
    title = schema.TextLine(
        title       = _(u'Filme'),
        description = _(u'Titulo do filme'),
        required    = True
    )
    sinopse = schema.Text(
        title       = _(u'Sinopse'),
        description = _(u'Breve resumo do filme'),
        required    = False
    )
    dataLancamento = schema.Datetime(
        title       = _(u'Dia de Lancamento e Horario'),
        required    = True
    )
