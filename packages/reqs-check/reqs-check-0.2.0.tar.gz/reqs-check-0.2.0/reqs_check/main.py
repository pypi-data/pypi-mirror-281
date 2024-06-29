import argparse
import logging
from tabulate import tabulate
from .diff import compare_requirements, filter_differences, highlight_differences
from .duplicates import find_duplicates

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")


def main():
    parser = argparse.ArgumentParser(
        description="Check and compare multiple requirements.txt files."
    )
    parser.add_argument(
        "files",
        metavar="F",
        type=str,
        nargs="+",
        help="Paths to the requirements.txt files",
    )
    parser.add_argument(
        "--only-diff",
        action="store_true",
        help="Only show packages with differing versions",
    )
    parser.add_argument(
        "--find-duplicates",
        action="store_true",
        help="Find duplicate packages in the requirements files",
    )

    args = parser.parse_args()

    if args.find_duplicates:
        all_duplicates = find_duplicates(args.files)
        if all_duplicates:
            for file, duplicates in all_duplicates.items():
                print(f"Duplicates in {file}:")
                for pkg, vers in duplicates.items():
                    print(f"  {pkg}:")
                    for ver, line_num in vers:
                        print(f"    - {ver} (line {line_num})")
                print()
            exit(1)
        else:
            print("No duplicate packages found.")
            exit(0)
    try:
        if len(args.files) == 1:
            logging.error("Please provide more than one file to compare.")
            exit(0)
        comparison_df = compare_requirements(args.files)
    except FileNotFoundError as e:
        logging.error(e)
        return

    if args.only_diff:
        comparison_df = filter_differences(comparison_df)
    highlighted_df = highlight_differences(comparison_df)

    logging.info("\n" + tabulate(highlighted_df, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    main()
