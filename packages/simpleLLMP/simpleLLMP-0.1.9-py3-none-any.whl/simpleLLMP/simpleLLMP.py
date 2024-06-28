from openai import OpenAI
import pytesseract
from pdf2image import convert_from_path
import os
import re
import json

class SimpleLLMP:
    def __init__(self):
        self.api_key = None
        self.model_version = None
        self.conversation_history = []

    def setup(self, api_key: str, model_version: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model_version = model_version
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """
        Takes in a prompt and returns a string response from the API.
        
        :param prompt: The prompt to send to the API.
        :return: The response from the API.
        """
        if not self.api_key or not self.model_version or not self.client:
            raise ValueError("API key and model version must be set up before calling generate.")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_version,
                messages=self.conversation_history + [{"role": "user", "content": prompt}],
            )
            # Get the assistant's message
            assistant_message = response.choices[0].message.content.strip()
            return assistant_message
        except Exception as e:
            return f"An error occurred: {e}"

    def add_to_history(self, role: str, content: str):
        """
        Manually add a message to the conversation history.
        
        :param role: The role of the message ('user' or 'assistant').
        :param content: The content of the message.
        """
        if role not in ['user', 'assistant']:
            raise ValueError("Role must be 'user' or 'assistant'.")
        self.conversation_history.append({"role": role, "content": content})

    def reset_conversation(self):
        """
        Resets the conversation history.
        """
        self.conversation_history = []

    def fine_tune_model(self, training_file_path: str) -> str:
        """
        Fine-tunes a model using the provided .json file and returns the name of the fine-tuned model.
        
        :param training_file_path: Path to the .json file containing the training data.
        :return: The name of the fine-tuned model.
        """
        try:
            # Upload the training file
            with open(training_file_path, 'rb') as f:
                response = self.client.files.create(file=f, purpose='fine-tune')
            file_id = response['id']
            
            # Create a fine-tune job
            fine_tune_response = self.client.fine_tuning.jobs.create(training_file=file_id, model=self.model_version)
            fine_tuned_model = fine_tune_response['fine_tuned_model']

            return fine_tuned_model
        except Exception as e:
            return f"An error occurred: {e}"

    def extract_training_data(pdf_path: str, json_path: str, tesseract_cmd: str = None):
        """
        Converts a PDF file to text using OCR, preprocesses the extracted text, and saves it to a .json file.

        :param pdf_path: Path to the PDF file.
        :param json_path: Path to the output .json file.
        :param tesseract_cmd: Path to the Tesseract executable (optional).
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

        # Convert PDF to a list of PIL images
        pages = convert_from_path(pdf_path)
        
        # Perform OCR on each image and preprocess the text
        extracted_text = []
        for page in pages:
            text = pytesseract.image_to_string(page)
            preprocessed_text = preprocess_text(text)
            extracted_text.append(preprocessed_text)
        
        # Combine all extracted text
        combined_text = "\n".join(extracted_text)
        
        # Convert text into JSON format suitable for fine-tuning
        json_data = convert_text_to_finetune_json(combined_text)
        
        # Save the JSON data to a file
        with open(json_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=2)

    def convert_text_to_finetune_json(text: str) -> list:
        """
        Converts text into a format suitable for fine-tuning.

        :param text: The preprocessed text.
        :return: A list of dictionaries with 'prompt' and 'completion' keys.
        """
        # Here, we split the text into sentences for simplicity
        # Adjust this logic based on your specific use case
        sentences = text.split('.')
        finetune_data = [{"prompt": sentence.strip(), "completion": ""} for sentence in sentences if sentence.strip()]
        return finetune_data


    