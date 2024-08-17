def hello_world_handler(content: str) -> str:
    """
    Handle the hello_world action.
    
    Args:
        content (str): The content from the request.
    
    Returns:
        str: The result of the hello_world action.
    """
    return f"Hello World! You said: {content}"