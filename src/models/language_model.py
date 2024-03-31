#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for model and token limits
SELECTED_MODEL = 'stabilityai/StableBeluga-7B'
MAX_TOKENS = 2048

# Initialize model and tokenizer
logging.info(f"Loading model {SELECTED_MODEL}")
tokenizer = AutoTokenizer.from_pretrained(SELECTED_MODEL, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(SELECTED_MODEL)

# Initialize global conversation history
conversation_history = ""

def truncate_conversation(history, max_length=MAX_TOKENS):
    """Truncate the conversation history to fit within a max token limit."""
    logger.info("truncating conversation history")
    tokens = tokenizer.encode(history, return_tensors="pt", truncation=True, max_length=max_length)
    return tokenizer.decode(tokens[0], skip_special_tokens=True)

def generate_response(user_message):
    """Generate a response from the AI model and update the conversation history."""
    global conversation_history

    # Update and truncate conversation history
    conversation_entry = f"### User:\n{user_message}\n\n### Assistant:\n"
    conversation_history += conversation_entry
    conversation_history = truncate_conversation(conversation_history)

    # Generate response from model
    logger.info("generating response")
    inputs = tokenizer(conversation_history, return_tensors="pt")
    output = model.generate(**inputs, max_length=MAX_TOKENS)
    assistant_message = tokenizer.decode(output[0], skip_special_tokens=True)

    # Extract and return the latest response
    latest_response = assistant_message.split("### Assistant:")[-1].strip()
    return latest_response

def send_message():
    """Send user message and get response from the model."""
    user_message = user_input.get("1.0", tk.END).strip()
    if user_message:
        # Clear user input and disable text area
        user_input.delete("1.0", tk.END)
        text_area.config(state=tk.NORMAL)

        # Update conversation display and highlight user message
        text_area.insert(tk.END, f"You: {user_message}\n", 'user')
        text_area.tag_add("highlight", "end-1c linestart", "end-1c lineend")
        text_area.see(tk.END)

        # Generate response in a separate thread to prevent UI freezing
        threading.Thread(target=lambda: update_conversation(user_message), daemon=True).start()

def update_conversation(user_message):
    """Update the conversation history with the response."""
    assistant_message = generate_response(user_message)

    # Enable text area, update conversation, and disable again
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, f"Assistant: {assistant_message}\n", 'assistant')
    text_area.see(tk.END)
    text_area.config(state=tk.DISABLED)

def on_closing():
    """Callback for when the application is closing."""
    with open("conversation_history.txt", "w") as file:
        file.write(conversation_history)
    root.destroy()

if __name__ == "__main__":
    # Initialize the main application window
    root = tk.Tk()
    root.title("Chat with AI")
    root.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window closing

    # Define frames: We will use frames to hold the widgets and use grid system on the frames
    top_frame = tk.Frame(root)
    top_frame.grid(row=0, column=0, sticky="nsew")

    bottom_frame = tk.Frame(root)
    bottom_frame.grid(row=1, column=0, sticky="nsew")

    # Allow frame to expand
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)  # Text area's frame expands vertically
    root.rowconfigure(1, weight=0)  # User input's frame doesn't expand vertically

    # Add text area for conversation history within top_frame
    text_area = tk.Text(top_frame, wrap=tk.WORD)
    text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Add user input field and send button within bottom_frame
    user_input = tk.Text(bottom_frame, wrap=tk.WORD, height=5)
    user_input.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10, pady=10)  # Expand horizontally, fixed height

    send_button = ttk.Button(bottom_frame, text="Send", command=send_message)
    send_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Configure tags for text area
    text_area.tag_configure('user', justify='right', background='lightgray')
    text_area.tag_configure('assistant', justify='left', background='lightblue')

    # Start the application
    logger.info("Starting the application")
    root.mainloop()
