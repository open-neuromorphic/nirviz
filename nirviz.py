import dataclasses
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

    def __post_init__(self):
        if isinstance(self.nir_graph, (str, pathlib.Path)):
            self.nir_graph = nir.read(self.nir_graph)

        self.digraph = graphviz.Digraph(format=self.format)
        for name in self.nir_graph.nodes.keys():
            self.digraph.node(name)
        for src, tgt in self.nir_graph.edges:
            self.digraph.edge(src, tgt)

    def __repr__(self) -> str:
        if self.render_ipython and not importlib.util.find_spec("IPython") is None:
            import IPython

            svg_output = self.digraph.pipe(format="svg")

            if self.format == "svg":
                image = IPython.display.SVG(svg_output)
            elif self.format == "png":
                # Convert SVG to PNG using cairosvg
                png_output = cairosvg.svg2png(bytestring=svg_output)
                image = IPython.display.Image(png_output)
            else:
                raise ValueError(f"Unsupported format: {self.format}")
            IPython.display.display(image)

        return self.digraph.pipe(format=self.format, encoding="utf-8")
