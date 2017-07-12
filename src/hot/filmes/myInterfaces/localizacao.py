from hot.filmes import _
from zope import schema
from zope.interface import Interface

class Ilocalizacao(Interface):
    title = schema.TextLine(
        title       = _(u'Pais'),
        required    = True
    )
    cidade = schema.TextLine(
        title       = _(u'Cidade'),
        required    = True
    )
    sigla = schema.TextLine(
        title       = _(u'Sigla(estado/pais)'),
        description = _(u'abreviatura'),
        required    = False
    )



    # campo com checkbox de uma escolha
    # <field name="type_of_talk" type="zope.schema.Choice"
    #   form:widget="z3c.form.browser.radio.RadioFieldWidget">
    #   <description />
    #   <title>Type of talk</title>
    #   <values>
    #     <element>Talk</element>
    #     <element>Training</element>
    #     <element>Keynote</element>
    #     <element>Lightning Talk</element>
    #   </values>
    # </field>
