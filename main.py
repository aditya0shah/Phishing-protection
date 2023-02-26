from flask import Flask, render_template, jsonify, request
import json
import torch
from transformers import BertTokenizer, BertForSequenceClassification

app = Flask(__name__, template_folder="/.", static_folder="/.")

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)


labels = ['Not phishing', 'Phishing']


def classify_text(text):
    inputs = tokenizer(text, return_tensors='pt')

    outputs = model(**inputs)

    predicted_class = torch.argmax(outputs.logits, dim=1).item()

    return labels[predicted_class]
    

@app.route('/classify', methods=['POST'])
def classify():
    text = request.json['text']

    prediction = classify_text(text)

    return jsonify({'prediction': prediction})


@app.route('/', methods=['POST'])
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
