# MkRDF

MkDocs plugin to build pages from RDF Graphs.


### Selection

The `selection` is responsible for choosing for which IRIs from the provided graph a page should be build.
The configuration key has four sub keys, `preset`, `query`, `list`, and `file`. If multiple of the keys are set, the union of the selections is build.

- `preset` can hold the values `subject_relative` (default), `subject_all`, or `none`,
  - `subject_relative` selects all subject IRIs that share the configured `base_iri`, i.e. `SELECT ?resourceIri { ?resourceIri ?p ?o . FILTER regex(str(?resourceIri), concat("^", str(?base_iri))) }`,
  - `subject_relative` selects all subject IRIs irrespective of the `base_iri`, i.e. `SELECT ?resourceIri { ?resourceIri ?p ?o }`.
  - `none` will skip all other selections and not IRI is selected
- `query` or `queries` needs to provide a string (or list of strings) with a valid SPARQL 1.1 query, that binds the variable `?resourceIri` to all selected IRIs.
- `list` an explicit list of IRIs
- `file` a file explicitly listing the IRIs

## Comparison to JekyllRDF

`path` is now `graph_file`
`restriction` is now `selection` (note, that the query now binds the variable `?resourceIri` instead of `?resourceUri`)
`baseiri` is now `base_iri`
