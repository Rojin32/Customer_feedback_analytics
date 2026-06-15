import sqlite3
from flask import Flask, render_template, request
from datetime import datetime
from textblob import TextBlob
app = Flask(__name__)
def init_db():

    conn = sqlite3.connect('feedback.db')

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            product_name TEXT,
            rating INTEGER,
            feedback TEXT,
            timestamp TEXT,
            sentiment TEXT
                   
        )
    ''')

    conn.commit()

    conn.close()

@app.route('/')
def home():

    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():

    name = request.form['name']
    product = request.form['product']
    rating = request.form['rating']
    feedback = request.form['feedback']
    sentiment = get_sentiment(feedback)
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    conn = sqlite3.connect('feedback.db')

    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO feedback
        (
            customer_name,
            product_name,
            rating,
            feedback,
            timestamp,
            sentiment   
        )

        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        name,
        product,
        rating,
        feedback,
        timestamp,
        sentiment
    ))

    conn.commit()

    conn.close()

    return render_template(
    "sucess.html",
    sentiment=sentiment
)

def get_sentiment(text):

    analysis = TextBlob(text)

    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "Positive"

    elif polarity < 0:
        return "Negative"

    else:
        return "Neutral"
if __name__ == '__main__':

    init_db()

    app.run(debug=True)