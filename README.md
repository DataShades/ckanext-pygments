[![Tests](https://github.com/mutantsan/ckanext-pygments/workflows/Tests/badge.svg?branch=main)](https://github.com/mutantsan/ckanext-pygments/actions)

# ckanext-pygments

This extension provides a preview with syntax highlight for multiple text resources formats.

## Caching
There is a caching mechanism implemented in this extension. It is disabled by default. To enable it, set `ckanext.pygments.cache.enable` to `True`. You can also set the time to live for the cache in seconds with `ckanext.pygments.cache.ttl`. The default is 7200 seconds (2 hours). You can also set the maximum size of the resource to cache in bytes with `ckanext.pygments.cache.resouce_max_size`. The default is 20MB.

### Why cache is disabled by default?
We use Redis for caching and it uses memory. If you have a lot of resources and they are big, you can run out of memory. That's why it is disabled by default.
It's still debatable if we need cache at all. Big resource processed with pygments will be even bigger. So we can have a lot of memory usage. But if we have a lot of resources and many users access it, we can save a lot of time on processing.

## Config settings

Supported config options:

1. `ckanext.pygments.supported_formats` (optional, default: `sql html xhtml htm xslt py pyw pyi jy sage sc rs rs.in rst rest md markdown xml xsl rss xslt xsd wsdl wsf json jsonld yaml yml dtd php inc rdf ttl js`).
    Specify the list of supported formats.

2. `ckanext.pygments.max_size` (optional, default: `1048576`).
    Specify how many bytes we are going to render from file. Default to 1MB.
    Set to `-1` if you want to disable a limit. This can cause the page to load very slowly.

3. `ckanext.pygments.include_htmx_asset` (optional, default: `True`).
    Include HTMX asset in the page. Set to `False` if you want to include it yourself or another extension already includes it.

4. `ckanext.pygments.default_theme` (optional, default: `default`).
    Specify the default theme to use.

5. `ckanext.pygments.cache.enable` (optional, default: `False`).
    Enable caching of the rendered previews. Set to `True` to enable caching.

6. `ckanext.pygments.cache.ttl` (optional, default: `7200`).
    Specify the time to live for the cache in seconds.

7. `ckanext.pygments.cache.resouce_max_size` (optional, default: `20971520`).
    Specify the maximum size of the resource to cache in bytes.

## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
