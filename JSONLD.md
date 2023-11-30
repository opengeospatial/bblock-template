# JSON-LD (Semantic Uplift)

Building Blocks defining JSON schemas can be annotated with JSON-LD contexts using the file _context.jsonld_

This: 

1. Maps JSON elements to URIs (which can be URIs of a richer semantic model)
2. Allows validation of complex logical constraints using SHACL Rules to [validate examples](TESTING.md#SHACL)
3. [Perform transforms](TXFORMS.md) to any other RDF model and validate results

## Modularity support

JSON-LD contexts are very complex and hard to debug if the schema is at all complex.  

The Building Blocks design allows automatic combination of contexts based on the schema re-use patterns.

## Context design

_TBD: document local contexts and use of @base mappings. _ 
