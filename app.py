from flask import Flask, render_template
import pandas as pd
import os
import re

app = Flask(__name__)

# --- Get the absolute path for the project's root directory ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# --- Helper functions to get project colors ---
def get_color_for_route(route):
    """Returns the color name associated with a project route."""
    colors = {
        '/books-to-scrape': 'violet',
        '/amazon-facewash': 'orange',
        '/flipkart-laptops': 'sky',
        '/goodreads-quotes': 'lime',
        '/top-mutual-funds': 'teal',
        '/crypto-gainers': 'fuchsia'
    }
    return colors.get(route, 'gray')

def get_color_rgb(color_name):
    """Returns the RGB value for a given color name for the chart."""
    rgb_map = {
        'violet': '139, 92, 246',
        'orange': '249, 115, 22',
        'sky': '14, 165, 233',
        'lime': '132, 204, 22',
        'teal': '20, 184, 166',
        'fuchsia': '217, 70, 239'
    }
    return rgb_map.get(color_name, '107, 114, 128') # Default to gray

# --- Main Home Page Route ---
@app.route('/')
def index():
    """Renders the new portfolio landing page."""
    # This will render the file named 'index.html' from your templates folder
    return render_template('index.html')

# --- NEW: Projects Showcase Route ---
@app.route('/projects')
def projects():
    """Renders the main showcase page with all the project buttons."""
    # This will render the file named 'home.html' from your templates folder
    return render_template('home.html')

# --- Data Loading Project Routes ---

@app.route('/books-to-scrape')
def show_books():
    """Displays data for 'Books to Scrape' from a CSV file."""
    try:
        csv_path = os.path.join(DATA_DIR, 'books.csv')
        df = pd.read_csv(csv_path)
        # Using the correct column names from books.csv
        df = df[['title', 'price', 'availability']]
        headers = ["Title", "Price", "Availability"]
        df.columns = headers
        data = list(df.to_records(index=False))
        
        chart_labels = df['Title'].tolist()
        chart_data = df['Price'].str.replace('Â£', '', regex=False).astype(float).tolist()
        chart_label = "Price (£)"
        color = get_color_for_route('/books-to-scrape')

    except FileNotFoundError:
        return "Error: books.csv not found in the 'data' folder.", 404
    except Exception as e:
        return f"An error occurred in show_books: {e}", 500

    return render_template('showcase.html', project_title="Books To Scrape", description="Data from a fictional online bookstore.", headers=headers, data=data, color=color, color_rgb=get_color_rgb(color), chart_labels=chart_labels, chart_data=chart_data, chart_label=chart_label)

@app.route('/amazon-facewash')
def show_amazon_facewash():
    """Displays data for Amazon Facewash products from a CSV file."""
    try:
        csv_path = os.path.join(DATA_DIR, 'amazon_facewash.csv')
        df = pd.read_csv(csv_path)
        # Using the correct column names from amazon_facewash.csv
        df = df[['Title', 'Price']]
        df['Price'] = df['Price'].astype(str).str.replace('₹', '', regex=False).str.replace(',', '', regex=False)
        df = df[pd.to_numeric(df['Price'], errors='coerce').notna()]
        df['Price'] = df['Price'].astype(float)
        
        headers = ["Product Name", "Price (₹)"]
        df.columns = headers
        data = list(df.to_records(index=False))

        chart_labels = df['Product Name'].tolist()
        chart_data = df['Price (₹)'].tolist()
        chart_label = "Price (₹)"
        color = get_color_for_route('/amazon-facewash')

    except FileNotFoundError:
        return "Error: amazon_facewash.csv not found in the 'data' folder.", 404
    except Exception as e:
        return f"An error occurred in show_amazon_facewash: {e}", 500

    return render_template('showcase.html', project_title="Amazon Facewash", description="Top facewash products from Amazon.", headers=headers, data=data, color=color, color_rgb=get_color_rgb(color), chart_labels=chart_labels, chart_data=chart_data, chart_label=chart_label)

@app.route('/flipkart-laptops')
def show_flipkart_laptops():
    """Displays data for Flipkart Laptops from a CSV file."""
    try:
        csv_path = os.path.join(DATA_DIR, 'flipkart-laptops.csv')
        df = pd.read_csv(csv_path)
        # Using the correct column names from flipkart-laptops.csv
        df = df[['Name', 'Price', 'Ratings']]
        headers = ["Laptop Model", "Price (₹)", "Rating"]
        df.columns = headers
        
        df['Price (₹)'] = df['Price (₹)'].astype(str).str.replace('₹', '', regex=False).str.replace(',', '', regex=False)
        df = df[pd.to_numeric(df['Price (₹)'], errors='coerce').notna()]
        df['Price (₹)'] = df['Price (₹)'].astype(int)
        data = list(df.to_records(index=False))

        chart_labels = df['Laptop Model'].tolist()
        chart_data = df['Price (₹)'].tolist()
        chart_label = "Price (₹)"
        color = get_color_for_route('/flipkart-laptops')

    except FileNotFoundError:
        return "Error: flipkart-laptops.csv not found in the 'data' folder.", 404
    except Exception as e:
        return f"An error occurred in show_flipkart_laptops: {e}", 500

    return render_template('showcase.html', project_title="Flipkart Laptops", description="Latest laptop listings from Flipkart.", headers=headers, data=data, color=color, color_rgb=get_color_rgb(color), chart_labels=chart_labels, chart_data=chart_data, chart_label=chart_label)

@app.route('/goodreads-quotes')
def show_goodreads_quotes():
    """Displays data for Goodreads Quotes from a CSV file."""
    try:
        csv_path = os.path.join(DATA_DIR, 'goodreads-quotes.csv')
        df = pd.read_csv(csv_path)
        # Using the correct column names from goodreads-quotes.csv
        headers = ['Quote', 'Author']
        df = df[headers]
        data = list(df.to_records(index=False))

        # Charting the length of quotes as 'Tags' column is not available
        df['Quote Length'] = df['Quote'].str.len()
        
        chart_df = df.nlargest(10, 'Quote Length') # Keep this to 10 for readability
        chart_labels = chart_df['Author'].tolist()
        chart_data = chart_df['Quote Length'].tolist()
        chart_label = "Quote Length (Characters)"
        color = get_color_for_route('/goodreads-quotes')

    except FileNotFoundError:
        return "Error: goodreads_quotes.csv not found in the 'data' folder.", 404
    except Exception as e:
        return f"An error occurred in show_goodreads_quotes: {e}", 500

    return render_template('showcase.html', project_title="Goodreads Quotes", description="Popular and inspiring quotes from Goodreads.", headers=headers, data=data, color=color, color_rgb=get_color_rgb(color), chart_labels=chart_labels, chart_data=chart_data, chart_label=chart_label)

@app.route('/top-mutual-funds')
def show_mutual_funds():
    """Displays data for Top Mutual Funds from a CSV file."""
    try:
        csv_path = os.path.join(DATA_DIR, 'mutual_funds.csv')
        df = pd.read_csv(csv_path)
        # Using the correct column names from mutual_funds.csv
        df = df[['Name', '52 Weeks Change%']]
        df['52 Weeks Change%'] = df['52 Weeks Change%'].astype(str).str.replace('%', '', regex=False)
        df = df[pd.to_numeric(df['52 Weeks Change%'], errors='coerce').notna()]
        df['52 Weeks Change%'] = df['52 Weeks Change%'].astype(float)

        headers = ["Fund Name", "52 Week Change (%)"]
        df.columns = headers
        data = list(df.to_records(index=False))

        chart_labels = df['Fund Name'].tolist()
        chart_data = df['52 Week Change (%)'].tolist()
        chart_label = "52 Week Change (%)"
        color = get_color_for_route('/top-mutual-funds')

    except FileNotFoundError:
        return "Error: mutual_funds.csv not found in the 'data' folder.", 404
    except Exception as e:
        return f"An error occurred in show_mutual_funds: {e}", 500

    return render_template('showcase.html', project_title="Top Mutual Funds", description="Top performing mutual funds.", headers=headers, data=data, color=color, color_rgb=get_color_rgb(color), chart_labels=chart_labels, chart_data=chart_data, chart_label=chart_label)

@app.route('/crypto-gainers')
def show_crypto_gainers():
    """Displays data for Top Crypto Gainers from a CSV file."""
    try:
        # IMPORTANT: The user must rename 'Top Gainer Crypto currency.csv' to 'crypto_gainers.csv'
        csv_path = os.path.join(DATA_DIR, 'crypto_gainers.csv')
        df = pd.read_csv(csv_path, on_bad_lines='skip')
        
        # Extracting data from the combined 'Price' column
        def extract_crypto_data(row):
            price_str = str(row)
            # Regex to find price and percentage change
            price_match = re.search(r'(\d+\.\d+)', price_str)
            change_match = re.search(r'\(([\+\-.,\d]+)%\)', price_str)
            
            price = float(price_match.group(1)) if price_match else 0
            change = float(change_match.group(1).replace(',', '')) if change_match else 0
            return price, change

        # The relevant data is in the 4th column (index 3), which is unnamed
        df[['Price (USD)', '24h Change (%)']] = df.iloc[:, 3].apply(lambda x: pd.Series(extract_crypto_data(x)))
        df = df[['Name', 'Price (USD)', '24h Change (%)']]
        df = df.dropna()

        headers = list(df.columns)
        data = list(df.to_records(index=False))

        chart_labels = df['Name'].tolist()
        chart_data = df['24h Change (%)'].tolist()
        chart_label = "24h Change (%)"
        color = get_color_for_route('/crypto-gainers')

    except FileNotFoundError:
        return "Error: crypto_gainers.csv not found in the 'data' folder. Please rename your file.", 404
    except Exception as e:
        return f"An error occurred in show_crypto_gainers: {e}", 500

    return render_template('showcase.html', project_title="Crypto Gainers", description="Top gainer cryptocurrencies.", headers=headers, data=data, color=color, color_rgb=get_color_rgb(color), chart_labels=chart_labels, chart_data=chart_data, chart_label=chart_label)

if __name__ == '__main__':
    app.run(debug=True)
