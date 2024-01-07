# RDF-only building blocks

Building Blocks can be defined that use RDF only, 

A RDF building block can

1. Define RDF (TTL) examples how to use the Semantic model
2. Apply SHACL Rules to [validate examples](TESTING.md#SHACL)
3. [Perform transforms](TXFORMS.md) and validate results

Test cases and examples as either TTL or JSONLD will undergo syntax and SHACL validation.

`examples.yaml` can have embedded TTL - eg.

```
- title: Example of SOSA ObservationCollection
  comment:
    This class is a target for the SOSA v 1.1 update. 

  snippets:
    - language: turtle
      code: |-
        @prefix sosa: <http://www.w3.org/ns/sosa/> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
        @prefix eg: <http://example.org/my-feature/> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        eg:c1 a sosa:ObservationCollection ;
          sosa:hasMember eg:pop1999, eg:pop2000 ;
          sosa:observedProperty <http://dbpedia.org/ontology/population> ;
        .

```
