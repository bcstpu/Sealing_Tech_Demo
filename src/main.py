import re
from ast import arguments
import sys
from default_args import DEFAULT_ARGS

__error_msgs = {
    "no_args": "Note: no or improper arguments provided via command line, using defaults as appropriate.",
    "no_regex": "No regex tokens could be extracted from the file (probable causes: didn't exist, access not given, or empty file).",
    "read_fail": "Failed to read the file (probable causes: didn't exist, access not given, or empty file).",
    "filter_fail": "Failed to filter (unclear how to fix).",
    "compile_fail": "Somehow failed to compile lines (unclear how to fix).",
    "write_fail": "Failed to write the output to a file (probably an access error).",
}


def read_file_lines(path: str) -> list:
    """
    Read the lines out cleanly from a file path into a list of strings, line by line.
    """
    lines = []
    with open(path, 'r') as f:
        for line in f.readlines():
            lines.append(line)
    return lines


def construct_args(arg_map: list, defaults: list) -> dict:
    """
    Constructs the arg_map listing with the console input arguments into a key-value map string map.
    Uses defaults when those are not available.
    """
    arg_mapping = {}

    for x in range(len(defaults)):
        if x < len(arg_map):
            arg_mapping[arg_map[x]] = defaults[x]

    for x in range(1, len(sys.argv)):
        if x < len(arg_map):
            arg_mapping[arg_map[x]] = sys.argv[x]

    return arg_mapping


def regex_tokens_from_filepath(file_path: str) -> list:
    """
    Construct regex string from a simple file.  Returns an empty list if none found, as fail-safe behavior.
    """
    regexes = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            tokens = line.split(" ")
            for token in tokens:
                regexes.append(token.strip())
    return regexes


def filter_word(word: str, regex_tokens: list) -> str:
    """
    Filter words based off input regex tokens.
    If the word matches a regex token, it will replace it with a "****" 
    form in an "overzealous" fashion, like "hotdog" -> "hot" -> "******".
    An inefficient, but thorough implementation.
    """
    for regex in regex_tokens:
        found = re.findall(regex, word)
        if(found.count(any) != 0):
            start_word = ""
            for c in word:
                start_word = start_word + "*"
            return start_word
    return word


def compile_lines(lines: list) -> str:
    """
    Compiles the lines in nice into a proper full string for writing.
    """
    s = ""
    l = len(lines)
    for x in range(len(lines)):
        s += lines[x]
        # if x < (l - 1):
        #    s += "\n"
    stripped = s.strip()
    return stripped


def filter_dirty_words(file_lines: list, regex_tokens: list) -> list:
    """
    Filter all dirty words, line by line.
    By doing this line by line, the memory messiness of raw string concat
    isn't too bad, because the stack frame dumps it all at once.
    """
    output_lines = []
    for line in file_lines:
        line_copy = "" + line

        # each regex is run on it
        for token in regex_tokens:
            # and each match found gets replacements overwriting the dummy copy of the line
            matches = re.findall(token, line_copy)
            for match in matches:
                # constructing a replacement like "*****" for "dirty"
                replacement = ""
                for _ in range(len(match)):
                    replacement = replacement + "*"
                line_copy = line_copy.replace(match, replacement)
        output_lines.append(line_copy)

    return output_lines

def write_output(output: str) -> bool:
    success = False
    try:
        with open(output, 'w') as f:
            f.write(output)
        success = True
    except:
        pass
    finally:
        return success

def main():
    cmd_line_args = construct_args(["config", "file"], DEFAULT_ARGS)
    if not (("config" in cmd_line_args) and ("file" in cmd_line_args)):
        print(__error_msgs["no_args"])

    regex_tokens = regex_tokens_from_filepath(cmd_line_args["config"])
    if len(regex_tokens) == 0:
        print(__error_msgs["no_regex"])
        return

    file_lines = read_file_lines(cmd_line_args["file"])
    if len(file_lines) == 0:
        print(__error_msgs["read_fail"])
        return

    output_lines = filter_dirty_words(file_lines, regex_tokens)
    if len(output_lines) == 0:
        print(__error_msgs["filter_fail"])
        return

    compiled_lines = compile_lines(output_lines)
    if(len(output_lines) == 0):
        print(__error_msgs["compile_fail"])
        return

    wrote = write_output(compile_lines(output_lines))
    if not wrote:
        print(__error_msgs["write_fail"])


if __name__ == '__main__':
    main()
