def index_vault_handler(vault_data: list) -> str:
    """
    Index a vault

    Args:
        vault_data: (list) Contains the vault name, file names and contents

    Returns:
        None
    """
    vault_name = vault_data[0]

    file_names = []
    file_contents = []

    for n,c in vault_data[1].items():
        file_names.append(n)
        file_contents.append(c)


    # remove special characters
    character_patterns = {
        "bold": r"\*\*(.*?)\*\*|__(.*?)__",  # Removes ** and __ while keeping the text
        "italic": r"\*(.*?)\*|_(.*?)_",  # Removes * and _ while keeping the text
        "inline_code": r"`(.*?)`",  # Removes ` while keeping the inline code text
        "links": r"$begin:math:display$(.*?)$end:math:display$$begin:math:text$.*?$end:math:text$",  # Removes the link notation, keeping the link text only
        "images": r"!$begin:math:display$.*?$end:math:display$$begin:math:text$.*?$end:math:text$",  # Removes the entire image markdown, as it typically doesn't have useful visible text
        "headings": r"^#+\s*(.*?)$",  # Removes the # characters while keeping the heading text
        "blockquotes": r"^>\s*(.*?)$",  # Removes the > character while keeping the quoted text
        "code_blocks": r"```(?:.|\n)*?```",  # Removes fenced code block notation while keeping the code
        "list_items": r"^[-*]\s+",  # Removes list markers (- or *) while keeping the list item text
        "extra_newlines": r"\n{2,}",  # Collapses multiple newlines into one
        "unicode escapes": r"(\\u[0-9a-fA-F]{4})+", 
        "outbound links": r"https?://\S+",
        "image linkes": r"!\[\[.*?\]\]|\!\[.*?\]\(.*?\)"
    }

    for key, value in character_patterns.items():
        file_contents = [re.sub(value, '', file) for file in file_contents]

    # tokenize the corpus and only keep the ids
    stemmer = Stemmer.Stemmer("english")
    corpus_tokens = bm25s.tokenize(file_contents, stopwords="en", stemmer=stemmer)

    # create the BM25 model and index the corpus
    retriever = bm25s.BM25()
    retriever.index(corpus_tokens)

    # save model and file names 
    retriever.save(f"./vault_indexes/{vault_name}_index/", corpus=file_names)

    # return a message
    return f"Vault {vault_name} indexed successfully"