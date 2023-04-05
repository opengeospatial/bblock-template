# OGC Building Block template

This repository can be used as a template to create new collections of
[OGC Building Blocks](https://opengeospatial.github.io/bblocks). 

## Building block structure

- `metadata.json`: Contains the metadata for the building block. Please refer to this
  [JSON schema](https://github.com/avillar/bblocks/blob/master/metadata-schema.yaml) for more information.
- `description.md`: Human-readable, Markdown document with the description of this building block.
- `examples.md`: A list of examples for this building block. See [Examples](#examples) below.
- `schema.yaml`: JSON schema for this building block, if any. See [JSON schema](#json-schema) below.
- `assets/`: Documentation assets (e.g. images) directory. See [Assets](#assets) below.

This repository includes a sample building block in the `my-building-block` directory.

### Examples

Each example consists of Markdown `content` and/or a list of `snippets`. `snippets`, in turn,
have a `language` (for highlighting, language tabs in Slate, etc.) and the `code` itself. 

The `examples.yaml` file in `my-building-block` can be used as a template.

### JSON schema

The JSON schema for a building block can be linked to a conceptual model by using a root-level `@modelReference`
property pointing to a JSON-LD context document (relative paths are ok). The Building Blocks Register can 
then annotate every property inside the JSON schemas with their corresponding RDF predicate automatically.

If a `schema.yaml` file is found, it is not necessary to add the `schema` property to `metadata.json`; it will
be done automatically on the OGC Building Blocks Register. `ldContext` however, is not auto-generated. 

### Assets

Assets (e.g., images) can be placed in the `assets/` directory for later use in documentation pages,
by using references to `@@assets@@/filename.ext`.

For example, a `sample.png` image in that directory can be included in the description
Markdown code of a building block like this:

```markdown
![This is a sample image](@@assets@@/sample.png)
```

## How-to

1. Fork (or click on "Use this template" on GitHub) this repository.
2. For each new building block, replace or create a copy of the `my-building-block`.
   Note: **the name of the new directory will be part of the building block identifier**.
3. Update the building [block's files](#building-block-structure).
4. Replace this README.md file with documentation about the new building block(s).
5. Contact OGC and request that your new building block(s) be added to the official Register.

Note: building blocks subdirectories can be grouped inside other directories, like so:

```
type1/
  bb1-1/
    metadata.json
  bb1-2/
    metadata.json
type2/
  subtype2-1/
    bb2-1-1/
        metadata.json
[...]
```

In that case, `type1`, `type2` and `subtype2-1` will also be part of the building block identifiers.