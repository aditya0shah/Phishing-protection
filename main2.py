from flask import Flask, jsonify, request
import torch
from pytext.config import PyTextConfig
from pytext.data.sources import RawDataSource
from pytext.data.tokenizers import Tokenizer
from pytext.data.utils import Vocabulary
from pytext.data.utils import (
    DEFAULT_PADDING_LABEL,
    BOS,
    EOS,
    UNK,
)
from pytext.models.doc_model import DocModel
from pytext.torchscript.pytext_lib import Lib
from pytext.torchscript.utils import (
    generate_module_and_store,
    save_module,
)

app = Flask(__name__)

# Load PyText model
model_config_path = "path/to/model_config.json"
model_state_path = "path/to/model_state.pt"
model_config = PyTextConfig.from_json(open(model_config_path))
vocab_path = "path/to/vocab.tsv"
vocab = Vocabulary.from_file(vocab_path)
tokenizer = Tokenizer.from_config(model_config.features)

# Load model state
model_state = torch.load(model_state_path, map_location=torch.device('cpu'))

# Create model and load state
model = DocModel.from_config(model_config, vocab)
model.load_state_dict(model_state["model_state"])

# PyText requires a model library to work with TorchScript
pytext_lib = Lib(model_config, model, tokenizer, vocab)
module, _ = generate_module_and_store(pytext_lib, torch.jit.script)

@app.route('/predict', methods=['POST'])
def predict():
    # Get input text from POST request
    text = request.json['text']
    
    # Tokenize input text
    tokens = tokenizer.tokenize(text)
    input_ids = vocab.lookup_indices_1d(tokens)
    
    # Pad input and create PyTorch tensor
    max_seq_len = model_config.features.max_seq_len
    input_ids = input_ids[:max_seq_len] + [vocab.get_pad_index()] * (max_seq_len - len(input_ids))
    input_ids = torch.tensor([input_ids], dtype=torch.long)
    
    # Run input through PyText model
    with torch.no_grad():
        output = module(input_ids)
        scores = output[0].tolist()
    
    # Determine if text is a phishing scam or not
    is_phishing = True if scores[1] > scores[0] else False
    
    # Return prediction result as JSON
    return jsonify({'is_phishing': is_phishing})