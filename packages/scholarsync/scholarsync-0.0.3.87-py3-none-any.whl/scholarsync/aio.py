from itertools import combinations
from Bio import Entrez
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urlparse, urljoin
import os
import hashlib
import shutil
from datetime import datetime
from PyPDF2 import PdfReader
from Bio import Medline
import xml.etree.ElementTree as ET
import subprocess
import sys
import os
import json









"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


"""-----------------------------------------------------------------------------------------------"""
#  Help Functions
"""-----------------------------------------------------------------------------------------------"""

def entry_point_help():
    def encapsulated_root_help():

        def extract_entry_point_content(file_path, entry_point):
            with open(file_path, 'r') as file:
                content = file.read()
                pattern = f'<{entry_point}>(.*?)</{entry_point}>'
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    return match.group(1)
                else:
                    return None

        def export_help(file_path):
            while True:
                export_dir = input("Enter the directory path for exporting help content (type 'cancel' to cancel): ")
                if export_dir.lower() == 'cancel':
                    print("Operation canceled.")
                    return
                elif os.path.isdir(export_dir):
                    break
                else:
                    print("Invalid directory path. Please enter a valid directory path.")

            export_file_path = os.path.join(export_dir, "the_help.txt")
            with open(file_path, 'r') as file:
                with open(export_file_path, 'w') as export_file:
                    export_file.write(file.read())
            print(f"Help content exported to {export_file_path}")

        # Accept file path from user
        def get_help_file_path():
            module_dir = os.path.dirname(__file__)  # Get the directory of the current module
            help_file_path = os.path.join(module_dir,'data', 'help.txt')
            return help_file_path

        file_path = get_help_file_path()

        while True:
            action = input("Choose an action (export_help, entry_point_all, or enter an entry point; type 'quit' to exit): ")
            if action.lower() == 'quit':
                break
            elif action.lower() == 'export_help':
                export_help(file_path)
            elif action.lower() == 'entry_point_all':
                with open(file_path, 'r') as file:
                    print("Content of entire file:")
                    print(file.read())
            else:
                content = extract_entry_point_content(file_path, action)
                if content:
                    print(f"Content of {action}: {content}")
                else:
                    print(f"No content found for {action}")

    encapsulated_root_help()






"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""








"""-----------------------------------------------------------------------------------------------"""
# The Pubmed Querying System function entry_point_01
# To seeing the code by which all tyhe promts for entry_point_1 are made go to bottom entry_point_01
"""-----------------------------------------------------------------------------------------------"""


"""-----------------------------------------------------------------------------------------------"""
# The Search Query function entry_point_01A
"""-----------------------------------------------------------------------------------------------"""

# Define functions from the entry_point_01A The Pubmed Querying System
def encasulated_advanced_pubmed_paper_counter():
    from itertools import combinations
    from Bio import Entrez
    import time
    from urllib.error import HTTPError

    def construct_query(terms):
        return ' AND '.join(terms)

    def search_and_store_papers(query_terms, filename, default_search_location, retmax, start_date=None, end_date=None):
        try:
            # Split query terms into individual components
            terms = []
            for term in query_terms:
                if '[' in term and ']' in term:
                    # Term contains explicit field tag, use as is
                    terms.append(term)
                else:
                    # Term does not contain field tag, treat as regular term with default search location (tiab)
                    terms.append(f'{term}[{default_search_location}]')
            # Generate all possible combinations of query terms
            combinations_list = []
            for r in range(1, len(terms) + 1):
                combinations_list.extend(combinations(terms, r))

            total_combinations = len(combinations_list)
            print(f"Total combinations to search: {total_combinations}")

            # Initialize BioPython
            Entrez.email = "your@email.com"  # Set your email here

            # Search and store total number of hits for each combination
            with open(filename, 'w') as file:
                file.write(f"Original Query Terms: {' '.join(query_terms)} \n\n")
                for index, combination in enumerate(combinations_list, start=1):
                    query = construct_query(combination)
                    if start_date and end_date:
                        query += f" AND ({start_date}[Date - Entrez] : {end_date}[Date - Entrez])"

                    print(f"Searching combination {index}/{total_combinations}: {query}")
                    retry_attempts = 0
                    while retry_attempts < 5:
                        try:
                            handle = Entrez.esearch(db="pubmed", term=query, retmax=min(retmax, 9999))
                            record = Entrez.read(handle)
                            handle.close()
                            total_hits = int(record["Count"])
                            file.write(f"Combination : {index}/{total_combinations}  ")
                            file.write(f" Query: {query}\n")
                            file.write(f"Total Hits: {total_hits}\n")
                            id_list = record["IdList"]
                            file.write("PMIDs: " + ', '.join(id_list) + "\n\n")
                            break
                        except HTTPError as e:
                            if e.code == 429:
                                print(f"HTTP 429 Too Many Requests: Retrying... ({retry_attempts+1}/5)")
                                retry_attempts += 1
                                time.sleep(2 ** retry_attempts)
                            else:
                                raise
                    else:
                        print("Failed to fetch data after several retries. Switching to batch method.")
                        total_hits = 0
                        while total_hits < min(retmax, 9999):
                            handle = Entrez.esearch(db="pubmed", term=query, retstart=total_hits, retmax=100)
                            record = Entrez.read(handle)
                            handle.close()
                            total_hits += int(record["Count"])
                            id_list = record["IdList"]
                            file.write("PMIDs: " + ', '.join(id_list) + "\n\n")
                        break
            print("Search completed. Results stored in", filename)

        except Exception as e:
            print("An error occurred:", str(e))

    def root_PubMed_search_query():
        try:
            print("")
            print("  The query can be made highly specific by using the wildcards, using synonyms and field specifiers like tittle, abstracts, or ti-ab")
            print("")
            print("  For Example: ' Micro*, money, malari*[tiab], asia[ti], biodiver*[ab] '")
            query = input("Enter PubMed search query: ")
            default_search_location = input("Enter the search location (e.g., ti, ab, or tiab): ") or "tiab"
            retmax = input("Enter the maximum number of records to retrieve, Default is 1000 (retmax): ") or 1000
            retmax = int(retmax)
            if retmax > 9999:
                print(f"retmax ({retmax}) is greater than 9999. Setting retmax to 9999.")
                retmax = 9999

            output_file_pubmed_paper_query_name = "output_file_pubmed_paper_query.txt"
            start_date = input("Enter start date (optional, format YYYY/MM/DD): ")
            end_date = input("Enter end date (optional, format YYYY/MM/DD): ")
            query_terms = query.split(',')
            # Remove leading and trailing whitespace from each term and filter out empty strings
            query_terms = [term.strip() for term in query_terms if term.strip()]
            search_and_store_papers(query_terms, output_file_pubmed_paper_query_name, default_search_location, retmax, start_date=start_date, end_date=end_date)

        except Exception as e:
            print("An error occurred:", str(e))

    root_PubMed_search_query()





"""-----------------------------------------------------------------------------------------------"""
# The Search Query manual filter function entry_point_01B
"""-----------------------------------------------------------------------------------------------"""

def entry_point_01B():
    def encapsulated_pubmedid_selector():
        import webbrowser
        import os

        # Path to your text file
        txt_file_path = 'output_file_pubmed_paper_query.txt'
        if not os.path.exists(txt_file_path):
            txt_file_path = input (r" Automatic mode failed no 'output_file_pubmed_paper_query.txt' found, enter the path manually ")
            while not os.path.exists(txt_file_path):
                    txt_file_path = input("The specified file does not exist. Please enter a valid file path: ")



        # Read the content of the text file
        with open(txt_file_path, 'r') as file:
            txt_content = file.readlines()

        # Function to generate HTML content
        def generate_html_content(txt_content):
            html_content = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>PubMed Query Results</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 20px;
                    }
                    h1 {
                        text-align: center;
                        color: #333;
                    }
                    .buttons-container {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin: 20px 0;
                    }
                    .buttons-container .left-buttons {
                        display: flex;
                        gap: 10px;
                    }
                    .buttons-container .right-buttons {
                        display: flex;
                        gap: 10px;
                    }
                    button {
                        padding: 10px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                    }
                    button:hover {
                        background-color: #45a049;
                    }
                    table {
                        width: calc(100% - 40px);
                        border-collapse: collapse;
                        margin: 20px auto;
                        background-color: #fff;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }
                    th, td {
                        border: 1px solid #ddd;
                        padding: 12px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                        color: #333;
                    }
                    td:first-child {
                        width: 10%;
                    }
                    tr:nth-child(even) {
                        background-color: #f9f9f9;
                    }
                    tr:hover {
                        background-color: #f1f1f1;
                    }
                    .selectable {
                        cursor: pointer;
                    }
                    .selected {
                        background-color: #d1e7dd !important;
                    }
                    #selectedCount, #visibleCount {
                        text-align: center;
                        margin: 10px 0;
                        font-size: 1.1em;
                    }
                </style>
            </head>
            <body>
                <h1>PubMed Query Results</h1>
                <div class="buttons-container">
                    <div class="left-buttons">
                        <button id="removeZeroHitsButton" onclick="removeZeroHits()">Remove Zero Hits (0)</button>
                        <button id="removeThresholdExceededButton" onclick="removeThresholdExceeded()">Remove Threshold Exceeded (0)</button>
                        <button onclick="clearSavedState()">Clear Saved State</button>
                    </div>
                    <div class="right-buttons">
                        <button onclick="exportSelected()">Export Selected</button>
                    </div>
                </div>
                <div id="selectedCount">Selected Rows: 0 | Unique PubMed IDs: 0</div>
                <div id="visibleCount">Visible Rows: 0</div>
                <table id="resultsTable">
                    <thead>
                        <tr>
                            <th>Combination Number</th>
                            <th>Query</th>
                            <th>Total Hits</th>
                            <th>Select</th>
                        </tr>
                    </thead>
                    <tbody>
            '''

            combination = ''
            query = ''
            total_hits = ''
            pmids = ''
            zero_hits_count = 0
            threshold_exceeded_count = 0

            for line in txt_content:
                if line.startswith('Combination :'):
                    if combination and query:  # Add the previous combination to the table
                        if total_hits == '0':
                            zero_hits_count += 1
                        elif pmids == 'exceeded_threshold':
                            threshold_exceeded_count += 1
                        html_content += f'''
                        <tr class="selectable" data-total-hits="{total_hits}" data-pmids="{pmids}">
                            <td>{combination}</td>
                            <td>{query}</td>
                            <td>{total_hits}</td>
                            <td><input type="checkbox" data-combination="{combination}" data-pmids="{pmids}" class="hidden-checkbox"></td>
                        </tr>
                        '''
                    combination = line.split(': ')[1].split(' ')[0]
                    query = line.split('Query: ')[1].strip()
                    pmids = ''  # Reset pmids for the new combination
                elif line.startswith('Total Hits:'):
                    total_hits = line.split(': ')[1].strip()
                elif line.startswith('PMIDs:'):
                    pmids = line.split(': ')[1].strip()
                    if pmids == 'Not fetched (hit count exceeds threshold)':
                        pmids = 'exceeded_threshold'

            # Add the last combination to the table
            if combination and query:
                if total_hits == '0':
                    zero_hits_count += 1
                elif pmids == 'exceeded_threshold':
                    threshold_exceeded_count += 1
                html_content += f'''
                <tr class="selectable" data-total-hits="{total_hits}" data-pmids="{pmids}">
                    <td>{combination}</td>
                    <td>{query}</td>
                    <td>{total_hits}</td>
                    <td><input type="checkbox" data-combination="{combination}" data-pmids="{pmids}" class="hidden-checkbox"></td>
                </tr>
                '''

            html_content += '''
                    </tbody>
                </table>

                <script>
                    function updateSelectedCount() {
                        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
                        const selectedCount = checkboxes.length;
                        const pmidSet = new Set();

                        checkboxes.forEach(checkbox => {
                            const pmids = checkbox.dataset.pmids.split(',').map(pmid => pmid.trim());
                            pmids.forEach(pmid => {
                                if (pmid) {
                                    pmidSet.add(pmid);
                                }
                            });
                        });

                        const uniquePmidsCount = pmidSet.size;
                        document.getElementById('selectedCount').textContent = `Selected Rows: ${selectedCount} | Unique PubMed IDs: ${uniquePmidsCount}`;
                    }

                    function updateVisibleCount() {
                        const visibleRows = document.querySelectorAll('tbody tr');
                        document.getElementById('visibleCount').textContent = `Visible Rows: ${visibleRows.length}`;
                    }

                    function updateRemoveButtons() {
                        const zeroHitsRows = document.querySelectorAll('tr[data-total-hits="0"]');
                        const thresholdExceededRows = document.querySelectorAll('tr[data-pmids="exceeded_threshold"]');
                        document.getElementById('removeZeroHitsButton').textContent = `Remove Zero Hits (${zeroHitsRows.length})`;
                        document.getElementById('removeThresholdExceededButton').textContent = `Remove Threshold Exceeded (${thresholdExceededRows.length})`;
                    }

                    document.querySelectorAll('.selectable').forEach(row => {
                        row.addEventListener('click', () => {
                            const checkbox = row.querySelector('input[type="checkbox"]');
                            checkbox.checked = !checkbox.checked;
                            row.classList.toggle('selected', checkbox.checked);
                            saveSelectedState();
                            updateSelectedCount();
                        });
                    });

                    function removeZeroHits() {
                        const rows = document.querySelectorAll('tr[data-total-hits="0"]');
                        rows.forEach(row => {
                            row.remove();
                        });
                        updateRemoveButtons();
                        updateVisibleCount();
                    }

                    function removeThresholdExceeded() {
                        const rows = document.querySelectorAll('tr[data-pmids="exceeded_threshold"]');
                        rows.forEach(row => {
                            row.remove();
                        });
                        updateRemoveButtons();
                        updateVisibleCount();
                    }

                    function exportSelected() {
                        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
                        const pmidSet = new Set();

                        checkboxes.forEach(checkbox => {
                            const pmids = checkbox.dataset.pmids.split(',').map(pmid => pmid.trim());
                            pmids.forEach(pmid => {
                                if (pmid) {
                                    pmidSet.add(pmid);
                                }
                            });
                        });

                        const pmidArray = Array.from(pmidSet);
                        const blob = new Blob([pmidArray.join('\\n')], { type: 'text/plain' });
                        const link = document.createElement('a');
                        link.href = URL.createObjectURL(blob);
                        link.download = 'selected_pmids.txt';
                        link.click();
                    }

                    function saveSelectedState() {
                        const selectedRows = [];
                        document.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
                            selectedRows.push(checkbox.dataset.combination);
                        });
                        localStorage.setItem('selectedRows', JSON.stringify(selectedRows));
                    }

                    function loadSelectedState() {
                        const selectedRows = JSON.parse(localStorage.getItem('selectedRows')) || [];
                        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                            if (selectedRows.includes(checkbox.dataset.combination)) {
                                checkbox.checked = true;
                                checkbox.closest('tr').classList.add('selected');
                            }
                        });
                        updateSelectedCount();
                    }

                    function clearSavedState() {
                        localStorage.removeItem('selectedRows');
                        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                            checkbox.checked = false;
                            checkbox.closest('tr').classList.remove('selected');
                        });
                        updateSelectedCount();
                    }

                    document.addEventListener('DOMContentLoaded', () => {
                        updateRemoveButtons();
                        loadSelectedState();
                        updateVisibleCount();
                    });
                </script>
            </body>
            </html>
            '''

            return html_content

        # Generate HTML content
        html_content = generate_html_content(txt_content)

        # Path to your HTML file
        html_file_path = 'query_results.html'

        # Write HTML content to file
        with open(html_file_path, 'w') as file:
            file.write(html_content)

        # Ensure the path is absolute
        absolute_path = os.path.abspath(html_file_path)

        # Open the HTML file in the default web browser
        webbrowser.open('file://' + absolute_path)
    encapsulated_pubmedid_selector()




"""-----------------------------------------------------------------------------------------------"""
# The Search Query Grapher function entry_point_01C
"""-----------------------------------------------------------------------------------------------"""

# Define the functions of the script 01C The Graph Maker
#
#
#

def entry_point_01C():
    def encapsulated_graphmaker():
        import os
        import re
        import csv
        import numpy as np
        import plotly.graph_objects as go

        def extract_hits_from_file(file_path):
            hits = []

            try:
                with open(file_path, 'r') as file:
                    content = file.read()

                # Use regex to find combination queries and total hits
                pattern = r'Combination : \d+/\d+.*?Query: (.*?)\nTotal Hits: (\d+)'
                matches = re.findall(pattern, content, re.DOTALL)

                for match in matches:
                    combination_query = match[0].strip()
                    total_hits = int(match[1])
                    hits.append((combination_query, total_hits))

                return hits

            except Exception as e:
                print(f"Error occurred during data extraction: {e}")
                return []

        def write_hits_to_csv(hits, output_csv):
            try:
                with open(output_csv, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Combination Query', 'Total Hits'])
                    for combination_query, total_hits in hits:
                        writer.writerow([combination_query, total_hits])

                print(f"Data extracted and saved to '{output_csv}'")

            except Exception as e:
                print(f"Error occurred while writing to CSV: {e}")

        def plot_hits_from_csv(csv_file):
            try:
                # Read data from CSV and sort by total hits in descending order
                hits = []
                with open(csv_file, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        combination_query = row['Combination Query']
                        total_hits = int(row['Total Hits'])
                        hits.append((combination_query, total_hits))

                # Sort hits by total hits in descending order
                hits.sort(key=lambda x: x[1], reverse=True)

                # Separate queries and hits for plotting
                queries = [f"{query} (Hits: {hits})" for query, hits in hits]  # Include total hits in label
                raw_hits = [hits for query, hits in hits]

                # Apply logarithmic scaling to hits (avoiding log(0) by adding a small value)
                hits_normalized = np.log10(np.array(raw_hits) + 1)  # Logarithmic scaling with base 10

                # Create filtered lists for zero-hit and non-zero-hit queries
                zero_hit_queries = [query for query, hits in hits if hits == 0]
                non_zero_hits = [hits for query, hits in hits if hits > 0]

                # Create hover text with original total hits values
                #hover_text = [f"Total Hits: {hits}" for hits in raw_hits]

                # Plotting with Plotly
                fig = go.Figure()

                # Add bar trace for non-zero-hit queries
                fig.add_trace(go.Bar(
                    y=queries,
                    x=[np.log10(hits + 1) for hits in non_zero_hits],
                    orientation='h',
                    marker_color='skyblue',
                    name='Non-Zero Hits',
                    #hovertext=hover_text
                ))

                # Configure layout settings
                fig.update_layout(
                    title='Logarithmic Scaled Total Hits per Combination Query',
                    xaxis_title='Log10(Total Hits + 1)',
                    yaxis_title='Combination Query',
                    height=800,
                    margin=dict(l=250, r=20, b=100, t=100),  # Adjust margins for better layout
                    yaxis={'categoryorder': 'total ascending'},  # Sort queries by total hits
                    showlegend=True,
                    yaxis_tickfont=dict(size=16),  # Change font size for y-axis labels
                    xaxis_tickfont=dict(size=16)   # Change font size for x-axis labels
                )

                # Add custom button to toggle visibility of zero-hit queries
                fig.update_layout(
                    updatemenus=[
                        dict(
                            type="buttons",
                            direction="left",
                            buttons=[
                                dict(
                                    label="Toggle Zero-Hit Queries",
                                    method="update",
                                    args=[
                                        {"visible": [True] * len(queries)},
                                        {"y": [query for query in queries if query not in zero_hit_queries]}
                                    ],
                                )
                            ],
                            pad={"r": 10, "t": 10},
                            showactive=True,
                            x=0.05,
                            xanchor="left",
                            y=1.15,
                            yanchor="top"
                        ),
                    ]
                )

                fig.show()

            except Exception as e:
                print(f"Error occurred during plot generation: {e}")

        def root_result_graph_maker():
            file_path = 'output_file_pubmed_paper_query.txt' # Update with the path to your text file
            if not os.path.exists(file_path):
                file_path = input (r" Automatic mode failed no 'output_file_pubmed_paper_query.txt' found, enter the path manually ")
                while not os.path.exists(file_path):
                    file_path = input("The specified file does not exist. Please enter a valid file path: ")
            output_csv = 'hits_data.csv'  # Temporary CSV file to store extracted hits


            hits_data = extract_hits_from_file(file_path)
            if hits_data:
                write_hits_to_csv(hits_data, output_csv)
                plot_hits_from_csv(output_csv)
            else:
                print("No data extracted from the file.")

        root_result_graph_maker()
    encapsulated_graphmaker()
    print(" You are advised to run entry_point_09.option.1 The citation script function when you feel you DOI are now fully collected and filtered \n")
    # Here I wish to make a sort of html based filtering with graphing utility, that will generate a file named as selected_pmids.txt contating a cenrral list of all the PubMed IDs.









"""-----------------------------------------------------------------------------------------------"""
# The Abstracts Retriver function entry_point_01 Runners
"""-----------------------------------------------------------------------------------------------"""



def entry_point_01():
    print(f" If you have not done the Query Search Earlier, and wish to continue to Query Search, use entry point '1A' ")
    print(f" If you have already done the Query Search, and now wish to use GUI Pubmed ID exporter use entry point '1B', or alternatively you can use any text editor")
    print(f" If you have already done the Query Search, and now wish to have Graph the Hits use entry point '1C' ")
    print(f" If you have already done the Query Search, have the PubMed IDs (a list in a text file) and wish to get abstracts skip to entry point '2' ")
    primary_distination = input( " Now tell where would you like to go ? Type the Entry Point: ")

    if primary_distination == '1A':
        encasulated_advanced_pubmed_paper_counter()
        entry_point_01B()

    elif primary_distination == '1B':
        entry_point_01B()
    elif primary_distination == '1C':
        entry_point_01C()
    elif primary_distination == '2':
        entry_point_02()
    elif primary_destination == '000':
        print("Exiting the Query section. Back in Main section \n")
        return









"""-----------------------------------------------------------------------------------------------"""
# The Abstracts Retriver function entry_point_02 see entry_point Runner for o_ex
"""-----------------------------------------------------------------------------------------------"""

# Define functions from the script 02 The Abstracts Retriver
# (checks selected_pmids.txt for automatic mode)
#
#

def entry_point_02A(): # maybe in subsequent updates called by entry_point_01A
    print("This Entry point is to attempt to fetch the abstracts for the PubMed IDs. (checks selected_pmids.txt for automatic mode) \n")

    def getabstracts():
        import xml.etree.ElementTree as ET
        import requests
        import concurrent.futures
        import time
        import os
        from requests.exceptions import RequestException, HTTPError

        # Function to fetch article details from PubMed API
        def fetch_pubmed_details(pubmed_ids_batch, retries=5, delay=1):
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            params = {
                "db": "pubmed",
                "id": ",".join(pubmed_ids_batch),
                "retmode": "json"
            }
            for attempt in range(retries):
                try:
                    response = requests.get(url, params=params)
                    response.raise_for_status()
                    return response.json()
                except HTTPError as e:
                    if response.status_code == 429:
                        print(f"Too many requests. Retrying in {delay * (attempt + 1)} seconds...")
                        time.sleep(delay * (attempt + 1))
                    else:
                        print(f"Error fetching details for batch {pubmed_ids_batch}: {e}")
                        break
                except Exception as e:
                    print(f"Error fetching details for batch {pubmed_ids_batch}: {e}")
                    break
            return None

        def fetch_pubmed_abstract(pubmed_id, retries=10, delay=1):
            url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pubmed_id}&retmode=xml"
            for attempt in range(retries):
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    root = ET.fromstring(response.text)
                    abstract = root.find(".//AbstractText")
                    if abstract is not None:
                        return abstract.text
                except HTTPError as e:
                    if response.status_code == 429:
                        print(f"Too many requests. Retrying in {delay * (attempt + 1)} seconds...")
                        time.sleep(delay * (attempt + 1))
                    else:
                        print(f"Error fetching abstract for PubMed ID {pubmed_id}: {e}")
                        break
                except RequestException as e:
                    print(f"Error fetching abstract for PubMed ID {pubmed_id}: {e}")
                    if attempt < retries - 1:
                        print(f"Retrying in {delay * (attempt + 1)} seconds...")
                        time.sleep(delay * (attempt + 1))
            return "No abstract available."

        def fetch_abstract_and_create_xml_entry(pubmed_id, pubmed_details, root, remaining_count):
            try:
                print(f"Fetching abstract for PubMed ID: {pubmed_id} (Remaining: {remaining_count})")
                article = pubmed_details["result"][pubmed_id]
                pubmed_article = ET.SubElement(root, "PubmedArticle")
                medline_citation = ET.SubElement(pubmed_article, "MedlineCitation", PMID=pubmed_id)

                article_title = ET.SubElement(medline_citation, "ArticleTitle")
                article_title.text = article.get("title", "No title available")

                doi = ET.SubElement(medline_citation, "DOI")
                doi.text = article.get("elocationid", "No DOI available")

                pub_date = article.get("pubdate", "No publication date available")
                pub_year = pub_date.split(" ")[0] if pub_date else "No year available"

                year_of_publication = ET.SubElement(medline_citation, "YearOfPublication")
                year_of_publication.text = pub_year

                abstract = ET.SubElement(medline_citation, "Abstract")
                abstract.text = fetch_pubmed_abstract(pubmed_id)
            except Exception as e:
                print(f"Error creating XML entry for PubMed ID {pubmed_id}: {e}")

        # Function to create the XML
        def create_xml(pubmed_details, pubmed_ids_batch, remaining_count):
            root = ET.Element("PubmedArticleSet")

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(fetch_abstract_and_create_xml_entry, uid, pubmed_details, root, remaining_count - i)
                           for i, uid in enumerate(pubmed_ids_batch)]
                concurrent.futures.wait(futures)

            return ET.ElementTree(root)

        # Read PubMed IDs from a tab-delimited text file
        def read_pubmed_ids(file_path):
            try:
                with open(file_path, "r") as file:
                    pubmed_ids = [line.strip().split("\t")[0] for line in file]
                return pubmed_ids
            except Exception as e:
                print(f"Error reading PubMed IDs from file {file_path}: {e}")
                return []

        # Split PubMed IDs into batches
        def split_into_batches(pubmed_ids, batch_size=100):
            for i in range(0, len(pubmed_ids), batch_size):
                yield pubmed_ids[i:i + batch_size]

        # Path to the input file containing PubMed IDs
        input_file_abs = "selected_pmids.txt"  # Replace with your input file path
        if not os.path.exists(input_file_abs):
            input_file_abs = input(r"Automatic mode failed, no 'selected_pmids.txt' found, enter the path manually: ")
            while not os.path.exists(input_file_abs):
                input_file_abs = input("The specified file does not exist. Please enter a valid file path: ")

        # Read PubMed IDs from the input file
        pubmed_ids = read_pubmed_ids(input_file_abs)
        if not pubmed_ids:
            print("No PubMed IDs found. Exiting...")
            return
        total_pubmed_ids = len(pubmed_ids)
        print(f"Total PubMed IDs to process: {total_pubmed_ids}")

        # Initialize XML root
        root = ET.Element("PubmedArticleSet")

        # Rate limiting variables
        ids_per_minute = 600  # Adjust this value as needed
        delay_per_id = 60.0 / ids_per_minute

        # Process PubMed IDs in batches
        for pubmed_ids_batch in split_into_batches(pubmed_ids):
            # Fetch PubMed details for the current batch
            print(f"Fetching PubMed details for batch: {pubmed_ids_batch[:10]}... (total {len(pubmed_ids_batch)} IDs)")
            pubmed_details = fetch_pubmed_details(pubmed_ids_batch, delay=delay_per_id)
            if not pubmed_details:
                print("Failed to fetch PubMed details. Skipping batch...")
                continue

            # Generate XML for the current batch
            remaining_count = total_pubmed_ids - pubmed_ids.index(pubmed_ids_batch[-1])
            print("Generating XML for the current batch...")
            batch_xml_tree = create_xml(pubmed_details, pubmed_ids_batch, remaining_count)

            # Append batch XML elements to the main root
            for elem in batch_xml_tree.getroot():
                root.append(elem)

            # Delay to maintain the processing rate
            time.sleep(delay_per_id * len(pubmed_ids_batch))

        # Save the final XML to file
        output_file = "pubmed_abstracts.xml"
        try:
            xml_tree = ET.ElementTree(root)
            xml_tree.write(output_file, encoding="UTF-8", xml_declaration=True)
            print(f"XML file has been saved as {output_file}")
        except Exception as e:
            print(f"Error saving XML file: {e}")

    getabstracts()
    # Entry point call
    entry_point_02B()


"""-----------------------------------------------------------------------------------------------"""
# The GUI dashboard Function Entry_point_02B
"""-----------------------------------------------------------------------------------------------"""



def entry_point_02B():
    import xml.etree.ElementTree as ET
    import webbrowser
    import os

    def generate_html_from_xml(xml_file, output_file):
        # Load XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Start writing the HTML content
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>PubMed Abstracts</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    max-width: 800px;
                    margin: 20px auto;
                    padding: 20px;
                    background-color: #fff;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    text-align: center;
                    color: #333;
                }
                .article {
                    border-bottom: 1px solid #ccc;
                    padding: 10px 0;
                }
                .article:last-child {
                    border-bottom: none;
                }
                .article-number {
                    font-size: 1.5em;
                    color: #007bff;
                }
                .article-title {
                    margin: 0;
                    font-size: 1em;
                    color: #000;
                    cursor: pointer;
                }
                .article .abstract-content {
                    display: none;
                    margin-top: 10px;
                }
                .article p {
                    margin: 0 0 5px;
                    color: #666;
                }
                .article p strong {
                    color: #333;
                }
                .article a {
                    color: #007bff;
                    text-decoration: none;
                }
                .article a:hover {
                    text-decoration: underline;
                }
                .remove-button, .export-button, .clear-button, .collapse-button, .copy-citation-button, .sort-button {
                    display: inline-block;
                    margin-top: 10px;
                    padding: 10px 15px;
                    color: #fff;
                    background-color: #dc3545;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    text-align: center;
                }
                .export-button {
                    background-color: #28a745;
                    margin-bottom: 20px;
                }
                .clear-button {
                    background-color: #ffc107;
                    margin-left: 10px;
                }
                .collapse-button, .sort-button {
                    background-color: #007bff;
                    margin-left: 10px;
                }
                .copy-citation-button {
                    background-color: #17a2b8;
                    margin-left: 10px;
                }
                .remove-button:hover {
                    background-color: #c82333;
                }
                .export-button:hover {
                    background-color: #218838;
                }
                .clear-button:hover {
                    background-color: #e0a800;
                }
                .collapse-button:hover, .sort-button:hover {
                    background-color: #0056b3;
                }
                .copy-citation-button:hover {
                    background-color: #138496;
                }
                .checkbox {
                    margin-top: 10px;
                }
            </style>
            <script>
                document.addEventListener("DOMContentLoaded", function() {
                    var removedArticles = JSON.parse(localStorage.getItem('removedArticles')) || [];
                    var checkboxes = document.querySelectorAll('.remove-checkbox');
                    checkboxes.forEach(function(checkbox) {
                        if (removedArticles.includes(checkbox.value)) {
                            checkbox.checked = true;
                            var article = checkbox.closest('.article');
                            article.style.display = 'none';
                        }
                        checkbox.addEventListener('change', function() {
                            var article = checkbox.closest('.article');
                            if (checkbox.checked) {
                                article.style.display = 'none';
                                if (!removedArticles.includes(checkbox.value)) {
                                    removedArticles.push(checkbox.value);
                                    localStorage.setItem('removedArticles', JSON.stringify(removedArticles));
                                }
                            } else {
                                article.style.display = '';
                                var index = removedArticles.indexOf(checkbox.value);
                                if (index !== -1) {
                                    removedArticles.splice(index, 1);
                                    localStorage.setItem('removedArticles', JSON.stringify(removedArticles));
                                }
                            }
                        });
                    });

                    var titles = document.querySelectorAll('.article-title');
                    titles.forEach(function(title) {
                        title.addEventListener('click', function() {
                            var content = title.nextElementSibling;
                            if (content.style.display === 'none' || content.style.display === '') {
                                content.style.display = 'block';
                            } else {
                                content.style.display = 'none';
                            }
                        });
                    });
                });

                function exportPubMedIDs() {
                    var pubMedIDs = [];
                    var articles = document.querySelectorAll('.article');
                    articles.forEach(function(article) {
                        if (article.style.display !== 'none') {
                            var pubMedID = article.getAttribute('data-pubmed-id');
                            pubMedIDs.push(pubMedID);
                        }
                    });
                    var dataStr = "data:text/plain;charset=utf-8," + encodeURIComponent(pubMedIDs.join("\\n"));
                    var downloadAnchorNode = document.createElement('a');
                    downloadAnchorNode.setAttribute("href", dataStr);
                    downloadAnchorNode.setAttribute("download", "pubmed_ids.txt");
                    document.body.appendChild(downloadAnchorNode);
                    downloadAnchorNode.click();
                    downloadAnchorNode.remove();
                }

                function clearSavedState() {
                    localStorage.removeItem('removedArticles');
                    var articles = document.querySelectorAll('.article');
                    articles.forEach(function(article) {
                        article.style.display = '';
                    });
                    var checkboxes = document.querySelectorAll('.remove-checkbox');
                    checkboxes.forEach(function(checkbox) {
                        checkbox.checked = false;
                    });
                }

                function collapseAllAbstracts() {
                    var abstracts = document.querySelectorAll('.abstract-content');
                    abstracts.forEach(function(abstract) {
                        abstract.style.display = 'none';
                    });
                }

                function changeSortOrder(order) {
                    var articles = Array.from(document.querySelectorAll('.article'));
                    var container = document.querySelector('.container');
                    var sortedArticles = articles.sort(function(a, b) {
                        var yearA = parseInt(a.getAttribute('data-year'));
                        var yearB = parseInt(b.getAttribute('data-year'));
                        return (order === 'ascending') ? yearA - yearB : yearB - yearA;
                    });
                    sortedArticles.forEach(function(article) {
                        container.appendChild(article);
                    });
                }

                function copyToClipboard(text) {
                    navigator.clipboard.writeText(text).then(function() {
                        alert('Citation copied to clipboard');
                    }, function(err) {
                        console.error('Could not copy text: ', err);
                    });
                }
            </script>
        </head>
        <body>
            <div class="container">
                <h1>PubMed Abstracts</h1>
                <button class="export-button" onclick="exportPubMedIDs()">Export PubMed IDs</button>
                <button class="clear-button" onclick="clearSavedState()">Remove Saved State</button>
                <button class="collapse-button" onclick="collapseAllAbstracts()">Collapse All Abstracts</button>
                <button class="sort-button" onclick="changeSortOrder('ascending')">Sort Ascending</button>
                <button class="sort-button" onclick="changeSortOrder('descending')">Sort Descending</button>
        """

        # Loop through XML elements and add them to the HTML content
        for article in root.findall('PubmedArticle'):
            medline_citation = article.find('MedlineCitation')
            pmid = medline_citation.attrib.get('PMID')
            year = medline_citation.findtext('YearOfPublication')
            title = medline_citation.findtext('ArticleTitle')
            abstract = medline_citation.findtext('Abstract')
            doi = medline_citation.findtext('DOI')

            html_content += f"""
                <div class="article" data-pubmed-id="{pmid}" data-year="{year}">
                    <input type="checkbox" class="remove-checkbox checkbox" value="{pmid}"/> Remove Article
                    <span><strong>Year:</strong> {year}</span>
                    <button class="copy-citation-button" onclick="copyToClipboard(
                        'APA Citation: {pmid}, {title}. ({year}). {doi}'
                    )">Copy APA Citation</button>
                    <div class="article-title">{title}</div>
                    <div class="abstract-content">
                        <p><strong>PubMed ID:</strong> {pmid}</p>
                        <p>
                            <strong>DOI:</strong>
                            <a href="https://doi.org/{doi}">{doi}</a>
                        </p>
                        <p><strong>Abstract:</strong> {abstract}</p>
                    </div>
                </div>
            """

        # Close the HTML content
        html_content += """
            </div>
        </body>
        </html>
        """

        # Save the HTML content to the output file
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(html_content)

    # Define the paths to your XML and output HTML files
    xml_file = "pubmed_abstracts.xml"
    output_file = "output_html_file.html"

    # Call the function to generate the HTML
    generate_html_from_xml(xml_file, output_file)

    print(f"HTML file generated: '{output_file}'")
    # Get the absolute path of the current directory
    current_dir = os.getcwd()

    # Formulate the full file URL
    file_url = f"file://{current_dir}/{output_file}"
    # Open the generated HTML file in the default web browser
    webbrowser.open(file_url, new=2)




"""-----------------------------------------------------------------------------------------------"""
# The Abstracts Retriver function entry_point_02 Runners
"""-----------------------------------------------------------------------------------------------"""



def entry_point_02():

    print(f" If you have wish to continue to get the abstracts for the file 'selected_pmids.txt' containg the Pubmed IDs select '2A' ")
    print(f" If you have already XML abstracts and wish to filter out use '2B' Must have 'pubmed_abstracts.xml' ready in PWD ")
    print(f" For back menu use '000' ")
    primary_distination = input( " Now tell where would you like to go ? Type the Entry Point: ")

    if primary_distination == '2A':
        entry_point_02A()
        encapsulated_pubmedid_selector()
    elif primary_distination == '2B':
        entry_point_02B()
    elif primary_destination == '000':
        print("Exiting the Abstracts section. Back in Main section \n")
        return



"""-----------------------------------------------------------------------------------------------"""
# The Full Text PubMed Retriver Function Entry_point_03
"""-----------------------------------------------------------------------------------------------"""

# Define functions from the 03 script The full text PubMed retriver (pdf and HTML)
# This will not take consideration of what abstract downloader says about the full text availibility, we can use that for checking and establishing the consensus. This will use the Final starter input (pubmed_ids.txt)
# (checks pubmed_ids.txt for automatic mode),
# This suports resume capabilities

def entry_point_03(): # called by entry_point_02
    print(" This entry point is to attempt full text download of PDF and HTML from the PubMed IDs, (checks pubmed_ids.txt for automatic mode) and supports resume capabilities. \n")
    #latest full test downloader pubmed
    import os
    import requests
    from Bio import Entrez
    from bs4 import BeautifulSoup
    import time
    from datetime import datetime

    Entrez.email = 'your_email@example.com'  # Provide your email here

    PROCESSED_IDS_FILE = "processed_pubmed_ids.log"
    NO_FULL_TEXT_IDS_FILE = "no_full_text_ids.log"

    def create_output_directory():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_directory = f"output_{timestamp}"
        os.makedirs(output_directory)  # Create the main output directory
        return output_directory

    def fetch_pmcid(pmid):
        try:
            handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="xml")
            record = Entrez.read(handle)
            pmcid = None
            for id in record['PubmedArticle'][0]['PubmedData']['ArticleIdList']:
                if id.attributes['IdType'] == 'pmc':
                    pmcid = id
                    break
            return pmcid
        except Exception as e:
            print(f"Error fetching PMCID for PMID {pmid}: {e}")
            return None

    def download_file(url, filepath):
        try:
            print(f"      Downloading from URL: {url}")
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, allow_redirects=True)
            final_url = response.url  # Get the final URL after following redirects
            print(f"      Final URL after redirects: {final_url}")
            print(f"      HTTP Status Code: {response.status_code}")

            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"      Downloaded: {filepath} \n")
            else:
                print(f"      Failed to download from {url} (Status Code: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"      Error downloading from URL {url}: {e}")

    def fetch_and_save_content(url, pmid, output_directory, retries=3):
        headers = {'User-Agent': 'Mozilla/5.0'}
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Save HTML content
                    html_filepath = os.path.join(output_directory, f"{pmid}_fulltext.html")
                    with open(html_filepath, "w", encoding='utf-8') as file:
                        file.write(soup.prettify())
                    print(f"Downloaded {pmid}.html to {output_directory}")

                    # Save XML content if available
                    xml_link = soup.find("link", {"type": "application/xml"})
                    if xml_link and xml_link.get('href'):
                        xml_url = xml_link['href']
                        xml_filepath = os.path.join(output_directory, f"{pmid}_fulltext.xml")
                        download_file(xml_url, xml_filepath)
                    return True
                else:
                    print(f"Failed to fetch content from {url}: HTTP {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} - Error fetching content from {url}: {e}")
            time.sleep(1)  # Wait before retrying
        print(f"Failed to fetch content from {url} after {retries} attempts")
        return False

    def summarize_downloads(pdf_count, html_count, not_available_ids, total_ids):
        # Print summary
        print(f"\nSummary:")
        print(f"Total number of input PubMed IDs: {total_ids}")
        print(f"Number of PubMed IDs for which PDFs were downloaded: {pdf_count}")
        print(f"Number of PubMed IDs for which HTML files were downloaded: {html_count}")
        print(f"Number of PubMed IDs for which full text was not available: {not_available_ids}")

    def log_processed_pmid(pmid):
        with open(PROCESSED_IDS_FILE, 'a') as file:
            file.write(pmid + '\n')

    def log_no_full_text_pmid(pmid):
        with open(NO_FULL_TEXT_IDS_FILE, 'a') as file:
            file.write(pmid + '\n')

    def load_processed_pmids():
        if os.path.exists(PROCESSED_IDS_FILE):
            with open(PROCESSED_IDS_FILE, 'r') as file:
                return set(line.strip() for line in file if line.strip())
        return set()

    def process_pubmed_ids(pmid_list, fresh_start=False):
        if fresh_start:
            if os.path.exists(PROCESSED_IDS_FILE):
                os.remove(PROCESSED_IDS_FILE)
            if os.path.exists(NO_FULL_TEXT_IDS_FILE):
                os.remove(NO_FULL_TEXT_IDS_FILE)
            processed_pmids = set()
        else:
            processed_pmids = load_processed_pmids()

        pmid_list = [pmid for pmid in pmid_list if pmid not in processed_pmids]

        output_directory = create_output_directory()
        pdf_count = 0
        html_count = 0
        not_available_ids = 0
        total_ids = len(pmid_list) + len(processed_pmids)
        current_counter_initialiser = len(processed_pmids)

        for pmid in pmid_list:
            try:
                pmcid = fetch_pmcid(pmid)
                current_counter_initialiser += 1
                print(f"Trying {current_counter_initialiser}/{total_ids} PubMed ID: {pmid}  \n")
                if pmcid:
                    print(f"      Downloading full-text for PubMed ID: {pmid} (PMCID: {pmcid})")

                    # Create subdirectory for the current PubMed ID
                    subdir_path = os.path.join(output_directory, pmid)
                    os.makedirs(subdir_path)

                    # Download PDF
                    pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/"
                    pdf_filepath = os.path.join(subdir_path, f"{pmid}_fulltext.pdf")
                    download_file(pdf_url, pdf_filepath)
                    pdf_count += 1

                    # Download HTML if available
                    html_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/"
                    if fetch_and_save_content(html_url, pmid, subdir_path):
                        html_count += 1

                else:
                    print(f"      Full-text not available for PubMed ID: {pmid} \n")
                    not_available_ids += 1
                    log_no_full_text_pmid(pmid)

                log_processed_pmid(pmid)
                time.sleep(1)  # Pause for 1 second before next request

            except Exception as e:
                print(f"Error processing PubMed ID {pmid}: {e}")

        summarize_downloads(pdf_count, html_count, not_available_ids, total_ids)

    def read_pubmed_ids_from_file(file_path):
        with open(file_path, 'r') as file:
            pubmed_ids = [line.strip() for line in file if line.strip()]
        return pubmed_ids

    def root_full_text_pubmed_downloader():
        pubmed_ids_file = "pubmed_ids.txt"

        if os.path.isfile(pubmed_ids_file):
            print(f"Reading PubMed IDs from {pubmed_ids_file}")
            pubmed_ids = read_pubmed_ids_from_file(pubmed_ids_file)
        else:
            input_data = input("Enter a comma-delimited list of PubMed IDs or provide the file path: ").strip()
            if os.path.isfile(input_data):
                print(f"Reading PubMed IDs from {input_data}")
                pubmed_ids = read_pubmed_ids_from_file(input_data)
            else:
                pubmed_ids = [id.strip() for id in input_data.split(',') if id.strip()]

        action = input("Would you like to start fresh or continue from where you left off? (Enter 'fresh' or 'continue'): ").strip().lower()
        fresh_start = (action == 'fresh')

        process_pubmed_ids(pubmed_ids, fresh_start)

    root_full_text_pubmed_downloader()
    #entry_point_04() # chained to call entry point 04 , to fetch the PMCID and the DOIs for the PubMed IDs (no full text available )



"""-----------------------------------------------------------------------------------------------"""
# The PMCID and the DOIs Retriver Function Entry_point_04
"""-----------------------------------------------------------------------------------------------"""

# Define functions from the first script
# This entry point is to try to fetch the PMCID and the DOIs for the PubMed IDs. ( For which no full text was downloaded )
# It uses the file 'pubmed_no_full_text_file.txt' created by the entry point 03
#

def entry_point_04(): # called by entry_point_03
    root_fetch_pmc_and_DOI()
    entry_point_05() # chained to Entry Point 05, Url transformer

def root_fetch_pmc_and_DOI():
    print(" This entry point is to try to fetch the PMCID and the DOIs for the PubMed IDs. ( For which no full text was downloaded ) \n")
    # Check if pubmed_no_full_text_file.txt exists in the current directory
    input_file_path = 'pubmed_no_full_text_file.txt'
    if not os.path.exists(input_file_path):
        # If input.txt doesn't exist, ask the user for input
        print("File 'pubmed_no_full_text_file.txt' not found in current directory. Entering Manual Mode \n")
        input_ids = input("Enter File Path or PubMed IDs (comma-separated): \n ").strip()
    else:
        # Read PubMed IDs from input.txt
        input_ids = input_file_path

        if input_ids.endswith('.txt'):
            # Read PubMed IDs from file
            try:
                with open(input_ids, 'r') as file:
                    pubmed_ids = []
                    for line in file:
                        ids = line.strip().split(',') # this is line wise stripping can accept file with comma delimited multiple entries per line , last id dont require comma at the end
                        pubmed_ids.extend(ids)
            except FileNotFoundError:
                print(f"Error: File '{input_ids}' not found.")
                return
        else:
            # Split comma-separated IDs
            pubmed_ids = [id.strip() for id in input_ids.split(',')]

    choice = input("Include reasons for PubMed IDs with no PMCIDs found? (yes/no): ").strip().lower()
    include_reason = choice == 'yes'

    process_pubmed_ids(pubmed_ids, include_reason)


def get_pmcid(pubmed_id):
    # Function implementation...
    base_url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
    params = {
        'ids': pubmed_id,
        'format': 'json'
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if 'records' in data and data['records']:
        record = data['records'][0]
        return record.get('pmcid', 'Not Found')
    elif 'status' in data and data['status'] == 'error':
        reason = data['message']
        return f'Not Found: {reason}'
    else:
        return 'Not Found: Unknown reason'


def get_doi_from_pubmed_id(pubmed_id):
    # Function implementation...
    url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        doi_tag = soup.find("meta", {"name": "citation_doi"})

        if doi_tag and doi_tag.get("content"):
            return doi_tag["content"]
        else:
            print(f"No DOI found for PubMed ID: {pubmed_id}")
    else:
        print(f"Failed to retrieve PubMed page for ID: {pubmed_id}")

    return None

def process_pubmed_ids(pubmed_ids, include_reason):
    # Function implementation...
    pmc_ids_found = []
    dois = []
    pmids_not_found = []
    pmids_no_doi = []

    total_pubmed_ids = len(pubmed_ids)  # Total number of PubMed IDs provided

    for index, pubmed_id in enumerate(pubmed_ids, start=1):
        pubmed_id = pubmed_id.strip()

        # Display current working PubMed ID's index and total count
        print(f"Processing PubMed ID {index}/{total_pubmed_ids}: {pubmed_id}")

        # Get PMC ID and print status
        pmcid = get_pmcid(pubmed_id)
        pmcid_status = f"Fetched: {pmcid}" if not pmcid.startswith('Not Found') else f"Not Fetched: {pmcid}"
        print(f"PubMed ID: {pubmed_id} - PMC ID Status: {pmcid_status}")

        if pmcid.startswith('Not Found'):
            if include_reason:
                reason_parts = pmcid.split(': ', 1)
                if len(reason_parts) > 1:
                    reason = reason_parts[1]
                else:
                    reason = 'Reason not available'
                pmids_not_found.append(f"{pubmed_id} - {reason}")
            else:
                pmids_not_found.append(pubmed_id)
        else:
            pmc_ids_found.append(pmcid)

        # Attempt to retrieve DOI and print DOI status
        doi = get_doi_from_pubmed_id(pubmed_id)
        doi_status = f"Fetched: {doi}" if doi else "Not Fetched"
        print(f"PubMed ID: {pubmed_id} - DOI Status: {doi_status}")

        if doi:
            dois.append(f"https://doi.org/{doi}")
        else:
            pmids_no_doi.append(pubmed_id)

    pmc_ids_count = len(pmc_ids_found)
    dois_count = len(dois)
    pmids_no_doi_count = len(pmids_no_doi)

    # Print summary
    print(f"Total PubMed IDs provided: {total_pubmed_ids}")
    print(f"PMC IDs retrieved: {pmc_ids_count}")
    print(f"DOIs retrieved: {dois_count}")
    print(f"PubMed IDs with no DOI retrieved: {pmids_no_doi_count}")

    # Write PubMed IDs with no DOI retrieved to a text file
    if pmids_no_doi:
        output_file_no_doi = 'pmids_no_doi.txt'
        with open(output_file_no_doi, 'w') as file:
            file.write("PubMed IDs with no DOI found:\n")
            for pmid in pmids_no_doi:
                file.write(f"{pmid}\n")
        print(f"PubMed IDs with no DOI found saved to '{output_file_no_doi}'.")

    # Write results to separate files
    if pmc_ids_found:
        output_file_found = 'pmc_ids_found.txt'
        with open(output_file_found, 'w') as file:
            file.write("Found PMCIDs:\n")
            for pmcid in pmc_ids_found:
                file.write(f"{pmcid}\n")
        print(f"Found PMCIDs saved to '{output_file_found}'.")

    if dois:
        output_file_dois = 'dois_found.txt'
        with open(output_file_dois, 'w') as file:
            file.write("Found DOIs:\n")
            for doi in dois:
                file.write(f"{doi} \n")
        print(f"Found DOIs saved to '{output_file_dois}'.")

    if pmids_not_found:
        if include_reason:
            output_file_not_found = 'pmids_not_found_with_reason.txt'
        else:
            output_file_not_found = 'pmids_not_found.txt'
        with open(output_file_not_found, 'w') as file:
            if include_reason:
                file.write("PubMed IDs with reasons for no PMCIDs found:\n")
            else:
                file.write("PubMed IDs with no PMCIDs found:\n")
            for item in pmids_not_found:
                file.write(f"{item}\n")
        print(f"PubMed IDs with {'reasons for ' if include_reason else ''}no PMCIDs found saved to '{output_file_not_found}'.")





"""-----------------------------------------------------------------------------------------------"""
# The URL trasformer Function Entry_point_05
"""-----------------------------------------------------------------------------------------------"""

# Define functions from the fifth script
#
#
#

# Default URL prefixes if no file or interactive input is provided
DEFAULT_URL_PREFIXES = [
]

def entry_point_05(): # called by entry_point_04
    print(" This entry point is the bulk url transformer. \n")
    root_url_transformer()
    entry_point_06()  # Chained to entry_point_06 ,main_crawler_downloader  retriver


def root_url_transformer():
         # Transform PubMed IDs
        transformed_url_path = "dois_found.txt"
        if file_exists(transformed_url_path):
            print(f"The file '{transformed_url_path}' was found in the current directory. \n Entering Automatic mode ")
            pubmed_ids_path = transformed_url_path
            operation_choice = "prefix"
            url_prefixes_path = ""
            url_prefixes = DEFAULT_URL_PREFIXES  # Use default prefixes if no file path is expected

        if not file_exists(transformed_url_path):
            print(f"The file '{transformed_url_path}' was not found in the current directory.")
            # Prompt user for the file path
            transformed_url_path = input("Enter the path to the transformed URL file: ")
            pubmed_ids_path = transformed_url_path
            # Prompt for operation choice
            operation_choice = input("Choose operation ('prefix' to add prefixes, 'strip' to remove prefixes): ").strip().lower()
            while operation_choice not in ['prefix', 'strip']:
                print("Invalid operation choice. Please choose 'prefix' or 'strip'.")
                operation_choice = input("Choose operation ('prefix' to add prefixes, 'strip' to remove prefixes): ").strip().lower()

            # Determine URL prefixes based on user input
            url_prefixes_path = input("Enter the path to the URL prefixes file (leave blank if not using file): ")
            if url_prefixes_path:
                url_prefixes = read_file_lines(url_prefixes_path)
            else:
                url_prefixes = DEFAULT_URL_PREFIXES  # Use default prefixes if no file path is provided

        # Transform PubMed IDs based on operation choice
        transformed_ids = transform_pubmed_ids(pubmed_ids_path, operation_choice, url_prefixes)


def file_exists(file_path):
    return os.path.isfile(file_path)

def read_file_lines(file_path):
    # Function implementation...
    """Read lines from a file and return them as a list."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def transform_pubmed_ids(pubmed_ids_path, operation_choice, url_prefixes=None):
    # Read PubMed IDs from the file
    pubmed_ids = read_file_lines(pubmed_ids_path)

    # Determine URL prefixes to use
    if not url_prefixes:
        url_prefixes = DEFAULT_URL_PREFIXES  # Use default prefixes if none provided

    # Process each PubMed ID based on operation choice
    transformed_ids = []
    for pubmed_id_line in pubmed_ids:
        pubmed_id_line = pubmed_id_line.strip()
        if pubmed_id_line:  # Check if line is not empty
            if operation_choice == 'prefix':
                # Split IDs based on comma, space, or tab
                pubmed_ids_split = re.split(r'[,\s\t]+', pubmed_id_line)
                # Prefix each PubMed ID with URL prefixes
                for pid in pubmed_ids_split:
                    for prefix in url_prefixes:
                        transformed_ids.append(f"{prefix}/{pid}")
            elif operation_choice == 'strip':
                # Strip existing prefixes from PubMed IDs
                stripped_id = pubmed_id_line
                for prefix in url_prefixes:
                    if stripped_id.startswith(prefix):
                        stripped_id = stripped_id[len(prefix):].lstrip('/')
                        break  # Stop after stripping the first matching prefix
                transformed_ids.append(stripped_id)

     # Output file path
    output_file_path = "transformed_pubmed_ids.txt"

    # Write transformed IDs to output file
    write_transformed_ids(output_file_path, transformed_ids)

    print(f"Transformation completed. Transformed IDs saved in '{output_file_path}'.")

    return transformed_ids



def write_transformed_ids(output_file_path, transformed_ids):
    # Function implementation...
    """Write transformed IDs to an output file."""
    with open(output_file_path, 'w') as outfile:
        for transformed_id in transformed_ids:
            outfile.write(transformed_id + ',')


"""-----------------------------------------------------------------------------------------------"""
# The URL reverse transformer Function Entry_point_5A
"""-----------------------------------------------------------------------------------------------"""


# Define functions for entry point 5A
# This is a reverse url transformer for the DOIs having prefixes of the third party URL
#
#

def entry_point_5A(): #chained from entry_point_06(), main crawler downloader from the third party sources
    root_url_reverse_transformer()
    entry_point_07AUTO()  #chained back to entry_point_07, deduplicator script(functions)

def root_url_reverse_transformer():
         # Transform PubMed IDs
        transformed_url_path_5A = "urls_without_pdf.txt"
        if file_exists_5A(transformed_url_path_5A):
            print(f" The file '{transformed_url_path_5A}' was found in the current directory. Continuing Automatic mode ")
            pubmed_ids_path_5A = transformed_url_path_5A
            operation_choice_5A = "strip"
            url_prefixes_path_5A = ""
            url_prefixes_5A = DEFAULT_URL_PREFIXES  # Use default prefixes if no file path is expected

        transformed_ids_5A = transform_pubmed_ids_5A(pubmed_ids_path_5A, operation_choice_5A, url_prefixes_5A)


def file_exists_5A(file_path_5A):
    return os.path.isfile(file_path_5A)

def read_file_lines_5A(file_path_5A):
    # Function implementation...
    """Read lines from a file and return them as a list."""
    with open(file_path_5A, 'r') as file:
        lines_5A = file.readlines()
    return lines_5A

def transform_pubmed_ids_5A(pubmed_ids_path_5A, operation_choice_5A, url_prefixes_5A=None):
    # Read PubMed IDs from the file
    pubmed_ids_5A = read_file_lines_5A(pubmed_ids_path_5A)

    # Determine URL prefixes to use
    if not url_prefixes_5A:
        url_prefixes_5A = DEFAULT_URL_PREFIXES  # Use default prefixes if none provided

    # Process each DOI based on operation choice
    transformed_ids_5A = []
    for pubmed_id_line_5A in pubmed_ids_5A:
        pubmed_id_line_5A = pubmed_id_line_5A.strip()
        if pubmed_id_line_5A:  # Check if line is not empty
            if operation_choice_5A == 'strip':
                # Strip existing prefixes from PubMed IDs
                stripped_id_5A = pubmed_id_line_5A
                for prefix_5A in url_prefixes_5A:
                    if stripped_id_5A.startswith(prefix_5A):
                        stripped_id_5A = stripped_id_5A[len(prefix_5A):].lstrip('/')
                        break  # Stop after stripping the first matching prefix
                transformed_ids_5A.append(stripped_id_5A)

     # Output file path
    output_file_path_5A = "urls_without_pdf.txt"

    # Write transformed IDs to output file
    write_transformed_ids_5A(output_file_path_5A, transformed_ids_5A)

    print(f" Reverse Transformation completed. Stripped DOIs saved in '{output_file_path_5A}' \n.")

    return transformed_ids_5A

def write_transformed_ids_5A(output_file_path_5A, transformed_ids_5A):
    # Function implementation...
    """Write transformed IDs to an output file."""
    with open(output_file_path_5A, 'w') as outfile_5A:
        for transformed_id_5A in transformed_ids_5A:
            outfile_5A.write(transformed_id_5A.strip() + '\n')





"""-----------------------------------------------------------------------------------------------"""
# The Main Crawler Downloader Function Entry_point_06
"""-----------------------------------------------------------------------------------------------"""


# Define functions from the sixth script
# This is main crawler downloader from the third party sources
#
#

def entry_point_06(): # called by entry_point_06, url transformer
    root_main_crawler_downloader()
    entry_point_5A() #chained back to entry_point_07, deduplicator script(functions)

def root_main_crawler_downloader():
# Crawl and Download from URLs
        if os.path.exists('transformed_pubmed_ids.txt'):
            print("File transformed_pubmed_ids.txt found, entering automatic mode ")
            file_path = 'transformed_pubmed_ids.txt'
            with open(file_path, 'r') as file:
                urls = []
                for line in file:
                        line = line.strip()
                        urls.extend(line.split(','))
                #content = file.read().strip()  # Read the file content and strip leading/trailing whitespace
                #urls = content.split(',')      # Split the content by commas
                print("Total URLs:", len(urls))
            crawl_and_download(urls)




        else:
            print("File transformed_pubmed_ids.txt not found, entering manual mode ")
            input_mode = input("Enter '1' to input URLs directly, '2' to specify a file path containing URLs: ")

            if input_mode == '1':
            # Input multiple URLs directly (comma-delimited)
                urls = input("Enter comma-separated URLs: ").split(',')
                print("\n Total URLs:", len(urls))
                crawl_and_download(urls)
            elif input_mode == '2':
                file_path = input("Enter file path containing URLs: ")
                with open(file_path, 'r') as file:
                    urls = []
                for line in file:
                        line = line.strip()
                        urls.extend(line.split(','))
                    #content = file.read().strip()  # Read the file content and strip leading/trailing whitespace
                    #urls = content.split(',')
                        print("\n Total URLs:", len(urls))
                        crawl_and_download(urls)
            else:
                print("Invalid input mode. Please enter '1' or '2'.")
        exit()


def extract_base_url(url):
    # Function implementation...
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def extract_src_urls(soup):
    # Function implementation...
    src_urls = []

    # Find all elements that might contain 'src' attributes
    elements_with_src = soup.find_all(['iframe', 'embed', 'object', 'video', 'audio', 'source', 'img', 'script', 'link', 'division', 'div', 'a'])

    # Extract 'src' attributes from elements
    for element in elements_with_src:
        if element.has_attr('src'):
            src_urls.append(element['src'])

        # Check additional attributes like 'data-src' or 'href' for certain elements
        if element.name == 'script' and element.has_attr('src'):
            src_urls.append(element['src'])
        elif element.name == 'link' and element.has_attr('href'):
            src_urls.append(element['href'])
        elif element.name == 'a' and element.has_attr('href'):
            src_urls.append(element['href'])
        elif element.name == 'source' and element.has_attr('src'):
            src_urls.append(element['src'])

    return src_urls

def print_src_with_pdf(src_urls):
    pdf_urls = [url for url in src_urls if '.pdf' in url.lower()]

    print("\nList of 'src' attributes containing '.pdf':")
    for url in pdf_urls:
        print(url)

    return pdf_urls


def download_pdfs(pdf_urls, base_url):
    if not pdf_urls:
        print("No PDF files found.")
        return

    print("\nAttempting to download PDF files:")
    for url in pdf_urls:
        # Resolve relative URLs against the base URL
        full_url = urljoin(base_url, url)

        try:
            print(full_url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(full_url, headers=headers, stream=True)
            response.raise_for_status()

            # Extract filename from URL and append '.pdf' extension
            filename = full_url.split('/')[-1]
            if not filename.lower().endswith('.pdf'):
                filename += '.pdf'

            # Save PDF content to a file with the correct filename and extension
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Downloaded PDF: {filename}")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading PDF from {full_url}: {e}")

def crawl_and_download(urls):
    total_urls = len(urls)
    pdf_urls_found = 0
    pdfs_downloaded = 0
    subcounter_nth_url = 0
    initialiser_no_pdf_url = 0
    urls_without_pdf = []


    for url in urls:

        subcounter_nth_url += 1
        print(f"\n Trying {subcounter_nth_url}/{total_urls} Of the Total Url Supplied:  {url} \n " )

        try:
            # Send a GET request to the URL
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad responses

            # Extract base URL from the current URL
            base_url = extract_base_url(url)
            print(f"     The Base Url detected was : {base_url}" )
            print(f"     Sleeping for 5 Seconds to allow page to load" )

            # Wait for 5 seconds to allow the page to load completely
            time.sleep(5)

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract all 'src' attributes from the HTML
            src_urls = extract_src_urls(soup)

            # Filter and collect 'src' attributes containing '.pdf'
            pdf_urls = [urljoin(base_url, src) for src in src_urls if '.pdf' in src.lower()]
            subcounter_total_pdf_url_in_this_link = len(pdf_urls)
            print(f"          Total Pdf Url detected in this page were : {subcounter_total_pdf_url_in_this_link}" )
            print("          The PDF URLs detected List is :")
            subcounter_initialiser_pdf_listing = 0
            for url in pdf_urls:
                subcounter_initialiser_pdf_listing += 1
                print(f"          {subcounter_initialiser_pdf_listing}/{subcounter_total_pdf_url_in_this_link} : {url} ")


            # Count PDF URLs found
            pdf_urls_found += len(pdf_urls)
            #print(f" Total Pdf Url detected in this page were : {pdf_urls_found}" )

            subcounter_nth_pdf_url = 0

            # Attempt to download PDF files using resolved URLs and base URL
            for pdf_url in pdf_urls:
                try:
                    subcounter_nth_pdf_url += 1
                    print(f"\n          Trying {subcounter_nth_pdf_url}/{subcounter_total_pdf_url_in_this_link}/{subcounter_nth_url}/{total_urls} : {pdf_url} " )
                    response = requests.get(pdf_url, headers=headers, stream=True)
                    response.raise_for_status()

                    # Extract filename from URL and append '.pdf' extension
                    filename = pdf_url.split('/')[-1]
                    if not filename.lower().endswith('.pdf'):
                        filename += '.pdf'

                    # Save PDF content to a file with the correct filename and extension
                    with open(filename, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    # Increment count of downloaded PDFs
                    pdfs_downloaded += 1
                    print(f"\n Downloaded PDF: {filename} \n {pdfs_downloaded} PDF downloaded yet. ")

                except requests.exceptions.RequestException as e:
                    print(f"\n Error downloading PDF from {pdf_url}: {e} \n \n")
                    print(f"\n Downloaded PDF: {filename} \n {pdfs_downloaded} PDF downloaded yet. ")


            #if not pdf_urls:
            #    urls_without_pdf.append(url)

        except requests.exceptions.RequestException as e:
            initialiser_no_pdf_url += 1
            urls_without_pdf.append(url)
            print(f" Error occurred while processing {url}: {e} \n \n")
            print(f"\n {pdfs_downloaded} PDF downloaded yet. ")
            print(f" Number of URLs for which no PDF could be downloaded : {initialiser_no_pdf_url}")



    # Print summary
    print("\n----- Summary -----")
    print(f"Total input URLs: {total_urls}")
   # print(f"Total PDF URLs found: {pdf_urls_found}")
    print(f"Total PDFs downloaded: {pdfs_downloaded}")
    ratio = pdfs_downloaded/total_urls
    print(f"Url to PDF ratio : {ratio} \n\n ")



    # Save URLs without PDFs to a text file
    if urls_without_pdf:
        total_urls_without_pdf = len(urls_without_pdf)
        print(f"Number of URLs for which no PDF could be downloaded : {total_urls_without_pdf}")
        with open('urls_without_pdf.txt', 'w') as file:
            for url in urls_without_pdf:
                file.write(url.strip() + " \n")
        print(f"List of URLs for which no PDF could be downloaded saved to 'urls_without_pdf.txt' \n")
        print(f"Starting to Unprefix the Transformed DOI of the URLs for which no PDF could be downloaded \n Entering Entry point 5A ")
        entry_point_5A()




"""-----------------------------------------------------------------------------------------------"""
# The Deduplicator Function Entry_point_07AUTO / Function Entry_point_07_manual
"""-----------------------------------------------------------------------------------------------"""

# Define functions from the seventh script
# This is deduplicator script
#
#
def entry_point_07_manual(): #called from main central script
    duplicate_main_manual()
    entry_point_08_AUTO() # chained to entry_point_08, Pdf to txt convertor

def entry_point_07AUTO(): #chained from enrtry_point_05A, reverse url transformer for the DOIs
    duplicate_main_auto()
    entry_point_08_AUTO() # chained to entry_point_08, Pdf to txt convertor

def calculate_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  # Read in 64k chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def copy_unique_files(source_directory, file_extension=None):
    sub_counter_permission_denied_files = 0

    # Create a timestamp for the destination directory
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    destination_dir_timestamped = f"no_duplicates_{timestamp}"

    # Create the timestamped destination directory
    os.makedirs(destination_dir_timestamped, exist_ok=True)

    # Dictionary to store hashes and corresponding file paths
    hash_to_path = {}

    # Convert the provided extension to lowercase for case-insensitive comparison
    if file_extension:
        file_extension = file_extension.lower()

    # Iterate over files in the source directory
    for file_name in os.listdir(source_directory):
        file_path = os.path.join(source_directory, file_name)
        if os.path.isfile(file_path):  # Check if it's a file (not a directory)
            # Get the lowercase extension of the file
            file_ext = os.path.splitext(file_name)[1].lower()
            # Check if the file extension matches the provided extension (case-insensitive)
            if file_extension and not file_ext == file_extension:
                continue  # Skip files with non-matching extensions
            try:
                file_hash = calculate_hash(file_path)
                if file_hash not in hash_to_path:
                    hash_to_path[file_hash] = file_path
            except PermissionError:
                sub_counter_permission_denied_files += 1
                # print(f"Permission denied for file: {file_path}. Skipping.")

    # Copy unique files to the destination directory
    for file_hash, file_path in hash_to_path.items():
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(destination_dir_timestamped, file_name)
        shutil.copy2(file_path, destination_path)

    return sub_counter_permission_denied_files  # Return the count of permission denied files

def duplicate_summary_print(source_directory, file_extension=None):
    # Print total number of files in source directory
    if file_extension:
        # If file_extension is provided, count only files with that extension
        total_files_source = sum(1 for file_name in os.listdir(source_directory) if os.path.isfile(os.path.join(source_directory, file_name)) and file_name.lower().endswith(file_extension))
    else:
        # If file_extension is not provided, count all files
        total_files_source = sum(1 for file_name in os.listdir(source_directory) if os.path.isfile(os.path.join(source_directory, file_name)))
    print(f" Total number of files in the source directory: {total_files_source}")

##       # List files in source and destination directories
##    source_files = set(os.listdir(source_directory))
##    destination_directory = f"no_duplicates_{datetime.now().strftime('%Y%m%d%H%M%S')}"
##    destination_files = set(os.listdir(destination_directory))
##

    # Print total number of files in destination directory
    destination_directory = f"no_duplicates_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    total_files_destination = sum(1 for _ in os.listdir(destination_directory) if os.path.isfile(os.path.join(destination_directory, _)))
    print(f" Total number of files in the destination directory: {total_files_destination}")


##    # Find missing files in the destination directory
##    missing_files = source_files - destination_files
##    if missing_files:
##        print(" Missing files in the destination directory:")
##        for file_name in missing_files:
##            print(f"  - {file_name}")


# Modified duplicate_main_manual function
def duplicate_main_manual():
    source_directory = input(r"path/to/source_directory: ")
    file_extension = input("'.txt'. Change this to the desired file extension, or leave as None to include all files: ")
    sub_counter_permission_denied_files = copy_unique_files(source_directory, file_extension)
    print(f" File extension used for target and scan duplicates was {file_extension}")
    print(f" Total files Skipped due to permission denied {sub_counter_permission_denied_files}")
    duplicate_summary_print(source_directory, file_extension)


def duplicate_main_auto():
    print(f" Welcome to Entry point 4 : Duplicate removal. This is to ensure we have only one copy of the downloaded corpus. As we used multiple mirrors to download, there can be redundancy of PDFs. This will create a time-stamped final output directory for you, and no alteration would be made to the current working directory.")
    source_directory = os.getcwd()
    sub_counter_permission_denied_files = 0
    file_extension = '.pdf'
    copy_unique_files(source_directory, file_extension)
    print(f" File extension used for target and scan duplicates was {file_extension}")
    print(f" Total files Skipped due to permission denied {sub_counter_permission_denied_files}")
    duplicate_summary_print(source_directory, file_extension)
    #pdf_2_txt_auto() # Calling Fifth Script in automatic mode






"""-----------------------------------------------------------------------------------------------"""
# The PDF to TXT convertor Function Entry_point_08_auto / entry_point_08_manual
"""-----------------------------------------------------------------------------------------------"""

# Define functions from the Eighth script
# This is pdf to txt convertor script/functions
#
#
def entry_point_08_manual(): #called from main central script
    pdf_2_txt_manual()
    # may in future chained to thhe summarisation modules

def entry_point_08_auto(): #chained from entry_point_07AUTO and entry_point_07_manual
    pdf_2_txt_auto()
    # may in future chained to thhe summarisation modules

def extract_text_from_pdf(pdf_path, output_directory):
    if os.path.isfile(pdf_path) and pdf_path.endswith('.pdf'):
        pdf_files = [pdf_path]
    elif os.path.isdir(pdf_path):
        pdf_files = [os.path.join(pdf_path, file) for file in os.listdir(pdf_path) if file.endswith('.pdf')]
    else:
        print("Invalid input: Not a valid PDF file or directory path.")
        return

    num_files = len(pdf_files)
    print("Number of PDF files detected: ", num_files)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print("Created output directory:", output_directory)

    # Iterate over each PDF file
    for i, file_path in enumerate(pdf_files, start=1):
        file_name = os.path.basename(file_path)
        output_file = os.path.splitext(file_name)[0] + '.txt'

        print("Processing PDF file {}/{}: {}".format(i, num_files, file_name))

        pdf = PdfReader(file_path)

        with open(os.path.join(output_directory, output_file), 'w', encoding='utf-8') as f:
            for page_num in range(len(pdf.pages)):
                pageObj = pdf.pages[page_num]

                try:
                    txt = pageObj.extract_text()
                  # print(''.center(100, '-'))
                except:
                    pass
                else:
                    f.write('Page {0}\n'.format(page_num+1))
                    f.write(''.center(100, '-'))
                    f.write(txt)

        print("Text extraction completed for {}.".format(file_name))

def pdf_2_txt_auto():
    pdf_path = r'/path/to/pdf/files'  # Replace with the path to your PDF file or directory

    # Create output directory in the same path as the source directory
    output_directory = os.path.join(os.path.dirname(pdf_path), datetime.now().strftime("%Y%m%d_%H%M%S") + "_pdf_2_txt")

    extract_text_from_pdf(pdf_path, output_directory)

def pdf_2_txt_manual():
    pdf_path = input(r"Enter the path to the PDF file or directory: ")

    # Create output directory in the same path as the source directory
    output_directory = os.path.join(os.path.dirname(pdf_path), datetime.now().strftime("%Y%m%d_%H%M%S") + "_pdf_2_txt")

    extract_text_from_pdf(pdf_path, output_directory)





"""-----------------------------------------------------------------------------------------------"""
# Utilities Subsection entry_point_09() # currently only called manually
"""-----------------------------------------------------------------------------------------------"""


# define function for ninth scrit
# The Utilties
#
#
def entry_point_09(): # currently only called manually

    print(" The Utilities  \n Type '10' to exit Utilities and return to the main section !\n")

    while True:
        entry_point = input("Select an entry point:\n"


                            "1.          Refrences (.bib file generation) \n"
                            "2.          The Named Entity Recognition (spaCy model) \n"
                            "3.          TF-IDF Validator \n"
                            "4.          Get File of an extension sorted in one place \n"
                            "5.          The Summarisation \n"

                            "5A.         Self Trainable NER will be available soon \n"
                            "5B.         Image maniulation detection will be available soon \n"
                            "5C.         Feature extraction will be available soon \n"
                            "1111.       Check for the Updates \n"
                            "1112.       The License \n"
                            "999.        Clear Screen\n"
                            "000.        Exit\n"
                            "Enter your choice (1/10): ")

        if entry_point == '1':
            entry_point_Util_01() # The Refrences
        if entry_point == '2':
            entry_point_Util_02() # The spaCy
        if entry_point == '3':
            entry_point_Util_03() # The TF-IDF
        elif entry_point == '4':
            entry_point_Util_04() # The File Sorter By type
        elif entry_point == '5':
            entry_point_Util_05() # The Summeriser

            entry_point_Util_1111() # The updater

        elif entry_point == '1112':
            entry_point_Util_1112() # The License

        elif entry_point == '999':
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen command


        elif entry_point == '000' :
            print("Exiting the Utilities section. Back in Main section \n")
            break
        else :
            print("Invalid Selection")



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This the Subsection Utilities executed under entry_point_9 #utilities
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
The References/Citation script function entry_point_Util_01
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def entry_point_Util_01(): # called by entry_point_09.option.1 The citation script function
    print(" Welcome to the Refrences/Citation Entry_point  (entry_point_Util_01)")
    encapsulated_refence_manager()



def encapsulated_refence_manager():
    import requests
    import time

    def fetch_pubmed_metadata(pmids_file, delimiter=','):
        # Read PMIDs from file
        with open(pmids_file, "r") as f:
            pmids = []
            for line in f:
                pmids.extend(line.strip().split(delimiter))

        # PubMed API base URL
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

        # Initialize list to store BibTeX entries
        bib_entries = []
        error_count = 0
        success_count = 0

        print(f"Total PMIDs to process: {len(pmids)}")

        # Iterate over each PMID and fetch metadata
        for pmid in pmids:
            try:
                print(f"Processing PMID: {pmid}")

                # Construct request parameters
                params = {
                    "db": "pubmed",
                    "id": pmid,
                    "retmode": "json"
                }

                # Make GET request to PubMed API
                response = requests.get(base_url, params=params)

                # Check if request was successful
                if response.status_code == 200:
                    data = response.json()

                    # Check if PMID is present in the result
                    if pmid in data['result']:
                        # Extract relevant metadata fields
                        title = data['result'][pmid].get('title', '')
                        authors_list = data['result'][pmid].get('authors', [])
                        authors = ", ".join([author['name'] for author in authors_list])
                        year = data['result'][pmid].get('pubdate', '').split()[0]  # Extract year from pubdate
                        doi = data['result'][pmid].get('articleids', [{}])[0].get('value', '')

                        # Construct BibTeX entry
                        bib_entry = f"@article{{PMID{pmid},\n"
                        bib_entry += f"  title = {{{title}}},\n"
                        bib_entry += f"  author = {{{authors}}},\n"
                        bib_entry += f"  year = {{{year}}},\n"
                        bib_entry += f"  doi = {{{doi}}}\n"
                        bib_entry += "}\n"

                        bib_entries.append(bib_entry)
                        success_count += 1
                    else:
                        print(f"No valid metadata found for PMID {pmid}")
                        error_count += 1
                else:
                    print(f"Error fetching PMID {pmid}: Status Code {response.status_code}")
                    error_count += 1

            except Exception as e:
                print(f"Error fetching PMID {pmid}: {e}")
                error_count += 1

            # Add a small delay to respect API rate limits
            time.sleep(0.5)

        # Save .bib file
        with open("pubmed_ids.bib", "w", encoding='utf-8') as f:
            f.write("\n".join(bib_entries))

        # Print summary
        print("\nSummary:")
        print(f"Total PMIDs processed: {len(pmids)}")
        print(f"Successful entries: {success_count}")
        print(f"Errors encountered: {error_count}")
        print(f"Final .bib file contains {len(bib_entries)} entries")

    # Example usage
    pmids_file_for_ref = "pubmed_ids.txt"
    if not os.path.exists(pmids_file_for_ref):
        pmids_file_for_ref = input (r" Automatic mode failed no 'pubmed_ids.txt' found, enter the path manually ")
        while not os.path.exists(pmids_file_for_ref):
            pmids_file_for_ref = "pubmed_ids.txt"  # Replace with your input file path
            if not os.path.exists(pmids_file_for_ref):
                pmids_file_for_ref = input (r" Automatic mode failed no 'pubmed_ids.txt' found, enter the path manually ")
                while not os.path.exists(pmids_file_for_ref):
                    pmids_file_for_ref = input("The specified file does not exist. Please enter a valid file path: ")


    custom_delimiter = ','

    fetch_pubmed_metadata(pmids_file_for_ref, delimiter=custom_delimiter)



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
The spaCy script function entry_point_Util_02
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def entry_point_Util_02():
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

    def root_encapsulated_spacy():
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
    root_encapsulated_spacy()
    entry_point_09()


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
The TF-IDF script function entry_point_Util_03
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def entry_point_Util_03():
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

    def root_encapsualted_TFIDF():
        # Select file type
        print("This calculate the TF-IDF relevancy score of the XML/HTML/TXT files in targeted directory")
        print(" Require Use input to mention the key terms for which TF-IDF is to be calculated.")

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
    root_encapsualted_TFIDF()


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
The Sorter script function entry_point_Util_04
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# This generates a flat file ssytem of a purticular extention by crawling into subdirectory tree
# This mainly used to collect the fragmented files of one extention, deduplicator can also be run after this

def entry_point_Util_04():
    import os
    import shutil

    def sort_files_by_extension(directory):
        # Get the extension from user input
        extension = input("Enter the file extension (without the '.' character): ")

        # Create a directory to store the sorted files
        # Using os.getcwd() to get the current working directory
        sorted_directory = os.path.join(os.getcwd(), extension)
        os.makedirs(sorted_directory, exist_ok=True)

        # Traverse the directory and its subdirectories
        for root, _, files in os.walk(directory):
            for file in files:
                # Get the full path of the file
                file_path = os.path.join(root, file)
                # Check if the file has the desired extension
                if file.endswith('.' + extension):
                    # Construct the destination file path
                    dest_file_path = os.path.join(sorted_directory, file)

                    # If the file already exists, add a number to the filename
                    if os.path.exists(dest_file_path):
                        base, ext = os.path.splitext(file)
                        counter = 1
                        new_file_name = f"{base}_{counter}{ext}"
                        dest_file_path = os.path.join(sorted_directory, new_file_name)

                        while os.path.exists(dest_file_path):
                            counter += 1
                            new_file_name = f"{base}_{counter}{ext}"
                            dest_file_path = os.path.join(sorted_directory, new_file_name)

                    # Copy the file to the sorted directory with the unique name
                    shutil.copy(file_path, dest_file_path)

        print(f"All files with extension '{extension}' have been copied to '{sorted_directory}'.")


    def file_sorter():
        print("This generates a flat file sytem of a purticular extention by crawling into subdirectory tree")
        print("This is mainly used to collect the fragmented files of an extention, deduplicator can also be run after this")
        # Get the directory path from user input
        directory_path = input("Enter the directory path: ")
        sort_files_by_extension(directory_path)

    if __name__ == "__main__":
        file_sorter()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
This script is for summerisation function entry_point_Util_05
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def entry_point_Util_05():
    print("This is summerisation entry_point, we recommend to use this on Goggle Colab")
    print("This is a strip down version and dont include the summurisation module for the above said reason. Last version to include that is 0.0.3.7")
    entry_point_09()


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
The updater script function entry_point_Util_1111
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def entry_point_Util_1111(): # called by entry_point_09.option.1111 The updater script function
    print(" Checking for the available updates : ")
    root_updater_main_function()

def download_file(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except:
        print(".\n.")
        pass

    #sys.exit()


def calculate_hash(contents):
    return hashlib.sha256(contents.encode()).hexdigest()

def root_updater_main_function():
    url = "https://raw.githubusercontent.com/ydv-amit-ydv/af_chainsaw/main/test.py"
    #url = ""
    remote_file_contents = download_file(url)

    if remote_file_contents:
        local_hash = calculate_hash(open(sys.argv[0], 'r').read())
        remote_hash = calculate_hash(remote_file_contents)

        if local_hash != remote_hash:
            with open(sys.argv[0], 'w') as file:
                file.write(remote_file_contents)
                print("!!!")



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
The License entry_point_Util_1112
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def entry_point_Util_1112():
    print("Checking for the available updates:")
    encapsulated_the_license_function()

def encapsulated_the_license_function():
    # Function to read the contents of license.txt file
    def read_license_file():
        module_dir = os.path.dirname(__file__)  # Get the directory of the current module
        license_file_path = os.path.join(module_dir, 'data', 'LICENSE.txt')
        with open(license_file_path, 'r') as file:
            license_content = file.read()
        return license_content

    # Display the contents of license.txt file
    print("License Agreement:")
    print(read_license_file())
    input("Press any key to go back...")






"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



# Main entry point for the combined script

def main():
    while True:
        try:
            print("Welcome to the Combined Data Mining Utility !\n By Using this script you agree to LICENSE")
            root_updater_main_function()
            while True:
                entry_point = input("Select an entry point :\n"
                                    "00.        Help \n"
                                    "1.         PubMed search/query \n"
                                    "2.         Abstracts \n"
                                    "3.         Attempt Full Text Download from PubMed\n"
                                    "4.         Process PubMed IDs to get DOI for  search\n"
                                    "5.         Url Transform PubMed IDs \n"
                                    "6.         Crawl and Download from URLs\n"
                                    "7.         Remove Duplicates\n"
                                    "8.         PDF_2_txt\n"
                                    "9.         Additional Utilities\n"
                                    "999.       Clear Screen\n"
                                    "0000.      Exit\n"
                                    "Enter your choice (1/2/3/4/5/6/7/8/9/999/10): ")

                if entry_point == '00' or entry_point.lower() == 'help':
                    entry_point_help()

                elif entry_point == '1':
                    entry_point_01() # This is to make the PubMed search
                    return

                elif entry_point == '1A':
                    entry_point_01A() #Graph maker based on the n of pubmed_ids retrived

                elif entry_point == '2':
                    entry_point_02() # This is to retrive abstracts from PubMed

                elif entry_point == '3':
                    entry_point_03() # This is to attempt full text downloads from the Pubmed this have resume capabilities

                elif entry_point == '4':
                    entry_point_04() # Get DOI from Pubmed_Id

                elif entry_point == '5':
                    entry_point_05() # Transform DOI (prefix) entry_point5A : exceuted after 3 to strip back the transformed Doi to DOI

                elif entry_point == '6':
                    entry_point_06() # Main scrapper and downloader

                elif entry_point == '7':
                    entry_point_07_manual() #as multiple sources can be used , so remove duplicate downloads

                elif entry_point == '8':
                    entry_point_08_manual() # to get txt files from the pdf file

                elif entry_point == '9':
                    entry_point_09() # Additional Utility

                elif entry_point == '999':
                    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen command

                elif entry_point == '0000' :
                    print("Exiting the Utility.")
                    #break
                    return
                else :
                    print("Invalid Selection")


        except Exception as e:
            print("An error occurred:", e)
            print("\n \n \n")
            continue  # Restart the loop from the beginning


    return


if __name__ == "__main__":
    main()
