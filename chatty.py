import streamlit as st
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# Define the transformer model
class TransformerModel(nn.Module):
    def __init__(self, vocab_size, d_model, nhead, num_encoder_layers, num_decoder_layers):
        super(TransformerModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.transformer = nn.Transformer(d_model, nhead, num_encoder_layers, num_decoder_layers)
        self.fc_out = nn.Linear(d_model, vocab_size)
    
    def forward(self, src, tgt):
        src = self.embedding(src)
        tgt = self.embedding(tgt)
        output = self.transformer(src, tgt)
        output = self.fc_out(output)
        return output

# Define the parameters for the transformer
vocab_size = 10000
d_model = 512
nhead = 8
num_encoder_layers = 6
num_decoder_layers = 6

# Instantiate the model
model = TransformerModel(vocab_size, d_model, nhead, num_encoder_layers, num_decoder_layers)

# Dummy data for demonstration purposes
def dummy_data():
    src = torch.randint(0, vocab_size, (10, 32))
    tgt = torch.randint(0, vocab_size, (10, 32))
    return src, tgt

# Streamlit app
st.title("Chatty - Simple Transformer Model")

# Get user input
src_text = st.text_input("Enter source text (comma-separated tokens):")
tgt_text = st.text_input("Enter target text (comma-separated tokens):")

if src_text and tgt_text:
    # Convert text inputs to token IDs
    src_tokens = [int(x) for x in src_text.split(',')]
    tgt_tokens = [int(x) for x in tgt_text.split(',')]
    
    # Create tensors
    src_tensor = torch.tensor(src_tokens).unsqueeze(1)  # Add batch dimension
    tgt_tensor = torch.tensor(tgt_tokens).unsqueeze(1)  # Add batch dimension
    
    # Run the model
    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():
        output = model(src_tensor, tgt_tensor)
    
    # Convert output to probabilities
    output_prob = torch.softmax(output, dim=-1)
    output_text = output_prob.argmax(dim=-1).squeeze().tolist()
    
    st.write("Model output (token IDs):")
    st.write(output_text)
else:
    st.write("Please enter source and target text.")

