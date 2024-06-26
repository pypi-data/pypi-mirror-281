import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pytz

from .config import OUTPUT_BASE_DIR

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def format_currency(value: float) -> str:
    """Formats a number into a currency string with a dollar sign and commas."""
    return f"${value:,.0f}"


def parse_line(line: str) -> Tuple[str, Optional[float]]:
    """Extracts the label and value from a line if it contains a monetary value."""
    parts = line.strip().split("=", 1)
    label = parts[0].strip().strip("-").strip()

    if len(parts) < 2:
        return label, None

    value = re.sub(r"[^\d.-]", "", parts[1].strip())

    try:
        return label, float(value) if value else None
    except ValueError:
        return label, None


def add_to_tree(tree: Dict[str, Any], path: list, value: float) -> None:
    """Adds or updates values in the tree at the specified path."""
    current = tree
    for level in path[:-1]:
        current = current.setdefault(level, {})

    last_level = path[-1]
    if isinstance(current.get(last_level), dict):
        return

    current[last_level] = current.get(last_level, 0) + value


def roll_up_values(tree: Dict[str, Any]) -> float:
    """Recursively sums the values from children to their parent nodes in the tree."""
    total = 0.0
    for key, value in tree.items():
        if isinstance(value, dict):
            child_total = roll_up_values(value)
            value["_total"] = child_total
            total += child_total
        else:
            total += float(value)
    return total


def get_indent_depth(line: str) -> int:
    """
    Calculate indentation level, considering both spaces and tabs.
    Tabs are counted as 4 spaces.
    """
    indent = 0
    for char in line:
        if char == " ":
            indent += 1
        elif char == "\t":
            # Round up to the next multiple of 4
            indent = (indent + 4) & ~3
        else:
            break
    return indent // 4


def parse_and_roll_up(filename: str) -> Dict[str, Any]:
    tree: Dict[str, Any] = {}
    path: List = []
    with open(filename, "r") as file:
        for line in file:
            if line.strip().endswith("#ignore") or not line.strip():
                continue

            depth = get_indent_depth(line)
            label, value = parse_line(line)

            if label is not None:
                path = path[:depth]
                if depth == len(path) and path:
                    path[-1] = label
                elif depth > len(path):
                    path.append(label)

                if value is not None:
                    add_to_tree(tree, path.copy(), value)

    roll_up_values(tree)
    return tree


def write_tree_to_file(tree: Dict[str, Any], file_path: Path) -> None:
    """Writes the tree to a file."""

    def print_tree(tree: Dict[str, Any], indent: int = 0) -> None:
        for key, value in tree.items():
            if key in ["_total", "_value"]:
                continue

            if isinstance(value, dict) and "_total" in value:
                formatted_value = format_currency(value["_total"])
            else:
                formatted_value = (
                    format_currency(value) if isinstance(value, (int, float)) else ""
                )

            file.write("    " * indent + f"{key} = {formatted_value}\n")

            if isinstance(value, dict):
                print_tree(value, indent + 1)

    with open(file_path, "w") as file:
        print_tree(tree)


def process_file(input_file_path: str, output_file_path: Optional[str] = None) -> None:
    result_tree = parse_and_roll_up(input_file_path)

    if output_file_path is None:
        sydney_tz = pytz.timezone("Australia/Sydney")
        now = datetime.now(sydney_tz)
        formatted_date = now.strftime("%Y%m%d%H%M")
        year_month = now.strftime("%Y-%m")
        file_name = f"{formatted_date}AEST.txt"

        output_dir = Path(OUTPUT_BASE_DIR) / year_month
        logger.debug(f"Output will be saved to {output_dir} with filename {file_name}")

        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / file_name
    else:
        file_path = Path(output_file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

    write_tree_to_file(result_tree, file_path)
    logger.info(f"Finished processing file and output saved to {file_path}")
