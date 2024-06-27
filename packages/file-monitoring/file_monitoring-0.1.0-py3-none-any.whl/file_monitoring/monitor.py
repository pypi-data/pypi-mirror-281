import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, directory, output_file):
        self.directory = directory
        self.output_file = output_file

    def on_modified(self, event):
        if not event.is_directory and event.src_path != os.path.abspath(self.output_file):
            self.update_file_content(event.src_path)

    def update_file_content(self, file_path):
        print(f"File modified: {file_path}")
        file_content = get_file_contents(file_path)
        update_txt_file(self.output_file, file_path, file_content)

def get_all_files(directory, output_file):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in {'venv', '.venv', 'env', '.env'}]
        for file in files:
            file_path = os.path.join(root, file)
            if file_path != os.path.abspath(output_file):
                file_paths.append(file_path)
    return file_paths

def get_file_contents(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
    except Exception as e:
        contents = f"Error reading file: {e}"
    return contents

def write_to_txt(output_file, data):
    with open(output_file, 'w') as file:
        file.write(data)

def update_txt_file(output_file, file_path, new_content):
    try:
        with open(output_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    start_index = -1
    end_index = -1
    for i, line in enumerate(lines):
        if line.strip() == f"Path: {file_path}":
            start_index = i
        if start_index != -1 and line.strip() == "-" * 40:
            end_index = i
            break

    if start_index != -1 and end_index != -1:
        del lines[start_index:end_index + 1]

    new_data = f"Path: {file_path}\nContents:\n{new_content}\n" + "-" * 40 + "\n"
    lines.insert(start_index if start_index != -1 else len(lines), new_data)

    with open(output_file, 'w') as file:
        file.writelines(lines)

def run_monitor(directory, output_file):
    files = get_all_files(directory, output_file)
    data = ""
    for file in files:
        data += f"Path: {file}\n"
        data += "Contents:\n"
        data += get_file_contents(file)
        data += "\n" + "-" * 40 + "\n"
    
    write_to_txt(output_file, data)
    print(f"Initial file paths and contents written to {output_file}")

    event_handler = FileChangeHandler(directory, output_file)
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
