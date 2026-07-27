# Security Notes for `<repository-name>` (OGC Blocks Register)

Thank you for helping protect the security, integrity, and trustworthiness of this OGC Blocks (bblocks) register.

This OGC Project adheres to the [OGC Vulnerability Reporting Policy](https://www.ogc.org/security/policy/). This repository authors and/or publishes an **OGC Blocks register** using the `bblocks-postprocess` tooling. Building a register can involve running code — see [Code Execution Surface](#code-execution-surface) — supplied by this repository's own transforms and plugins, or pulled in from other registers it imports.

## Repository Classification

| Dimension | Classification |
| --- | --- |
| Visibility | Public |
| Content Model | Mixed (schemas, documentation, and potentially executable transform/plugin code) |
| Primary Function | Trust / Registry (OGC Blocks) |
| Profile | `PUB-MIX-TRUST-PUBLIC-ARTIFACT` |
| Deployable Code | Potentially — see [Code Execution Surface](#code-execution-surface) |
| External User Impact | Public — register outputs (`register.json`, schemas, contexts, SHACL shapes, docs) are consumed directly by external tools and integrators |

## What This Repository Publishes

Depending on its contents, building this repository's register may produce, per block:

- a JSON Schema, annotated with resolved references and semantic properties;
- a JSON-LD context and SHACL shapes;
- examples and generated documentation;
- validation/test reports;
- and a `register.json` index, which other registers, client libraries, and tooling may depend on directly.

## What To Report

Please report any of the following:

- credentials, tokens, private keys, or other secrets committed to the repository (including in workflow files or `bblocks-config.yaml`);
- vulnerable, unsupported, or suspicious dependencies used by this repository's tooling or CI;
- insecure CI/CD workflow configuration (excessive permissions, unpinned actions, unreviewed secrets exposure);
- schema, SHACL, or JSON-LD content that could cause unsafe behavior in downstream consumers that build directly on this register's outputs;
- a transform, transform plugin, or validator plugin whose code appears malicious, backdoored, or unrelated to its stated purpose (see [Code Execution Surface](#code-execution-surface));
- an `imports` entry referencing an untrusted, unavailable, or unexpectedly-changed third-party register (see [Cross-Register Trust Boundary](#cross-register-trust-boundary));
- and any other issue affecting the trustworthiness of this register's published artifacts.

## How To Report

**Please do not report security vulnerabilities through public issues, discussions, or pull/merge requests.**

Please report suspected security issues by email to:

**security@ogc.org**

Alternatively, you can:

- create a [confidential issue](https://gitlab.ogc.org/security/vulnerability-reports/-/issues/new?issuable_template=new_vulnerability) in the OGC Vulnerability Reporting Tracker;
- <!-- delete this line if this repository does not use GitHub Advisories --> report a [vulnerability](https://github.com/<organization>/<repository>/security/advisories/new) directly via private vulnerability reporting on GitHub.

You can find more information about reporting and disclosure at the [OGC Security page](https://www.ogc.org/security/).

Reports sent to `security@ogc.org` may be processed through OGC's managed security case-handling workflow.

Please include:

- repository and register name;
- affected block identifier(s), file path, or transform/plugin/import declaration, if applicable;
- description of the issue and, where safe to share, reproduction steps;
- likely impact, including whether it could propagate to registers that `import` this one;
- and screenshots, logs, or excerpts where appropriate.

## Scope Notes

This repository may contain:

- block source files (schemas, `bblock.json`, examples, tests, transforms);
- JSON-LD contexts and SHACL shapes;
- `bblocks-config.yaml`, including `imports` and `plugins` declarations;
- CI/CD workflow files that build and publish the register;
- and generated build output where explicitly checked in.

This repository should not contain:

- service credentials, tokens, or private keys (including SPARQL push credentials — see below);
- unreviewed third-party transform/plugin code copied inline instead of referenced by a reviewed `pip`/`git+https` specifier;
- or live personal, member, or operational data used as example/test fixtures.

## Code Execution Surface

Building the register from this repository's sources *can* execute code declared in:

- **`transforms.yaml`** — inline `python`, `node`, `jq`, `xslt`, SPARQL, SHACL-AF, or `semantic-uplift` logic, run automatically against matching example snippets during postprocessing;
- **transform plugins** and **validator plugins** declared under `plugins.transforms` / `plugins.validators` in `bblocks-config.yaml` — installed via `pip`, which accepts arbitrary specifiers including `git+https://...` URLs, i.e. code from any source the plugin declaration points to;
- **cross-block `get_transformer` / `getTransformer` calls**, which can invoke a transform defined in a *different* block — including a block from an imported, potentially third-party register.

How and when this code runs depends on the environment:

- **In CI**, the postprocessor runs unattended: declared transforms and plugins execute automatically, with no confirmation step. A malicious or compromised transform or plugin therefore runs with whatever access the CI job has (secrets, network, write access to the publishing target); a slow or resource-heavy one can also inflate CI run time and cost.
- **Running locally** (for example via the provided Docker image), the tool asks for explicit confirmation before installing any plugin and before executing any Python or Node transform code.

Either way, plugin isolation — each transform/validator plugin runs in its own virtual environment — protects against dependency conflicts between plugins, not against malicious code. It does not limit what a plugin can do once it runs.

## Cross-Register Trust Boundary

`bblocks-config.yaml`'s `imports` list can reference **any** register URL, not only OGC-maintained registers. Once a register is imported:

- `bblocks://` references in schemas resolve to that register's annotated schemas,
- that register's JSON-LD context is inherited into this repository's assembled context,
- that register's SHACL shapes are inherited for validation,
- and any block in this repository can call transforms defined in that imported register.

OGC's review of this repository covers the content **authored in this repository**. It does not, by that fact alone, extend to the content, availability, or integrity of third-party registers this repository chooses to import — those are a supply-chain dependency and should be reviewed accordingly before being added or updated. Aliases such as `@org/register` are resolved via the OGC Blocks meta-register, a separate, PR-governed index; resolving an alias does not itself vouch for the target register's content.

## CI Credentials

If this repository enables SPARQL push (`sparql.push` in `bblocks-config.yaml`), the build workflow uses repository secrets (commonly `sparql_username` / `sparql_password`) to authenticate to the target endpoint. These credentials must never be placed in `bblocks-config.yaml` or any other version-controlled file, and access to them should be limited to maintainers who need it.

## Security Expectations for Contributors

Contributors and maintainers should:

- review any new or changed `transforms.yaml` entry, and any new `plugins.transforms` / `plugins.validators` declaration, with the same rigor as application code — these execute;
- review the source and maintainer of any `pip`/`git+https` plugin reference before adding or updating it;
- review any new `imports` entry for trustworthiness and maintenance status before adding it, and periodically re-check existing imports;
- never commit SPARQL push or other credentials — use repository/organization secrets;
- keep transform/plugin dependencies current and free of known-vulnerable versions;
- avoid broadening CI/CD workflow permissions beyond what postprocessing and publishing require;
- and escalate suspicious transform, plugin, or import content rather than silently removing or working around it.

## Out of Scope

The following are generally not security reports for this repository:

- ordinary schema, documentation, or content-modeling disagreements without a concrete security implication;
- feature requests for the `bblocks-postprocess` tooling unrelated to security (report those to the [bblocks-postprocess](https://github.com/opengeospatial/bblocks-postprocess) project instead);
- issues in a third-party register reached only through an `imports` chain, unless this repository's own choice to import it is the actual concern;
- social engineering, physical attacks, denial-of-service testing, or spam;
- and disruptive testing against live publishing infrastructure without approval.

## Coordinated Disclosure

OGC follows a Coordinated Vulnerability Disclosure process.

Please allow OGC a reasonable opportunity to investigate and remediate reported vulnerabilities before public disclosure. OGC will work collaboratively with researchers throughout the disclosure process.

## Safe Harbor

OGC supports good-faith security research.

OGC will not pursue legal action against individuals who:

- act in good faith,
- avoid privacy violations,
- avoid service disruption,
- avoid data destruction,
- promptly report discovered vulnerabilities, and
- comply with this policy.

## Response Targets

OGC aims to:

| Activity | Target |
| --- | --- |
| Acknowledge report | Within 3 business days |
| Initial assessment | Within 10 business days |
| Status updates | Approximately every 30 days |
| Resolution | As appropriate to the issue and its impact |

These are targets rather than guarantees.

## Recognition

OGC appreciates responsible disclosure. Researchers who responsibly disclose vulnerabilities may be publicly acknowledged with their consent.

## Related Documents

- [OGC Vulnerability Reporting Policy](https://www.ogc.org/security/policy/)
- [OGC Security page](https://www.ogc.org/security/)
- [OGC Blocks postprocessor](https://github.com/opengeospatial/bblocks-postprocess)
