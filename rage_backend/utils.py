import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(
    text,
    chunk_size=500,
    chunk_overlap=100
):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_text(text)

    return chunks

def clean_text(text):
    text=text.replace("\n", " ")
    text=text.replace("\t", " ")
    text=re.sub(r'\s+', ' ', text)
    text=re.sub(r'\.{2,}', '.', text)
    text=text.strip()

    return text