import csv
import json
import os

def read_csv_file(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Quantity'] and row['Price']:
                data.append(row)
    return data

def clean_numeric(value):
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return None

def get_fields_metadata(data):
    """Get metadata about fields including their categories and icons."""
    fields = {
        'Size': {
            'category': 'stock',
            'icon': 'fas fa-ruler-combined',
            'order': 1
        },
        'Paper Weight': {
            'category': 'stock',
            'icon': 'fas fa-balance-scale',
            'order': 2
        },
        'Paper Type': {
            'category': 'stock',
            'icon': 'fas fa-file-alt',
            'order': 3
        },
        'Paper Color': {
            'category': 'stock',
            'icon': 'fas fa-palette',
            'order': 4
        },
        'Parts': {
            'category': 'print',
            'icon': 'fas fa-layer-group',
            'order': 1
        },
        'Sides': {
            'category': 'print',
            'icon': 'fas fa-copy',
            'order': 2
        },
        'Ink Color': {
            'category': 'print',
            'icon': 'fas fa-fill-drip',
            'order': 3
        }
    }
    
    categories = {
        'stock': {
            'name': 'Stock Options',
            'icon': 'fas fa-box',
            'fields': {}
        },
        'print': {
            'name': 'Print Options',
            'icon': 'fas fa-print',
            'fields': {}
        }
    }
    
    # Process each field
    for field, meta in fields.items():
        values = sorted(list(set(row[field] for row in data if row.get(field))))
        if values:  # Only include fields that have values
            category = meta['category']
            categories[category]['fields'][field] = {
                'values': values,
                'icon': meta['icon'],
                'order': meta['order']
            }
    
    # Only include categories that have fields
    return {k: v for k, v in categories.items() if v['fields']}

def process_pricing_data(data, product_name):
    """Process data for a single product type."""
    categories = get_fields_metadata(data)
    
    processed = {
        'name': product_name,
        'categories': categories,
        'prices': {}
    }
    
    # Process pricing data
    for row in data:
        price_key_parts = []
        for category in categories.values():
            for field in category['fields'].keys():
                if field in row and row[field]:
                    price_key_parts.append(f"{field}={row[field]}")
        
        if price_key_parts:  # Only create price entry if we have valid fields
            price_key = '|'.join(price_key_parts)
            quantity = clean_numeric(row['Quantity'])
            price = clean_numeric(row['Price'])
            
            if quantity and price:
                if price_key not in processed['prices']:
                    processed['prices'][price_key] = {}
                processed['prices'][price_key][str(quantity)] = price
    
    return processed

def main():
    pricing_data = {
        'products': {},
        'version': '1.0'
    }

    # Process each CSV file
    csv_files = sorted([f for f in os.listdir('.') if f.endswith('.csv')])
    
    for filename in csv_files:
        print(f"Processing {filename}...")
        product_name = os.path.splitext(os.path.basename(filename))[0].split('-', 1)[1].replace('-', ' ')
        
        data = read_csv_file(filename)
        if data:
            try:
                product_data = process_pricing_data(data, product_name)
                if product_data['categories'] and product_data['prices']:  # Only include products with valid data
                    pricing_data['products'][product_name] = product_data
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    if not pricing_data['products']:
        raise Exception("No valid pricing data was generated!")

    # Write the data to a JSON file
    with open('pricing_data.json', 'w') as f:
        json.dump(pricing_data, f, indent=2)

    print("Pricing data has been generated successfully!")

if __name__ == "__main__":
    main()
