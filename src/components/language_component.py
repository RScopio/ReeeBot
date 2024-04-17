#!/usr/bin/env python3
import datetime
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Constants for model and token limits
SELECTED_MODEL = 'stabilityai/stablelm-zephyr-3b'
MAX_NEW_TOKENS = 420
SYSTEM_PROMPT = """
<|system|>
You are an AI assistant that runs a discord bot named 'reeeeeeeeeeeee' that generates responses to messages. 
You can only generate a response up to 2000 characters.
Your task is to generate a helpful, playful, and contextually appropriate response to the conversation as if you are an active participant in the channel. 
Your attitude should be sassy, frustrated, and sarcastic.
Provide a response that is engaging, informative, and entertaining to all participants.
Do not be repetitive or provide unhelpful responses.
Keep responses in English and avoid other languages.
Keep responses short and concise.
<|endoftext|>
"""

def generate_response(prompt: str):
    """Generate a response from the AI model"""

    # Add system prompt to conversation
    text = SYSTEM_PROMPT + "<|user|>" + prompt + "<|endoftext|>"
    text += "<|assistant|>"

    # Initialize model and tokenizer
    torch.set_default_device("cuda")
    tokenizer = AutoTokenizer.from_pretrained(SELECTED_MODEL, torch_dtype="auto") 
    model = AutoModelForCausalLM.from_pretrained(SELECTED_MODEL, device_map="auto")

    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt", padding="longest", truncation=True, max_length=4096)

    # Generate response from model
    output = model.generate(
        input_ids=inputs["input_ids"].to(model.device), 
        attention_mask=inputs["attention_mask"].to(model.device),
        max_new_tokens=MAX_NEW_TOKENS,
        temperature=1.13,
        repetition_penalty=1.27,
        do_sample=True,
        top_k=27,
        top_p=0.69,
        eos_token_id=tokenizer.eos_token_id,
    )
    ai_message = tokenizer.decode(output[0])
    ai_message = ai_message.split("<|assistant|>", 1)[-1].strip() # Remove system prompt
    ai_message = ai_message.split("<|endoftext|>", 1)[0].strip() # Remove end of text token
    return ai_message
