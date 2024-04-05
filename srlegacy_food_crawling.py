import json
import requests
import numpy as np
import csv

def url():
    return "https://fdc.nal.usda.gov/portal-data/external/search"

def headers():
    # Function to set request headers
    return {
        "Content-Type": "application/json",
        "Host": "fdc.nal.usda.gov",
        "Origin": "https://fdc.nal.usda.gov",
        "Referer": "https://fdc.nal.usda.gov/fdc-app.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
    }

def payload(page_number):
    # Function to set request payload
    return {
        "includeDataTypes": {"SR Legacy": True},
        "referenceFoodsCheckBox": False,
        "requireAllWords": False,
        "includeMarketCountries": None,
        "sortField": "",
        "sortDirection": None,
        "pageNumber": page_number,
        "exactBrandOwner": None
    }

def get_data(page_number):
    # Function to fetch data from the API and save to files
    response = requests.post(url(), headers=headers(), json=payload(page_number))
    
    # Save each page's response in separate files in json_data folder
    with open(f'json_data/data_{page_number}.text', 'w') as f:
        f.write(response.text)

def write_header_to_cvs():
    # Function to process JSON data from files and extract nutrient fields
    all_nutrient_fields = set()

    # Read through all JSON files and extract data
    for page_number in range(1, 157):
        with open(f'json_data/data_{page_number}.text', 'r') as f:
            data = json.load(f)
        
        for food in data['foods']:
            for nutrient in food['foodNutrients']:
                nutrient_name = nutrient.get('nutrientName', '').lower()
                if nutrient_name not in all_nutrient_fields:
                    all_nutrient_fields.add(nutrient_name)

    write_csv_header(all_nutrient_fields)

def write_csv_header(all_nutrient_fields):
    # Function to write CSV file header
    with open('Food_nutrions_fact.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        header = ['food_id', 'food_name', 'food_group'] + list(all_nutrient_fields)
        writer.writerow(header)
        
def write_to_csv(data, all_nutrient_fields):
    # Function to write data to CSV file
    with open('Food_nutrions_fact.csv', 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for food in data['foods']:
            food_id = food['fdcId']
            food_name = food['lowercaseDescription'].lower()
            food_group = food['foodCategory']
            nutrient_dict = {nutrient_name: '-' for nutrient_name in all_nutrient_fields}
            for nutrient in food['foodNutrients']:
                nutrient_name = nutrient.get('nutrientName', '').lower()
                nutrient_value = nutrient.get('value', np.nan)
                nutrient_dict[nutrient_name] = nutrient_value
            row = [food_id, food_name, food_group] + list(nutrient_dict.values())
            writer.writerow(row)

if __name__ == '__main__':
    # write_header_to_cvs()
    # all_nutrient_fields = []

    # # Read the first line as the header and store it in all_nutrient_fields
    # with open("Food_nutrions_fact.csv", "r", encoding='utf-8') as f:
    #     reader = csv.reader(f)
    #     all_nutrient_fields = next(reader)[3:]
    
    # # Process JSON files and write to CSV
    # for page_number in range(1, 157):
    #     with open(f'json_data/data_{page_number}.text', 'r') as f:
    #         data = json.load(f)
    #         write_to_csv(data, all_nutrient_fields)
    #         print(f"Page {page_number} is done.")

    # Just open the csv file to new window
    import os
    os.system("start Food_nutrions_fact.csv")
