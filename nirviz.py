import dataclasses
import yaml
import re
import graphviz
import cairosvg
import nir
import typing
import importlib.util
import pathlib


@dataclasses.dataclass
class visualize:
    nir_graph: typing.Union[nir.NIRGraph, str, pathlib.Path]
    format: str = "svg"
    render_ipython: bool = True
    style_file = pathlib.Path("./style.yml")

    def __post_init__(self):
        if isinstance(self.nir_graph, (str, pathlib.Path)):
            self.nir_graph = nir.read(self.nir_graph)

        self.style_dict = self.__load_style_file()
        self.viz_graph = self.__construct_graph()

    def __load_style_file(self) -> typing.Dict[str, typing.Dict[str, str]]:
        with open(self.style_file, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def __pick_style(self, name: str) -> typing.Dict[str, str]:
        categories = self.style_dict['node-categories']
        for cat in categories:
            for p in cat['patterns']:
                regexp = re.compile(f"^{p}.*")
                if re.fullmatch(regexp, name.lower()):
                    return cat['style']
        return categories['defaults']['node']


    def __construct_graph(self) -> graphviz.Digraph:
        viz_graph = graphviz.Digraph(format=self.format,
                                     graph_attr={'rankdir': 'LR'})

        # Generate nodes
        for name in self.nir_graph.nodes.keys():
            style = self.__pick_style(name)
            viz_graph.node(name, **style)

        # Generate edges
        for src, tgt in self.nir_graph.edges:
            viz_graph.edge(src, tgt)

        return viz_graph



    def __repr__(self) -> str:
        if self.render_ipython and not importlib.util.find_spec("IPython") is None:
            import IPython

            svg_output = self.viz_graph.pipe(format="svg")

            if self.format == "svg":
                image = IPython.display.SVG(svg_output)
            elif self.format == "png":
                # Convert SVG to PNG using cairosvg
                png_output = cairosvg.svg2png(bytestring=svg_output)
                image = IPython.display.Image(png_output)
            else:
                raise ValueError(f"Unsupported format: {self.format}")
            IPython.display.display(image)

        return self.viz_graph.pipe(format=self.format, encoding="utf-8")
