# Reusing existing JSON Schemas

Building Blocks can be defined to reuse existing JSON schemas in a more sophisticated way.

A re-used schema can be:

1. [profiled (by extension or constraints)](JSONSCHEMA-PROFILING.md)
2. Mapped to a [semantic (RDF)](RDF.md) model allowing richer specification of constraints.
3. [Tested](TESTING.md) with examples and test cases.

## How to reuse

This is simply a matter of referencing the reused schema in the building block schema(.json|.yaml):

```json
{ "$ref": "http://somestablelocation.org/schema.json" }
```

## How to reuse a building block with its added components...

this is done in a two-step process:

1. in the (_bblocks-config.yaml)[_bblocks-config.yaml] file tell the processing where to find building block registers:
```yaml
schema-mapping:
  default: https://opengeospatial.github.io/bblocks/annotated-schemas/

imports:
  - default
  - https://opengeospatial.github.io/ogcapi-sosa/build/register.json
```

The default is the OGC master register of building blocks.

2. use the _bblocks:{id}_ syntax as href in schema $ref elements.

This means your building block will inherit all json-ld contexts and SHACL rules from the referenced building block automatically and apply during [testing](TESTING.md).
