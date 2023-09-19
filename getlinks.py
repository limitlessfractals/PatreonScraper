from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from selenium.common.exceptions import TimeoutException

def main():
    # Get user input
    patreon_name = input("Enter the username of the Patreon you want to download from: ")
    while True:
        try:
            # Get start month
            start_month = int(input("Enter start month (1-12): "))
            if not 1 <= start_month <= 12:
                print("Please enter a valid start month (1-12).")
                continue
            
            # Get start year
            start_year = int(input("Enter start year (e.g., 2021): "))

            # Get end month
            end_month = int(input("Enter end month (1-12): "))
            if not 1 <= end_month <= 12:
                print("Please enter a valid end month (1-12).")
                continue
            
            # Get end year
            end_year = int(input("Enter end year (e.g., 2023): "))
            
            # If everything is valid, break out of the loop
            break
            
        except ValueError:
            print("Please enter valid numbers.")

    # Function to generate a list of month-year combinations between two dates
    def generate_month_year_range(start_month, start_year, end_month, end_year):
        month_years = []
        current_month, current_year = start_month, start_year
        while (current_year, current_month) <= (end_year, end_month):
            month_years.append(f"{current_year}-{current_month}")
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
        return month_years

    # Generate month-year combinations
    month_years = generate_month_year_range(start_month, start_year, end_month, end_year)

    # Set up Chrome options to connect to the debugging session
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")

    # Set up the Selenium driver using the Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 2)

    # Initialize an empty set for all the links across all month-year combinations
    all_links = set()

    # Load the existing links from links.json
    try:
        with open('links.json', 'r') as file:
            all_links = set(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # Loop over each month-year combination
    for month_year in month_years:
        # Navigate to the desired page
        driver.get(f'https://www.patreon.com/{patreon_name}/posts?filters[month]={month_year}')

        try:
            # Wait for the presence of all elements with the data-tag attribute set to 'post-published-at'
            post_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@data-tag="post-published-at"]')))
            
            # Extract the href attributes and construct the full URLs
            post_links = [element.get_attribute('href') for element in post_elements]
            
            # Add the links to the overall set of links
            all_links.update(post_links)
        except TimeoutException:
            # If there are no posts for the month, continue to the next month
            continue

    # Close the Selenium driver (this will NOT close the Chrome instance)
    driver.quit()

    # Save the combined set of links back to links.json
    with open('links.json', 'w') as file:
        json.dump(list(all_links), file)

    print(f"Extracted {len(all_links)} links.")

if __name__ == "__main__":
    main()

