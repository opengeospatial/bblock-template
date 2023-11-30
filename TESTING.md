# Testing

Building Blocks have powerful testing capabilities.

## Examples

Examples defined in the _examples.yaml_ (inline or by file reference) get validated and included in generated documentation.

Test cases defines in the _tests/_ subdirectory of each building block get validated.

In each case, the _/build/tests/_ directory contains a set of validation outputs.

Validation includes the following steps:

1. (if JSON and context supplied) JSON-LD uplift ( {testcase}.ttl generated)
2. (if JSON schema supplied) JSON schema validation
3. (if SHACL rules defined) SHACL validation

## SHACL Validation

SHACL rules can be defined in a _rules.shacl_ file or any other files or URLs in the bblocks.json:

```json
 "shaclRules": [
    "vocabs-shacl.ttl"
  ]
  "shaclClosures": [
    "../../vocabularies/terms.ttl",
```

 "shaclClosures" refers to additional files with RDF data required to perform validation - such as checking the types of related objects.

this is particularly useful for relatively small, static vocabularies (e.g. "codelists") that form part of the specification realised by the building block
