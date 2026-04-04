from flask import Flask, render_template, send_from_directory
import pandas as pd
import os
import re
import requests
# import yfinance as yf # Import the yfinance library - commented out due to issues
from datetime import datetime, timedelta # Import datetime for date calculations

app = Flask(__name__)

# --- Get the absolute path for the project's root directory ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# --- Helper functions to get project colors ---
def get_color_for_route(route):
    """Returns the color name associated with a project route for UI consistency."""
    colors = {
        '/projects/web-scraping/books-to-scrape': 'violet',
        '/projects/web-scraping/amazon-facewash': 'orange',
        '/projects/web-scraping/flipkart-laptops': 'sky',
        '/projects/web-scraping/goodreads-quotes': 'lime',
        '/projects/web-scraping/top-mutual-funds': 'teal',
        '/projects/web-scraping/crypto-gainers': 'fuchsia'
    }
    return colors.get(route, 'gray')

def get_color_rgb(color_name):
    """Returns the RGB value for a given color name for the chart's styling."""
    rgb_map = {
        'violet': '139, 92, 246',
        'orange': '249, 115, 22',
        'sky': '14, 165, 233',
        'lime': '132, 204, 22',
        'teal': '20, 184, 166',
        'fuchsia': '217, 70, 239'
    }
    return rgb_map.get(color_name, '107, 114, 128')

# --- Main App Routes ---
@app.route('/')
def index():
    """Renders the main portfolio landing page."""
    return render_template('home.html')

@app.route('/projects')
def projects():
    """Renders the page with the grid of all project categories."""
    return render_template('projects.html')

@app.route('/about-me')
def about_me():
    """Renders the dedicated 'About Me' page."""
    return render_template('aboutme.html')

@app.route('/blogs')
def blogs():
    """Renders the blogs page."""
    return render_template('blogs.html')

@app.route('/codroidhub')
def codroidhub():
    """Renders the CodroidHub page (placeholder)."""
    return render_template('codroidhub.html')

@app.route('/github')
def github():
    """Fetches and displays GitHub repositories and stats."""
    github_username = "anshiiii-hub"
    api_url = f"https://api.github.com/users/{github_username}/repos?sort=updated&direction=desc"
    repos = []
    error = None
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        repos = response.json()
    except requests.exceptions.RequestException as e:
        error = f"Could not fetch GitHub repositories: {e}"
    
    return render_template('github.html', username=github_username, repos=repos, error=error)

@app.route('/journey')
def journey():
    return render_template('journey.html')


# --- Project Category Routes ---
@app.route('/projects/web-scraping')
def web_scraping_projects():
    """Renders the page showing all individual web scraping projects."""
    return render_template('web_scraping_projects.html')

@app.route('/projects/data-science')
def data_science_projects():
    """Renders the page showing all individual data science projects."""
    projects_list = [
        {
            "title": "Tech Stock Volatility Analysis",
            "url": "/projects/data-science/stock-market-analysis",
            "image": "images/stock-market.jpg",
            "objective": "To analyze and compare the historical stock price volatility and daily returns of major tech giants, Apple (AAPL) and Google (GOOG).",
            "insight": "Visualizing daily returns and moving averages reveals distinct volatility patterns and potential investment signals, such as golden cross events."
        },
        {
            "title": "IPL Match & Player Performance Analysis",
            "url": "/projects/data-science/ipl-analysis",
            "image": "images/ipl.png",
            "objective": "To perform an exploratory data analysis on historical IPL data to uncover strategic insights related to match outcomes, toss decisions, and top player performances.",
            "insight": "Analysis reveals that while winning the toss provides a slight advantage, the decision to bat or field has a significant, venue-dependent impact on match outcomes."
        },
        {
            "title": "UPI Transaction Growth Analysis",
            "url": "/projects/data-science/upi-analysis",
            "image": "images/upi.avif",
            "objective": "To analyze the exponential growth of India's Unified Payments Interface (UPI) by examining transaction volume and value over time.",
            "insight": "The time-series analysis clearly illustrates the hockey-stick growth curve of UPI adoption, highlighting its rapid integration into the Indian economy."
        }
    ]
    return render_template('data_science_projects.html', projects=projects_list)

# --- Placeholder route for other project categories ---
@app.route('/aiml')
def aiml():
    """Renders a generic 'Coming Soon' page for unfinished sections."""
    return render_template('aiml.html')

@app.route('/power-bi')
def power_bi():
    """Renders a generic 'Coming Soon' page for unfinished sections."""
    return render_template('power_bi.html')


# --- Individual Data Project Routes ---

@app.route('/projects/web-scraping/books-to-scrape')
def show_books():
    """Displays data and charts for 'Books to Scrape'."""
    try:
        csv_path = os.path.join(DATA_DIR, 'books.csv')
        df = pd.read_csv(csv_path)
        df = df[['title', 'price', 'availability']]
        df['price'] = df['price'].str.replace('Â£', '', regex=False).astype(float)
        headers = ["Title", "Price (£)", "Availability"]
        df.columns = headers
        data = df.to_dict('records')  # Convert to list of dictionaries for template compatibility
        charts_data = {
            'bar_chart_data': {
                'labels': df.head(20)['Title'].apply(lambda x: x[:25] + '...').tolist(),
                'data': df.head(20)['Price (£)'].tolist()
            },
            'pie_chart_data': {
                'labels': df['Availability'].value_counts().index.tolist(),
                'data': df['Availability'].value_counts().values.tolist()
            }
        }
        color = get_color_for_route('/projects/web-scraping/books-to-scrape')
        source_url = "http://books.toscrape.com"
    except FileNotFoundError:
        return "Error: books.csv not found.", 404
    except Exception as e:
        return f"An error occurred: {e}", 500
    return render_template('books-to-scrape.html', project_title="Books To Scrape", description="Data from a fictional online bookstore.", headers=headers, data=data, color=color, color_rgb=get_color_rgb(color), source_url=source_url, bar_chart_data=charts_data['bar_chart_data'], pie_chart_data=charts_data['pie_chart_data'])

@app.route('/projects/data-science/stock-market-analysis')
def show_stock_market_analysis():
    """Displays data and charts for Stock Market Analysis."""
    try:
        # Using placeholder data instead of yfinance due to import issues
        data = {
            'Date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']),
            'AAPL_Close': [170.1, 172.3, 171.5, 175.0, 174.9],
            'GOOG_Close': [2800.5, 2820.0, 2815.3, 2850.1, 2845.8]
        }
        df = pd.DataFrame(data)
        df['AAPL_Returns'] = df['AAPL_Close'].pct_change() * 100
        df['GOOG_Returns'] = df['GOOG_Close'].pct_change() * 100
        
        headers = ["Date", "Apple Close", "Google Close", "Apple Daily % Return", "Google Daily % Return"]
        
        # Prepare data for rendering
        table_data = df[['Date', 'AAPL_Close', 'GOOG_Close', 'AAPL_Returns', 'GOOG_Returns']].fillna(0)
        table_data['Date'] = table_data['Date'].dt.strftime('%Y-%m-%d')
        
        # Chart data
        line_chart_data = {
            'labels': table_data['Date'].tolist(),
            'datasets': [
                {
                    'label': 'Apple Close Price',
                    'data': df['AAPL_Close'].tolist(),
                    'borderColor': 'rgba(96, 165, 250, 1)',
                    'backgroundColor': 'rgba(96, 165, 250, 0.5)',
                },
                {
                    'label': 'Google Close Price',
                    'data': df['GOOG_Close'].tolist(),
                    'borderColor': 'rgba(251, 146, 60, 1)',
                    'backgroundColor': 'rgba(251, 146, 60, 0.5)',
                }
            ]
        }

        bar_chart_data = {
            'labels': table_data['Date'].tolist(),
            'datasets': [
                {
                    'label': 'Apple Daily Return %',
                    'data': df['AAPL_Returns'].fillna(0).tolist(),
                    'backgroundColor': 'rgba(52, 211, 153, 0.7)',
                },
                {
                    'label': 'Google Daily Return %',
                    'data': df['GOOG_Returns'].fillna(0).tolist(),
                    'backgroundColor': 'rgba(248, 113, 113, 0.7)',
                }
            ]
        }

        color = 'violet'
        
    except Exception as e:
        return f"An error occurred: {e}", 500
        
    return render_template(
        'stock-market-analysis.html', 
        project_title="Tech Stock Market Analysis", 
        description="Analysis of Apple (AAPL) vs. Google (GOOG) stock performance.", 
        headers=headers, 
        data=table_data.to_dict(orient='records'), 
        color=color, 
        color_rgb=get_color_rgb(color), 
        source_url="#",
        line_chart_data=line_chart_data,
        bar_chart_data=bar_chart_data
    )

@app.route('/projects/web-scraping/amazon-facewash')
def show_amazon_facewash():
    """Displays data and charts for Amazon Facewash products."""
    try:
        csv_path = os.path.join(DATA_DIR, 'amazon_facewash.csv')
        df = pd.read_csv(csv_path)
        
        # Data cleaning and preparation
        df = df[['Title', 'Price']].copy()
        df.columns = ['Name', 'Price']
        df['Price'] = df['Price'].astype(str).str.replace('₹', '', regex=False).str.replace(',', '', regex=False)
        df = df[pd.to_numeric(df['Price'], errors='coerce').notna()]
        df['Price'] = df['Price'].astype(float)
        
        # Prepare data for the template
        headers = ["Product Name", "Price (₹)"]
        df.columns = headers
        data = df.to_dict(orient='records')

        # Bar chart data: Top 15 most expensive products
        bar_chart_df = df.nlargest(15, 'Price (₹)')
        bar_chart_data = {
            'labels': bar_chart_df['Product Name'].apply(lambda x: x[:25] + '...').tolist(),
            'data': bar_chart_df['Price (₹)'].tolist()
        }

        # No pie chart since there is no rating data
        pie_chart_data = None

        color = get_color_for_route('/projects/web-scraping/amazon-facewash')
        source_url = "https://www.amazon.in/s?k=facewash"
        
    except FileNotFoundError:
        return "Error: amazon_facewash.csv not found.", 404
    except Exception as e:
        return f"An error occurred: {e}", 500
        
    return render_template(
        'amazon-facewash.html', 
        project_title="Amazon Facewash", 
        description="Top facewash products from Amazon.", 
        headers=headers, 
        data=data, 
        color=color, 
        color_rgb=get_color_rgb(color), 
        source_url=source_url, 
        bar_chart_data=bar_chart_data,
        pie_chart_data=pie_chart_data
    )

@app.route('/projects/web-scraping/flipkart-laptops')
def show_laptops():
    """Displays data and charts for Flipkart Laptops."""
    try:
        csv_path = os.path.join(DATA_DIR, 'flipkart-laptops.csv')
        df = pd.read_csv(csv_path)
        # It's better to work with copies to avoid SettingWithCopyWarning
        df = df[['Name', 'Price', 'Ratings']].copy()
        
        # Keep original price format for display but create numeric version for charts
        df['price_numeric'] = df['Price'].str.replace('[₹,]', '', regex=True).astype(float)
        df['Ratings'] = pd.to_numeric(df['Ratings'], errors='coerce').fillna(0)

        # Rename columns to match template expectations - fixing the column count issue
        df = df.rename(columns={'Name': 'name', 'Price': 'price', 'Ratings': 'rating'})
        
        # Prepare data for rendering - include both display price and numeric price
        data_for_template = df[['name', 'price', 'price_numeric', 'rating']].to_dict(orient='records')

    except FileNotFoundError:
        return "Error: flipkart-laptops.csv not found.", 404
    except Exception as e:
        return f"An error occurred: {e}", 500
        
    return render_template(
        'flipkart-laptops.html', 
        data=data_for_template
    )

@app.route('/projects/web-scraping/goodreads-quotes')
def show_goodreads_quotes():
    """Displays data for Goodreads Quotes."""
    try:
        csv_path = os.path.join(DATA_DIR, 'goodreads-quotes.csv')
        df = pd.read_csv(csv_path)
        # Ensure the columns are named 'quote' and 'author' for the template
        df = df[['Quote', 'Author']].copy()
        df.columns = ['quote', 'author']
        
        # Prepare data for rendering
        data_for_template = df.to_dict(orient='records')

    except FileNotFoundError:
        return "Error: goodreads-quotes.csv not found.", 404
    except Exception as e:
        return f"An error occurred: {e}", 500
        
    return render_template(
        'goodreads-quotes.html', 
        data=data_for_template
    )

@app.route('/projects/web-scraping/top-mutual-funds')
def show_mutual_funds():
    """Displays data for Top Mutual Funds."""
    try:
        csv_path = os.path.join(DATA_DIR, 'mutual_funds.csv')
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()
        display_cols = ['Name', 'Symbol', 'Last Price', 'Change', '52 Weeks Change%']
        df_display = df[display_cols].copy()
        df_display['52 Weeks Change%'] = pd.to_numeric(df_display['52 Weeks Change%'].astype(str).str.replace('%', '', regex=False), errors='coerce')
        df_display = df_display.dropna()  # Remove rows with NaN values
        headers = ["Fund Name", "Symbol", "Last Price", "Change", "52 Week Change (%)"]
        df_display.columns = headers
        data = df_display.values.tolist()
        chart_df = df_display.nlargest(15, '52 Week Change (%)')
        charts_data = [{'type': 'bar', 'title': 'Top 15 by 52 Week Change (%)', 'labels': chart_df['Fund Name'].apply(lambda x: x[:25] + '...').tolist(), 'data': chart_df['52 Week Change (%)'].tolist(), 'label': '52 Week Change (%)'}]
        color = get_color_for_route('/projects/web-scraping/top-mutual-funds')
        source_url = "https://finance.yahoo.com/markets/mutualfunds"
    except FileNotFoundError:
        return "Error: mutual_funds.csv not found.", 404
    except Exception as e:
        return f"An error occurred: {e}", 500
    return render_template('top-mutual-funds.html', project_title="Top Mutual Funds", description="Top performing mutual funds.", headers=headers, data=data, color=color, color_rgb=get_color_rgb(color), source_url=source_url, charts_data=charts_data)

@app.route('/projects/web-scraping/crypto-gainers')
def show_crypto_gainers():
    """Displays data for Top Crypto Gainers."""
    try:
        csv_path = os.path.join(DATA_DIR, 'crypto_gainers.csv')
        df = pd.read_csv(csv_path, on_bad_lines='skip')
        df.columns = [col.strip() for col in df.columns]
        
        # Use the actual columns from the CSV
        display_cols = ['Name', 'Symbol', 'Price', '% Change', 'Market Cap', 'Volume']
        df_display = df[display_cols].copy().dropna()
        
        # Clean the data
        df_display['Price'] = pd.to_numeric(df_display['Price'], errors='coerce').fillna(0)
        df_display['% Change'] = pd.to_numeric(df_display['% Change'], errors='coerce').fillna(0)
        
        headers=["Name", "Symbol", "Price (USD)", "24h Change (%)", "Market Cap", "Volume"]
        df_display.columns = headers
        data = df_display.to_dict(orient='records')  # Convert to list of dictionaries for template compatibility
        
        change_chart_df = df_display.nlargest(15, '24h Change (%)')
        price_chart_df = df_display.nlargest(10, 'Price (USD)')
        charts_data = [
            {
                'type': 'bar', 
                'title': 'Top 15 by 24h Change (%)', 
                'labels': change_chart_df['Name'].tolist(), 
                'data': change_chart_df['24h Change (%)'].tolist(), 
                'label': '24h Change (%)'
            }, 
            {
                'type': 'bar', 
                'title': 'Top 10 by Price (USD)', 
                'labels': price_chart_df['Name'].tolist(), 
                'data': price_chart_df['Price (USD)'].tolist(), 
                'label': 'Price (USD)'
            }
        ]
        color = get_color_for_route('/projects/web-scraping/crypto-gainers')
        source_url = "https://finance.yahoo.com/markets/crypto/gainers/"
    except FileNotFoundError:
        return "Error: crypto_gainers.csv not found.", 404
    except Exception as e:
        return f"An error occurred: {e}", 500
    return render_template('crypto-gainers.html', project_title="Crypto Gainers", description="Top gainer cryptocurrencies.", headers=headers, data=data, color=color, color_rgb=get_color_rgb(color), source_url=source_url, charts_data=charts_data)

@app.route('/projects/data-science/ipl-analysis')
def show_ipl_analysis():
    """Displays data and charts for IPL Analysis."""
    try:
        matches_path = os.path.join(DATA_DIR, 'IPL', 'matches.csv')
        deliveries_path = os.path.join(DATA_DIR, 'IPL', 'deliveries.csv')
        
        matches_df = pd.read_csv(matches_path)
        deliveries_df = pd.read_csv(deliveries_path)

        # --- Prepare data for template ---
        project_title = "IPL Data Analysis (2008-2020)"
        description = "An in-depth analysis of historical IPL data to uncover trends in match outcomes, player performances, and team strategies."

        # --- Table Preview (from matches.csv) ---
        preview_df = matches_df.head()
        headers = preview_df.columns.tolist()
        data = preview_df.values.tolist()
        
        # Ensure data is not empty
        if not data:
            data = [['No data'] * len(headers) if headers else ['No data']]

        # --- Chart 1: Toss Decision Percentage ---
        toss_decision_counts = matches_df['toss_decision'].value_counts()
        chart1 = {
            'type': 'pie',
            'title': 'Toss Decision Percentage',
            'labels': toss_decision_counts.index.tolist(),
            'data': toss_decision_counts.values.tolist(),
            'label': 'Toss Decision'
        }

        # --- Chart 2: Matches Won by Biggest Margin (Runs) ---
        runs_wins = matches_df[matches_df['result'] == 'runs'].nlargest(5, 'result_margin')[['winner', 'result_margin']]
        chart2 = {
            'type': 'bar',
            'title': 'Top 5 Wins by Runs Margin',
            'labels': runs_wins['winner'].tolist(),
            'data': runs_wins['result_margin'].tolist(),
            'label': 'Runs'
        }

        # --- Chart 3: Top 5 Venues by Match Count ---
        top_venues = matches_df['venue'].value_counts().nlargest(5)
        chart3 = {
            'type': 'bar',
            'title': 'Top 5 Venues by Match Count',
            'labels': top_venues.index.tolist(),
            'data': top_venues.values.tolist(),
            'label': 'Matches Hosted'
        }

        # --- Chart 4: Top 5 Batsmen by Total Runs ---
        top_batsmen = deliveries_df.groupby('batter')['batsman_runs'].sum().nlargest(5)
        chart4 = {
            'type': 'bar',
            'title': 'Top 5 Batsmen by Total Runs',
            'labels': top_batsmen.index.tolist(),
            'data': top_batsmen.values.tolist(),
            'label': 'Total Runs'
        }
        
        charts_data = [chart1, chart2, chart3, chart4]

    except FileNotFoundError:
        return "Error: IPL dataset not found in data/IPL/", 404
    except Exception as e:
        return f"An error occurred: {e}", 500
        
    return render_template(
        'ipl-analysis.html', 
        project_title=project_title,
        description=description,
        headers=headers,
        data=data,
        charts_data=charts_data
    )

@app.route('/projects/data-science/upi-analysis')
def show_upi_analysis():
    """Displays data and charts for UPI Transaction Analysis."""
    try:
        csv_path = os.path.join(DATA_DIR, 'UPI.csv')
        df = pd.read_csv(csv_path)

        # --- Data Cleaning and Preparation ---
        # Use the correct date column and convert to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Create volume in billions (from Mn column)
        df['Volume_in_Billions'] = df['Volume (in Mn)'] / 1000  # Convert millions to billions
        
        # Create value in trillions (from Cr column) 
        df['Value_in_Trillions_INR'] = df['Value (in Cr.)'] / 100000  # Convert crores to trillions
        
        # Filter out rows with zero or null values
        df = df[(df['Volume_in_Billions'] > 0) & (df['Value_in_Trillions_INR'] > 0)]
        df = df.sort_values('Date')
        
        # Check if we have any data left after filtering
        if df.empty:
            return "Error: No valid UPI data found after filtering.", 404

        # --- Prepare data for template ---
        project_title = "Decoding India's UPI Revolution"
        description = "An analysis of the explosive growth of India's Unified Payments Interface and its impact on the digital economy."
        
        # Use relevant columns for table display
        display_df = df[['Date', 'Volume_in_Billions', 'Value_in_Trillions_INR']].copy()
        headers = ['Date', 'Volume (Billions)', 'Value (Trillions INR)']
        # Format date for display in the table
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m')
        data = display_df.values.tolist()
        
        # Ensure data is not empty
        if not data:
            data = [['No data', 'No data', 'No data']]

        # --- Chart 1: Transaction Volume Over Time ---
        chart1 = {
            'type': 'line',
            'title': 'UPI Transaction Volume (in Billions)',
            'labels': df['Date'].dt.strftime('%Y-%m').tolist(),
            'data': df['Volume_in_Billions'].tolist(),
            'label': 'Volume (Billions)'
        }

        # --- Chart 2: Transaction Value Over Time ---
        chart2 = {
            'type': 'line',
            'title': 'UPI Transaction Value (in Trillions INR)',
            'labels': df['Date'].dt.strftime('%Y-%m').tolist(),
            'data': df['Value_in_Trillions_INR'].tolist(),
            'label': 'Value (Trillions INR)'
        }

        # --- Chart 3: Year-over-Year Growth in Volume ---
        df['Year'] = df['Date'].dt.year
        yearly_volume = df.groupby('Year')['Volume_in_Billions'].sum()
        yoy_growth = yearly_volume.pct_change() * 100
        
        # Remove NaN values and infinite values
        yoy_growth = yoy_growth.dropna()
        yoy_growth = yoy_growth.replace([float('inf'), float('-inf')], 0)
        
        chart3 = {
            'type': 'bar',
            'title': 'Year-over-Year Volume Growth (%)',
            'labels': yoy_growth.index.astype(str).tolist() if not yoy_growth.empty else ['No Data'],
            'data': yoy_growth.values.tolist() if not yoy_growth.empty else [0],
            'label': 'YoY Growth (%)'
        }
        
        charts_data = [chart1, chart2, chart3]

    except FileNotFoundError:
        return "Error: UPI.csv not found.", 404
    except Exception as e:
        return f"An error occurred: {e}", 500
        
    return render_template(
        'upi-analysis.html', 
        project_title=project_title,
        description=description,
        headers=headers,
        data=data,
        charts_data=charts_data
    )


@app.route('/download/<path:filename>')
def download_file(filename):
    """Serve a file from the data directory for download."""
    return send_from_directory(DATA_DIR, filename, as_attachment=True)

@app.route('/download-pdf/<path:filename>')
def download_pdf(filename):
    """Serve a file from the pdf directory for download."""
    PDF_DIR = os.path.join(BASE_DIR, 'pdf')
    return send_from_directory(PDF_DIR, filename, as_attachment=True)

@app.route('/view-pdf/<path:filename>')
def view_pdf(filename):
    """Serve a file from the pdf directory for viewing in browser."""
    PDF_DIR = os.path.join(BASE_DIR, 'pdf')
    return send_from_directory(PDF_DIR, filename)

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('data'):
        os.makedirs('data')
    app.run(debug=False,port=3000,host='0.0.0.0')
