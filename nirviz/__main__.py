import argparse
import sys

import nirviz

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI tool for visualizing NIR graphs.")
    parser.add_argument("file", type=argparse.FileType('r'), help="The NIR graph file to read from.")
    parser.add_argument("output", type=str, default="stdout", nargs='?', help="The output file to write the graph to. Defaults to stdout.")
    parser.add_argument("--yaml", type=str, default=None, help="Style file defined in yaml. Defaults to the bundled style file.")

    args = parser.parse_args()

    nir_file = args.file.name
    yaml_file = args.yaml
    # Load the NIR graph
    if args.output == "stdout":
        graph = nirviz.visualize(nir_file, style_file=yaml_file)
        graph_svg = str(graph)
        sys.stdout.write(graph_svg)
    elif args.output.endswith(".svg"):
        graph = nirviz.visualize(nir_file, style_file=yaml_file)
        graph_svg = str(graph)
        with open(args.output, "w") as f:
            f.write(graph_svg)
    elif args.output.endswith(".png"):
        graph = nirviz.visualize(nir_file, style_file=yaml_file)
        graph_image = graph.to_image()
        graph_image.save(args.output)

    else:
        raise ValueError("Output file must be either .svg or .png format.")
