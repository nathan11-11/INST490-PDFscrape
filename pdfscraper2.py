import pdfplumber
import pandas as pd
import os

# Load the PDF
pdf_path = 'ee2005.pdf'
output_dir = 'ee2005csv'  # Output directory for CSV files

# Create output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Extract tables from the PDF
with pdfplumber.open(pdf_path) as pdf:
    table_counter = 1  # To keep track of table numbers for CSV file names
    for page_number, page in enumerate(pdf.pages, start=1):
        tables = page.extract_tables()
        
        for table in tables:
            # Clean and process the table data to remove empty rows and columns
            cleaned_table = [row for row in table if any(cell is not None and cell.strip() for cell in row)]
            if len(cleaned_table) == 0:
                continue
            
            # Standardize the number of columns for all rows by filling missing values
            max_columns = max(len(row) for row in cleaned_table)
            cleaned_table = [row + [''] * (max_columns - len(row)) for row in cleaned_table]
            
            # Convert extracted table to a DataFrame
            df = pd.DataFrame(cleaned_table[1:], columns=cleaned_table[0])
            
            # Define output CSV file path
            csv_file_path = f"{output_dir}table_{table_counter}.csv"
            
            # Save the DataFrame as a CSV
            df.to_csv(csv_file_path, index=False)
            
            print(f"Extracted table {table_counter} from page {page_number} and saved to {csv_file_path}")
            
            table_counter += 1

print("Extraction complete.")
