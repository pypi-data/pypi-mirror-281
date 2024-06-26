import pandas as pd
import json
import re
from collections import defaultdict
from difflib import SequenceMatcher
from unidecode import unidecode
from datetime import datetime
import ast

def cleaner_json_func(df2, df1):
    
    def category_priority(category):
        if 'food' in category:
            return 1
        elif 'food' in category and 'drinks' in category:
            return 2
        elif 'food' in category and 'desserts' in category:
            return 3
        elif 'food' in category and 'drinks' in category and 'desserts' in category:
            return 4
        elif 'drinks' in category:
            return 5
        elif 'drinks' in category and 'dessert' in category:
            return 6
        elif 'dessert' in category:
            return 7

    def sort_group(group):
        group['priority'] = group['category'].apply(category_priority)
        group = group.sort_values(by=['priority', 'category']).drop(columns=['priority'])
        return group

    sorted_data = df2.groupby('name').apply(sort_group).reset_index(drop=True)
    filtered_data = sorted_data[['name','review_img_big','recency','category','gpt-o']]

    

    def process_record(record, ls):
    # Join the list of strings into a single regex pattern
        pattern = r'\[({})\]'.format('|'.join(ls))
    
    # Extract the matching patterns and remove them from the Name
        matches = re.findall(pattern, record['Name'])
        if matches:
        # Join all matched patterns and assign to DO
            record['DO'] = ' '.join(matches)
        # Remove the patterns from Name
            record['Name'] = re.sub(pattern, '', record['Name']).strip()
    
        return record

    def process_json_column(json_column, ls):
        processed_column = []
        for record in json.loads(json_column):
            processed_record = process_record(record, ls)
            processed_column.append(processed_record)
        return json.dumps(processed_column)

    ls = ["V", "VG", "VGN", "GF", "DF", "NF", "LC", "P", "K", "H", "O", "L"]
    filtered_data['gpt-o_cleansed'] = filtered_data['gpt-o'].apply(lambda x: process_json_column(x, ls))

    def decode_unicode(records):
        try:
        # Decode the JSON string
            decoded_records = json.loads(records)
        # Encode back to JSON string with ensure_ascii=False
            return json.dumps(decoded_records, ensure_ascii=False)
        except json.JSONDecodeError:
            return records

    filtered_data['gpt-o_cleansed'] = filtered_data['gpt-o_cleansed'].apply(decode_unicode)


    def combine_records(records):
        combined = []
        for record in records:
        # Decode the JSON string into a Python list
            decoded_record = json.loads(record)
        # Combine the lists
            combined.extend(decoded_record)
    # Return the combined records as a JSON string
        return json.dumps(combined, ensure_ascii=False)

    def wrap_in_json(records):
        return json.dumps(list(records), ensure_ascii=False)

    grouped_df = filtered_data.groupby('name').agg({
    'review_img_big': wrap_in_json,
    'recency' : wrap_in_json,# Combine image URLs into a JSON array            # Combine recency dates into a JSON array
    'category': wrap_in_json,           # Combine categories into a JSON array
    'gpt-o': combine_records,
    'gpt-o_cleansed' : combine_records
    }).reset_index()

    def rename_menu_section(json_str):
        try:
            records = json.loads(json_str)
            for i, record in enumerate(records):
                if 'Menu_Section' in record:
                    record['Type'] = record.pop('Menu_Section')
                # Reorder the dictionary keys
                    records[i] = {'Name': record['Name'], 'Type': record['Type'], **{k: v for k, v in record.items() if k not in ['Name', 'Type']}}
            return json.dumps(records, ensure_ascii=False)
        except json.JSONDecodeError:
            return json_str

    grouped_df['gpt-o_cleansed'] = grouped_df['gpt-o_cleansed'].apply(rename_menu_section)

    def normalize_for_analysis(name):
        return name.strip().lower().replace(' ', '_')

    def remove_duplicates_from_json(json_str):
        try:
            records = json.loads(json_str)
        
        # Normalize for analysis and store original structure
            normalized_records = {}
            original_names = {}
            for record in records:
                original_name = record['Name']
                normalized_name = normalize_for_analysis(original_name)
            
            # Store the original name
                original_names[normalized_name] = original_name
            
            # Lowercase the name for the main processing
                record['Name'] = original_name.lower()
            
            # Normalize description if it exists
                if 'Description' in record:
                    record['Description'] = record['Description'].strip().lower()
                
                if normalized_name not in normalized_records:
                    normalized_records[normalized_name] = record
        
        # Collect the unique records
            unique_records = list(normalized_records.values())
        
        # Restore original name structure
            for record in unique_records:
                normalized_name = normalize_for_analysis(record['Name'])
                record['Name'] = original_names[normalized_name]

            return json.dumps(unique_records, ensure_ascii=False)
        except json.JSONDecodeError:
            return json_str

    grouped_df['gpt-o_cleansed'] = grouped_df['gpt-o_cleansed'].apply(remove_duplicates_from_json)

    def normalize_description(description):
        return description.strip().lower()

    def fill_missing_values(main_record, duplicate_records):
        for record in duplicate_records:
            for key in main_record:
                if key not in ['Name', 'Desc'] and not main_record[key]:
                    main_record[key] = record[key]
        return main_record

    def remove_duplicates_by_description(json_str):
        try:
            records = json.loads(json_str)
        
        # Store unique records based on normalized descriptions
            normalized_records = {}
            original_records = {}
            duplicate_groups = {}

            for record in records:
                original_name = record['Name']
                original_description = record.get('Desc', '')
            
                normalized_description = normalize_description(original_description)
            
            # Use normalized description as the key
                if normalized_description not in normalized_records:
                    normalized_records[normalized_description] = record
                    original_records[normalized_description] = original_description
                    duplicate_groups[normalized_description] = [record]
                else:
                    duplicate_groups[normalized_description].append(record)
        
        # Collect the unique records and process duplicates
            unique_records = []
        
            for normalized_description, group in duplicate_groups.items():
            # Find the record with the largest name
                largest_name_record = max(group, key=lambda x: x['Name'])
            # Fill missing values from other records in the group
                filled_record = fill_missing_values(largest_name_record, [rec for rec in group if rec != largest_name_record])
                filled_record['Desc'] = original_records[normalized_description]
                unique_records.append(filled_record)

            return json.dumps(unique_records, ensure_ascii=False, indent=4)
        except json.JSONDecodeError:
            return json_str

    grouped_df['gpt-o_cleansed'] = grouped_df['gpt-o_cleansed'].apply(remove_duplicates_from_json)


    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()

# Preprocess function to convert to lower case, strip spaces, and replace spaces with underscores in names
    def preprocess(item):
        item['Original_Name'] = item['Name']
        item['Original_Desc'] = item['Desc']
        item['Name'] = item['Name'].strip().lower().replace(" ", "_")
        item['Desc'] = item['Desc'].strip().lower()
        return item

# Function to restore original names and descriptions
    def restore(item):
        item['Name'] = item.pop('Original_Name')
        item['Desc'] = item.pop('Original_Desc')
        return item

# Function to fill in missing values
    def fill_missing_values(main_item, items_to_merge):
        for item in items_to_merge:
            for key in main_item:
                if key not in ['Name', 'Desc', 'Original_Name', 'Original_Desc'] and not main_item[key]:  # If the main item has an empty value for the key
                    main_item[key] = item[key]
        return main_item

# Function to process and group menu items
    def process_menu_items(menu_items, threshold=0.90):
    # Preprocess items
        menu_items = [preprocess(item) for item in menu_items]

        n = len(menu_items)
        grouped = defaultdict(list)

    # Calculate similarity and group items
        for i in range(n):
            for j in range(i + 1, n):
                name_sim = similarity(menu_items[i]['Name'], menu_items[j]['Name'])
                desc_sim = similarity(menu_items[i]['Desc'], menu_items[j]['Desc'])
                price_sim = similarity(menu_items[i]['Price'], menu_items[j]['Price'])
                avg_sim = (name_sim + desc_sim + price_sim) / 3

                if avg_sim > threshold:
                    grouped[i].append(j)
                    grouped[j].append(i)

    # Reduce groups to unique items with the largest name and fill missing values
        result = []
        visited = set()
        for i in range(n):
            if i not in visited:
                group = [i] + grouped[i]
                visited.update(group)
                largest_name_item = max((menu_items[k] for k in group), key=lambda x: x['Name'])
            # Fill missing values from other items in the group
                items_to_merge = [menu_items[k] for k in group if k != largest_name_item]
                filled_item = fill_missing_values(largest_name_item, items_to_merge)
                result.append(filled_item)

    # Restore original names and descriptions
        result = [restore(item) for item in result]
        return result

    grouped_df['gpt-o_cleansed'] = grouped_df['gpt-o_cleansed'].apply(remove_duplicates_from_json)

    def sort_and_filter_json_records(json_str):
        try:
            data = json.loads(json_str)
        # Filter out records where the Name contains 'WTF'
            filtered_data = [record for record in data if 'WTF' not in record.get('Name', '')]
        
        # Sort the remaining records based on the 'Type' key, using a temporary lowercase version for sorting
            sorted_data = sorted(filtered_data, key=lambda x: (x.get('Type', '').lower()))
        
            return json.dumps(sorted_data, ensure_ascii=False)
        except json.JSONDecodeError:
            return json_str

    grouped_df['gpt-o_cleansed'] = grouped_df['gpt-o_cleansed'].apply(sort_and_filter_json_records)


    def normalize_name(json_str):
        try:
            records = json.loads(json_str)
            normalized_records = []
        
            for record in records:
                if 'Name' in record:
                    name = record['Name']
                # Normalize the name by removing accents and special characters
                    normalized_name = unidecode(name)  # Convert accented characters to non-accented
                    normalized_name = re.sub(r'[^\w\s]', '', normalized_name)  # Remove special characters
                    record['Name'] = normalized_name.strip()  # Remove leading/trailing whitespace
                normalized_records.append(record)
        
            return json.dumps(normalized_records, ensure_ascii=False)
        except json.JSONDecodeError:
            return json_str

    grouped_df['gpt-o_cleansed'] = grouped_df['gpt-o_cleansed'].apply(normalize_name)

    def map_do(emoji):
        mapping = {
            "🌶️🌱": [["Spicy", "🌶️"], ["V", "🌱"]],
            "🌶️": ["Spicy", "🌶️"],
            "🌱": ["V", "🌱"]
        }
        return mapping.get(emoji, ["", ""])

    grouped_df['gpt-o_cleansed'] = grouped_df['gpt-o_cleansed'].apply(lambda x: json.loads(x))
    grouped_df['gpt-o_cleansed'] = grouped_df['gpt-o_cleansed'].apply(lambda menu_items: [{**item, 'DO': map_do(item['DO'])} for item in menu_items])

    def process_json_records(json_str):
    #data = json.loads(json_str)
        processed_data = [record for record in json_str]
        return json.dumps(processed_data, ensure_ascii=False)

    grouped_df['gpt-o_cleansed'] = grouped_df['gpt-o_cleansed'].apply(process_json_records)

    def replace_empty_do(record):
    # Replace empty lists in DO with an empty string
        if record.get('DO') == ['', '']:
            record['DO'] = ""
        return record

    def process_price(record):
    # Remove extra spaces in the Price field
        record['Price'] = record['Price'].lower()

        record['Price'] = re.sub(r'\s+', ' ', record['Price']).strip()
    
    # Extracting all numerical values followed by "oz" in the Price field
        matches = re.findall(r'(\d+(?:\.\d+)?)\s*oz', record['Price'])
        if matches:
        # Assign the matched quantities to Quantity
            record['Quantity'] = [f"{match} oz" for match in matches]
        # Removing the "oz" values from Price
            record['Price'] = re.sub(r'(\d+(?:\.\d+)?)\s*oz', '', record['Price']).strip()
    
    # Extract and assign add-ons
        add_ons_matches = re.findall(r'\+\d+(?:\.\d+)?', record['Price'])
        if add_ons_matches:
            record['Add-ons'] = ' '.join(add_ons_matches)
        # Removing the add-ons values from Price
            record['Price'] = re.sub(r'\+\d+(?:\.\d+)?', '', record['Price']).strip()
    
    # Ensuring the $ sign is before each numeric value in Price
        if record['Price']:
        # Remove any existing $ signs
            record['Price'] = record['Price'].replace('$', '')
        # Add $ sign before each numeric value
            record['Price'] = re.sub(r'(\d+(?:\.\d+)?)', r'$\1', record['Price'])
    
    # Apply the replace_empty_do function to handle DO field
        record = replace_empty_do(record)
    
        return record

    def process_price_records(records_json):
        records = json.loads(records_json)
        processed_records = [process_price(record) for record in records]
        return json.dumps(processed_records, ensure_ascii=False)

    grouped_df['gpt-o_cleansed'] = grouped_df['gpt-o_cleansed'].apply(process_price_records)

    def convert_to_json_records(json_string):
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            print("Invalid JSON string")
            return None

    grouped_df['gpt-o_cleansed'] = grouped_df['gpt-o_cleansed'].apply(convert_to_json_records)
    grouped_df['gpt-o'] = grouped_df['gpt-o'].apply(convert_to_json_records)

    def correct_price(record):
        price = record['Price']
    
    # If the price contains '€', remove the '$' sign
        if '€' in price:
            price = price.replace('$', '')
        if '¢' in price:
            price = price.replace('$', '')

        price = price.replace('()', '')
    
    # Remove '$' sign from numeric values in brackets
        price = re.sub(r'\(\$(\d+)\)', r'(\1)', price)
    
        record['Price'] = price.strip()
        return record

    def apply_corrections(json_list):
        return [correct_price(rec) for rec in json_list]

    grouped_df['gpt-o_cleansed'] = grouped_df['gpt-o_cleansed'].apply(apply_corrections)

    category_dict = df2.set_index('name')['category_cuisine_google'].to_dict()
    address_dict = df2.set_index('name')['address'].to_dict()
    phone_no_dict = df2.set_index('name')['phone'].to_dict()
    website_dict = df1.set_index('name')['website'].to_dict()
    opening_hours_dict = df1.set_index('name')['opening_hours'].to_dict()

    grouped_df['category_cuisine_google'] = grouped_df['name'].map(category_dict)
    grouped_df['address'] = grouped_df['name'].map(address_dict)
    grouped_df['phone_no'] = grouped_df['name'].map(phone_no_dict)
    grouped_df['website'] = grouped_df['name'].map(website_dict)
    grouped_df['opening_hours'] = grouped_df['name'].map(opening_hours_dict)

    current_utc_time = datetime.now()
    grouped_df['Created_on'] = current_utc_time

    

    def safe_literal_eval(val):
        try:
            if pd.isna(val):
                return None
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return val

    grouped_df['opening_hours'] = grouped_df['opening_hours'].apply(safe_literal_eval)

    grouped_df['opening_hours'] = grouped_df['opening_hours'].astype(object)
    df_dict = grouped_df.to_dict(orient='records')
    
    for item in df_dict:
        for key in ['review_img_big', 'recency', 'category']:
            if isinstance(item[key], str):  # Check if the value is a string
                try:
                    item[key] = ast.literal_eval(item[key])
                except ValueError:
                    item[key] = []

    return df_dict