# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SSE(Component):
    """A SSE component.
The SSE component makes it possible to collect data from e.g. a ResponseStream. It's a wrapper around the SSE.js library.
https://github.com/mpetazzoni/sse.js

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- concat (boolean; default True):
    A boolean indicating if the stream values should be concatenated.

- done (boolean; optional):
    A boolean indicating if the (current) stream has ended.

- options (dict; optional):
    Options passed to the SSE constructor.
    https://github.com/mpetazzoni/sse.js?tab=readme-ov-file#options-reference.

    `options` is a dict with keys:

    - debug (boolean; optional)

    - headers (dict; optional)

    - method (string; optional)

    - payload (dict; optional)

    - start (boolean; optional)

    - withCredentials (boolean; optional)

- url (string; optional):
    URL of the endpoint.

- value (string; optional):
    The data value. Either the latest, or the concatenated dependenig
    on the `concat` property."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_extensions'
    _type = 'SSE'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, options=Component.UNDEFINED, url=Component.UNDEFINED, concat=Component.UNDEFINED, value=Component.UNDEFINED, done=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'concat', 'done', 'options', 'url', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'concat', 'done', 'options', 'url', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(SSE, self).__init__(**args)
