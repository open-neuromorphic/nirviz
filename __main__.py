import argparse
import sys

import nirviz

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI tool for visualizing NIR graphs.")
    parser.add_argument("file", type=argparse.FileType('r'), help="The NIR graph file to read from.")
    parser.add_argument("output", type=str, default="stdout", nargs='?', help="The output file to write the graph to. Defaults to stdout.")
    args = parser.parse_args()

    # Load the NIR graph
    if args.output == "stdout":
        graph = nirviz.visualize(args.file, format="svg", render_ipython=False)
        sys.stdout.write(graph)
    elif args.output.endswith(".svg"):
        graph = nirviz.visualize(args.file, format="svg", render_ipython=False)
        with open(args.output, "w") as f:
            f.write(graph)
    elif args.output.endswith(".png"):
        graph = nirviz.visualize(args.file, format="png", render_ipython=False)
        with open(args.output, "wb") as f:
            f.write(graph)
    else:
        raise ValueError("Output file must be either .svg or .png format.")