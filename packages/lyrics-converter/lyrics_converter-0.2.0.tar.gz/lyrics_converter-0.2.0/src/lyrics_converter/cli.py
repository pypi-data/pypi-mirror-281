import argparse
import os
import logging
from lyrics_converter import LyricsConverter

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    parser = argparse.ArgumentParser(description="Lyrics Converter CLI")
    parser.add_argument("input", type=str, help="Input file path")
    parser.add_argument("output", type=str, help="Output file path")
    parser.add_argument("--format", type=str, default="txt", help="Output format (default: txt)")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        logging.error(f"The file {args.input} does not exist.")
        return

    converter = LyricsConverter(output_format=args.format, filepath=args.input)

    try:
        content = converter.read_file(args.input)
        converted_content = converter.convert(content)
        converter.write_file(args.output, converted_content)
        logging.info(f"File has been converted and saved to {args.output}")
    except ValueError as e:
        logging.error(e)


if __name__ == "__main__":
    main()
