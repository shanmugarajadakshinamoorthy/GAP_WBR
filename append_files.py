import os

def append_files_with_headings(directory, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            filename = filename.replace("_edit_summary.txt",'')
            if os.path.isfile(file_path):  # Ensure it's a file
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(f'### {filename} ###\n')  # Add filename as heading
                    outfile.write(infile.read())  # Append file content
                    outfile.write('\n\n')  # Add spacing between files

# Example usage
directory_path = "edited_summary"  # Change this to your directory path
output_file_path = "edited_summary/output.txt"  # Output file name
append_files_with_headings(directory_path, output_file_path)
print(f"Contents appended to {output_file_path}")