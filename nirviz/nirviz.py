from dataclasses import dataclass
import yaml
import re
import graphviz
import cairosvg
import nir
import typing
import importlib.util
import importlib.resources
import pathlib
import PIL
import io


@dataclass
class visualize:
    nir_graph: typing.Union[nir.NIRGraph, str, pathlib.Path]
    style_file: typing.Optional[pathlib.Path] = None

    def __post_init__(self):
        if isinstance(self.nir_graph, (str, pathlib.Path)):
            self.nir_graph = nir.read(self.nir_graph)

        if self.style_file is not None and not isinstance(self.style_file, pathlib.Path):
            self.style_file = pathlib.Path(self.style_file)

        self.style_dict = self.__load_style_file()
        self.viz_graph = self.__construct_graph()

    def __load_style_file(self) -> typing.Dict[str, typing.Dict[str, str]]:
        if self.style_file is None:
            with importlib.resources.files('nirviz').joinpath('style.yml').open('r') as f:
                config = yaml.safe_load(f)
        else:
            with open(self.style_file, 'r') as f:
                config = yaml.safe_load(f)
        return config

    def __pick_style(self, name: str) -> typing.Dict[str, str]:
        categories = self.style_dict['node-categories']
        for cat_id in categories:
            cat = categories[cat_id]
            if name in cat['patterns']:
                return cat['style']

        return self.style_dict['defaults']['node']['style']


    def __construct_graph(self) -> graphviz.Digraph:
        viz_graph = graphviz.Digraph(format="svg",
                                     graph_attr={'rankdir': 'LR'})
        # Generate nodes
        for node_id in self.nir_graph.nodes:
            name = type(self.nir_graph.nodes[node_id]).__name__
            style = self.__pick_style(name)
            viz_graph.node(node_id, label=name, **style)

        # Generate edges
        for src_id, tgt_id in self.nir_graph.edges:
            viz_graph.edge(src_id, tgt_id)

        return viz_graph

    def show(self) -> None:
        if importlib.util.find_spec("IPython"):
            import IPython

            svg_output = self.viz_graph.pipe(format="svg")
            image = IPython.display.SVG(svg_output)
            IPython.display.display(image)
        else:
            print("error: cannot display graph: no IPython environment detected.")

    def to_image(self) -> PIL.Image.Image:
        svg_output = self.viz_graph.pipe(format="svg")
        png_bytes = cairosvg.svg2png(bytestring=svg_output)
        return PIL.Image.open(io.BytesIO(png_bytes))

    def __repr__(self) -> str:
        return self.viz_graph.pipe(format="svg", encoding="utf-8")
