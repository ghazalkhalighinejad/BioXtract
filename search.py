
import os
import json
import re

def get_all_jsons():
    jsons_folder = "jsons"
    all_jsons = []
    for root, dirs, files in os.walk(jsons_folder):
        for file in files:
            print(os.path.join(root, file))
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as json_file:
                    json_string = json_file.read()
                    json_data = json.loads(json_string)
                    all_jsons.append(json_data)
    return all_jsons

def get_attribute_values(all_jsons):
    attribute_values = {}
    for json_data in all_jsons:
        for key, value in json_data.items():
            if key != "Biodegradation":
                if key not in attribute_values:
                    attribute_values[key] = set()
                attribute_values[key].add(str(value))
    attribute_values = {key: list(values) for key, values in attribute_values.items()}
    return attribute_values

def get_subset_jsons(all_jsons, criteria):
    subset_jsons = [
        json_data
        for json_data in all_jsons
        if all(json_data.get(key) == value for key, value in criteria.items())
    ]
    return subset_jsons

def get_user_criteria(attribute_values):
    criteria = {}
    for attribute, values in attribute_values.items():
        print(f"Enter the value for {attribute} (or press Enter to skip):")
        for i, value in enumerate(values, start=1):
            print(f"{i}. {value}")
        choice = input("Enter the number corresponding to your choice (or press Enter to skip): ")
        if choice == "":
            continue
        while not choice.isdigit() or int(choice) < 1 or int(choice) > len(values):
            choice = input("Invalid choice. Please enter a valid number (or press Enter to skip): ")
            if choice == "":
                break
        if choice != "":
            criteria[attribute] = values[int(choice) - 1]
    return criteria

def main():
    all_jsons = get_all_jsons()
    attribute_values = get_attribute_values(all_jsons)
    user_criteria = get_user_criteria(attribute_values)
    subset_jsons = get_subset_jsons(all_jsons, user_criteria)
    print(f"\nSamples matching the selected criteria:")
    for json_data in subset_jsons:
        print(json_data)

if __name__ == "__main__":
    main()