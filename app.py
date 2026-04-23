from flask import Flask, request, render_template_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import webbrowser
import threading

app = Flask(__name__)

# Sample dataset
messages = [
    "Hello how are you",
    "Let's meet tomorrow",
    "Are you coming to class",
    "Hi friend good morning",
    "Call me when you are free",
    "Congratulations you won lottery",
    "Urgent! send your bank details",
    "Click this link to get reward"
]

labels = [0, 0, 0, 0, 0, 1, 1, 1]  # 0 = Not Spam, 1 = Spam

# Vectorizer + Model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(messages)

model = MultinomialNB()
model.fit(X, labels)

# HTML inside Python
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Online Scam Detection</title>
</head>
<body style="text-align:center; font-family:Arial; margin-top:50px;">

    <h1>Online Scam Detection</h1>

    <form method="POST">
        <textarea name="message" placeholder="Enter message here..." required 
        style="width:300px; height:100px; padding:10px;"></textarea>
        <br><br>
        <button type="submit" style="padding:10px 20px;">Check Message</button>
    </form>

    {% if result %}
        <h3 style="color:green;">{{ result }}</h3>
    {% endif %}

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    if request.method == 'POST':
        message = request.form['message']
        data = vectorizer.transform([message])
        prediction = model.predict(data)[0]

        result = f"Message: {message} → {'Spam' if prediction == 1 else 'Not Spam'}"

    return render_template_string(HTML_PAGE, result=result)


# Auto open browser
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True, use_reloader=False)
