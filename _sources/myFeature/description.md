## Custom Feature Type 

This building block illustrates a typical "Feature Type" - where an object is modelled as a "Feature with geometry", but has its own "native schema" - or "domain model".

This is an **interoperable** approach to defining a Feature, allowing re-use of a well-defined domain model.

i.e. the attributes (properties) are managed independently of the packaging container (Feature) 

the **mySchema" building block is referenced by this container, complete with an example of semantic annotations for the domain model.  It may inherit reusable sub-components using the same mechanisms - after all there is usually a lot in common across a range of FeatureTypes in any environment.  

This building block **inherits** reusable semantic annotations from a common library, simplifying implementation. 



