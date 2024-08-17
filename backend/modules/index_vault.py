import re
import os
from typing import List, Dict
from Stemmer import Stemmer
import bm25s

def index_vault_handler(vault_data: List) -> str:
    """
    Index a vault

    Args:
        vault_data (List): Contains the vault name and a dict of file names and contents
                           [vault_name, {file_name: file_content, ...}]

    Returns:
        str: A message indicating the vault has been indexed
    """
    try:
        vault_name = vault_data[0]
        files_dict = vault_data[1]

        file_names = list(files_dict.keys())
        file_contents = list(files_dict.values())

        print(f"Starting indexing for vault: {vault_name}")
        print(f"Total files to process: {len(file_names)}")

        # Character patterns to remove
        character_patterns = {
            "bold": r"\*\*(.*?)\*\*|__(.*?)__",
            "italic": r"\*(.*?)\*|_(.*?)_",
            "inline_code": r"`(.*?)`",
            "links": r"\[\[(.*?)\]\]|\[([^\]]+)\]\(([^\)]+)\)",
            "images": r"!\[\[.*?\]\]|!\[.*?\]\(.*?\)",
            "headings": r"^#+\s*(.*?)$",
            "blockquotes": r"^>\s*(.*?)$",
            "code_blocks": r"```(?:.|\n)*?```",
            "list_items": r"^[-*]\s+",
            "extra_newlines": r"\n{2,}",
            "unicode_escapes": r"(\\u[0-9a-fA-F]{4})+",
            "outbound_links": r"https?://\S+",
        }

        # Clean file contents
        print("Cleaning file contents...")
        for i, (pattern, regex) in enumerate(character_patterns.items()):
            file_contents = [re.sub(regex, '', content, flags=re.MULTILINE) for content in file_contents]
            print(f"Cleaned pattern {i+1}/{len(character_patterns)}: {pattern}")

        # Tokenize the corpus
        print("Tokenizing corpus...")
        stemmer = Stemmer("english")
        corpus_tokens = bm25s.tokenize(file_contents, stopwords="en", stemmer=stemmer)
        print("Tokenization complete")

        # Create and index the BM25 model
        print("Creating and indexing BM25 model...")
        retriever = bm25s.BM25()
        retriever.index(corpus_tokens)
        print("BM25 model created and indexed")

        # Ensure the directory exists
        save_dir = f"./vault_indexes/{vault_name}_index/"
        os.makedirs(save_dir, exist_ok=True)

        # Save model and file names
        print(f"Saving model and file names to {save_dir}")
        retriever.save(save_dir, corpus=file_names)
        print("Model and file names saved")

        return f"Vault {vault_name} indexed successfully"

    except Exception as e:
        print(f"Error occurred during indexing: {str(e)}")
        return f"Error indexing vault: {str(e)}"