import os
import sys
import mimetypes
import chardet
import re

def is_text_file(file_path):
    mimetypes.init()
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('text/')

def should_include_file(file_name):
    # 隠しファイルや特定の拡張子を持つファイルを除外
    excluded_patterns = r'^\..*|.*\.(pyc|pyo|pyd|dll|exe|obj|o)$'
    return not re.match(excluded_patterns, file_name, re.IGNORECASE)

def get_file_list(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if should_include_file(file):
                file_path = os.path.join(root, file)
                if is_text_file(file_path):
                    file_list.append(file_path)
    return file_list

def detect_encoding(file_path):
    try:
        with open(file_path, 'rb') as file:
            result = chardet.detect(file.read())
        return result['encoding'] or 'utf-8'
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return 'utf-8'

def create_prompt_file(directory, file_list):
    prompt_file = os.path.join(directory, 'prompt.txt')
    try:
        with open(prompt_file, 'w', encoding='utf-8') as outfile:
            for file_path in file_list:
                rel_path = os.path.relpath(file_path, directory)
                outfile.write(f"{rel_path}:\n")
                encoding = detect_encoding(file_path)
                try:
                    with open(file_path, 'r', encoding=encoding) as infile:
                        for line in infile:
                            outfile.write(line)
                    outfile.write("\n\n")
                except IOError as e:
                    print(f"Error reading file {file_path}: {e}")
                except UnicodeDecodeError:
                    print(f"Error decoding file {file_path} with encoding {encoding}")
    except IOError as e:
        print(f"Error creating prompt file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) == 1:
        print("Usage: s2p <directory>")
        print("       s2p here")
        sys.exit(1)
    
    if sys.argv[1] == 'here':
        directory = os.getcwd()
    else:
        directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"{directory} is not a valid directory.")
        sys.exit(1)
    
    file_list = get_file_list(directory)
    if not file_list:
        print(f"No text files found in {directory}")
        sys.exit(1)
    
    create_prompt_file(os.path.abspath(directory), file_list)
    print(f"Prompt file created: {os.path.join(os.path.abspath(directory), 'prompt.txt')}")

if __name__ == '__main__':
    main()