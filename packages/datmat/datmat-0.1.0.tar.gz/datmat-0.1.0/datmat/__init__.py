from .ioplugin import IOPlugin, pull_source_data, push_sink_data, put_url, expand_url, materialize

# Import one plugin from the plugins to trigger the whole sub-package to be loaded
from . import plugins

__version__ = "0.1.0"


PLUGINS = IOPlugin.PLUGIN_MAP
