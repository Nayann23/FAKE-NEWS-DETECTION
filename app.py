from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Load trained model and vectorizer
model = pickle.load(open('Models/fake_news_model.pkl', 'rb'))
vectorizer = pickle.load(open('Models/tfidf_vectorizer.pkl', 'rb'))

# Load test dataset for random samples
test_dataset = pd.read_csv('Data/test.csv')

# Initialize stemmer
port_stem = PorterStemmer()

# Preprocessing function
def preprocess_text(author, title, text=''):
    content = f"{author} {title} {text}"
    stemmed_content = re.sub('[^a-zA-Z]', ' ', content).lower().split()
    stemmed_content = [port_stem.stem(word) for word in stemmed_content if word not in stopwords.words('english')]
    return ' '.join(stemmed_content)

app = Flask(__name__)

# Endpoint to serve a random sample
@app.route('/sample')
def sample_news():
    sample = test_dataset.sample(n=1).iloc[0]
    author_val = sample['author'] if pd.notna(sample['author']) else ''
    title_val = sample['title'] if pd.notna(sample['title']) else ''
    text_val = sample['text'] if pd.notna(sample['text']) else ''
    
    # Return in a delimiter "|||"
    return jsonify({'text': f"{author_val}|||{title_val}|||{text_val}"})


# Main page
@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    mode = 'manual'
    author_val = ''
    title_val = ''
    text_val = ''

    if request.method == 'POST':
        # Check News button pressed
        if 'check-news' in request.form:
            text_val = request.form['text']
            author_val = request.form.get('author', '')
            title_val = request.form.get('title', '')
            mode = 'autofill' if author_val or title_val else 'manual'

            processed_content = preprocess_text(author_val, title_val, text_val)
            vector_input = vectorizer.transform([processed_content])
            result = model.predict(vector_input)
            prediction = "Real News ✅" if result[0] == 0 else "Fake News ❌"

        # Clear Input button pressed
        elif 'clear' in request.form:
            author_val = ''
            title_val = ''
            text_val = ''
            mode = 'manual'
            prediction = None

    return render_template('index.html',
                           prediction=prediction,
                           author_val=author_val,
                           title_val=title_val,
                           text_val=text_val,
                           mode=mode)

if __name__ == '__main__':
    app.run(debug=True)
