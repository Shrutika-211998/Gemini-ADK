"""
Google Search Tool wrapper for Elegance Hair Salon & Spa.
Uses Google Search as a fallback when knowledge base doesn't have the answer.
"""

from google.adk.tools import google_search
from google.adk.tools.tool_context import ToolContext


def search_web(query: str, tool_context: ToolContext = None) -> str:
    """
    Search the web using Google Search for general information.
    
    This tool is used as a fallback when the salon knowledge base doesn't contain
    the answer to a customer's question. It performs a web search for general information.
    
    Args:
        query: The search query.
        tool_context: The invocation context for state management.
    
    Returns:
        A string containing search results or a message if no results found.
    """
    try:
        # Use the built-in google_search tool
        result = google_search(query)
        
        if not result or not str(result).strip():
            return f"Hmm, I couldn't find information about '{query}'. Could you ask something else?"
        
        # Log search in context state
        if tool_context:
            if 'searches' not in tool_context.state:
                tool_context.state['searches'] = []
            tool_context.state['searches'].append({
                'query': query,
                'type': 'web_search'
            })
        
        return str(result)
    
    except Exception as e:
        return f"Hmm, I encountered an issue searching the web. Could you try a different question?"
