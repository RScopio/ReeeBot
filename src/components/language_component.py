#!/usr/bin/env python3
import datetime
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Constants for model and token limits
SELECTED_MODEL = 'stabilityai/stablelm-2-1_6b-zephyr'
MAX_NEW_TOKENS = 69
SYSTEM_PROMPT = """
========== System Prompt ==========
You are a discord bot named 'reeeeeeeeeeeee' that generates responses to messages. 
You are given the last 300 messages from a discord channel and you generate a response based on them.
Each line represents a single message from a user in a 'username: message' format.
You can only generate a response up to 2000 characters.
Your task is to generate a helpful, playful, and contextually appropriate response to the conversation as if you are an active participant in the channel. 
Consider the tone, the content of the messages, and any specific questions or topics that have been discussed. 
Provide a response that is engaging, informative, and entertaining to all participants.
Do not be repetitive or provide unhelpful responses.
Do not add any text seperators or additional information to the response such as '<|endofgeneration|>' or '<|endoftext|>'
Keep responses in English and avoid other languages.
Good luck!
I love you!
========== End of System Prompt ==========
"""

def generate_response(conversation: str):
    """Generate a response from the AI model and update the conversation history."""

    # Add system prompt to conversation
    text = SYSTEM_PROMPT + "========== Discord Channel Transcript ==========" + conversation + "========== End of Discord Channel Transcript =========="
    text += "reeeeeeeeeeeee (you):"

    # Initialize model and tokenizer
    torch.set_default_device("cuda")
    tokenizer = AutoTokenizer.from_pretrained(SELECTED_MODEL, torch_dtype="auto") 
    model = AutoModelForCausalLM.from_pretrained(SELECTED_MODEL)

    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt")
    if inputs["input_ids"].shape[1] > 2048:
        inputs["input_ids"] = inputs["input_ids"][:, -2048:]
        inputs["attention_mask"] = inputs["attention_mask"][:, -2048:]

    # Generate response from model
    output = model.generate(
        **inputs, 
        max_new_tokens=MAX_NEW_TOKENS,
        temperature=0.8,
        repetition_penalty=1.2,
        do_sample=True,
        top_k=50,
        top_p=0.95,
    )
    ai_message = tokenizer.decode(output[0])

    ai_message = ai_message.split("reeeeeeeeeeeee (you):")[-1].strip()
    return ai_message
