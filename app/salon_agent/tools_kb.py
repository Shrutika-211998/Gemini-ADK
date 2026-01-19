"""
Knowledge Base Tool for Elegance Hair Salon & Spa.
Performs RAG (Retrieval-Augmented Generation) on the salon's knowledge base.
"""

from pathlib import Path
from google.adk.tools.tool_context import ToolContext


def search_knowledge_base(query: str, tool_context: ToolContext) -> str:
    """
    Search the salon knowledge base for answers to customer questions.
    
    This tool searches the knowledge base for hair treatments, services, pricing,
    and salon-related information. It performs a simple text-based search.
    
    Args:
        query: The customer's question or search query about salon services.
        tool_context: The invocation context for state management.
    
    Returns:
        A string containing relevant information from the knowledge base,
        or a message indicating no relevant information was found.
    """
    # Load knowledge base
    kb_path = Path(__file__).parent.parent / "knowledge" / "hair_salon_treatment_knowledge_base.txt"
    
    if not kb_path.exists():
        return "Hmm, the knowledge base is not available right now. Please try again later."
    
    kb_content = kb_path.read_text(encoding="utf-8")
    
    # Simple keyword-based search (can be enhanced with vector similarity)
    query_lower = query.lower()
    keywords = query_lower.split()
    
    # Split KB into sections and find relevant sections
    sections = kb_content.split("\n\n")
    relevant_sections = []
    
    for section in sections:
        section_lower = section.lower()
        # Count keyword matches
        matches = sum(1 for keyword in keywords if keyword in section_lower and len(keyword) > 3)
        if matches > 0:
            relevant_sections.append((section, matches))
    
    if not relevant_sections:
        return (
            "Hmm, I don't see this information specific to our salon. "
            "Would you like to book a consultation instead?"
        )
    
    # Sort by relevance and return top results
    relevant_sections.sort(key=lambda x: x[1], reverse=True)
    result = "\n\n".join([section for section, _ in relevant_sections[:3]])
    
    # Limit response length
    if len(result) > 1500:
        result = result[:1500] + "..."
    
    return result
