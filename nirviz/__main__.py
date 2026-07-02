import argparse
import sys

import nirviz

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI tool for visualizing NIR graphs.")
    parser.add_argument("file", type=argparse.FileType('r'), help="The NIR graph file to read from.")

    parser.add_argument("output", type=str, default="stdout", nargs='?', help="The output file to write the graph to. Defaults to stdout.")
    parser.add_argument("--orientation", choices=["horizontal", "vertical"], default="horizontal", help="Set orientation to 'horizontal' or 'vertical' (default: horizontal).")
    parser.add_argument("--yaml", type=str, default=None, help="Style file defined in yaml. Defaults to the bundled style file.")

    args = parser.parse_args()

    nir_file = args.file.name
    yaml_file = args.yaml
    orientation = args.orientation
    # Load the NIR graph
    graph = nirviz.visualize(nir_file, style_file=yaml_file, orientation=orientation)
    if args.output == "stdout":
        sys.stdout.write(str(graph))
    elif args.output.endswith(".svg") or args.output.endswith(".png"):
        graph.save(args.output)
    else:
        raise ValueError("Output file must be either .svg or .png format.")
