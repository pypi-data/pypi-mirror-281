"""Random values workflow plugin module"""

import re
import shlex
import unicodedata
from collections import OrderedDict
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from subprocess import run
from time import time
from uuid import uuid4
from xml.etree.ElementTree import (
    Element,
    SubElement,
    tostring,
)

import validators.url
from cmem.cmempy.dp.proxy.graph import get, get_graph_import_tree, post_streamed
from cmem.cmempy.workspace.projects.resources.resource import create_resource
from cmem_plugin_base.dataintegration.context import ExecutionContext
from cmem_plugin_base.dataintegration.description import Icon, Plugin, PluginParameter
from cmem_plugin_base.dataintegration.entity import (
    Entities,
    Entity,
    EntityPath,
    EntitySchema,
)
from cmem_plugin_base.dataintegration.parameter.choice import ChoiceParameterType
from cmem_plugin_base.dataintegration.parameter.graph import GraphParameterType
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin
from cmem_plugin_base.dataintegration.types import BoolParameterType, StringParameterType
from cmem_plugin_base.dataintegration.utils import setup_cmempy_user_access
from defusedxml import minidom
from pathvalidate import validate_filename

from . import __path__

ROBOT = Path(__path__[0]) / "bin" / "robot.jar"
REASONERS = OrderedDict(
    {
        "elk": "ELK",
        "emr": "Expression Materializing Reasoner",
        "hermit": "HermiT",
        "jfact": "JFact",
        "structural": "Structural Reasoner",
        "whelk": "Whelk",
    }
)


def convert_iri_to_filename(value: str) -> str:
    """Convert IRI to filename"""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"\.", "_", value.lower())
    value = re.sub(r"/", "_", value.lower())
    value = re.sub(r"[^\w\s-]", "", value.lower())
    value = re.sub(r"[-\s]+", "-", value).strip("-_")
    return value + ".nt"


@Plugin(
    label="Validate ontology consistency",
    description="",
    documentation="""""",
    icon=Icon(package=__package__, file_name="obofoundry.png"),
    parameters=[
        PluginParameter(
            param_type=GraphParameterType(classes=["http://www.w3.org/2002/07/owl#Ontology"]),
            name="ontology_graph_iri",
            label="Ontology_graph_IRI",
            description="The IRI of the input ontology graph.",
        ),
        PluginParameter(
            param_type=ChoiceParameterType(REASONERS),
            name="reasoner",
            label="Reasoner",
            description="Reasoner option.",
            default_value="elk",
        ),
        PluginParameter(
            param_type=BoolParameterType(),
            name="write_md",
            label="Write Markdown explanation file",
            description="Write Markdownn file with explanation to project.",
            default_value=False,
        ),
        PluginParameter(
            param_type=BoolParameterType(),
            name="produce_graph",
            label="Produce output graph",
            description="Produce graph with explanation.",
            default_value=False,
        ),
        PluginParameter(
            param_type=StringParameterType(),
            name="output_graph_iri",
            label="Output graph IRI",
            description="The IRI of the output graph for the inconsistency validation.",
        ),
        PluginParameter(
            param_type=StringParameterType(),
            name="md_filename",
            label="Output filename",
            description="The filename of the Markdown file with the explanation of "
            "inconsistencies.",
        ),
        PluginParameter(
            param_type=BoolParameterType(),
            name="stop_at_inconsistencies",
            label="Stop at inconsistencies",
            description="Raise an error if inconsistencies are found. If enabled, the plugin does "
            "not output entities.",
            default_value=False,
        ),
    ],
)
class ValidatePlugin(WorkflowPlugin):
    """Example Workflow Plugin: Random Values"""

    def __init__(  # noqa: PLR0913
        self,
        ontology_graph_iri: str = "",
        reasoner: str = "elk",
        produce_graph: bool = False,
        output_graph_iri: str = "",
        write_md: bool = False,
        md_filename: str = "",
        stop_at_inconsistencies: bool = False,
    ) -> None:
        errors = ""
        if not validators.url(ontology_graph_iri):
            errors += "Invalid IRI for parameter Ontology graph IRI. "
        if reasoner not in REASONERS:
            errors += "Invalid value for parameter Reasoner. "
        if produce_graph and not validators.url(output_graph_iri):
            errors += "Invalid IRI for parameter Output graph IRI. "
        if write_md:
            try:
                validate_filename(md_filename)
            except:  # noqa: E722
                errors += "Invalid filename for parameter Output filename. "
        if errors:
            raise ValueError(errors[:-1])

        self.ontology_graph_iri = ontology_graph_iri
        self.reasoner = reasoner
        self.produce_graph = produce_graph
        self.output_graph_iri = output_graph_iri
        self.write_md = write_md
        self.stop_at_inconsistencies = stop_at_inconsistencies
        self.temp = f"robot_{uuid4().hex}"
        self.md_filename = md_filename if md_filename and write_md else "mdfile.md"

    def create_xml_catalog_file(self, graphs: dict) -> None:
        """Create XML catalog file"""
        file_name = Path(self.temp) / "catalog-v001.xml"
        catalog = Element("catalog")
        catalog.set("prefer", "public")
        catalog.set("xmlns", "urn:oasis:names:tc:entity:xmlns:xml:catalog")
        for i, graph in enumerate(graphs):
            uri = SubElement(catalog, "uri")
            uri.set("id", f"id{i}")
            uri.set("name", graph)
            uri.set("uri", graphs[graph])
        reparsed = minidom.parseString(tostring(catalog, "utf-8")).toxml()
        with Path(file_name).open("w", encoding="utf-8") as file:
            file.truncate(0)
            file.write(reparsed)

    def get_graphs(self, graphs: dict, context: ExecutionContext) -> None:
        """Get graphs from CMEM"""
        if not Path(self.temp).exists():
            Path(self.temp).mkdir(parents=True)
        for graph in graphs:
            with (Path(self.temp) / graphs[graph]).open("w", encoding="utf-8") as file:
                setup_cmempy_user_access(context.user)
                file.write(get(graph).text)

    def get_graphs_tree(self) -> dict:
        """Get graph import tree"""
        graphs = {self.ontology_graph_iri: convert_iri_to_filename(self.ontology_graph_iri)}
        tree = get_graph_import_tree(self.ontology_graph_iri)
        for value in tree["tree"].values():
            for iri in value:
                if iri not in graphs:
                    graphs[iri] = convert_iri_to_filename(iri)
        return graphs

    def validate(self, graphs: dict) -> None:
        """Reason"""
        data_location = f"{self.temp}/{graphs[self.ontology_graph_iri]}"
        utctime = str(datetime.fromtimestamp(int(time()), tz=UTC))[:-6].replace(" ", "T") + "Z"

        cmd = (
            f'java -XX:MaxRAMPercentage=15 -jar {ROBOT} merge --input "{data_location}" '
            f"explain --reasoner {self.reasoner} -M inconsistency "
            f'--explanation "{self.temp}/{self.md_filename}"'
        )

        if self.produce_graph:
            cmd += (
                f' annotate --ontology-iri "{self.output_graph_iri}" '
                f'--language-annotation rdfs:label "Ontology Validation Result {utctime}" en '
                f"--language-annotation rdfs:comment "
                f'"Ontology validation of <{self.ontology_graph_iri}>" en '
                f"--language-annotation prov:wasGeneratedBy "
                f'"cmem-plugin-validate ({self.reasoner})" en '
                f'--link-annotation prov:wasDerivedFrom "{self.ontology_graph_iri}" '
                f'--typed-annotation dc:created "{utctime}" xsd:dateTime '
                f'--output "{self.temp}/output.ttl"'
            )

        response = run(shlex.split(cmd), check=False, capture_output=True)  # noqa: S603
        if response.returncode != 0:
            if response.stdout:
                raise OSError(response.stdout.decode())
            if response.stderr:
                raise OSError(response.stderr.decode())
            raise OSError("ROBOT error")

    def send_output_graph(self) -> None:
        """Send result graph"""
        post_streamed(
            self.output_graph_iri,
            str(Path(self.temp) / "output.ttl"),
            replace=True,
            content_type="text/turtle",
        )

    def make_resource(self, context: ExecutionContext) -> None:
        """Make MD resource in project"""
        create_resource(
            project_name=context.task.project_id(),
            resource_name=self.md_filename,
            file_resource=(Path(self.temp) / self.md_filename).open("r"),
            replace=True,
        )

    def clean_up(self, graphs: dict) -> None:
        """Remove temporary files"""
        files = ["catalog-v001.xml", "output.ttl", self.md_filename]
        files += list(graphs.values())
        for file in files:
            try:
                (Path(self.temp) / file).unlink()
            except (OSError, FileNotFoundError) as err:
                self.log.warning(f"Cannot remove file {file} ({err})")
        try:
            Path(self.temp).rmdir()
        except (OSError, FileNotFoundError) as err:
            self.log.warning(f"Cannot remove directory {self.temp} ({err})")

    def execute(
        self,
        inputs: Sequence[Entities],  # noqa: ARG002
        context: ExecutionContext,
    ) -> Entities | None:
        """Run the workflow operator."""
        setup_cmempy_user_access(context.user)
        graphs = self.get_graphs_tree()
        self.get_graphs(graphs, context)
        self.create_xml_catalog_file(graphs)
        self.validate(graphs)

        text = (Path(self.temp) / self.md_filename).read_text()
        if text == "No explanations found.":
            self.clean_up(graphs)
            return None

        if self.produce_graph:
            setup_cmempy_user_access(context.user)
            self.send_output_graph()

        if self.write_md:
            setup_cmempy_user_access(context.user)
            self.make_resource(context)

        self.clean_up(graphs)

        if self.stop_at_inconsistencies:
            raise RuntimeError("Inconsistencies found in Ontology.")

        entities = [
            Entity(
                uri="https://eccenca.com/plugin_validateontology/md",
                values=[[text]],
            )
        ]
        schema = EntitySchema(
            type_uri="https://eccenca.com/plugin_validateontology/text",
            paths=[EntityPath(path="text")],
        )
        return Entities(entities=iter(entities), schema=schema)
