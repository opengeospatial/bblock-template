# Testing

Building Blocks have powerful automated testing capabilities using the built-in github actions.

These can be supplemented with additional custom validation and transformation processes as required.


## Examples

Examples defined in the `examples.yaml` (inline or by file reference) get validated and included in generated documentation.

Test cases defines in the `tests/` subdirectory of each building block get validated. Additional or external tests
can be added in `tests.yaml` as a list of objects with a `ref` property pointing to the test resource's location,
and optionally defining the `output-filename` and/or `require-fail` properties (for more information, see the 
example `tests.yaml` file provided in the template and 
[the JSON Schema for `tests.yaml`](https://github.com/opengeospatial/bblocks-postprocess/blob/master/ogc/bblocks/extra-tests-schema.yaml).

In each case, the `/build/tests/` directory contains a set of validation outputs.

Validation includes the following steps:

1. (if JSON and context supplied) JSON-LD uplift ( {testcase}.ttl generated)
2. (if JSON schema supplied) JSON schema validation
3. (if SHACL rules defined) SHACL validation

A summary report is produced at `/build/tests/report.html`.

This is linked from the generated building block index.

## SHACL Validation

SHACL rules can be defined in a ```rules.shacl``` file or any other files or URLs in the bblocks.json:

```
 "shaclRules": [
    "vocabs-shacl.ttl"
  ]
  "shaclClosures": [
    "../../vocabularies/terms.ttl",
```

 "shaclClosures" refers to additional files with RDF data required to perform validation - such as checking the types of related objects.

this is particularly useful for relatively small, static vocabularies (e.g. "codelists") that form part of the specification realised by the building block

## Tools

In addition to built-in testing capabilities the following online tools can be helpful in developing and debugging different layers of the design:

* [JSON Schema validator](https://www.jsonschemavalidator.net/)
* [JSON-LD Playground](https://json-ld.org/playground/)
* [SHACL Validator](https://shacl-play.sparna.fr/play/validate)

Hint - to use the JSON Schema validator with a published schema you can create a wrapper such as 

```json
{
  "$ref": "https://my.org/schema.json?version"
}
```

(updating ```version``` forces the validator to pick up any changes in the published schema.)