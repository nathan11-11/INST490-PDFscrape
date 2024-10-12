# PDF Scraper

This repository contains a Python script that scrapes text from PDF files. The script can extract and organize text data from PDF documents for further analysis, storage, or presentation. Additionally, folders in this repository contain sample PDF files and their respective scraped results to demonstrate the functionality of the scraper.

## Features

- Extract text from PDFs using Python.
- Save extracted data into organized folders for easy reference.
- Handles different structures of PDF documents, allowing for versatile use.

## Requirements

To run the PDF scraper, you will need the following dependencies installed:

- Python 3.x
- Required libraries: `PyPDF2`, `os`, `re`

You can install the required libraries using the command:

```sh
pip install -r requirements.txt
```

## Usage

To use the PDF scraper, follow these steps:

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/pdf-scraper.git
   ```

2. Navigate to the project directory:

   ```sh
   cd pdf-scraper
   ```

3. Place the PDFs you want to scrape inside the `pdfs/` folder.

4. Run the scraper script:

   ```sh
   python pdfscraper.py
   ```

5. Extracted text will be saved in the `scraped_results/` folder, with each PDF having its own corresponding output file.

## Folder Structure

- `pdf/` - Contains the original PDF files to be scraped.
- `scraped/` - Stores the text extracted from each PDF in separate files.
- `pdfscraper.py` - The Python script that performs the scraping.

