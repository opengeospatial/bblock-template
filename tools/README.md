# OGC Building Block Schema Tools

Standalone Python tools for resolving and validating [OGC Building Block](https://opengeospatial.github.io/bblocks/) schemas.

## Background

The `bblocks-postprocess` Docker tool (used by all OGC building block repositories) generates annotated schemas in `build/annotated/`, but these still contain `$ref` references to remote URLs. There is currently no standard way for building block authors to produce a **fully-resolved, self-contained JSON Schema** suitable for local validation, tooling integration, or inspection.

These tools fill that gap:

| Tool | Purpose |
|------|---------|
| `resolve_schema.py` | Recursively resolve all `$ref` in a building block schema into a single self-contained JSON Schema |
| `compare_schemas.py` | Compare `schema.yaml` source files against companion JSON schemas for consistency |

## Prerequisites

- Python 3.6+
- [pyyaml](https://pypi.org/project/PyYAML/) (`pip install pyyaml`)

## resolve_schema.py

Recursively resolves ALL `$ref` references from modular YAML/JSON source schemas into one fully-inlined JSON Schema.

### `$ref` patterns handled

1. **Relative path:** `$ref: ../detailEMPA/schema.yaml`
2. **Fragment-only:** `$ref: '#/$defs/Identifier'`
3. **Cross-file fragment:** `$ref: ../metaMetadata/schema.yaml#/$defs/conformsTo_item`
4. **Both YAML and JSON** file extensions
5. **`bblocks://` URI:** `$ref: bblocks://ogc.geo.features.feature` — cross-building-block references using OGC's `bblocks://` (or `bblocks:`) URI scheme, resolved via the `identifier-prefix` in `bblocks-config.yaml`

### Usage

```bash
# Resolve a building block by name (searches _sources/ automatically)
python tools/resolve_schema.py --bblock dataDownload

# Resolve an arbitrary schema file by path
python tools/resolve_schema.py --file _sources/myFeature/schema.yaml

# Write to a file instead of stdout
python tools/resolve_schema.py --bblock dataDownload -o resolved.json

# Flatten allOf entries into merged objects
python tools/resolve_schema.py --file schema.yaml --flatten-allof -o resolved.json

# Keep metadata keys ($id, x-jsonld-*, etc.) that are stripped by default
python tools/resolve_schema.py --file schema.yaml --keep-metadata

# Custom _sources directory
python tools/resolve_schema.py --bblock myBlock --sources-dir path/to/_sources
```

### Options

| Option | Description |
|--------|-------------|
| `--file PATH` | Resolve a schema file by path (mutually exclusive with `--bblock`) |
| `--bblock NAME` | Resolve a building block by name (mutually exclusive with `--file`) |
| `--sources-dir PATH` | Path to `_sources/` directory (auto-detected if omitted) |
| `-o, --output PATH` | Write output to file (default: stdout) |
| `--flatten-allof` | Merge `allOf` entries into single objects |
| `--keep-metadata` | Preserve `$id`, `x-jsonld-*`, and other metadata keys |
| `--strip-keys KEY ...` | Custom set of keys to strip (overrides defaults; ignored with `--keep-metadata`) |

### Building block discovery

When using `--bblock`, the tool searches for the schema in this order:

1. `{sources_dir}/{name}/schema.yaml` (flat layout)
2. `{sources_dir}/{name}/schema.json` (flat layout, JSON)
3. `{sources_dir}/**/{name}/schema.yaml` (nested layout, filtered by `bblock.json` presence)
4. `{sources_dir}/**/{name}/schema.json` (nested layout, JSON fallback)

### `bblocks://` cross-building-block references

Many OGC building block schemas reference other building blocks using the `bblocks://` URI scheme (e.g., `$ref: bblocks://ogc.geo.common.data_types.bounding_box`). The resolver handles these automatically by:

1. Reading `bblocks-config.yaml` from the repo root (parent of the sources directory) to get the `identifier-prefix` (e.g., `ogc.`)
2. Scanning all `bblock.json` files to build an index mapping identifiers to schema paths
3. Resolving `bblocks://` refs by looking up the identifier in the index

This works for all local building blocks within the same repository. References to building blocks from imported registries (external repos) will produce a `$comment` noting they could not be resolved locally.

Fragment refs are also supported: `$ref: bblocks://ogc.geo.features.feature#/$defs/Something`

### Example: validate data against resolved schema

```bash
# Resolve, then validate
python tools/resolve_schema.py --bblock myFeature -o resolved.json
python -c "
import json, jsonschema
schema = json.load(open('resolved.json'))
data = json.load(open('example.json'))
jsonschema.validate(data, schema)
print('Valid!')
"
```

## compare_schemas.py

Compares `schema.yaml` source files against their companion JSON schemas (`{blockName}Schema.json` or `schema.json`) to detect structural inconsistencies.

### What it checks

- Missing or extra properties in either file
- Top-level `type` mismatches
- `required` field differences
- Constraint mismatches (enum, const, etc.)
- Description drift (case-insensitive comparison)

### What it skips

- `$ref` path differences (YAML uses `.yaml`, JSON uses `.json` or `$defs`)
- `$defs` presence (JSON schemas commonly use `$defs` for ref indirection)

### Usage

```bash
# Auto-detect _sources/ directory
python tools/compare_schemas.py

# Specify _sources/ directory explicitly
python tools/compare_schemas.py --sources-dir _sources

# Use with a custom path
python tools/compare_schemas.py --sources-dir path/to/my/_sources
```

### Options

| Option | Description |
|--------|-------------|
| `--sources-dir PATH` | Path to `_sources/` directory (auto-detected if omitted) |

### Building block discovery

The tool recursively searches for `bblock.json` files under `_sources/`. Each directory containing `bblock.json` is treated as a building block. This works with both:

- **Flat layouts:** `_sources/myBlock/bblock.json`
- **Nested layouts:** `_sources/category/myBlock/bblock.json`

### Companion JSON detection

For each building block directory, the tool looks for the companion JSON schema in this order:

1. `{blockName}Schema.json` (e.g., `dataDownloadSchema.json`)
2. `{blockName}schema.json` (case variant)
3. `schema.json` (generic name)
4. Case-insensitive fallback

## Comparison: bblocks-postprocess vs these tools

| | bblocks-postprocess | resolve_schema.py |
|---|---|---|
| **Runs as** | Docker container | Standalone Python script |
| **Input** | Full repo build | Single schema file or building block name |
| **Output** | `build/annotated/` with remote `$ref` URLs | Fully-resolved, self-contained JSON Schema |
| **Remote refs** | Rewrites to absolute URLs | Resolves to inline definitions |
| **`bblocks://` refs** | Resolved via registry imports | Resolved locally via `bblocks-config.yaml` index |
| **Use case** | CI/CD pipeline, publishing | Local validation, tooling integration, inspection |

## Installation

Copy the `tools/` directory into your OGC building block repository:

```bash
cp -r tools/ /path/to/your-bblock-repo/tools/
pip install pyyaml
```

Or add to your existing `tools/` directory alongside other build scripts.
