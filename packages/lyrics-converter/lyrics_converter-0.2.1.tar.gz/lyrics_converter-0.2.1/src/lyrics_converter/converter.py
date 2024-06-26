import logging
import re


class LyricsConverter:
    def __init__(self, output_format, filepath=None):
        self.output_format = output_format
        self.filepath = filepath
        logging.info(f"LyricsConverter initialized with output_format={output_format} and filepath={filepath}")

    def read_file(self, filepath):
        logging.info(f"Reading file from {filepath}")
        with open(filepath, "r") as file:
            content = file.read()
        logging.info(f"File read successfully from {filepath}")
        return content

    def write_file(self, filepath, content):
        logging.info(f"Writing content to file at {filepath}")
        with open(filepath, "w") as file:
            file.write(content)
        logging.info(f"Content written successfully to {filepath}")

    def detect_format(self, content):
        logging.info("Detecting format of the content")
        first_line = content.splitlines()[0]
        if first_line == "[re:MidiCo]":
            logging.info("Success: Detected MidiCo LRC format.")
        else:
            logging.error("Error: The input format did not match any of the supported formats.")
            raise ValueError("Error: The input format did not match any of the supported formats.")

    def parse_lrc(self, content):
        logging.info("Parsing LRC content")
        lines = content.splitlines()[1:]  # Skip the first line
        words = []
        for line in lines:
            match = re.match(r"\[(\d+):(\d+\.\d+)\](\d+):(/?)(.*)", line)
            if match:
                minutes, seconds, singer_id, new_line, word = match.groups()
                start_time = int(minutes) * 60 + float(seconds)
                words.append((start_time, new_line, word))
                logging.debug(f"Parsed line: {line} -> {start_time}, {new_line}, {word}")
        logging.info("LRC content parsed successfully")
        return words

    def format_timestamp(self, seconds):
        logging.debug(f"Formatting timestamp for {seconds} seconds")
        if seconds < 60:
            return f"{seconds:.3f}"
        else:
            minutes = int(seconds // 60)
            seconds = seconds % 60
            return f"{minutes}:{seconds:06.3f}"

    def convert_to_txt(self, words):
        logging.info("Converting words to TXT format")
        result = []
        for i in range(len(words)):
            start_time, new_line, word = words[i]

            # Determine the end time for the current word
            if i < len(words) - 1:
                next_start_time = words[i + 1][0]
                duration = next_start_time - start_time
                if duration > 5:
                    # If duration is too long, assume 1 second duration
                    end_time = start_time + 1
                else:
                    # Otherwise, use the next word's start time
                    end_time = next_start_time
            else:
                # Last word, assume 1 second duration
                end_time = start_time + 1

            # If this word starts a new line and it's not the first word, append \n to the previous word
            if new_line and i > 0:
                result[-1] += "\\n"

            # Append the formatted timestamp and word to the result list
            result.append(f"{self.format_timestamp(start_time)} {self.format_timestamp(end_time)} {word}")
            logging.debug(f"Converted word: {word} with start_time={start_time} and end_time={end_time}")

        # Ensure the last word ends with \n if it was the last word of a line
        if words and words[-1][1]:
            result[-1] += "\\n"

        logging.info("Conversion to TXT format completed")
        return "\n".join(result)

    def convert(self, content):
        logging.info("Starting conversion process")
        self.detect_format(content)
        words = self.parse_lrc(content)
        if self.output_format == "txt":
            converted_content = self.convert_to_txt(words)
            logging.info("Conversion to TXT format successful")
            return converted_content
        else:
            logging.error(f"Unsupported output format: {self.output_format}")
            raise ValueError(f"Unsupported output format: {self.output_format}")

    def convert_file(self):
        if not self.filepath:
            logging.error("Filepath must be provided for file conversion.")
            raise ValueError("Filepath must be provided for file conversion.")
        logging.info(f"Starting file conversion for {self.filepath}")
        content = self.read_file(self.filepath)
        converted_content = self.convert(content)
        logging.info(f"File conversion completed for {self.filepath}")
        return converted_content
