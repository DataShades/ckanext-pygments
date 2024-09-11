[![Tests](https://github.com/mutantsan/ckanext-pygments/workflows/Tests/badge.svg?branch=main)](https://github.com/mutantsan/ckanext-pygments/actions)

# ckanext-pygments

This extension provides a preview with syntax highlight for multiple text resources formats.

## Caching
There is a caching mechanism implemented in this extension. It is disabled by default. To enable it, set `ckanext.pygments.cache.enable` to `True`. You can also set the time to live for the cache in seconds with `ckanext.pygments.cache.ttl`. The default is 7200 seconds (2 hours). You can also set the maximum size of the resource to cache in bytes with `ckanext.pygments.cache.resouce_max_size`. The default is 20MB.

### Why cache is disabled by default?
We use Redis for caching and it uses memory. If you have a lot of resources and they are big, you can run out of memory. That's why it is disabled by default.
It's still debatable if we need cache at all. Big resource processed with pygments will be even bigger. So we can have a lot of memory usage. But if we have a lot of resources and many users access it, we can save a lot of time on processing.

### Admin configuration page
If you're using the [ckanext-admin-panel](https://github.com/mutantsan/ckanext-admin-panel) extension, you can configure the pygments settings from the admin panel.

![Configuration page](doc/config.png)

Otherwise, you can configure it in the `ckan.ini` file.

## Config settings

Supported config options:

```yaml
- key: ckanext.pygments.supported_formats
  type: list
  description: Specify a list of supported formats
  default: sql html xhtml htm xslt py pyw pyi jy sage sc rs rs.in rst rest md markdown xml xsl rss xslt xsd wsdl wsf json jsonld yaml yml dtd php inc rdf ttl js

- key: ckanext.pygments.max_size
  type: int
  description: Specify how many bytes we are going to render from file. Default to 1MB
  default: 1048576

- key: ckanext.pygments.include_htmx_asset
  description: Include HTMX asset
  default: true
  type: bool

- key: ckanext.pygments.default_theme
  description: Default theme for preview
  default: default

- key: ckanext.pygments.cache.enable
  description: Enable cache
  default: false
  type: bool

- key: ckanext.pygments.cache.preview_max_size
  description: Specify what is the maximum size of a preview we are going to cache
  default: 20971520 # 20MB
  type: int

- key: ckanext.pygments.cache.ttl
  description: Specify the time to live of the cache
  default: 7200 # 2 hours
  type: int
```

## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
