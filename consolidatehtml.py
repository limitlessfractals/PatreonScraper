import os
import shutil
import tkinter as tk
from tkinter import filedialog

def main(html_directory):
    # Ensure the 'html_directory' exists
    if not os.path.exists(html_directory):
        print(f"Directory {html_directory} does not exist.")
        return

    # List of all HTML and image files in the directory
    html_files = [f for f in os.listdir(html_directory) if f.endswith('.html')]
    image_files = [f for f in os.listdir(html_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # If no HTML files found, exit
    if not html_files:
        print("No HTML files found in the specified directory.")
        return

    # Concatenate all HTML files
    consolidated_content = ""
    for html_file in html_files:
        with open(os.path.join(html_directory, html_file), 'r', encoding='utf-8') as file:
            consolidated_content += file.read()
            consolidated_content += "<hr>"  # Add a horizontal line for separation

    # Ask the user where to save the consolidated HTML file
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    save_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")], title="Save consolidated HTML as")
    
    if not save_path:
        print("No file location was chosen. Exiting.")
        return

    # Determine the directory of the saved path
    save_directory = os.path.dirname(save_path)

    # Copy image files to the directory of the consolidated HTML
    for image_file in image_files:
        shutil.copy(os.path.join(html_directory, image_file), save_directory)

    # Save the consolidated content
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(consolidated_content)
    print(f"Consolidated HTML saved to {save_path}")

if __name__ == "__main__":
    consolidatehtml()
