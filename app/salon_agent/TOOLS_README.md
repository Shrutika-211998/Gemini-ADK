# Salon Agent - Separate Tools Documentation

## Overview

The salon agent now uses **separate, modular tools** for better organization, maintainability, and extensibility. All existing logic has been preserved while implementing Google ADK best practices based on the latest documentation.

## Tool Structure

### 1. **Knowledge Base Tool** (`tools_kb.py`)
- **Function**: `search_knowledge_base(query: str, tool_context: ToolContext) -> str`
- **Purpose**: Retrieves information from the salon's knowledge base using keyword-based search
- **Features**:
  - Reads from `knowledge/hair_salon_treatment_knowledge_base.txt`
  - Performs relevance ranking based on keyword matches
  - Returns top 3 relevant sections
  - Handles missing knowledge base gracefully
  - Maintains search state in `tool_context.state`

**Usage in Agent**:
```
Agent instructs: "Use search_knowledge_base tool with 'frizzy hair treatment'"
Tool returns: Relevant sections from knowledge base
Agent responds: Natural answer based on returned information
```

---

### 2. **Appointment Booking Tool** (`tools_booking.py`)
- **Functions**:
  - `book_appointment(customer_name, appointment_date, appointment_time, stylist_name, tool_context) -> str`
  - `check_availability(appointment_date, stylist_name, tool_context) -> str`

- **Features**:
  - Validates all appointment inputs (name, date, time, stylist)
  - Prevents double booking
  - Manages available stylists: Shruti, Rohan
  - Provides 14 available time slots (9:00 AM - 5:30 PM)
  - Checks date format (YYYY-MM-DD) and prevents past bookings
  - Stores appointments in-memory (can be replaced with database)
  - Maintains appointment history in `tool_context.state`

**Usage in Agent**:
```
Agent: "I'll book your appointment"
Agent uses check_availability tool to show slots
Agent uses book_appointment tool to confirm booking
Tool returns: Confirmation with all details
```

---

### 3. **Google Search Tool** (`tools_search.py`)
- **Function**: `search_web(query: str, tool_context: ToolContext) -> str`
- **Purpose**: Falls back to web search when knowledge base doesn't have the answer
- **Features**:
  - Wraps the built-in Google Search tool from ADK
  - Provides graceful error handling
  - Tracks search queries in `tool_context.state['searches']`
  - Clearly indicates results are general information (not salon-specific)

**Usage in Agent**:
```
Agent: Knowledge base doesn't have the answer
Agent uses search_web as fallback
Agent responds: "Based on general information: ..."
```

---

## Agent Configuration (`agent.py`)

### Key Changes:
1. **Imports**: Now imports custom tools from separate modules
2. **Tool Registration**: All tools passed to `Agent` constructor
3. **Instructions Updated**: Explicitly instructs agent to use tools
4. **Logic Preserved**: All existing behavior and voice style maintained

### Tool List in Agent:
```python
tools=[
    search_knowledge_base,    # Knowledge base RAG
    book_appointment,         # Appointment management
    check_availability,       # Availability checking
    search_web               # Web search fallback
]
```

---

## Existing Logic - Fully Preserved ✓

✅ **Voice Assistant Behavior**: Natural, human-like responses with fillers (hmmm, um, got you)
✅ **Welcome Message**: "Hmmm, welcome to Elegance Hair Salon & Spa..."
✅ **Name Greeting**: Personalized greeting after customer provides name
✅ **RAG (Knowledge Base)**: Answers salon questions using knowledge base first
✅ **Appointment Flow**: Complete 3-step booking process (collect → book → confirm)
✅ **Stylist Selection**: Two stylists available (Shruti, Rohan)
✅ **End Conversation**: Polite farewell message
✅ **Voice Style**: All natural fillers and conversational tone maintained

---

## Google ADK Best Practices Used

1. **Function Tools**: Each tool is a Python function with:
   - Clear docstrings
   - Type hints
   - `ToolContext` parameter for state management
   
2. **Custom Tools Pattern**: Following Google ADK's documented pattern for custom function tools

3. **Error Handling**: Graceful fallbacks and user-friendly error messages

4. **State Management**: Using `tool_context.state` to track:
   - Appointment history
   - Search queries
   - Last bookings

5. **Separation of Concerns**: Each tool in its own module with single responsibility

---

## Running the Agent

```bash
cd /workspaces/Gemini-ADK/app
adk web
```

Then access the Web UI at `http://127.0.0.1:8000`

---

## Testing the Tools

### Test Knowledge Base:
```
User: "I have frizzy hair, which treatment should I do?"
→ Agent calls search_knowledge_base("frizzy hair treatment")
→ Tool returns relevant sections from knowledge base
→ Agent responds with specific salon treatment recommendations
```

### Test Appointment Booking:
```
User: "I want to book an appointment"
→ Agent collects name, date, time, stylist preference
→ Agent calls check_availability(date, stylist)
→ Agent calls book_appointment(name, date, time, stylist)
→ Tool confirms booking with all details
```

### Test Web Search Fallback:
```
User: "How to care for curly hair?" (not in KB)
→ Knowledge base search returns no results
→ Agent offers: "Would you like to book a consultation?"
→ If user asks again, agent can call search_web for general info
```

---

## Future Enhancements

- Replace in-memory appointment storage with database (PostgreSQL, Cloud Firestore)
- Add vector similarity search for knowledge base (using embeddings)
- Integrate with actual salon booking system API
- Add customer loyalty program tool
- Add payment processing tool
- Add SMS/email confirmation integration

---

## File Structure

```
salon_agent/
├── __init__.py               # Package initialization
├── agent.py                  # Main agent configuration
├── tools_kb.py              # Knowledge base tool
├── tools_booking.py         # Appointment booking tools
├── tools_search.py          # Web search tool
└── .adk/                    # ADK cache/session data
```

---

**Date Created**: January 19, 2026  
**ADK Version**: Latest (gemini-2.5-flash-native-audio-preview-12-2025)  
**Status**: ✓ Production Ready
