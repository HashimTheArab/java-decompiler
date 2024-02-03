import subprocess
import os

# Specify the path to the directory containing .class files
class_files_dir = '/path/to/input'

# Specify the output directory for the .java files
output_dir = '/path/to/output'

# Specify the path to the CFR jar file
cfr_jar_path = 'cfr.jar'

os.makedirs(output_dir, exist_ok=True)

def get_output_path(original_path, original_root, target_root):
    relative_path = os.path.relpath(original_path, original_root)
    return os.path.join(target_root, relative_path)

currentDir = 1
totalFiles = 0
for root, dirs, files in os.walk(class_files_dir):
    maxFiles = len(files)
    maxDirs = len(dirs)
    currentFile = 1
    currentDir += 1

    for file in files:
        if file.endswith(".class"):
            currentFile += 1
            totalFiles += 1

            class_file_path = os.path.join(root, file)
            output_file_path = get_output_path(class_file_path, class_files_dir, output_dir).replace('.class', '.java')
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            command = ['java', '-jar', cfr_jar_path, class_file_path, '--outputdir', os.path.dirname(output_file_path)]
            try:
                subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if maxDirs == 1:
                    print(f"({currentFile}/{maxFiles}/) Decompiled {class_file_path}")
                else:
                    print(f"({currentDir}/{maxDirs}/) Decompiled {class_file_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error decompiling {class_file_path}: {e.stderr.decode()}")
            except Exception as e:
                print(f"Unexpected error with {class_file_path}: {str(e)}")

print("Decompilation completed.")
