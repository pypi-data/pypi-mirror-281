import argparse
import os
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def read_file(filepath):
    with open(filepath, "r") as file:
        return file.read()


def write_file(filepath, content):
    with open(filepath, "w") as file:
        file.write(content)


def detect_format(content):
    first_line = content.splitlines()[0]
    if first_line == "[re:MidiCo]":
        logging.info("Success: Detected MidiCo LRC format.")
    else:
        raise ValueError("Error: The input format did not match any of the supported formats.")


def parse_lrc(content):
    lines = content.splitlines()[1:]  # Skip the first line
    words = []
    for line in lines:
        match = re.match(r"\[(\d+):(\d+\.\d+)\](\d+):(/?)(.*)", line)
        if match:
            minutes, seconds, singer_id, new_line, word = match.groups()
            start_time = int(minutes) * 60 + float(seconds)
            words.append((start_time, new_line, word))
    return words


def format_timestamp(seconds):
    if seconds < 60:
        return f"{seconds:.3f}"
    else:
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes}:{seconds:06.3f}"


def convert_to_txt(words):
    result = []
    for i in range(len(words)):
        start_time, new_line, word = words[i]
        if i < len(words) - 1:
            next_start_time = words[i + 1][0]
            duration = next_start_time - start_time
            if duration > 5:
                end_time = start_time + 1
            else:
                end_time = next_start_time
        else:
            end_time = start_time + 1  # Last word, assume 1 second duration

        if new_line and i > 0:
            result[-1] += "\\n"  # Append \n to the previous word if this word starts a new line

        result.append(f"{format_timestamp(start_time)} {format_timestamp(end_time)} {word}")

    # Ensure the last word ends with \n if it was the last word of a line
    if words and words[-1][1]:
        result[-1] += "\\n"

    return "\n".join(result)


def main():
    parser = argparse.ArgumentParser(description="Lyrics Converter CLI")
    parser.add_argument("input", type=str, help="Input file path")
    parser.add_argument("output", type=str, help="Output file path")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        logging.error(f"The file {args.input} does not exist.")
        return

    content = read_file(args.input)

    try:
        detect_format(content)
    except ValueError as e:
        logging.error(e)
        return

    words = parse_lrc(content)
    txt_content = convert_to_txt(words)
    write_file(args.output, txt_content)
    logging.info(f"File has been converted and saved to {args.output}")


if __name__ == "__main__":
    main()
