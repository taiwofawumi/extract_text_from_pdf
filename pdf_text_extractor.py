import PyPDF2 as pdf
import pandas as pd
import glog as log
import argparse
import tkinter as tk
from tkinter import filedialog
import json
import os

import warnings
warnings.filterwarnings('ignore')

def main():
    log.info("starting main...")

    # get pdf file
    log.info("please select your pdf file...")
    pdf_file, filename = get_pdf_file()

    # parse pdf file
    pdf_reader = pdf.PdfReader(pdf_file)

    # extract text from pdf
    log.info("extracting text from pdf file...")
    pdf_text = extract_text_from_pdf(pdf_reader)

    # export text to csv
    log.info("exporting extracted text to csv...")
    pdf_text.to_csv(f'output/{filename.replace(".","_")}_text.csv', index=False)

def get_pdf_file():
    root = tk.Tk()
    root.withdraw()
    pdf_file = filedialog.askopenfilename()
    log.info(f'pdf file: {pdf_file}')

    if os.path.exists(pdf_file):
        filename = os.path.basename(pdf_file)
        return pdf_file, filename

def extract_text_from_pdf(pdf_reader):
    pdf_text = pd.DataFrame(columns = ['page','text'])
    for i in range(len(pdf_reader.pages)):
        pdf_page_text = pdf_reader.pages[i]
        page_text = pd.DataFrame()
        page_text = pd.DataFrame({"page":[i+1], "text":[pdf_page_text.extract_text()]})
        pdf_text = pd.concat([pdf_text, page_text], ignore_index=True)
    
    return pdf_text

if __name__ == "__main__":
    main()
