import os
import spacy
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_html(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            return soup.get_text()
    except Exception as e:
        print(f"Error reading HTML file {file_path}: {e}")
        return ""

def extract_text_from_xml(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "xml")
            return soup.get_text()
    except Exception as e:
        print(f"Error reading XML file {file_path}: {e}")
        return ""

def process_file(file_path):
    if file_path.endswith(".html"):
        return extract_text_from_html(file_path)
    elif file_path.endswith(".xml"):
        return extract_text_from_xml(file_path)
    else:
        return None

def display_menu():
    menu = """
Choose what to extract:
1. Named Entities
2. Nouns
3. Verbs
4. Sentences
5. Countries (GPE)
6. Abbreviations
7. Organizations
8. People (PERSON)
9. Nationalities/Religious/Political Groups (NORP)
10. Facilities (FAC)
11. Locations (LOC)
12. Products (PRODUCT)
13. Events (EVENT)
14. Works of Art (WORK_OF_ART)
15. Laws (LAW)
16. Languages (LANGUAGE)
17. Dates (DATE)
18. Times (TIME)
19. Percentages (PERCENT)
20. Monetary Values (MONEY)
21. Quantities (QUANTITY)
22. Ordinals (ORDINAL)
23. Cardinals (CARDINAL)
24. Exit
"""
    print(menu)
    return input("Enter your choice: ")

def root():
    directory = input("Enter the directory path containing XML/HTML files: ").strip()
    if not os.path.isdir(directory):
        print("Invalid directory path")
        return

    file_type = input("Enter the file type to process (xml/html): ").strip().lower()
    if file_type not in ["xml", "html"]:
        print("Invalid file type. Please enter 'xml' or 'html'.")
        return

    files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(f".{file_type}")]
    if not files:
        print(f"No {file_type.upper()} files found in the directory")
        return

    while True:
        choice = display_menu().strip()

        if choice == "24":
            print("Exiting...")
            break

        all_entities = []
        valid_choices = {str(i) for i in range(1, 24)}

        if choice not in valid_choices:
            print("Invalid choice. Please try again.")
            continue

        for file_path in files:
            print(f"\nProcessing file: {file_path}")
            text = process_file(file_path)
            if text:
                doc = nlp(text)
                entities = []

                if choice == "1":
                    entities = [(file_path, ent.text, ent.label_, ent.sent.text) for ent in doc.ents]
                elif choice == "2":
                    entities = [(file_path, token.text, "NOUN", token.sent.text) for token in doc if token.pos_ == "NOUN"]
                elif choice == "3":
                    entities = [(file_path, token.text, "VERB", token.sent.text) for token in doc if token.pos_ == "VERB"]
                elif choice == "4":
                    entities = [(file_path, sent.text, "SENTENCE", sent.text) for sent in doc.sents]
                elif choice == "5":
                    entities = [(file_path, ent.text, "GPE", ent.sent.text) for ent in doc.ents if ent.label_ == "GPE"]
                elif choice == "6":
                    entities = [(file_path, token.text, "ABBREV", token.sent.text) for token in doc if token.is_alpha and token.is_upper and len(token.text) > 1]
                elif choice == "7":
                    entities = [(file_path, ent.text, "ORG", ent.sent.text) for ent in doc.ents if ent.label_ == "ORG"]
                elif choice == "8":
                    entities = [(file_path, ent.text, "PERSON", ent.sent.text) for ent in doc.ents if ent.label_ == "PERSON"]
                elif choice == "9":
                    entities = [(file_path, ent.text, "NORP", ent.sent.text) for ent in doc.ents if ent.label_ == "NORP"]
                elif choice == "10":
                    entities = [(file_path, ent.text, "FAC", ent.sent.text) for ent in doc.ents if ent.label_ == "FAC"]
                elif choice == "11":
                    entities = [(file_path, ent.text, "LOC", ent.sent.text) for ent in doc.ents if ent.label_ == "LOC"]
                elif choice == "12":
                    entities = [(file_path, ent.text, "PRODUCT", ent.sent.text) for ent in doc.ents if ent.label_ == "PRODUCT"]
                elif choice == "13":
                    entities = [(file_path, ent.text, "EVENT", ent.sent.text) for ent in doc.ents if ent.label_ == "EVENT"]
                elif choice == "14":
                    entities = [(file_path, ent.text, "WORK_OF_ART", ent.sent.text) for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
                elif choice == "15":
                    entities = [(file_path, ent.text, "LAW", ent.sent.text) for ent in doc.ents if ent.label_ == "LAW"]
                elif choice == "16":
                    entities = [(file_path, ent.text, "LANGUAGE", ent.sent.text) for ent in doc.ents if ent.label_ == "LANGUAGE"]
                elif choice == "17":
                    entities = [(file_path, ent.text, "DATE", ent.sent.text) for ent in doc.ents if ent.label_ == "DATE"]
                elif choice == "18":
                    entities = [(file_path, ent.text, "TIME", ent.sent.text) for ent in doc.ents if ent.label_ == "TIME"]
                elif choice == "19":
                    entities = [(file_path, ent.text, "PERCENT", ent.sent.text) for ent in doc.ents if ent.label_ == "PERCENT"]
                elif choice == "20":
                    entities = [(file_path, ent.text, "MONEY", ent.sent.text) for ent in doc.ents if ent.label_ == "MONEY"]
                elif choice == "21":
                    entities = [(file_path, ent.text, "QUANTITY", ent.sent.text) for ent in doc.ents if ent.label_ == "QUANTITY"]
                elif choice == "22":
                    entities = [(file_path, ent.text, "ORDINAL", ent.sent.text) for ent in doc.ents if ent.label_ == "ORDINAL"]
                elif choice == "23":
                    entities = [(file_path, ent.text, "CARDINAL", ent.sent.text) for ent in doc.ents if ent.label_ == "CARDINAL"]

                all_entities.extend(entities)

                for entity in entities:
                    print(f"File: {entity[0]}, Text: {entity[1]}, Label: {entity[2]}, Sentence: {entity[3]}")

        if all_entities:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"extracted_entities_{timestamp}.csv"
            df = pd.DataFrame(all_entities, columns=["File", "Text", "Label", "Sentence"])
            df.to_csv(output_file, index=False, encoding='utf-8')
            print(f"\nExtracted entities saved to {output_file}")

if __name__ == "__main__":
    root()
