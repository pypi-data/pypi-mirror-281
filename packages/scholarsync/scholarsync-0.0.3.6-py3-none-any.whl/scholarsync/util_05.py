import os
import torch
from transformers import BartTokenizer, BartForConditionalGeneration

# Load BART model and tokenizer
model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Function to summarize text based on an input query
def summarize_text(text, query):
    # Combine query and text
    input_text = f"summarize: {query} {text}"
    inputs = tokenizer(input_text, return_tensors="pt", max_length=2096, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], num_beams=4, length_penalty=2.0, max_length=523, min_length=56, no_repeat_ngram_size=3)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Function to process text files and summarize
def process_text_files(input_query, text_files_directory):
    summaries = []
    for filename in os.listdir(text_files_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(text_files_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                summary = summarize_text(text, input_query)
                summaries.append(f"Summary of {filename}:\n{summary}\n")
    return summaries

# Main loop for continuous conversation
def main_summarise():
    while True:
        input_query = input("Enter your specific query for summarization (or 'exit' to quit): ")
        if input_query.lower() == 'exit':
            break
        text_files_directory = input("Enter the path to the directory containing text files: ")
        if not os.path.isdir(text_files_directory):
            print("Invalid directory path. Please try again.")
            continue

        summaries = process_text_files(input_query, text_files_directory)
        for summary in summaries:
            print(summary)

if __name__ == "__main__":
    main_summarise()
