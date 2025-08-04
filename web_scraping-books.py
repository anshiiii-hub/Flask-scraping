import pandas as pd
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/books')    
def books():    
    url = 'https://books.toscrape.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    product=soup.find_all('article', class_='product_pod')
    book_list = []
    for book in product:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        availability = book.find('p', class_='instock availability').text.strip()
        book_list.append({'title': title, 'price': price, 'availability': availability})
    df = pd.DataFrame(book_list)
    df.to_csv('books.csv', index=False)
    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == '__main__':
    app.run(debug=True)
