import os
import csv
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel(model_name='gemini-pro')

def read_input():
    link = {"1": ["BookToScrape", "https://books.toscrape.com/"]}

    for i in range(1, 2): # Loop through one link for now
        url = link[str(i)][1]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the website text and links
        data = soup.text
        links = soup.find_all('a', href=True)
        urls = ""
        for a in links:
            urls = urls + "\n" + a['href'][1:]

        query = (
            data + "Jumbled links about book categories:" + urls +
            "\n Create a table with the following columns: Book category and Category link\n"
            "And append this URL without space for every book category link: 'https://books.toscrape.com/'"
        )

        # Send query to the generative model
        main_response = model.generate_content(query)

        # Extract the table data from the generated response
        structured_data = extract_table_data(main_response.text)

        # Write the structured data to a CSV file
        csv_file = 'book_categories_v2.csv'
        write_to_csv(structured_data, csv_file)

def extract_table_data(response_text):
    """Extracts book categories and links from the response text."""
    lines = response_text.split('\n')
    structured_data = []

    for line in lines[1:]:
        # Skip empty lines and headers
        if line.strip() and "---" not in line:
            parts = line.split('|')
            if len(parts) == 4: # We expect 3 parts: empty, Book Category, Category Link
                category_name = parts[1].strip()
                category_link = parts[2].strip()
                structured_data.append([category_name, category_link])

    return structured_data

def write_to_csv(data, filename):
    """Writes structured data to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Book Category', 'Category Link']) # Write header
        writer.writerows(data) # Write data rows
    print(f"Data has been written to '{filename}'.")

read_input()