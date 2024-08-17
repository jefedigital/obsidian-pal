from typing import List, Dict
from Stemmer import Stemmer
import bm25s
import os

def search_vault_handler(query_data: List) -> List[Dict[str, float]]:
    """
    Search the vault for the query and return the results

    Args:
        query_data (List): Contains the vault name and the search query
                            [vault_name, query]

    Returns:
        List[Dict[str, float]]: A list of dictionaries containing file names and their scores
    """
    try:
        vault_name, query = query_data

        # tokenize query
        stemmer = Stemmer("english")
        query_tokens = bm25s.tokenize(query, stemmer=stemmer)
        
        # load the model
        save_dir = f"./vault_indexes/{vault_name}_index/"
        retriever = bm25s.BM25.load(save_dir, load_corpus=True)

        # retrieve results
        results, scores = retriever.retrieve(query_tokens, k=10)  # Return top 10 results

        # format results
        formatted_results = [{"file": file, "score": round(float(score), 2)} for file, score in zip((result['text'] for result in results[0]), scores[0])]

        return formatted_results

    except Exception as e:
        print(f"Error occurred during search: {str(e)}")
        return []