#!/usr/bin/env python3
import datetime
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Constants for model and token limits
SELECTED_MODEL = 'gpt2'
MAX_TOKENS = 500

def generate_response(conversation: str):
    """Generate a response from the AI model and update the conversation history."""

    # Add a prompt to the conversation
    conversation += (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + "reeeeeeeeeeeee (me):")

    # Initialize model and tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained(SELECTED_MODEL) 
    model = GPT2LMHeadModel.from_pretrained(SELECTED_MODEL)

    # Generate response from model
    inputs = tokenizer(conversation, return_tensors="pt")
    output = model.generate(**inputs, max_length=MAX_TOKENS)
    ai_message = tokenizer.decode(output[0], skip_special_tokens=True)

    # Extract and return the latest response
    latest_response = ai_message.split("reeeeeeeeeeeee (me):")[-1].strip()
    return latest_response
