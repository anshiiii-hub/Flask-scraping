# PDF and CSV File Connections Summary

## Overview
Successfully connected all PDF and CSV files with their respective download and view buttons across the portfolio website.

## Flask Routes Added

### 1. Existing Route (Enhanced)
- **Route**: `/download/<path:filename>`
- **Purpose**: Download CSV files from the `data/` directory
- **Usage**: `{{ url_for('download_file', filename='filename.csv') }}`

### 2. New PDF Download Route
- **Route**: `/download-pdf/<path:filename>`
- **Purpose**: Download PDF files from the `pdf/` directory
- **Usage**: `{{ url_for('download_pdf', filename='filename.pdf') }}`

### 3. New PDF View Route
- **Route**: `/view-pdf/<path:filename>`
- **Purpose**: View PDF files in browser from the `pdf/` directory
- **Usage**: `{{ url_for('view_pdf', filename='filename.pdf') }}`

## File Connections by Template

### 1. Amazon Facewash (`amazon-facewash.html`)
- **PDF**: `amazon.pdf`
  - View: `{{ url_for('view_pdf', filename='amazon.pdf') }}`
  - Download: `{{ url_for('download_pdf', filename='amazon.pdf') }}`
- **CSV**: `amazon_facewash.csv`
  - View/Download: `{{ url_for('download_file', filename='amazon_facewash.csv') }}`

### 2. Books to Scrape (`books-to-scrape.html`)
- **PDF**: `goodreads.pdf` (Note: Using goodreads.pdf as books-specific PDF wasn't available)
  - View: `{{ url_for('view_pdf', filename='goodreads.pdf') }}`
  - Download: `{{ url_for('download_pdf', filename='goodreads.pdf') }}`
- **CSV**: `books.csv`
  - View/Download: `{{ url_for('download_file', filename='books.csv') }}`

### 3. Crypto Gainers (`crypto-gainers.html`)
- **PDF**: `crypto.pdf`
  - View: `{{ url_for('view_pdf', filename='crypto.pdf') }}`
  - Download: `{{ url_for('download_pdf', filename='crypto.pdf') }}`
- **CSV**: `crypto_gainers.csv`
  - View/Download: `{{ url_for('download_file', filename='crypto_gainers.csv') }}`

### 4. Flipkart Laptops (`flipkart-laptops.html`)
- **CSV**: `flipkart-laptops.csv`
  - View/Download: `{{ url_for('download_file', filename='flipkart-laptops.csv') }}`
- **PDF**: Not available (could be added if laptop analysis PDF is created)

### 5. Goodreads Quotes (`goodreads-quotes.html`)
- **PDF**: `goodreads.pdf`
  - View: `{{ url_for('view_pdf', filename='goodreads.pdf') }}`
  - Download: `{{ url_for('download_pdf', filename='goodreads.pdf') }}`
- **CSV**: `goodreads-quotes.csv`
  - View/Download: `{{ url_for('download_file', filename='goodreads-quotes.csv') }}`

### 6. Top Mutual Funds (`top-mutual-funds.html`)
- **PDF**: `mutual funds.pdf`
  - View: `{{ url_for('view_pdf', filename='mutual funds.pdf') }}`
  - Download: `{{ url_for('download_pdf', filename='mutual funds.pdf') }}`
- **CSV**: `mutual_funds.csv`
  - View/Download: `{{ url_for('download_file', filename='mutual_funds.csv') }}`

### 7. IPL Analysis (`ipl-analysis.html`)
- **CSV**: `IPL/matches.csv` and `IPL/deliveries.csv`
  - Download: `{{ url_for('download_file', filename='IPL/matches.csv') }}`
  - Download: `{{ url_for('download_file', filename='IPL/deliveries.csv') }}`

### 8. UPI Analysis (`upi-analysis.html`)
- **CSV**: `UPI.csv`
  - Download: `{{ url_for('download_file', filename='UPI.csv') }}`

### 9. Stock Market Analysis (`stock-market-analysis.html`)
- **CSV**: Dynamic CSV generation via JavaScript function
  - Download: Custom `downloadCSV()` JavaScript function

## Available Files

### PDF Files in `/pdf/` directory:
- `amazon.pdf` - Amazon facewash analysis
- `crypto.pdf` - Cryptocurrency gainers analysis
- `goodreads.pdf` - Goodreads quotes analysis
- `mutual funds.pdf` - Mutual funds analysis

### CSV Files in `/data/` directory:
- `amazon_facewash.csv` - Amazon facewash data
- `books.csv` - Books scraping data
- `crypto_gainers.csv` - Cryptocurrency data
- `flipkart-laptops.csv` - Flipkart laptop data
- `goodreads-quotes.csv` - Goodreads quotes data
- `mutual_funds.csv` - Mutual funds data
- `UPI.csv` - UPI analysis data
- `IPL/matches.csv` - IPL matches data
- `IPL/deliveries.csv` - IPL deliveries data

## Button Styling
All download and view buttons use the `asset-button` CSS class with consistent styling:
- SVG icons for visual clarity
- Hover effects
- Proper spacing and alignment
- Responsive design

## Security and Best Practices
- All file serving uses Flask's `send_from_directory()` function for security
- PDF viewing opens in new tab (`target="_blank"`)
- Download links use the `download` attribute for forced downloads
- Proper URL generation using `url_for()` for maintainability

## Testing
- All routes successfully imported and available
- Flask application runs without errors
- File paths correctly resolve to existing files