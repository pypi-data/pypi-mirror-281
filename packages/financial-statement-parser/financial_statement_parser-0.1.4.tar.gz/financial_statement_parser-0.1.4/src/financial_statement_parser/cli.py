import argparse

from .parser import process_file


def main():
    parser = argparse.ArgumentParser(
        description="Process financial statements and generate rolled-up data."
    )
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("-o", "--output", help="Path to the output file (optional)")

    args = parser.parse_args()

    process_file(args.input_file, args.output)


if __name__ == "__main__":
    main()
