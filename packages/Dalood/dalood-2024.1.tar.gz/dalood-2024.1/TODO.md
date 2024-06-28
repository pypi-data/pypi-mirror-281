# TODO

# Development

* Add utilities to register common loaders via convenient patterns, e.g. extensions such as csv, json, yaml (e.g. `^(?!https?://).*\.yaml`).
* Investigate ways to compare different patterns by their specificity for the sake of ordering. For example, `http://*.json` should probably take precedence over `*.json`.

# Metadata

* Generate documentation with Sphinx.
* Replace source links with API documentation links in README.
* Add a usage section to the README.
* Add metadata with Prometa.
