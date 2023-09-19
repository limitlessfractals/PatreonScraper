import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from tkinter import filedialog, Tk

def main():
    # Chrome options for remote debugging
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")

    # Connect to the existing Chrome session
    driver = webdriver.Chrome(options=chrome_options)

    # Read links from links.json
    with open('links.json', 'r') as file:
        links = json.load(file)

    # Ask the user to select a folder
    root = Tk()
    root.withdraw()  # Hide the main window
    folder_selected = filedialog.askdirectory(title="Select a directory to save the HTML files and images")
    html_directory = os.path.join(folder_selected, 'PatreonHTML')

    # Ensure the 'html' directory exists
    if not os.path.exists(html_directory):
        os.makedirs(html_directory)

    for url in links:
        print(f"Processing URL: {url}")
        try:
            # Navigate to the webpage
            driver.get(url)
            time.sleep(3)  # Giving some time for page to load

            # Extract content inside the targeted div
            post_card_element = driver.find_element(By.XPATH, '//div[@data-tag="post-card"]')
            page_source = post_card_element.get_attribute('outerHTML')

            # Using the last part of the URL as the file name
            file_name = url.split('/')[-1] + '.html'

            # Path for the final HTML file within 'html' directory
            html_file_path = os.path.join(html_directory, file_name)

            # Find all the file links
            file_links = driver.find_elements(By.XPATH, '//a[starts-with(@href, "https://www.patreon.com/file?")]')

            # Open each link in a new tab and download the associated file
            for link in file_links:
                file_name_in_link = link.text
                link_url = link.get_attribute('href')

                # Open the link in a new tab
                driver.execute_script("window.open('"+link_url+"', '_blank');")
                time.sleep(5)  # Allow time for download

                download_path = os.path.join(os.path.expanduser('~'), 'Downloads', file_name_in_link)

                 # If it's an image, move it to 'html' directory and append its tag to the page source
                if any(download_path.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
                    new_path = os.path.join(html_directory, file_name_in_link)
                    shutil.move(download_path, new_path)
                    print("Before addition:", len(page_source))
                    appended_string = f'<img src="{file_name_in_link}" alt="{file_name_in_link}" />'
                    # Check if the page_source contains the </html> tag
                    closing_tag_position = page_source.rfind('<div data-tag="post-attachments"')
                    
                    if closing_tag_position != -1:
                        # Insert the appended_string just before the </html> tag
                        page_source = page_source[:closing_tag_position] + appended_string + page_source[closing_tag_position:]
                    else:
                        # If there's no </html> tag, just append the string at the end
                        page_source += appended_string
                    
                    print("After addition:", len(page_source))

            # Save the full page source to an HTML file inside 'html' directory
            with open(html_file_path, 'w', encoding='utf-8') as file:
                file.write(page_source)

        except Exception as e:
            print(f"Error processing {url}. Error: {e}")

    # Close the Selenium driver (this will not close your existing browser session)
    driver.close()

    return html_directory

if __name__ == "__main__":
    main()
