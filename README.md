# Patreon Scraper Documentation

## Overview

This program is designed to scrape content from Patreon creators, focusing primarily on posts. The scraped content is saved as individual HTML files and can be further consolidated into a single HTML file.

## Modules:

1. `getlinks.py`: Fetches the links to the posts of a given Patreon creator.
2. `createHtml.py`: Downloads the content of the links fetched by `getlinks.py` and saves them as individual HTML files. It also handles downloading images linked within the posts.
3. `consolidatehtml.py`: Consolidates all the HTML files generated by `createHtml.py` into a single HTML file.
4. `main.py`: An orchestrator that runs the above three modules in sequence.

## Usage:

1. **Starting a Remote Debugging Session in Chrome**:
   - First, start Chrome with remote debugging enabled on port 9223:
     ```
     chrome.exe --remote-debugging-port=9223
     ```
   - Ensure no other Chrome windows are open when you start this.

2. **Running the Program**:
   - Navigate to the directory containing the scripts.
   - Run `main.py`:
     ```
     python main.py
     ```
   - Follow the on-screen prompts.

3. **Providing Inputs**:
   - **Patreon Creator Name**: When prompted, enter the **username** of the Patreon creator whose posts you want to scrape.
   - **Date Range**: You'll be asked to provide a start month/year and an end month/year. This range determines which posts will be scraped based on their publication date.
   - **Select a Directory**: A file dialog will open, asking you to select a directory. The HTML files (and associated images) will be saved in a subdirectory within your chosen directory.

4. **Output**:
   - The individual posts will be saved as HTML files in the specified directory, under a subfolder named after the Patreon creator.
   - A consolidated HTML file will also be generated in a new specified directory.

5. **Post-Processing**:
   - You can open the generated HTML files in a browser. For the consolidated file, ensure all images and linked content display correctly.

6. **Re-Scraping or Re-Running**:
   - If you encounter issues with the fetched links or the output seems incorrect, delete the `links.json` file and run the program again.
   - If you wish to scrape the posts again or perform another scraping session for a different creator, you should either delete the existing `patreonHTML` folder or rename it to avoid potential conflicts.

## Notes:

- Ensure the required Python packages are installed. You can do this using:
  ```
  pip install -r requirements.txt
  ```
- Make sure the ChromeDriver version matches the version of your Chrome browser.
- The program is designed to handle most common scenarios, but there may be unique posts or media types that aren't perfectly handled. Always verify the output.

## Troubleshooting:

1. **ChromeDriver Version Mismatch**: If there's a mismatch between ChromeDriver and your Chrome browser, download the correct version of ChromeDriver and replace the existing executable.

2. **Content Not Appearing in HTML**: Sometimes, the content might not appear as expected due to the dynamic nature of web pages. Ensure JavaScript content has loaded before scraping.

3. **Network Errors**: If you encounter network-related errors, ensure you have a stable internet connection and that the Patreon website is accessible from your location.

4. **File Errors**: Ensure the directory where files are being written has the necessary write permissions.

For further issues or customization requirements, refer to the source code or seek assistance from a developer familiar with web scraping and Python.
