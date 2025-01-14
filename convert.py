import xml.etree.ElementTree as ET
import csv

def convert_xmi_to_csv(input_file, output_file):
    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    # Open CSV file for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write headers based on your XML structure
        csvwriter.writerow(['Element', 'Attribute', 'Value'])
        
        # Iterate over XML elements
        for element in root.iter():
            if element.tag.endswith('Element'):
                element_name = element.get('name', '')
                attribute_name = element.find('Attribute').get('name', '')
                value = element.find('Attribute').text if element.find('Attribute') is not None else ''
                csvwriter.writerow([element_name, attribute_name, value])


# Example usage:
#if __name__ == "__main__":
 #   input_file = 'input.xmi'  # Replace with your XMI file path
  #  output_file = 'output.csv'  # Replace with desired CSV output path
   # convert_xmi_to_csv(input_file, output_file)
