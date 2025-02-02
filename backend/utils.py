import csv

# Converting csv to JSON
def csv_to_json(csv_file):
    json_data = []
    
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            json_item = {
                "Name": row["Name"],
                "Job Title": row["Job Title"],
                "Location": row["Location"],
                "Education": row["Education"],
                "Years of Experience": int(row["Years of Experience"]),
                "Skills": row["Skills"].split(", "),
                "LinkedIn Profile": row["LinkedIn Profile"]
            }
            json_data.append(json_item)
    
    return json_data