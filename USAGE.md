# OGC Building Block template

This repository can be used as a template to create new collections of
[OGC Building Blocks](https://opengeospatial.github.io/bblocks).

Building Blocks can be reused by either:

- cut and paste "ready to use" forms from the "build/" directory
- directly reference the artefacts in the "build" directory using the URL pattern specified in the building block
  description

## How-to

1. Click on "Use this template" on GitHub (do not fork this repository, or you will have to manually enable the
   workflows).
2. Set the `identifier-prefix` provided by OGC in `bblocks-config.yaml`:
   * The first component of the prefix should represent the entity defining or maintaining this building block
     collection. If this is an OGC-related project, you may use `ogc.` here.
   * The rest of the prefix components should be chosen according to the nature of the collection. For example, if
     this repository only contained schemas for *OGC API X*, a possible prefix could be `ogc.apis.api-x.schemas.`.
   * Bear in mind that the path of the building blocks inside `_sources` will be used in their identifiers (see below).
   * **Identifiers should be as stable as possible**, even when under development. This makes it easier to promote
     building blocks to production (i.e., being adopted by the OGC as official), and avoids having to manually/update
     references (in dependency declarations, schemas, etc.).
3. Set a `name` for the repository inside `bblocks-config.yaml`.
4. Configure any necessary [imports](#setting-up-imports) inside `bblocks-config.yaml`.
5. Set the [additional register metadata properties]() in `bblocks-config.yaml`.
6. For each new building block, replace or create a copy of the `mySchema` or `myFeature` inside `_sources`.
   Note: **the path to and name of the new directory will be part of the building block identifier**.
7. Update the [building block's files](#building-block-structure).
   1. See [Using a published schema](SCHEMAS.md) for information how test an existing schema.
   2. See [Semantic Annotation](JSONLD.md) for information how to "uplift" a schema - linking to a model using JSON-LD.
   3. See [Semantic Models in RDF](RDF.md) for information how to create a building block to profile and test semantic models.
   4. See [JSON Schema Profiling](JSONSCHEMA-PROFILING.md) for information how to specialise an existing schema.
   5. See [SHACL Rules](TESTING.md) for information how to define powerful constraints for semantic models.
   6. See [Transforms](TXFORMS.md) for information how to define and test transformations.
8. Replace the README.md file with documentation about the new building block(s).
9. Enable GitHub pages in the repository settings, setting "Source" (under "Build and deployment")
   to "GitHub Actions".

Note: building blocks subdirectories can be grouped inside other directories, like so:

```
type1/
  bb1-1/
    bblock.json
  bb1-2/
    bblock.json
type2/
  subtype2-1/
    bb2-1-1/
        bblock.json
[...]
```

In that case, `type1`, `type2` and `subtype2-1` will also be part of the building block identifiers.

## Registering your building block

Building blocks can be aggregated into registers, such as OGC's official and incubator registries.

### Making your own Building Block Register

TBD 

## Building block structure

The following image summarizes the general usage of a building block:

![Usage](usage.png)

### Sources

The `_sources` directory will contain the sources for the building blocks inside this repository.

- `bblock.json`: Contains the metadata for the building block. Please refer to this
  [JSON schema](https://raw.githubusercontent.com/opengeospatial/bblocks-postprocess/master/ogc/bblocks/metadata-schema.yaml)
  for more information.
- `description.md`: Human-readable, Markdown document with the description of this building block.
  Relative links and images can be included in this file, and they will be resolved to full
  URLs when the building block is processed. 
- `examples.yaml`: A list of examples for this building block. See [Examples](#examples) below.
- `schema.json`: JSON schema for this building block, if any. See [JSON schema](#json-schema) below.
    - `schema.yaml`, in YAML format, is also accepted (and even preferred).
- `assets/`: Documentation assets (e.g. images) directory. See [Assets](#assets) below.
- `tests/`: Test resources. See [Validation](#validation-and-tests).

This repository includes a sample building block in the `my-building-block` directory.

Building Block identifiers are automatically generated in the form:

```
<identifier-prefix><bb-path>
```

where:

- `identifier-prefix` is read from `bblocks-config.yaml`. This will initially be a placeholder value,
  but should have an official value eventually (see [How-to](#how-to)).
- `bb-path` is the dot-separated path to the building block inside the repository.

For example, given a `r1.branch1.` identifier prefix and a `cat1/cat2/my-bb/bblock.json` metadata file,
the generated identifier would be `r1.branch1.cat1.cat2.my-bb`. This applies to the documentation
subdirectories as well, after removing the first element (e.g., Markdown documentation will be written to
`generateddocs/markdown/branch1/cat1/cat2/my-bb/index.md`).

### Setting up imports

Any building blocks repository can import any other repository, so that references by id to building blocks
(e.g. inside schemas, in `bblock.json`, etc.) belonging to the imported repositories can be automatically resolved.

Repository imports can be defined as an array of URLs to the output `register.json` of other repositories inside
`bblocks-config.yaml`:

* If `imports` is missing from `bblocks-config.yaml`, the
  [main OGC Building Blocks repository](http://blocks.ogc.org/register.html) will be imported by default.
* `default` can be used instead of a URL to refer to the
  [main OGC Building Blocks repository](http://blocks.ogc.org/register.html). 
* If `imports` is an empty array, no repositories will be imported.

For example, the following will import two repositories, one of them being the main OGC Building Blocks repository:

```yaml
name: Repository with imports
imports:
  - default
  - https://example.com/bbr/repository.json
```

### Additional register metadata properties

The following additional properties can be set inside `bblocks-config.yml`:

* `name`: A (short) string with the name of the register.
* `abstract`: A short text to serve as an introduction to the register or building blocks collection. 
  Markdown can be used here.
* `description`: A longer text with a description of the register or collection. Markdown can be used here.

### Ready to use components

The `build/` directory will contain the **_reusable assets_** for implementing this building block.

*Sources* minimise redundant information and preserve original forms of inputs, such as externally published
schemas, etc. This allows these to be updated safely, and also allows for alternative forms of original source
material to be used whilst preserving uniformity of the reusable assets.

**The `build` directory should never be edited**. Moreover, applications should only use (copy or reference) resources
from this directory.

### Examples

Each example consists of Markdown `content` and/or a list of `snippets`. `snippets`, in turn,
have a `language` (for highlighting, language tabs in Slate, etc.) and the `code` itself.

`content` accepts text in Markdown format. Any relative links or images will be resolved to full
URLs when the building block is published (see [Assets](#assets)).

Instead of the `code`, a `ref` with a filename relative to `examples.yaml` can be provided:

```yaml
- title: My inline example
  content: Example with its code in the examples.yaml file
  snippets:
    - language: json
      code: '{ "a": 1 }'
- title: My referenced example
  content: Example with its code pulled from a file
  snippets:
    - language: json
      ref: example1.json # in the same directory as examples.yaml  
```

Please refer to
[the updated JSON schema for `examples.yaml`](https://raw.githubusercontent.com/opengeospatial/bblocks-postprocess/master/ogc/bblocks/examples-schema.yaml)
for more information.

The `examples.yaml` file in `my-building-block` can be used as a template.

### JSON schema

If a `schema.json` (or `schema.yaml`) file is found, it is not necessary to add the `schema` property
to `bblock.json`; it will be done automatically on the OGC Building Blocks Register. The same thing
applies to the `context.jsonld` file and the `ldContext` property.

References to the schemas of other building blocks can be added using `$ref`. The special `$_ROOT_/` directory
can be used to refer to the root of the central OGC Building Blocks tree.

### "Semantic Annotation"

The Building block design allows for "semantic annotation" through the use of a **_context_** document that
cross-references each schema element to a URI, using the JSON-LD syntax. The end result is still a valid JSON schema,
but may also be parsed as flexible RDF graphs if desired.

This provides multiple significant improvements over non-annotated schemas:

1. differentiates between the same and different meanings for common element names used in different places
2. can be used to link to a semantic model further describing each element
3. allows use of advanced, standardised validation of instance data
4. allows automated annotation of schemas themselves for tools able ot exploit additional information

The JSON schema for a building block is optionally linked to a conceptual model by using a root-level `x-jsonld-context`
property pointing to a JSON-LD context document (relative paths are ok). The Building Blocks Register can
then annotate every property inside the JSON schemas with their corresponding RDF predicate automatically.

### Validation and tests

The `tests` directory contains test resources that can be used for performing validation tasks. There are two
types of validations:

- JSON schema
- RDF / [SHACL](https://www.w3.org/TR/shacl/), if a top-level (i.e., same directory as `bblock.json`).

Inside the `tests` directory, 3 types of files will be processed:

- `*.ttl`: [Turtle](https://www.w3.org/TR/turtle/) RDF files that will be validated against the SHACL rules.
    - SHACL rules are loaded from the `shaclRules` property inside `bblock.json`. If a `rules.shacl` file is found
      in the Building Block directory it will be used by default. **SHACL files must be serialized as Turtle**.
- `*.jsonld`: JSON-LD files that will be first validated against the Building Block JSON Schema
  and then against the SHACL rules.
- `*.json`: JSON files that will be first validated against the JSON Schema, then "semantically uplifted"
  by embedding the Building Block's `context.jsonld`, and finally validated against the SHACL rules.

If the filename for a test resource ends in `-fail` (e.g., `missing-id-fail.json`), validation will only pass
if the test fails (JSON SCHEMA, SHACL shapes, etc.); this allows writing negative test cases.

[Examples](#examples) in JSON and JSON-LD format will also be uplifted and validated. 

### Assets

Any relative URL included in the description of the building block and in the markdown content of the
examples will be converted into a full URL relative to the source location (i.e., that of `bblock.json`).-

Assets (e.g., images) can be placed in the `assets/` directory for later use in documentation pages,
by using references to `assets/filename.ext`.

For example, a `sample.png` image in that directory can be included in the description
Markdown code of a building block like this:

```markdown
![This is a sample image](assets/sample.png)
```

### "Super Building Blocks"

A super building block is a building block whose `schema.yaml` is automatically generated as the `oneOf`
union of all the schemas recursively found in all its subdirectories. This needs to be enabled
in `bblock.json` by setting the `superBBlock` property to `true`.

When super building block mode is enabled, the `schema.yaml` inside the source directory for the building
block **will be overwritten**.

## Postprocessing overview

This repository comes with a GitHub workflow that detects, validates and processes its building blocks,
so that their outputs can be tested before inclusion in the main OGC Register:

![OGC Building Blocks processing](https://raw.githubusercontent.com/opengeospatial/bblocks-postprocess/master/process.png)

### Output testing

The outputs can be generated locally by running the following:

```shell
# Process building blocks
docker run --pull=always --rm --workdir /workspace -v "$(pwd):/workspace" \
  ghcr.io/opengeospatial/bblocks-postprocess  --clean true --base-url http://localhost:9090/register/
```

**Notes**:

* Docker must be installed locally for the above commands to run
* The syntax for `-v "$(pwd):/workspace"` may vary depending on your operating system
* Output files will be created under `build-local` (not tracked by git by default)
* The value for `--base-url` will be used to generate the public URLs (schemas, documentation, etc.). In this case,
  we use the local `http://localhost:9090/register/` URL to make the output **compatible with the
  viewer** when running locally (see below). If omitted, the value will be autodetected from the repository
  metadata.

#### Building Blocks Viewer

You can also preview what the output will look like inside the Building Blocks Viewer application:

```shell
docker run --rm --pull=always -v "$(pwd):/register" -p 9090:9090 ghcr.io/ogcincubator/bblocks-viewer
```

**Notes**:

* Make sure to [compile the register](#output-testing) before running the viewer (or delete `build-local`
  altogether to view the current build inside `build`).  
* Docker must be installed locally for the above commands to run
* The syntax for `-v "$(pwd):/register"` may vary depending on your operating system
* `-p 9090:9090` will publish the Viewer on port 9090 on your machine

## Tools

The following tools are useful for getting each component working during development:

