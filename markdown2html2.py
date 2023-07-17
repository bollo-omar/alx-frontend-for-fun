#!/usr/bin/python3
"""
A script that converts Markdown to HTML.
"""

import sys
import os
import re

def convert_markdown_to_html(input_file, output_file):
    """
    Converts a Markdown file to HTML and writes the output to a file.
    """
    # Check that the Markdown file exists and is a file
    if not (os.path.exists(input_file) and os.path.isfile(input_file)):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    # Read the Markdown file and convert it to HTML
    with open(input_file, encoding="utf-8") as f:
        markdown_lines = f.readlines()

    html_lines = convert_lines_to_html(markdown_lines)

    # Write the HTML output to a file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

def convert_lines_to_html(markdown_lines):
    """
    Converts a list of Markdown lines to HTML lines.
    """
    html_lines = []
    inside_unordered_list = False
    inside_ordered_list = False
    inside_paragraph = False

    for line in markdown_lines:
        # Check for Markdown headings
        match = re.match(r"^(#+) (.*)$", line)
        if match:
            heading_level = len(match.group(1))
            heading_text = match.group(2)
            html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
            inside_paragraph = False
        else:
            # Check for unordered list items
            match = re.match(r"^- (.*)$", line)
            if match:
                list_item_text = match.group(1)
                if not inside_unordered_list:
                    if inside_ordered_list:
                        html_lines.append("</ol>")
                        inside_ordered_list = False
                    if inside_paragraph:
                        html_lines.append("</p>")
                        inside_paragraph = False
                    html_lines.append("<ul>")
                    inside_unordered_list = True
                html_lines.append(f"<li>{list_item_text}</li>")
            elif inside_unordered_list:
                html_lines.append("</ul>")
                inside_unordered_list = False

            # Check for ordered list items
            match = re.match(r"^\* (.*)$", line)
            if match:
                list_item_text = match.group(1)
                if not inside_ordered_list:
                    if inside_unordered_list:
                        html_lines.append("</ul>")
                        inside_unordered_list = False
                    if inside_paragraph:
                        html_lines.append("</p>")
                        inside_paragraph = False
                    html_lines.append("<ol>")
                    inside_ordered_list = True
                html_lines.append(f"<li>{list_item_text}</li>")
            elif inside_ordered_list:
                html_lines.append("</ol>")
                inside_ordered_list = False

            # Check for paragraphs
            if not inside_unordered_list and not inside_ordered_list and line.strip() != "":
                if not inside_paragraph:
                    html_lines.append("<p>")
                    inside_paragraph = True
                html_lines.append(line.rstrip())

    if inside_unordered_list:
        html_lines.append("</ul>")
    if inside_ordered_list:
        html_lines.append("</ol>")
    if inside_paragraph:
        html_lines.append("</p>")

    return html_lines

if __name__ == "__main__":
    # Check that the correct number of arguments were provided
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    # Get the input and output file names from the command-line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Convert the Markdown file to HTML and write the output to a file
    convert_markdown_to_html(input_file, output_file)

    # Exit with a successful status code
    sys.exit(0)

