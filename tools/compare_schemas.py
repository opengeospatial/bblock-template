#!/usr/bin/env python3
"""
Compare schema.yaml against companion JSON schemas for each OGC building block.

Reports structural inconsistencies: missing/extra properties, type mismatches,
different constraints (required, enum, const), and description drift.

$ref paths are expected to differ (YAML -> .yaml, JSON -> .json or $defs)
and are not flagged as errors.

The script auto-discovers building blocks by recursively searching for
bblock.json files under the _sources directory. It supports both flat layouts
(_sources/myBlock/) and nested layouts (_sources/category/myBlock/).

Usage:
    python tools/compare_schemas.py
    python tools/compare_schemas.py --sources-dir _sources
    python tools/compare_schemas.py --sources-dir path/to/custom/_sources
"""

import json
import os
import sys

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml required. Install with: pip install pyyaml")
    sys.exit(1)


# Keys that are expected to differ between YAML and JSON representations
REF_KEYS = {"$ref"}
# Keys where minor wording changes are acceptable
DESCRIPTION_KEYS = {"description"}


def find_companion_json(block_dir, block_name):
    """Find the companion JSON schema for a building block.

    Looks for:
      1. {blockName}Schema.json  (e.g., dataDownloadSchema.json)
      2. {blockName}schema.json  (case variant)
      3. schema.json             (generic name)
      4. Case-insensitive fallback for {blockName}Schema.json
    """
    # Try {blockName}Schema.json / {blockName}schema.json
    for pattern in [
        f"{block_name}Schema.json",
        f"{block_name}schema.json",
    ]:
        candidate = os.path.join(block_dir, pattern)
        if os.path.exists(candidate):
            return candidate

    # Try generic schema.json
    generic = os.path.join(block_dir, "schema.json")
    if os.path.exists(generic):
        return generic

    # Case-insensitive fallback
    lower = f"{block_name}schema.json".lower()
    try:
        for f in os.listdir(block_dir):
            if f.lower() == lower:
                return os.path.join(block_dir, f)
    except OSError:
        pass

    return None


def find_building_blocks(sources_dir):
    """Discover all building blocks under sources_dir.

    Walks the directory tree looking for bblock.json files. Each directory
    containing bblock.json is treated as a building block. Works with both
    flat layouts (_sources/myBlock/) and nested layouts
    (_sources/category/myBlock/).

    Returns a sorted list of (display_name, block_dir, block_name) tuples.
    """
    blocks = []
    sources_dir = os.path.abspath(sources_dir)

    for root, dirs, files in os.walk(sources_dir):
        if "bblock.json" in files:
            block_dir = root
            block_name = os.path.basename(block_dir)
            # Create a display name showing path relative to sources_dir
            rel_path = os.path.relpath(block_dir, sources_dir)
            blocks.append((rel_path, block_dir, block_name))

    return sorted(blocks)


def compare_values(yaml_val, json_val, path):
    """Compare two schema values, returning a list of differences."""
    diffs = []

    if isinstance(yaml_val, dict) and isinstance(json_val, dict):
        diffs.extend(compare_dicts(yaml_val, json_val, path))
    elif isinstance(yaml_val, list) and isinstance(json_val, list):
        diffs.extend(compare_lists(yaml_val, json_val, path))
    elif yaml_val != json_val:
        diffs.append(f"  {path}: YAML={repr(yaml_val)} vs JSON={repr(json_val)}")

    return diffs


def compare_lists(yaml_list, json_list, path):
    """Compare two lists element by element."""
    diffs = []
    if len(yaml_list) != len(json_list):
        diffs.append(
            f"  {path}: array length differs: YAML={len(yaml_list)} vs JSON={len(json_list)}"
        )
    for i in range(min(len(yaml_list), len(json_list))):
        diffs.extend(compare_values(yaml_list[i], json_list[i], f"{path}[{i}]"))
    return diffs


def compare_dicts(yaml_dict, json_dict, path):
    """Compare two dicts, skipping $ref differences and noting structural issues."""
    diffs = []

    yaml_keys = set(yaml_dict.keys())
    json_keys = set(json_dict.keys())

    # If one side has a $ref, skip deep comparison (different ref styles expected)
    if "$ref" in yaml_keys or "$ref" in json_keys:
        # Both have $ref -- that's fine, paths will differ
        if "$ref" in yaml_keys and "$ref" in json_keys:
            return []
        # One has $ref, other is expanded or uses $defs -- note but don't error
        if "$ref" in yaml_keys and "$ref" not in json_keys:
            diffs.append(f"  {path}: YAML has $ref, JSON has inline definition")
            return diffs
        if "$ref" not in yaml_keys and "$ref" in json_keys:
            diffs.append(f"  {path}: JSON has $ref, YAML has inline definition")
            return diffs

    # Check for $defs in JSON (expected pattern for ref indirection)
    yaml_no_defs = {k: v for k, v in yaml_dict.items() if k != "$defs"}
    json_no_defs = {k: v for k, v in json_dict.items() if k != "$defs"}

    yaml_keys_compare = set(yaml_no_defs.keys())
    json_keys_compare = set(json_no_defs.keys())

    only_yaml = yaml_keys_compare - json_keys_compare
    only_json = json_keys_compare - yaml_keys_compare

    if only_yaml:
        for k in sorted(only_yaml):
            diffs.append(f"  {path}: property '{k}' in YAML only")
    if only_json:
        for k in sorted(only_json):
            diffs.append(f"  {path}: property '{k}' in JSON only")

    # Compare shared keys
    for key in sorted(yaml_keys_compare & json_keys_compare):
        child_path = f"{path}.{key}" if path else key
        y_val = yaml_dict[key]
        j_val = json_dict[key]

        # Skip description wording differences (flag only if one is missing)
        if key == "description" and isinstance(y_val, str) and isinstance(j_val, str):
            if y_val.strip().lower() != j_val.strip().lower():
                diffs.append(
                    f"  {child_path}: description differs:"
                    f"\n    YAML: {y_val[:80]}"
                    f"\n    JSON: {j_val[:80]}"
                )
            continue

        diffs.extend(compare_values(y_val, j_val, child_path))

    return diffs


def check_property_coverage(yaml_schema, json_schema, block_name):
    """High-level check: do both schemas define the same top-level properties?"""
    issues = []

    yaml_props = set((yaml_schema.get("properties") or {}).keys())
    json_props = set((json_schema.get("properties") or {}).keys())

    only_yaml = yaml_props - json_props
    only_json = json_props - yaml_props

    if only_yaml:
        issues.append(f"  Properties in YAML only: {sorted(only_yaml)}")
    if only_json:
        issues.append(f"  Properties in JSON only: {sorted(only_json)}")

    # Check top-level type
    if yaml_schema.get("type") != json_schema.get("type"):
        issues.append(
            f"  Top-level type: YAML={yaml_schema.get('type')} vs JSON={json_schema.get('type')}"
        )

    # Check required fields
    yaml_req = extract_required(yaml_schema)
    json_req = extract_required(json_schema)
    if yaml_req != json_req:
        only_y = yaml_req - json_req
        only_j = json_req - yaml_req
        if only_y:
            issues.append(f"  Required in YAML only: {sorted(only_y)}")
        if only_j:
            issues.append(f"  Required in JSON only: {sorted(only_j)}")

    return issues


def extract_required(schema):
    """Extract all required field names from a schema, including nested allOf/anyOf."""
    required = set(schema.get("required", []))
    for entry in schema.get("allOf", []):
        required.update(entry.get("required", []))
    return required


def _detect_sources_dir():
    """Auto-detect the _sources directory relative to the script or CWD."""
    # Relative to script location (tools/ lives next to _sources/)
    script_based = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_sources")
    if os.path.isdir(script_based):
        return script_based

    # Relative to CWD
    cwd_based = os.path.join(os.getcwd(), "_sources")
    if os.path.isdir(cwd_based):
        return cwd_based

    return script_based  # Fall back; will produce clear error later


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Compare schema.yaml against companion JSON schemas for OGC building blocks.",
    )
    parser.add_argument(
        "--sources-dir",
        default=None,
        help="Path to the _sources directory (auto-detected if omitted)",
    )
    args = parser.parse_args()

    sources_dir = args.sources_dir or _detect_sources_dir()
    sources_dir = os.path.abspath(sources_dir)

    if not os.path.isdir(sources_dir):
        print(f"ERROR: Sources directory not found: {sources_dir}", file=sys.stderr)
        sys.exit(1)

    blocks = find_building_blocks(sources_dir)
    if not blocks:
        print(f"No building blocks found in {sources_dir}", file=sys.stderr)
        sys.exit(1)

    total = 0
    checked = 0
    passed = 0
    failed = 0
    skipped_no_json = 0
    results = []

    for display_name, block_dir, block_name in blocks:
        total += 1
        yaml_path = os.path.join(block_dir, "schema.yaml")
        json_path = find_companion_json(block_dir, block_name)

        if not os.path.exists(yaml_path):
            results.append((display_name, "SKIP", ["No schema.yaml"]))
            continue

        if not json_path:
            skipped_no_json += 1
            continue

        checked += 1
        json_filename = os.path.basename(json_path)

        # Load both
        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                yaml_schema = yaml.safe_load(f)
        except Exception as e:
            results.append(
                (display_name, "ERROR", [f"YAML parse error: {e}"])
            )
            failed += 1
            continue

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                json_schema = json.load(f)
        except Exception as e:
            results.append(
                (
                    display_name,
                    "ERROR",
                    [f"JSON parse error ({json_filename}): {e}"],
                )
            )
            failed += 1
            continue

        # Compare
        issues = []
        issues.extend(check_property_coverage(yaml_schema, json_schema, block_name))
        issues.extend(compare_dicts(yaml_schema, json_schema, ""))

        if issues:
            results.append((display_name, "DIFF", issues))
            failed += 1
        else:
            results.append((display_name, "OK", []))
            passed += 1

    # Report
    print("=" * 70)
    print("OGC Building Block Schema Consistency Report")
    print(f"  schema.yaml vs companion JSON schema")
    print(f"  Sources: {sources_dir}")
    print("=" * 70)
    print(
        f"\nTotal blocks: {total} | Checked: {checked} | "
        f"Passed: {passed} | Differences: {failed} | "
        f"No JSON schema: {skipped_no_json}\n"
    )

    # Show passes
    ok_results = [r for r in results if r[1] == "OK"]
    if ok_results:
        print(f"--- CONSISTENT ({len(ok_results)}) ---")
        for name, status, _ in ok_results:
            print(f"  OK  {name}")
        print()

    # Show diffs
    diff_results = [r for r in results if r[1] in ("DIFF", "ERROR")]
    if diff_results:
        print(f"--- DIFFERENCES ({len(diff_results)}) ---")
        for name, status, issues in diff_results:
            print(f"\n  {status}  {name}")
            for issue in issues:
                print(f"    {issue}")
        print()

    if failed:
        print(f"\n{failed} building block(s) have inconsistencies.")
        return 1
    else:
        print("\nAll checked building blocks are consistent.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
