# MkRDF

> [!WARNING]
>
> This project is still under development and does not yet covers all use cases of Jekyll RDF.
> The interface are unstable and might break in future versions.


MkDocs plugin to build pages from RDF Graphs.

A use case it to covers the representation of an entire graph with templates to represent instances of each class.

You need to install `mkrdf` e.g. with pip and configure your [mkdocs setup to use it](https://www.mkdocs.org/dev-guide/plugins/#using-plugins).

The section in your `mkdocs.yml` file could look as follows:

```
[…]

plugins:
  - mkrdf:
      graph_file: simpsons.ttl
      base_iri: https://simpsons.example.org/
      selection:
        preset: subject_relative
      class_template_map:
        http://xmlns.com/foaf/0.1/Person: person.html
      instance_template_map:
        https://simpsons.example.org/Marge: marge.html

```

### Selection

The `selection` is responsible to choose for which IRIs from the provided graph a page should be build.
The configuration key has four sub keys, `preset`, `query`, `list`, and `file`. If multiple of the keys are set, the union of the selections is build.

- `preset` can hold the values `subject_relative` (default), `subject_all`, or `none`,
  - `subject_relative` selects all subject IRIs that share the configured `base_iri`, i.e. `SELECT ?resourceIri { ?resourceIri ?p ?o . FILTER regex(str(?resourceIri), concat("^", str(?base_iri))) }`,
  - `subject_relative` selects all subject IRIs irrespective of the `base_iri`, i.e. `SELECT ?resourceIri { ?resourceIri ?p ?o }`.
  - `none` will skip all other selections and not IRI is selected
- `query` or `queries` needs to provide a string (or list of strings) with a valid SPARQL 1.1 query, that binds the variable `?resourceIri` to all selected IRIs.
- `list` an explicit list of IRIs
- `file` a file explicitly listing the IRIs


## Related Projects

The implementation of jinja-rdf, kisumu, and mkrdf is a result of the lessons learned from JekyllRDF.

### Jinja RDF

[Jinja RDF](https://github.com/AKSW/jinja-rdf)

The library that provides the filters and data model (the core).

### Kisumu

[kisumu](https://github.com/AKSW/kisumu)

A simple command line tool and library to render a template + an RDF graph -> a static document.
It is also build on top of Jinja RDF.

### Jekyll RDF

[Jekyll RDF](https://github.com/AKSW/jekyll-rdf)

The implementation of jinja-rdf, kisumu, and mkrdf is a result of the lessons learned from JekyllRDF.
Currently the three tools don't cover all features, that were implemented in JekyllRDF, if you miss a feature that you need, please provide a pull request to one of the projects.
([Read more about the relation](https://github.com/AKSW/jinja-rdf/blob/main/README.md#jekyll-rdf).)

## Migrate from Jekyll RDF

If you migrate from Jekyll RDF you need to setup a new mkdocs project, adjust your templates and configuration.
Many things are named differently with the hope to make it simpler for users of mkrdf without previous knowledge about Jekyll RDF.

### Configuration

`path` is now `graph_file`
`restriction` is now `selection` (note, that the query now binds the variable `?resourceIri` instead of `?resourceUri`)
`baseiri` is now `base_iri`

### Filters

Those are the filters provided by JekyllRDF.

- `rdf_get` (not available)
- `rdf_property`  -> `property`, `properties` `Resource[]`
- `rdf_inverse_property` -> `property_inv`, `properties_inv`
- `sparql_query`  -> `query`
- `rdf_container` (not available, TODO)
- `rdf_collection` (not available, TODO)
