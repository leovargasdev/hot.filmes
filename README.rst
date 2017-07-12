.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
hot.filmes
==============================================================================

Esse repositorio se encontra um projeto desenvolvido em cima do framework Plone

Implementações do Projeto
--------

- Criação de interfaces

- Criação de viewslets

- Criação de templates


Documentation
-------------

Full documentation for end users can be found in the "docs" folder, and is also available online at http://docs.plone.org/foo/bar


Translations
------------

This product has been translated into

- Klingon (thanks, K'Plai)


Instalação
------------

Instale o hot.filmes adicionando-o buildout::

    [buildout]

    ...

    eggs =
        hot.filmes

    develop =
	src/hot.filmes

Neste projeto também foi utilizado o framework bootstrap, então no buildout adicione::

    [versions]
	
	...

	Plone.app.jquery = 1.11.2
	Plone.app.jquerytools = 1.7.0
	Collective.js.bootstrap = 3.3.5	
	
e agora excute o arquivo ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/hot.filmes/issues
- Source Code: https://github.com/collective/hot.filmes
- Documentation: https://docs.plone.org/foo/bar

License
-------

The project is licensed under the GPLv2.
