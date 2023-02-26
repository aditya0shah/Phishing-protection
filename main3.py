from flask import Flask, jsonify, request
from transformers import RobertaForSequenceClassification, RobertaTokenizer

app = Flask(__name__)

# Load the pre-trained RoBERTa model and tokenizer
model = RobertaForSequenceClassification.from_pretrained('roberta-base')
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

# Set the model to evaluation mode
model.eval()

@app.route('/classify', methods=['POST'])
def classify():
    # Retrieve input text from POST request
    text = request.json['text']
    
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt')
    
    # Run the model on the input text
    outputs = model(**inputs)
    predicted_class = int(outputs.logits.argmax(dim=-1).detach().cpu().numpy())
    
    # Return a message indicating whether or not the text is a phishing scam
    if predicted_class == 0:
        return jsonify({'message': 'The text is not a phishing scam.'})
    else:
        return jsonify({'message': 'The text is a phishing scam.'})

if __name__ == '__main__':
    app.run(debug=True)