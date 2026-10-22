import json

from pathlib import Path
from src.config.env import env_variables
from tavily import TavilyClient
from typing import Final


MEMORY_FILE: Final[Path] = Path(env_variables.memory_path)
ENCODING = "utf-8"


def load_memory() -> dict:
    """
    Loads the agent's memory from a JSON file.

    Returns:
        dict: The memory data, or an empty dictionary if the file doesn't exist or is
        invalid.
    """

    if not MEMORY_FILE.exists():
        return {}

    try:
        return json.loads(MEMORY_FILE.read_text(encoding=ENCODING))
    except json.JSONDecodeError:
        return {}


def save_memory(memory: dict) -> None:
    """
    Persists the agent's memory dictionary to the designated JSON file.

    Args:
        memory (dict): The memory data to save.
    """

    data = json.dumps(memory, ensure_ascii=False, indent=2)
    MEMORY_FILE.write_text(data, encoding=ENCODING)


def remember(user_id: str, key: str, value: str) -> str:
    """
    Saves a specific key-value pair for a user in the agent's memory.

    Args:
        user_id (str): The unique identifier of the user.
        key (str): The key under which the information should be stored.
        value (str): The information to remember.

    Returns:
        str: A confirmation message.
    """

    memory = load_memory()
    memory.setdefault(user_id, {})[key] = value
    save_memory(memory)

    return f"Memory saved: {key}."


def recall(user_id: str, key: str) -> str:
    """
    Retrieves information associated with a specific key for a user.

    Args:
        user_id (str): The unique identifier of the user.
        key (str): The key to look up in memory.

    Returns:
        str: The stored value or a message indicating no information was found.
    """

    value = load_memory().get(user_id, {}).get(key)

    return value if value is not None else "No information saved for this key."


def web_search(query: str, max_results: int = 5) -> str:
    """
    Performs a web search using the Tavily API and returns formatted results.

    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to return (default 5).

    Returns:
        str: A formatted string containing titles, URLs, and summaries of the results.
    """

    api_key = env_variables.tavily_api_key
    if not api_key:
        return "Web search unavailable: TAVILY_API_KEY is missing."

    response = TavilyClient(api_key=api_key).search(
        query=query,
        search_depth="basic",
        max_results=max_results,
    )
    results = response.get("results", [])

    if not results:
        return "No web results found."

    return "\n\n".join(
        f"\tTitle: {result.get('title', 'Untitled')}\n"
        f"\tURL: {result.get('url', '')}\n"
        f"\tSummary: {result.get('content', '')}"
        for result in results
    )


def run_tool(name: str, arguments: dict, user_id: str) -> str:
    """
    Dispatches and executes a tool by name with the provided arguments and user context.

    Args:
        name (str): The name of the tool to execute.
        arguments (dict): The arguments to pass to the tool.
        user_id (str): The unique identifier of the user.

    Returns:
        str: The result of the tool execution.
    """

    match name:
        case "remember":
            return remember(user_id=user_id, **arguments)
        case "recall":
            return recall(user_id=user_id, **arguments)
        case "web_search":
            return web_search(**arguments)
        case _:
            return f"Unknown tool name {name}"
