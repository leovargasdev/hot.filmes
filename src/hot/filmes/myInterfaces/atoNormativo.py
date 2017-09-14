# encoding: utf-8
from zope import schema
from hot.filmes import _
from plone.supermodel import model
from plone.autoform import directives
from plone.app.textfield import RichText
from plone.namedfile import field as namedfile
from plone.supermodel.directives import fieldset
from z3c.form.browser.radio import RadioFieldWidget
from plone.app.vocabularies.catalog import CatalogSource
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from z3c.relationfield.schema import RelationChoice, RelationList
# bibliotecas para otimizar busca
from collective import dexteritytextindexer
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides

from zope.schema.interfaces import IContextSourceBinder

class IatoNormativo(model.Schema):

    """Elementos da Aba Ato"""

    fieldset('Ato', fields = ['numero', 'data', 'documento_historico', 'description', 'conteudo',
    'pessoas_citadas_no_ato', 'autoridade', 'integrante_cargo', 'diario_oficial_da_uniao', 'municipio', 'atos_relacionados'])

    description = schema.Text(
        title       = _(u'Ementa'),
        description = _(u'Título ou assunto de que se trata o Ato.'),
        required    = True
    )
    numero = schema.Int(
        title       = _(u'Número'),
        description = _(u'Número único de identificação do Ato.'),
        required    = True
    )
    data = schema.Date(
        title       = _(u'Data'),
        description = _(u'Data de criação deste Ato.'),
        required    = True
    )
    documento_historico = namedfile.NamedBlobFile(
        title       = _(u'Documento'),
        description = _(u'Para quando houver um documento antigo que contém o mesmo conteúdo deste Ato. \
                        Usado para migração do site antigo para o atual.'),
        required    = True,
    )
    conteudo = RichText(
        title       = _(u'Conteúdo'),
        description = _(u'Conteúdo do Ato, onde se encontrarão os parágrafos, artigos, incisos, numerações, etc...'),
        required    = True
    )
    pessoas_citadas_no_ato = RelationList(
        title       = _(u'Pessoas Citadas'),
        description = _(u'[RECOMENDADO] Neste campo é possível informar pessoas que integram o ato. Isto servirá para buscas \
                        direcionadas, onde se poderá clicar em um nome/tag e será possível visualizar todos os atos em que a \
                        pessoa esteve citada. Obs.: Este campo não lê o conteúdo, portanto, mesmo que os nomes estejam citados \
                        no corpo do ato, ainda assim será necessário informá-los neste campo.'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'pessoa')),
        required    = False
    )
    autoridade = RelationList(
        title       = _(u'Cargo/Autoridade'),
        description = _(u'[OPCIONAL] Preencher apenas se no Ato constar assinatura de autoridade complementar ao Órgão ou diferente da \
                        titular. Exemplo: Ato emitido pela "Câmara de Graduação" é assinado pelo  "Presidente da Câmara de Graduação" \
                        e pelo "Presidente do CONSUNI", neste caso, se não informar ambos os cargos neste campo, aparecerá apenas o \
                        "Presidente da Câmara de Graduação". Após salvar é possível corrigir possíveis erros editando o Ato, informando as autoridades corretas salvando.'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'cargo')),
        required    = False
    )
    integrante_cargo = RelationList(
        title       = _(u'Titular do Cargo (Pessoa)'),
        description = _(u'[OPCIONAL] Preencher apenas se a pessoa que estiver como Titular do Cargo não for a atual e não for possível \
                        ou necessário atualizar a informação do cargo no momento da criação do Ato. Ex.: Criar uma Portaria de 2009 \
                        onde o Titular do Cargo de "Reitor" era outra Pessoa.'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'pessoa')),
        required    = False
    )
    diario_oficial_da_uniao = schema.URI(
        title       = _(u'Diário Oficial da União'),
        description = _(u'[OPCIONAL] Informar o Link nos casos em que o Ato foi enviado para o D.O.U. Diário Oficial da União.'),
        required    = False
    )
    municipio = schema.Choice(
        title       = _(u"Município"),
        description = _(u'[OPCIONAL] Preencha apenas se o Ato possuir local diferente do cadastro do órgão que o emitiu.'),
        source      = CatalogSource(portal_type = 'municipio'),
        required    = False
    )
    atos_relacionados = RelationList(
        title       = _(u'Atos Relacionados'),
        description = _(u'Selecionar atos que podem estar relacionados de alguma forma com esse ato. Obs: atos alterados \
                        , anulados... por este ato já são automaticamente adicionados.'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False
    )

    """Elementos da Aba Ações do Ato"""

    fieldset('Ações do Ato', fields = ['atos_que_este_ato_altera', 'atos_que_este_ato_anula', 'atos_que_este_ato_retifica',
    'atos_que_este_ato_revoga', 'atos_que_este_ato_torna_sem_efeito'])

    atos_que_este_ato_altera = RelationList(
        title       = _(u'Ato(s) que este ato altera'),
        description = _(u'Escolher os atos que são ALTERADOS por este ato.'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False
    )
    atos_que_este_ato_anula = RelationList(
        title       = _(u'Ato(s) que este ato anula'),
        description = _(u'Escolher os atos que são ANULADOS por este ato.'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False
    )
    atos_que_este_ato_retifica = RelationList(
        title       = _(u'Ato(s) que este ato retifica'),
        description = _(u'Escolher os atos que são RETIFICADOS por este ato.'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False
    )
    atos_que_este_ato_revoga = RelationList(
        title       = _(u'Ato(s) que este ato revoga'),
        description = _(u'Escolher os atos que são REVOGADOS por este ato.'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False
    )
    atos_que_este_ato_torna_sem_efeito = RelationList(
        title       = _(u'Ato(s) que este ato torna sem efeito'),
        description = _(u'Escolher os atos que são TORNADOS SEM EFEITO por este ato.'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False
    )

    """Elementos da Aba DT"""

    fieldset('DT', fields = ['data_publicacao'])

    data_publicacao = schema.Date(
        title       = _(u'Data Diferente'),
        description = _(u'Data de publicação, cuja é distinta da data de criação do ato.'),
        required    = False
    )

    """Elementos da Aba Anexos"""

    fieldset('Anexos', fields = ['anexo1', 'anexo2', 'anexo3', 'anexo4', 'anexo5', 'anexo6', 'anexo7', 'anexo8', 'anexo9',
    'anexo10', 'anexo11', 'anexo12', 'anexo13', 'anexo14', 'anexo15', 'anexo16', 'anexo17', 'anexo18', 'anexo19', 'anexo20'])

    anexo1 = namedfile.NamedBlobFile(title=_(u'Anexo 1'),   required=False)
    anexo2 = namedfile.NamedBlobFile(title=_(u'Anexo 2'),   required=False)
    anexo3 = namedfile.NamedBlobFile(title=_(u'Anexo 3'),   required=False)
    anexo4 = namedfile.NamedBlobFile(title=_(u'Anexo 4'),   required=False)
    anexo5 = namedfile.NamedBlobFile(title=_(u'Anexo 5'),   required=False)
    anexo6 = namedfile.NamedBlobFile(title=_(u'Anexo 6'),   required=False)
    anexo7 = namedfile.NamedBlobFile(title=_(u'Anexo 7'),   required=False)
    anexo8 = namedfile.NamedBlobFile(title=_(u'Anexo 8'),   required=False)
    anexo9 = namedfile.NamedBlobFile(title=_(u'Anexo 9'),   required=False)
    anexo10 = namedfile.NamedBlobFile(title=_(u'Anexo 10'), required=False)
    anexo11 = namedfile.NamedBlobFile(title=_(u'Anexo 11'), required=False)
    anexo12 = namedfile.NamedBlobFile(title=_(u'Anexo 12'), required=False)
    anexo13 = namedfile.NamedBlobFile(title=_(u'Anexo 13'), required=False)
    anexo14 = namedfile.NamedBlobFile(title=_(u'Anexo 14'), required=False)
    anexo15 = namedfile.NamedBlobFile(title=_(u'Anexo 15'), required=False)
    anexo16 = namedfile.NamedBlobFile(title=_(u'Anexo 16'), required=False)
    anexo17 = namedfile.NamedBlobFile(title=_(u'Anexo 17'), required=False)
    anexo18 = namedfile.NamedBlobFile(title=_(u'Anexo 18'), required=False)
    anexo19 = namedfile.NamedBlobFile(title=_(u'Anexo 19'), required=False)
    anexo20 = namedfile.NamedBlobFile(title=_(u'Anexo 20'), required=False)

    """Elementos da Aba Padrão (obs: Todos esses campos estão ocultos para o Usuário)"""

    title = schema.TextLine(
        title       = _(u'Título'),
        description = _(u'Título do Ato'),
        required    = False,
        readonly    = True
    )
    oculto_tagsSubject = schema.TextLine(
        title       = _(u'Tags do Subjects'),
        description = _(u'Campo que pega a informação do Subjects'),
        required    = False,
        readonly    = True
    )
    oculto_autoridade = schema.TextLine(
        title       = _(u'[OCULTO] Autoridade'),
        required    = False,
        readonly    = True
    )
    oculto_municipio = schema.TextLine(
        title       = _(u'[OCULTO] Municipio'),
        required    = False,
        readonly    = True
    )
    oculto_sigla = schema.TextLine(
        title       = _(u'[OCULTO] Sigla do Setor'),
        required    = False,
        readonly    = True
    )
    oculto_tag = schema.TextLine(
        title       = _(u'[OCULTO] Tags do Ato'),
        required    = False,
        readonly    = True
    )
    oculto_redirect = schema.Bool(
        title       = _(u'[OCULTO] Redireciona para Edição'),
        description = _(u'Usado para quando o ato normativo que se quis criar/editar possuir id (nome_curto) já existente.\
                        True: Redireciona a página para a template de edição.'),
        required    = False,
        readonly    = True
    )
    oculto_altera = RelationList(
        title       = _(u'[OCULTO] Atos que ALTERAM este ato.'),
        description = _(u'Atos Normativos que alteram este ato.[OBS: Campo preenchido automaticamente]'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False,
        readonly    = True
    )
    oculto_anula = RelationList(
        title       = _(u'[OCULTO] Atos que ANULAM este ato.'),
        description = _(u'Atos Normativos que anulam este ato.[OBS: Campo preenchido automaticamente]'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False,
        readonly    = True
    )
    oculto_retifica = RelationList(
        title       = _(u'[OCULTO] Atos que RETIFICAM este ato.'),
        description = _(u'Atos Normativos que retificam este ato.[OBS: Campo preenchido automaticamente]'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False,
        readonly    = True
    )
    oculto_revoga = RelationList(
        title       = _(u'[OCULTO] Atos que REVOGAM este ato.'),
        description = _(u'Atos Normativos que revogam este ato.[OBS: Campo preenchido automaticamente]'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False,
        readonly    = True
    )
    oculto_torna_sem_efeito = RelationList(
        title       = _(u'[OCULTO] Atos que TORNAM este ato SEM EFEITO.'),
        description = _(u'Atos Normativos que TORNAM este ato SEM EFEITO.[OBS: Campo preenchido automaticamente]'),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False,
        readonly    = True
    )
    oculto_estados = schema.Set(
        title       = _(u'[OCULTO] Estados'),
        description = _(u'Conjunto de estados do ato normativo.[OBS: Campo preenchido automaticamente]'),
        value_type  = schema.TextLine(),
        required    = False,
        readonly    = True
    )
    atos_que_este_ato_altera_copia = RelationList(
        title       = _(u'Ato(s) que este ato altera'),
        description = _(u''),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False,
        readonly    = True
    )
    atos_que_este_ato_anula_copia = RelationList(
        title       = _(u'Ato(s) que este ato anula'),
        description = _(u''),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False,
        readonly    = True
    )
    atos_que_este_ato_retifica_copia = RelationList(
        title       = _(u'Ato(s) que este ato retifica'),
        description = _(u''),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False,
        readonly    = True
    )
    atos_que_este_ato_revoga_copia = RelationList(
        title       = _(u'Ato(s) que este ato revoga'),
        description = _(u''),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False,
        readonly    = True
    )
    atos_que_este_ato_torna_sem_efeito_copia = RelationList(
        title       = _(u'Ato(s) que este ato torna sem efeito'),
        description = _(u''),
        value_type  = RelationChoice(source = CatalogSource(portal_type = 'ato_normativo')),
        required    = False,
        readonly    = True
    )

    #campos que são buscados no SearchableText
    dexteritytextindexer.searchable('title', 'description', 'oculto_tagsSubject')

alsoProvides(IatoNormativo, IFormFieldProvider)
