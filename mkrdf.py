from mkdocs.plugins import BasePlugin
from mkdocs.config import base, config_options as c
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files, File
from jinja2 import Environment
from rdflib import Graph
from jinja_rdf import register_filters
from jinja_rdf.graph_handling import GraphToFilesystemHelper
from loguru import logger


def get_content(resource_iri, path):
    return f"""## {{{{ {path} | upper }}}}
iri: `{resource_iri}`
name: {path}
"""


class MkRDFPluginConfig(base.Config):
    graph_file = c.Optional(c.File(exists=True))
    base_iri = c.Type(str, default="a default value")


class MkRDFPlugin(BasePlugin[MkRDFPluginConfig]):
    def on_files(self, files: Files, config: MkDocsConfig, **kwargs) -> Files | None:
        """Register a new file per resource"""
        g = Graph()
        g.parse(source=self.config.graph_file)

        for resource_iri, path, _ in GraphToFilesystemHelper(
            self.config.base_iri
        ).graph_to_paths(g):
            logger.debug(f'Append file for iri: "{resource_iri}" at path: "{path}"')
            content = get_content(resource_iri, path)
            files.append(
                File.generated(config=config, src_uri=path + ".md", content=content)
            )
        return files

    def on_env(
        self, env: Environment, config: MkDocsConfig, files: Files, **kwargs
    ) -> Environment | None:
        """Register the jinja filters"""
        register_filters(env)
        return env

    # def on_page_context(self, **kwargs):
    #     """Set the relevant variables for each page.
    #     Maybe we don't need it."""
    #     pass
