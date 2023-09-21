# Profiles and BuildingBlocks

BuildingBlocks support two modes:
- composition
- profiling

[USAGE](USAGE.md) describes common aspects.  This document described profiling mechanisms.

**Profiles** allow all the underlying details of base standards to be automatically included in testing and validation - this _encapsulates_ the underlying complexity of base specifications.
 
This dramatically **simplifies** profiles in terms of both development and usage, and ensures **consistency** and conformance of profiles with base specifications.

In particular, if base specifications use the OGC BuildingBlocks then profiles can _leverage_ all the effort in design, testing and validation capabilities.

Thus profiles also use the same structures, so they can be profiled in turn.

## What is a profile?

A profile defines a set of constraints on a base specification. Implementations of profiles conform to the base specification.

Because many technologies like JSON and RDF are permissive (by default) about additional information being present, definition of an *extension* is effectively defining a *constraint* on how additional information should be represented.

## Profiles of profiles... 

Profiles can be designed as separate re-usable sets of constraints that can be reused - for example a time-series of water-quality monitoring observations could be specified as a profile of both a time-series profile of Observations and a water-quality profile for the results of such observations.
In turn the time-series profile could defined as data structure using GeoJSON, or Coverage JSON.  The water-quality content requirements could be described using constraints independent of the data structure.

## What forms of constraints are possible?

The **OGC BuildingBlock** model supports a range of possible constraint approaches.  The goal is to make such constraints **_machine-readable_** to the extent possible.

Constraints SHOULD be defined in a form that allows for **_validation_** of test cases and examples.

Built-in support is provided for automatic validation of the following forms:
- project metadata (description)
- well-formed example encoding (JSON, TTL)
- JSON schema (for JSON examples) for **structure**
- SHACL (Shapes Constraint Language for RDF) for **content** and **logical consistency**

In addition [custom validators](VALIDATORS) can be added to the validation workflow. 

Using a JSON-LD context "semantic uplift" of JSON to RDF supports use of SHACL and other forms of validators to 

## Testing

Test cases should be provided for each component part of a specification.  This requires a minimal conformant **base example** that the specific test case can be added to.

(Note consideration is being given to making such a baseline example resuable by reference instead of duplication, and potentially derived automatically from declared schema)

Testing should start by validating the **base example** passes all declared constraints, then for each profile constraint:
- identifying a set of valid cases that should conform to the constraint, testing each aspect
- creating a copy of the base under the **/tests/** folder with a name indicating which constraint and case is being tested - e.g. **my-building-block/tests/mything-property-b-number.json**
- adding the specific example to the example
- creating one or more failure tests with **-fail** file name endings - e.g. **my-building-block/tests/mything-property-b-number-fail.json**








