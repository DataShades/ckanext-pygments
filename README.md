[![Tests](https://github.com/mutantsan/ckanext-pygments/workflows/Tests/badge.svg?branch=main)](https://github.com/mutantsan/ckanext-pygments/actions)

# ckanext-pygments

This extension provides a preview with syntax highlight for multiple resources formats

### TODO
- try to implement cache for preview to recalculate only styles. The structure could be pretty big so it must be taken into account.
 - this solves problem with big resources and remote resources
 - we must invalidate the cache on resources update/delete
- rewrite preview initialization with ajax to load page faster
- if caching does not fit us, think about **load more** button and ajax approach
- update doc to make it beautiful

## Config settings

Supported config options:

1. `ckanext.pygments.supported_formats` (optional, default: `sql html xhtml htm xslt py pyw pyi jy sage sc rs rs.in rst rest md markdown xml xsl rss xslt xsd wsdl wsf json jsonld yaml yml dtd php inc rdf ttl js`).
    Specify the list of supported formats.

2. `ckanext.pygments.max_size` (optional, default: `1048576`).
    Specify how many bytes we are going to render from file. Default to 1MB.
    Set to `-1` if you want to disable a limit. This can cause the page to load very slowly.

## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
