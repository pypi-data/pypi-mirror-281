import copy
import importlib.metadata
import pathlib

import anywidget
import traitlets

try:
    __version__ = importlib.metadata.version("widget_dropdown")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

DEFAULT_OPTIONS = [{"text": "No options", "value": "", "disabled": True}]


class DropdownWidget(anywidget.AnyWidget):
    """
    A Jupyter widget that displays a dropdown menu.

    Dropdown entries are represented by a dictionary with the following
    structure:

    .. code-block:: python

        {"text": text, "value": value, "disabled": True/False}

    where the value can be a custom python object. These values are not
    used in the javascript frontend, which just tracks the selected index.

    Entries can be grouped under a common title:

    .. code-block:: python

        {
            "group": "Group 1",
            "options": [
                {"text": "Option 1", "value": value1, "disabled": False},
                {"text": "Option 2", "value": value2, "disabled": True},
            ],
        }

    """

    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"

    # options traitlet is not synced to js, as it can contain non-serializable values
    options = traitlets.List([])

    # values are removed in _options_js and it is synced to js
    _options_js = traitlets.List([]).tag(sync=True)

    index = traitlets.Int(0).tag(sync=True)
    disabled = traitlets.Bool(False).tag(sync=True)

    value = traitlets.Any()

    def __init__(self, options=None, **kwargs):
        """Method to create the widget.

        The traitlets defined above can be set as a kwargs.
        """
        super().__init__(**kwargs)

        if options is None:
            options = DEFAULT_OPTIONS

        self.values = []
        self.options = options

    @traitlets.observe("options")
    def _observe_options(self, change):
        self.values = []
        temp_options = copy.deepcopy(change.new)
        self._parse_values(temp_options)
        self._options_js = temp_options

    def _parse_values(self, options):
        """
        Extract values from the input dict into self.values
        and deletes them from the original dict.
        """
        for opt in options:
            if "group" in opt:
                self._parse_values(opt["options"])
            else:
                self.values.append(opt["value"])
                del opt["value"]

    @traitlets.observe("index")
    def _observe_index(self, change):
        self.value = self.values[change.new]

    @traitlets.observe("value")
    def _observe_value(self, change):
        self.index = self.values.index(change.new)
