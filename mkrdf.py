from mkdocs.plugins import BasePlugin
from mkdocs.config import base, config_options as c
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files, File
from jinja2 import Environment
from rdflib import Graph
from jinja_rdf import register_filters
from jinja_rdf.graph_handling import GraphToFilesystemHelper
from loguru import logger


class MkRDFPluginConfig(base.Config):
    graph_file = c.Optional(c.File(exists=True))
    base_iri = c.Type(str, default="a default value")


class MkRDFPlugin(BasePlugin[MkRDFPluginConfig]):
    def on_files(self, files: Files, config: MkDocsConfig, **kwargs) -> Files | None:
        """Register a new file per resource"""
        logger.debug(self.config)
        g = Graph()
        g.parse(source=self.config.graph_file)

        for path, _ in GraphToFilesystemHelper(self.config.base_iri).graph_to_paths(g):
            logger.debug(path)
            files.append(
                File(
                    path=path,
                    src_dir=".",
                    dest_dir=config.site_dir,
                    use_directory_urls=config.use_directory_urls,
                )
            )
        return files

    def on_env(
        self, env: Environment, config: MkDocsConfig, files: Files, **kwargs
    ) -> Environment | None:
        """Register the jinja filters"""
        register_filters(env)
        return env

    def on_page_context(self, **kwargs):
        """Set the relevant variables for each page.
        Maybe we don't need it."""
        pass
