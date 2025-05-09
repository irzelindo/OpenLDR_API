import pandas as pd
from googletrans import Translator
import os

def translate_excel(input_file, output_file, source_lang='pt', target_lang='en'):
    """
    Translate an Excel file from source language to target language.
    
    Args:
        input_file (str): Path to the input Excel file
        output_file (str): Path to save the translated Excel file
        source_lang (str): Source language code (default: 'pt' for Portuguese)
        target_lang (str): Target language code (default: 'en' for English)
    """
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    # Initialize translator
    translator = Translator()
    
    # Function to translate text
    def translate_text(text):
        if pd.isna(text):
            return text
        try:
            return translator.translate(str(text), src=source_lang, dest=target_lang).text
        except:
            return text
    
    # Translate all string columns
    for column in df.columns:
        if df[column].dtype == 'object':  # Only translate string columns
            df[column] = df[column].apply(translate_text)
    
    # Save the translated DataFrame to Excel
    df.to_excel(output_file, index=False)
    print(f"Translation complete. File saved as: {output_file}")

if __name__ == "__main__":
    # Example usage
    input_file = "input.xlsx"  # Change this to your input file
    output_file = "translated_output.xlsx"  # Change this to your desired output file
    
    if os.path.exists(input_file):
        translate_excel(input_file, output_file)
    else:
        print(f"Error: Input file '{input_file}' not found!") 