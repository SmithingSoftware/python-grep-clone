import os
import sys

from argparse import ArgumentParser
from pathlib import Path

exits = {
    "INVALID_PATH": 1,
}

verbose = False


def setup():
    global verbose
    argparser = ArgumentParser()
    argparser.add_argument("pattern", help="Pattern to search for", type=str)
    argparser.add_argument("directory", help="Directory to search", type=str)
    argparser.add_argument(
        "-v", "--verbose", required=False, default=False, action="store_true"
    )
    args = argparser.parse_args()
    verbose = args.verbose

    return {
        "verbose": args.verbose,
        "pattern": args.pattern,
        "directory": args.directory,
    }


def search(pattern: str, path: Path):
    if verbose:
        print(f"searching path: {p}")
    line_no = 1
    results = []
    with path.open("r") as f:
        for line in f.readlines():
            if pattern in line:
                results.append((path, line_no, line))
            line_no += 1
    if verbose:
        print(f"found {len(results)} in {path}")
    return results


def traverse_and_search(pattern, path, search_fn):
    found = []
    for p in path.glob("**/*"):
        if p.is_file():
            results = search_fn(pattern, p)
            if results:
                found.extend(results)
    return found


def print_results(results):
    for result in results:
        print(f"{result[0]}:{result[1]} -> {result[2]}")


def main():
    config = setup()
    path = Path(config["directory"])
    if not path.exists():
        print("Path did not exist!")
        sys.exit(exits["INVALID_PATH"])

    results = traverse_and_search(config["pattern"], path, search)
    print_results(results)


if __name__ == "__main__":
    main()
