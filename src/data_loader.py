import re

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path



### Read all the pdf inside the directory
def process_all_pdfs(pdf_directory):
    """Process all pdf files in a directory"""
    all_documents=[]
    pdf_dirs=Path(pdf_directory)

    #find allpdf files recursively
    pdf_files=list(pdf_dirs.glob("**/*.pdf"))

    print(f"found {len(pdf_files)} pdf files to be processed")

    for pdf_file in pdf_files:
        print(f"\n Processing:{pdf_file.name}")

        try:
            loader=PyMuPDFLoader(str(pdf_file))
            documents=loader.load()
            #Add source info

            for doc in documents:
                doc.metadata['source_file']=pdf_file.name
                doc.metadata["file_type"]='pdf'

            all_documents.extend(documents)
            print(f" Loaded {len(documents)}pages")
        except Exception as e:
            print(f" Error:{e}")
    print(f"\n total documents loaded:{len(all_documents)}")
    return all_documents

def process_single_pdf(file_path):
    """Load a single uploaded PDF."""

    loader = PyMuPDFLoader(file_path)

    documents = loader.load()

    for doc in documents:
        doc.metadata["source_file"] = file_path.split("/")[-1]
        doc.metadata["file_type"] = "pdf"

    return documents




def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def split_documents(documents,chunk_size=1000,chunk_overlap=200):
    """split documents into smaller chunks"""

    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

    text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap,
       length_function=len,
       separators=["\n\n", "\n", ". ", " ",""] 
       )
    split_docs=text_splitter.split_documents(documents)
    print(f"split{len(documents)} document into {len(split_docs)} chunks")

    if split_docs:
        print(f"example chunk:\n {split_docs[0].page_content[:200]}...")
        print(f"metadata:{split_docs[0].metadata}")
    return split_docs

