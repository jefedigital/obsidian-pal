import os
from pathlib import Path

def concat_markdown_files(source_dir, target_dir):
    # Create target directory if it doesn't exist
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    
    # Walk through the source directory
    for root, dirs, files in os.walk(source_dir):
        # Filter for markdown files
        md_files = [f for f in files if f.endswith('.md')]
        
        if md_files:
            # Get relative path to create appropriate output file
            rel_path = os.path.relpath(root, source_dir)
            output_filename = f"combined_{os.path.basename(root) or 'root'}.md"
            output_path = os.path.join(target_dir, output_filename)
            
            # Concatenate all markdown files in the current directory
            with open(output_path, 'w', encoding='utf-8') as outfile:
                for md_file in sorted(md_files):
                    file_path = os.path.join(root, md_file)
                    
                    # Add a clear separator with file name
                    outfile.write(f"\n\n{'='*80}\n")
                    outfile.write(f"Source: {os.path.join(rel_path, md_file)}\n")
                    outfile.write('='*80 + "\n\n")
                    
                    # Read and write content
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
            
            print(f"Created combined file: {output_path}")

if __name__ == "__main__":
    # Define source and target directories
    source_directory = "files"
    target_directory = "target"
    
    # Run the concatenation
    concat_markdown_files(source_directory, target_directory)
    print("Markdown concatenation complete!") 