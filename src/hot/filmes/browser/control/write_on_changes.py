#!/opt/plone/zinstance/bin/python2.7
# -*- coding: utf-8 -*-
import re
import sys
from unicodedata import normalize

import transaction
from Products.AdvancedQuery import Eq
from five import grok
from plone import api
from plone.uuid.interfaces import IUUID
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectAddedEvent
from zope.lifecycleevent import ObjectModifiedEvent

reload(sys)
sys.setdefaultencoding('utf8')

"""
##########################################################################################################################
#
#	O objetivo deste programa é escrever nos campos dos objetos quando estes são criados ou editados
#
#	ATENÇÃO:
# 		Quando escreve num objeto, o objeto pai pode sofrer alterações,
#		o que irá gerar evento de modificação também (tratado com isinstance).
#
##########################################################################################################################
"""

@grok.subscribe(ObjectModifiedEvent)
@grok.subscribe(ObjectAddedEvent)
def modifiedObject(event):
	type_obj = ''
	try:
		obj = event.object
		type_obj = str(obj.portal_type)
	except Exception as e:
		return

	if ('ato_normativo' == type_obj):
		setValues_ato_normativo(obj)
	elif ('ato_normativo_pasta_setor' == type_obj):
		setValues_ato_normativo_pasta_setor(obj)
	elif ('organograma' == type_obj):
		setValues_organograma(obj)
	elif ('pessoa' == type_obj):
		setValues_pessoa(obj)
	elif ('apresentacao_dinamica' == type_obj):
		setValues_apresentacao_dinamica(obj)
	obj.reindexObject()
	return


def setValues_apresentacao_dinamica(apresentacao):
	##########################################################################################
	#								  DEFINE O TIPO DO OBJETO
	#	tipo_objeto mantém o tipo do objeto do qual os campos estão selecionados
	#	objetos diferentes do primeiro selecionado são retirados
	#	caso o tipo de objeto mude, é feito um refresh nos campos listados
	##########################################################################################

	if (len(apresentacao.tipo) <= 0):
		apresentacao.campo = []
		return

	"""
		ISSUE : O redirecionamento (apresentacao.REQUEST.response.redirect(url)) não funciona.
				Acredito que isso se dá pela chamada do 'xml_elements.py'

			# url = apresentacao.absolute_url()
			# url = str(url) + '/edit'
			# apresentacao.REQUEST.response.redirect(url)
	"""

	obj = apresentacao.tipo[0]
	obj_tipo = obj.to_object.portal_type

	if (apresentacao.tipo_objeto is None):
		apresentacao.tipo_objeto = obj_tipo
	elif (apresentacao.tipo_objeto != obj_tipo):
		apresentacao.campo = []
		apresentacao.vocabulario = ["--CONTEUDO-DE-PASTA--","--SEPARADOR1--","--SEPARADOR2--","--SEPARADOR3--"]
		apresentacao.tipo_objeto = obj_tipo

	index = 0
	index_del = []
	for obj in apresentacao.tipo:
		obj = obj.to_object
		if (str(obj_tipo) != str(obj.portal_type)):
			index_del.append(index)
		index += 1

	i = len(index_del) - 1

	while(i >= 0):
		index = index_del[i]
		apresentacao.tipo.pop(index)	# remove da lista referências de objetos diferentes do primeiro
		i -= 1


	if not isinstance(apresentacao.vocabulario, list):
		apresentacao.vocabulario = ["--CONTEUDO-DE-PASTA--","--SEPARADOR1--","--SEPARADOR2--","--SEPARADOR3--"]

	temp = []
	for termo in apresentacao.vocabulario:
		if termo.count("/") < int(apresentacao.nivel):
			temp.append(termo)
	apresentacao.vocabulario = list(temp)
	temp = []
	for termo in apresentacao.campo:
		if termo.count("/") < int(apresentacao.nivel):
			temp.append(termo)
	apresentacao.campo = list(temp)

	return



def setValues_pessoa(obj):
	##########################################################################################
	#								  GERA TAG
	# geração de tag a partir do titulo
	##########################################################################################
	obj.setSubject(obj.title) # tuple

	"""
		ISSUE: tag de pessoa só busca depois de editado e salvo novamente
	"""
	return

def changeBack_workFlow(obj):
	estado = api.content.get_state(obj=obj)
	"""
		changeBack_workFlow(obj)
		Gambiarra para que o title surta efeito em vários lugares (e.g.: folder_contents)
		já que o id (nome curto) não está sendo escrito.
		Se isto não é feito, o title não aparece, por exemplo em
		'folder_contents'

		Funciona para Workflow Internal/External. Para Publicação Simples pode ocorrer erro.
	"""

	if estado == 'private':
		change = "show_internally"
		back = "hide"
	elif estado == "internal":
		change = "hide"
		back = "show_internally"
	elif estado == "pending":
		change = "retract"
		back = "submit"
	elif estado == "internally_published":
		change = "retract"
		back = "publish_internally"
	elif estado == 'external':
		api.content.transition(obj=obj, transition="retract")
		change = "submit"
		back = "publish_externally"

	api.content.transition(obj=obj, transition=change)
	api.content.transition(obj=obj, transition=back)
	return


def setValues_organograma(obj):
	##########################################################################################
	#								   GERA TITULO
	##########################################################################################
	titulo = "Organograma: " # + setor.title + " (setor.sigla)"
	if obj.setor is not None:
		if not obj.setor.isBroken():
			setor = obj.setor.to_object
			titulo = titulo+setor.title
			descr = setor.description
			obj.title = titulo
			obj.description = descr
		else:
			obj.title = "ERRO: Campo setor tem referência quebrada (selecione outro setor)"
			url = str(obj.absolute_url())
			obj.REQUEST.response.redirect(url+'/edit')
	else:
		obj.title = "ERRO: Campo setor é vazio (insira um setor)"
		url = str(obj.absolute_url())
		obj.REQUEST.response.redirect(url+'/edit')
	changeBack_workFlow(obj)
	return



def setValues_ato_normativo_pasta_setor(obj):
	##########################################################################################
	#								  GERA TITULO e ID (NOME CURTO)
	#   obj.oculto_titulo serve para não perder a referencia de obj.nome_do_setor
	#   em caso de edição (até que seja bloqueado a edição, até para o criador)
	#   a referência do setor é necessária, pois o 'cargo de gestão' não é estático.
	#   obj.oculto_sigla mantém a sigla estática, pois é responsavel pela geração do id
	##########################################################################################

	id = obj.getId()
	if((obj.oculto_titulo is None) or (len(obj.oculto_titulo) == 0)) or (len(id) >= 32):
		obj.oculto_titulo = obj.nome_do_setor
	elif(obj.title is not None): # caso o ato normativo cause o evento de modificação
		return
	obj.nome_do_setor = obj.oculto_titulo	 # independentemente da edição da pasta o setor se mantem no qual foi criado

	nome_pasta = ''
	sigla = ''
	if (obj.oculto_titulo) > 0:
		for s in obj.oculto_titulo:
			if (not s.isBroken()):
				setor = s.to_object		 # obj setor
				nome_pasta = nome_pasta+str(setor.title)
				nome_pasta = nome_pasta+'/'
				sigla_limpa = str(setor.description).replace('-',' ')
				sigla = sigla+sigla_limpa+'-'

	i = len(nome_pasta)
	nome_pasta = nome_pasta[:i-1]	   # tira o ultimo '-'
	i = len(sigla)
	sigla = sigla[:i-1]	   # tira o ultimo '-'
	sigla = sigla.lower()
	sigla = sigla.replace('/', ' ') # caso seja previsto numa sigla ex: 'CONSUNI/PPGP' deve ficar 'CONSUNI PPGP'

	if(obj.oculto_sigla is None):
		# removendo caracteres inválidos
		carac_invalid = "|\?/!@#$&¨¬¢£³²¹%*()_+=§ªº°;:.>,<´`^~'\"}{€®ŧ←↓→øþłĸŋđðßæ«»©“”µ"
		for i in range(0,len(carac_invalid)):
			sigla =sigla.replace(carac_invalid[i],'')
		obj.oculto_sigla = sigla

	obj.title = nome_pasta
	parent = obj.aq_parent

	current_path = '/'.join(parent.getPhysicalPath())

	flag_redirect = False
	flag_writeID = False	# reescreve o id do ato
	new_id = ''

	sigla_limpa = normalize('NFKD', obj.oculto_sigla.decode('utf-8')).encode('ASCII','ignore')

	if (id.find('setor') != -1 or len(id) >= 32): # nome curto: de padrão para criado
		portal_catalog = parent.portal_catalog
		all_setor = portal_catalog(portal_type="ato_normativo_pasta_setor", path=current_path)
		flag_writeID = True
		if (str(obj.oculto_sigla) not in [t.getObject().getId() for t in all_setor]):
			new_id = str(sigla_limpa).replace(' ', '')
		else:
			flag_redirect = True
			context = obj.aq_base
			new_id = str(sigla_limpa)+str(IUUID(context, None))
			obj.title = "ERRO: Pasta "+ obj.oculto_sigla.upper() + " já existe!"
			obj.oculto_sigla = None	# necessário para ser atualizada
			if(new_id == id):
				flag_writeID = False
	if(True == flag_writeID):
		transaction.savepoint(optimistic=True)
		parent.manage_renameObject(id, new_id)
	if(True == flag_redirect):
		obj.REQUEST.response.redirect(str(obj.absolute_url())+'/edit')

	return


def obterData(data):
	mes = ["","janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
	dt = data.isoformat()
	dt = dt.split('-')
	yy = dt[0]
	mm = dt[1]
	dd = dt[2]

	result = ", de "+dd+" de "+mes[int(mm)]+" de "+yy

	return result

def obterAcaoCampoAto(estado):
	all_acao = ['oculto_altera', 'oculto_anula', 'oculto_retifica', 'oculto_revoga', 'oculto_torna_sem_efeito']

	all_estado = {
		'Alterado': 0,
		'Anulado': 1,
		'Retificado': 2,
		'Revogado': 3,
		'Tornado sem efeito': 4,
		'Alterada': 0,
		'Anulada': 1,
		'Retificada': 2,
		'Revogada': 3,
		'Tornada sem efeito': 4,
		'Altera': 0,
		'Anula': 1,
		'Retifica': 2,
		'Revoga': 3,
		'Torna sem efeito': 4
	}

	return all_acao[all_estado[estado]]

def obterAcaoAto(acao_campo):
	all_acao = ['Altera', 'Anula', 'Retifica', 'Revoga', 'Torna sem efeito']

	all_acao_campo = {
		'oculto_altera' : 0,
		'oculto_anula' : 1,
		'oculto_retifica' : 2,
		'oculto_revoga' : 3,
		'oculto_torna_sem_efeito' : 4
	}

	return all_acao[all_acao_campo[acao_campo]]

def obterEstadoAto(genero, acao):
	masc = ['Alterado', 'Anulado', 'Retificado', 'Revogado', 'Tornado sem efeito']
	fem = ['Alterada', 'Anulada', 'Retificada', 'Revogada', 'Tornada sem efeito']
	all_estado = fem if str(genero).lower() == 'feminino' else masc

	all_acao = {
		'oculto_altera' : 0,
		'oculto_anula' : 1,
		'oculto_retifica' : 2,
		'oculto_revoga' : 3,
		'oculto_torna_sem_efeito' : 4
	}

	return all_estado[all_acao[acao]]

def acaoOculto_OcultoAcao(campo):
	campos_acao = ['atos_que_este_ato_altera', 'atos_que_este_ato_anula', 'atos_que_este_ato_retifica', 'atos_que_este_ato_revoga', 'atos_que_este_ato_torna_sem_efeito']
	campos_ocultos = ['oculto_altera', 'oculto_anula', 'oculto_retifica', 'oculto_revoga', 'oculto_torna_sem_efeito']
	if campo in campos_acao:
		return campos_ocultos[campos_acao.index(campo)]
	return campos_acao[campos_ocultos.index(campo)]


def ato_modificadoTitle(ato):

	all_campo_acao = ['oculto_altera', 'oculto_anula', 'oculto_retifica', 'oculto_revoga', 'oculto_torna_sem_efeito']

	ato.oculto_estados = set()

	for campo_acao in all_campo_acao:
		acao_genero = obterEstadoAto(ato.aq_parent.aq_parent.genero, campo_acao)
		if getattr(ato, campo_acao):
			ato.oculto_estados.update([acao_genero])
		else:
			if acao_genero in ato.oculto_estados:
				ato.oculto_estados.remove(acao_genero)

	titulo = str(ato.title).split('(')[0].rstrip(' ')

	if ato.oculto_estados is None:
		ato.oculto_estados = set([estado_acao])

	all_estados = list(ato.oculto_estados)

	result = ''
	for estado in all_estados:
		result = result + estado + ', '

	if result:
		result = ' (' + result[:len(result)-2] + ')'

	return titulo + result.upper()


def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def setValues_ato_normativo(obj):
	"""
	 	Não redireciona em caso de duplicidade em edição (salva o próximo número disponível)
	 	estado_do_ato não é mais usado, apenas para leitura dos atos antigos
	"""
	##########################################################################################
	#								   GERA SIGLA
	#   variável de leitura: obj.oculto_sigla
	##########################################################################################
	setor_sigla = obj.aq_parent.oculto_sigla
	obj.oculto_sigla = str(setor_sigla)

	##########################################################################################
	#								   GERA TITULO E ID (NOME CURTO)
	#   o 'id' tem impacto na apresentação do 'title' em 'uffs.edu.br/.../folder_contents'
	#   e por isso deve ser setado após a geração do título
	##########################################################################################

	genero = obj.aq_parent.aq_parent.genero
	if obj.oculto_sigla.find('-') == -1:
		cnj = ''
	elif genero.upper() == 'MASCULINO':
		cnj = ' conjunto'
	else:
		cnj = ' conjunta'

	parent = obj.aq_parent
	current_path = '/'.join(parent.getPhysicalPath())

	numero = obj.numero
	ano = obj.data.isoformat().split('-', 1)[0]
	id = obj.getId()
	numero_id = ''
	ano_id = ''
	nome_curto = "{0}-{1}".format(ano, '%04d'%numero).lower()
	nome_curto_id = str(id)

	if str(id).find('_') == -1:
		numero_id = str(id).split('-')[1]
		ano_id = str(id).split('-')[0]

	flag_redirect = False   # redirecionamento para edição em caso de duplicidade de id
	flag_writeID = False	# reescreve o id do ato

	if ('%04d'%numero != numero_id or ano != ano_id):
		while True:
			if nome_curto_id == nome_curto:
				obj.numero = numero
				break
			query = Eq('path', current_path) & Eq('id', nome_curto)
			result_q = obj.portal_catalog.evalAdvancedQuery(query)
			if len(result_q) > 0:
				flag_redirect = True
				numero += 1
				nome_curto = "{0}-{1}".format(ano, '%04d'%numero).lower()
			else:
				obj.numero = numero
				flag_writeID = True
				break

	tipo  = obj.aq_parent.aq_parent.title
	titulo = "{0}{1} Nº {2}/{3}/UFFS/{4}".format(tipo.upper(), cnj, obj.numero, obj.oculto_sigla, ano).upper()

	if obj.oculto_estados is not None:
		estado = ''
		for e in obj.oculto_estados:
			estado = estado + e + ', '
		if estado:
			estado = estado[:-2]
			titulo = "{0} ({1})".format(titulo, estado).upper()

	# faz o redirecionamento na view, se a flag for True
	obj.oculto_redirect = flag_redirect

	obj.setTitle(titulo)
	if flag_writeID is True:
		transaction.savepoint(optimistic=True)
		parent.manage_renameObject(id, nome_curto)	  # gera erro: em caso de duplicidade de ID (tratado acima)

	##########################################################################################
	#								  GERA AUTORIDADES
	#   variável de leitura: obj.oculto_autoridade
	##########################################################################################

	aut = []
	if((len(obj.autoridade) == 0) and (len(obj.integrante_cargo) == 0)):
		if(obj.oculto_autoridade is None):
			setor = obj.aq_parent
			setor = setor.nome_do_setor
			for s in setor:
				if (not s.isBroken()):	# se a referencia é válida
					s = s.to_object
					cargo_gestao = s.cargo_de_gestao
					if (not cargo_gestao.isBroken()):   # se a referencia é válida
						aut.append({
							"cargo_de_gestao" : cargo_gestao.to_object,		 # obj: cargo de gestão em referência do setor
							})
			nome = ''
			cargo = '$$'											   # nome $$ cargo
			for autoridade in  aut:
				autoridade = autoridade["cargo_de_gestao"]
				exe = str(autoridade.exercicio).lower()
				exerce = getattr(autoridade, exe)
				if (not exerce.isBroken()):
					em_exercicio = exerce.to_object						# obj: pessoa
				if(em_exercicio.genero.lower() == 'masculino'):
					aux = autoridade.title
				else:
					aux = autoridade.titlef

				aux = aux.replace('#','')
				aux = aux.replace('$','')
				sufixo = ''
				if (exe != 'titular') and (autoridade.sufixo is not None):
					sufixo = str(autoridade.sufixo)
					if re.match("^[\w\d-]+$", sufixo[0]):
						sufixo = " "+sufixo
				cargo = cargo+aux+sufixo+'##'
				if isinstance(em_exercicio, str) is False:
					aux = str(em_exercicio.title)
				else:
					aux = em_exercicio
				aux = aux.replace('#','')
				aux = aux.replace('$','')
				nome = nome+aux+'##'

				arranjo = nome+cargo
				obj.oculto_autoridade = str(arranjo)
	else:
		cargo = []
		pessoa = []


		for cargo_gestao in obj.autoridade:
			if (not cargo_gestao.isBroken()):
				cargo.append({
					"cargo" : cargo_gestao.to_object,			 # obj: cargo de gestão do campo autoridade
					})
		for p in obj.integrante_cargo:
			if (not p.isBroken()):
				pessoa.append({
					"pessoa" : p.to_object,			 # obj: cargo de gestão do campo autoridade
					})
		# zerando os campos para próxima edição
		obj.autoridade = []
		obj.integrante_cargo = []

		setor = obj.aq_parent
		setor = setor.nome_do_setor

		MAXC = len(cargo) 	# tamanho da lista de cargos
		MAXP = len(pessoa)  # tamanho da lista de pessoas
		MAXS = len(setor)	# numero de setores conjuntos

		if ((MAXC == 0) and (MAXP > 0)): # ao menos uma pessoa e cargo vazio
			for s in setor:
				if (not s.isBroken()):	# se a referencia é válida
					s = s.to_object
					cargo_gestao = s.cargo_de_gestao
					if (not cargo_gestao.isBroken()):   # se a referencia é válida
						cargo.append({
							"cargo" : cargo_gestao.to_object,		 # obj: cargo de gestão em referência do setor
							})
		elif ((MAXC > 0) and MAXC < MAXS):
			i = MAXC
			while (i < MAXS):
				s = setor[i]
				if (not s.isBroken()):	# se a referencia é válida
					s = s.to_object
					cargo_gestao = s.cargo_de_gestao
					if (not cargo_gestao.isBroken()):   # se a referencia é válida
						cargo.append({
							"cargo" : cargo_gestao.to_object,		 # obj: cargo de gestão em referência do setor
							})
				i += 1

		integrante_cargo = ''
		cargo_de_gestao = ''											   # nome $$ cargo
		MAXC = len(cargo)

		if (MAXC > 0):
			for i in  range(0, MAXC):
				autoridade = cargo[i]["cargo"]
				if (i >=  MAXP):
					integrante = getattr(autoridade, str(autoridade.exercicio).lower())
					if integrante.isBroken():
						break
					# integrante = integrante.to_object
					pessoa.append({
						"pessoa" : integrante.to_object,			 # obj: cargo de gestão do campo autoridade
						})

				integrante = pessoa[i]["pessoa"]

				sufixo = ''
				if (str(autoridade.exercicio).lower() != 'titular') and (autoridade.sufixo is not None):
					sufixo = str(autoridade.sufixo)
					if re.match("^[\w\d-]+$", sufixo[0]):
						sufixo = " "+sufixo

				nome_pessoa = integrante.title
				if (integrante.genero.lower() == 'masculino'):
					nome_cargo = autoridade.title
				else:
					nome_cargo = autoridade.titlef

				nome_cargo += sufixo

				nome_pessoa = str(nome_pessoa).replace('#', '')
				nome_pessoa = str(nome_pessoa).replace('$', '')
				nome_cargo = str(nome_cargo).replace('#', '')
				nome_cargo = str(nome_cargo).replace('$', '')

				integrante_cargo = integrante_cargo+nome_pessoa+'##'
				cargo_de_gestao  = cargo_de_gestao+nome_cargo+'##'

		arranjo = integrante_cargo+'$$'+cargo_de_gestao
		obj.oculto_autoridade = str(arranjo)


	##########################################################################################
	#								  GERA TAGS
	# geração de tag a partir da relção obj.pessoas_citadas_no_ato e das tags adicionais
	# variável de leitura: obj.oculto_tag
	##########################################################################################

	obj.oculto_tag = ''

	for p in obj.pessoas_citadas_no_ato:
		if (not p.isBroken()):
			obj.oculto_tag = obj.oculto_tag+str(p.to_object.title)+';'

	autoridade = str(obj.oculto_autoridade).split("$$", 1)
	autoridade = autoridade[0].split("##")
	for a in autoridade:
		if ( (len(a) > 2) and (str(obj.oculto_tag).find(a) == -1)):
			obj.oculto_tag = obj.oculto_tag + a + ';'

	i = len(obj.oculto_tag)
	obj.oculto_tag = obj.oculto_tag[:i-1]

	if (len(obj.oculto_tag) == 0):
		obj.oculto_tag = None
	else:
		aux = obj.oculto_tag.split(';')
		aux = sorted(aux, key=lambda s: s.lower())
		obj.oculto_tag =''
		tag_list = list()
		for a in aux:
			tag_list.append(a)
			obj.oculto_tag = obj.oculto_tag+a+';'
		obj.setSubject(tag_list)

	if obj.oculto_tag is not None:
		i = len(obj.oculto_tag)
		obj.oculto_tag = obj.oculto_tag[:i-1]

	##########################################################################################
	#								  GERA MUNICIPIO
	#   variável de leitura: obj.oculto_municipio
	##########################################################################################
	if (obj.municipio is None):
		if(obj.oculto_municipio is None):
			setor = obj.aq_parent
			if (not setor.nome_do_setor[0].isBroken()):
				setor = setor.nome_do_setor[0].to_object
				unidade = setor.unidade[0].to_object
				mcpio = unidade.municipio.to_object
				obj.oculto_municipio = str(mcpio.title)
	elif(not obj.municipio.isBroken()):
		mcpio = obj.municipio.to_object
		obj.oculto_municipio = str(mcpio.title)
		obj.municipio = None


	##########################################################################################
	#								Alteração de estado
	#
	##########################################################################################


	intids = getUtility(IIntIds)
	obj_rel = RelationValue(intids.getId(obj))
	campos_acao = ['atos_que_este_ato_altera', 'atos_que_este_ato_anula', 'atos_que_este_ato_retifica', 'atos_que_este_ato_revoga', 'atos_que_este_ato_torna_sem_efeito']


	#LIMPEZA
	obj.relatedItems = list(obj.atos_relacionados)
	#limpar tudo dos atos que estão nas copias
	for ca in campos_acao:
		co = acaoOculto_OcultoAcao(ca)
		campo_copia = getattr(obj, ca+'_copia') if getattr(obj, ca+'_copia') is not None else []
		for a in campo_copia:
			a = a.to_object
			result  = [x.to_object for x in getattr(a, co)]
			if obj in result:
				result.remove(obj)
				setattr(a, co, [RelationValue(intids.getId(x)) for x in result]) if result else setattr(a, co, [])
				a.setTitle(ato_modificadoTitle(a))

	#ATRIBUIÇÃO
	#fazer o processo de modificação
	for ca in campos_acao:
		co = acaoOculto_OcultoAcao(ca)

		#fazendo backups nas copias
		setattr(obj, ca+'_copia', getattr(obj, ca))

		for a in getattr(obj, ca):
			a = a.to_object

			#colocar o obj nos oculto_acao do ato
			result = getattr(a, co)
			if isinstance(result, list):
				if obj not in [x.to_object for x in result]:
					result.append(obj_rel)
			else:
				result = [obj_rel]
			setattr(a, co, result)

			#atualizar o titulo do ato
			a.setTitle(ato_modificadoTitle(a))

			#colocar o ato no relacionados do obj
			a_rel = RelationValue(intids.getId(a))
			if a not in [x.to_object for x in obj.relatedItems] and a != obj:
				obj.relatedItems.append(a_rel)
	# Campo onde fica as tag's citados no ato
	obj.oculto_tagsSubject = tuple([slugify(x.decode('utf-8'), ' ') for x in obj.subject])