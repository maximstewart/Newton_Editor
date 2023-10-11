# Python imports
import os
import json
from os.path import join

# Lib imports

# Application imports




class ManifestProcessor(Exception):
    ...


class Plugin:
    path: str       = None
    name: str       = None
    author: str     = None
    version: str    = None
    support: str    = None
    requests:{}     = None
    reference: type = None


class ManifestProcessor:
    def __init__(self, path, builder):
        manifest = join(path, "manifest.json")
        if not os.path.exists(manifest):
            raise Exception("Invalid Plugin Structure: Plugin doesn't have 'manifest.json'. Aboarting load...")

        self._path    = path
        self._builder = builder
        with open(manifest) as f:
            data           = json.load(f)
            self._manifest = data["manifest"]
            self._plugin   = self.collect_info()

    def collect_info(self) -> Plugin:
        plugin          = Plugin()
        plugin.path     = self._path
        plugin.name     = self._manifest["name"]
        plugin.author   = self._manifest["author"]
        plugin.version  = self._manifest["version"]
        plugin.support  = self._manifest["support"]
        plugin.requests = self._manifest["requests"]

        return plugin

    def get_loading_data(self):
        loading_data = {}
        requests     = self._plugin.requests
        keys         = requests.keys()

        if "pass_events" in keys:
            if requests["pass_events"] in ["true"]:
                loading_data["pass_events"] = True

        if "bind_keys" in keys:
            if isinstance(requests["bind_keys"], list):
                loading_data["bind_keys"] = requests["bind_keys"]

        if "pass_ui_objects" in keys:
            if isinstance(requests["pass_ui_objects"], list):
                loading_data["pass_ui_objects"] = [ self._builder.get_object(obj) for obj in requests["pass_ui_objects"] ]

        return self._plugin, loading_data
