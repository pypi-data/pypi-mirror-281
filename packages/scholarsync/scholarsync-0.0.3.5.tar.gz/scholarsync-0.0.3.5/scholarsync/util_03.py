import os
import glob
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def extract_text_from_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        text_content = []
        for elem in root.iter():
            if elem.text:
                text_content.append(elem.text.strip())
        return ' '.join(text_content)
    except ET.ParseError:
        return None

def extract_text_from_html(html_file):
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            return soup.get_text(separator=' ')
    except Exception as e:
        print(f"Error parsing file: {html_file} - {e}")
        return None

def extract_text_from_txt(txt_file):
    try:
        with open(txt_file, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {txt_file} - {e}")
        return None

def preprocess_text(text):
    # Add any additional preprocessing steps here
    return ' '.join(text.split())

def calculate_relevance_scores(tfidf_matrix, query_vector):
    relevance_scores = cosine_similarity(tfidf_matrix, query_vector).flatten()
    return relevance_scores

def analyze_relevance(directory, query_terms, file_type):
    # Select the appropriate text extraction function
    if file_type == 'xml':
        extract_text = extract_text_from_xml
    elif file_type == 'html':
        extract_text = extract_text_from_html
    elif file_type == 'txt':
        extract_text = extract_text_from_txt
    else:
        raise ValueError("Unsupported file type")

    # Extract texts from all files of the specified type
    file_paths = glob.glob(os.path.join(directory, f"*.{file_type}"))
    documents = []
    skipped_files = 0

    for file in file_paths:
        text = extract_text(file)
        if text is None:
            print(f"Error processing file: {file}")
            skipped_files += 1
        else:
            documents.append(preprocess_text(text))

    # Calculate TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Create query vector
    query_vector = vectorizer.transform([' '.join(query_terms)])

    # Calculate relevance scores for each document with respect to the query terms
    relevance_scores = calculate_relevance_scores(tfidf_matrix, query_vector)

    # Compute statistical measures
    avg_relevance_score = np.mean(relevance_scores)
    std_dev_relevance_score = np.std(relevance_scores)
    mean_dev_relevance_score = np.mean(np.abs(relevance_scores - avg_relevance_score))

    return avg_relevance_score, std_dev_relevance_score, mean_dev_relevance_score, relevance_scores, skipped_files

def test_TFIDF():
    # Select file type
    file_type = input("Enter the file type (xml/html/txt): ").strip().lower()

    # Directory containing your files
    directory_path = input(" Enter ther target directory path where the files are placed ")

    # Prompt user to enter query terms
    query_terms_input = input("Enter the query terms separated by commas: ").strip()
    query_terms = [term.strip() for term in query_terms_input.split(',')]

    # Analyze relevance and print the results
    avg_relevance_score, std_dev_relevance_score, mean_dev_relevance_score, relevance_scores, skipped_files = analyze_relevance(directory_path, query_terms, file_type)

    print(f"Average Relevance Score: {avg_relevance_score:.4f}")
    print(f"Standard Deviation of Relevance Scores: {std_dev_relevance_score:.4f}")
    print(f"Mean Deviation of Relevance Scores: {mean_dev_relevance_score:.4f}")
    print(f"Relevance Scores for each document: {relevance_scores}")
    print(f"Number of files skipped due to processing errors: {skipped_files}")
if __name__ == "__main__":
    print("This calculate the TF-IDF relevancy score of the XML/HTML/TXT files in targeted directory")
    print(" Require Use input to mention the key terms for which TF-IDF is to be calculated.")
    test_TFIDF()