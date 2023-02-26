from flask import Flask, jsonify, request
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = Flask(__name__)

# Load the pre-trained phishing scam detection model
model_name = 'distilbert-base-uncased-finetuned-sst-2-english'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Set the model to evaluation mode
model.eval()

# Set the threshold for phishing scam classification
threshold = 0.5

@app.route('/classify', methods=['POST'])
def classify():
    # Retrieve input text from POST request
    text = request.json['text']
    
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt')
    
    # Run the model on the input text
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Extract the predicted class from the model output
    predicted_class = int(torch.argmax(outputs.logits).item())
    
    # Check if the predicted class is a phishing scam and if the score is above the threshold
    if predicted_class == 1 and torch.softmax(outputs.logits, dim=1)[0][1].item() >= threshold:
        return jsonify({'message': 'The text is a phishing scam.', 'output': outputs.logits.tolist()})
    else:
        return jsonify({'message': 'The text is not a phishing scam.', 'output': outputs.logits.tolist()})

if __name__ == '__main__':
    app.run(debug=True)




