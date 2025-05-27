from mkdocs.plugins import BasePlugin
from mkdocs.config import base, config_options as c, MkDocsConfig
from mkdocs.structure.files import Files
from jinja2 import Environment
from rdflib import Graph
from jinja-rdf import register_filters

class MkRDFPluginConfig(base.Config):
    graph_file = c.Optional(c.File(exists=True))
    base_iri = c.Type(str, default='a default value')

class MkRDFPlugin(BasePlugin[MkRDFPluginConfig]):
    def on_files(self, files: Files, config: MkDocsConfig, **kwargs) -> Files | None:
        """Register a new file per resource"""
        g = Graph()
        g.parse(source=config.graph_file)
        g
        return files

    def on_env(self, env: Environment, config: MkDocsConfig, files: Files, **kwargs) -> Environment | None:
        """Register the jinja filters"""
        register_filters(env)
        return env

    def on_page_context(self, **kwargs):
        """Set the relevant variables for each page.
        Maybe we don't need it."""
        pass
