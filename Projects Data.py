import os
import pandas as pd
import matplotlib.pyplot as plt

def find_files(directory, extension):
    return [os.path.join(root, file)
            for root, _, files in os.walk(directory)
            for file in files
            if file.endswith(extension)]

def extract_text_from_files(files):
    extracted_text = []
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as file:
            extracted_text.append(file.read())
    return extracted_text

# Example usage
folder_path = '\\path\\to\\directory' # Change this to the desired path
file_extension = '.txt'  # Change this to the desired file extension
found_files = find_files(folder_path, file_extension)
extracted_text = extract_text_from_files(found_files)

def extract_key_value_pairs(text):
    # Split the text into lines
    lines = text.split('\n')
    # Find the index of the line containing "Address"
    address_index = next((i for i, line in enumerate(lines) if "Address" in line), None)
    # Extract the desired information if "Address" is found
    if address_index is not None:
        # Ensure we have enough lines to extract
        if len(lines) > address_index + 1:
            # Extract "Address" line and the following line
            address_info = {
                "Address": lines[address_index],
                "Value": lines[address_index + 1]
            }
            return address_info
    return None
    
data = [extract_key_value_pairs(text) for text in extracted_text if extract_key_value_pairs(text) is not None]

# Create a DataFrame from the extracted data
df = pd.DataFrame(data)

# Convert all values in the DataFrame to uppercase
df = df.apply(lambda x: x.str.upper() if x.dtype == "object" else x)

# Show only values
values = df["Value"]

# Filter rows where the value contains 'CA'
ca_addresses = df[df['Value'].str.contains('CA')]

# Add a new column 'State' by extracting state information from 'Value' column
df['State'] = df['Value'].str.split(',').str[-2].str.strip()

# Group data by 'State' and calculate the count of rows in each group
state_counts = df.groupby('State').size()

# Calculate percentages
state_percentages = (state_counts / state_counts.sum()) * 100

# Plot the bar chart
plt.figure(figsize=(16, 8))  # Set the figure size
bars = plt.bar(state_percentages.index, state_percentages.values, color='skyblue')  # Create a bar plot

# Highlight the column with the highest percentage
max_percentage_index = state_percentages.idxmax()
max_percentage_bar = bars[state_percentages.index.get_loc(max_percentage_index)]
max_percentage_bar.set_color('orange')  # Set color to orange

# Add annotations for percentages
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom')

plt.title('Sum of projects grouped by State, shown in percentages')  # Set the title
plt.xlabel('States')  # Set the x-axis label
plt.ylabel('Percentage')  # Set the y-axis label
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()  # Show the plot
