"""
Appointment Booking Tool for Elegance Hair Salon & Spa.
Handles appointment booking and management.
"""

from datetime import datetime, timedelta
from google.adk.tools.tool_context import ToolContext


# In-memory appointment storage (in production, use a database)
APPOINTMENTS = []
AVAILABLE_STYLISTS = ["Shruti", "Rohan", "Aasha"]
AVAILABLE_TIME_SLOTS = [
    "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM",
    "2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM"
]


def book_appointment(
    customer_name: str,
    appointment_date: str,
    appointment_time: str,
    stylist_name: str = None,
    tool_context: ToolContext = None
) -> str:
    """
    Book an appointment for a customer at the salon.
    
    Args:
        customer_name: The customer's full name.
        appointment_date: The appointment date (e.g., "2025-01-25").
        appointment_time: The appointment time (e.g., "10:00 AM").
        stylist_name: Optional stylist preference (Shruti, Rohan, or Aasha).
        tool_context: The invocation context for state management.
    
    Returns:
        A confirmation string with appointment details, or an error message.
    """
    # Validate inputs
    if not customer_name or not appointment_date or not appointment_time:
        return "Hmm, I need your name, appointment date, and time to book. Could you please provide that?"
    
    # Normalize stylist name (case-insensitive matching)
    if stylist_name:
        # Find matching stylist (case-insensitive)
        matched_stylist = None
        for stylist in AVAILABLE_STYLISTS:
            if stylist.lower() == stylist_name.lower():
                matched_stylist = stylist
                break
        
        if not matched_stylist:
            return f"Hmm, {stylist_name} is not available. Available stylists are: {', '.join(AVAILABLE_STYLISTS)}."
        
        stylist_name = matched_stylist  # Use the properly cased name
    
    # Validate date
    try:
        appt_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        if appt_date < datetime.now().date():
            return f"Hmm, {appointment_date} is in the past. Could you please choose a future date?"
    except ValueError:
        return f"Hmm, I couldn't understand the date '{appointment_date}'. Please use the format YYYY-MM-DD."
    
    # Validate time
    if appointment_time not in AVAILABLE_TIME_SLOTS:
        available = ", ".join(AVAILABLE_TIME_SLOTS[:7])
        return f"Hmm, {appointment_time} is not available. Available times are: {available}, etc."
    
    # Check for double booking
    for appt in APPOINTMENTS:
        if (appt["date"] == appointment_date and 
            appt["time"] == appointment_time and 
            (not stylist_name or appt.get("stylist") == stylist_name)):
            return f"Hmm, {appointment_time} on {appointment_date} with {stylist_name or 'any stylist'} is already booked. Please choose another time."
    
    # Create appointment
    appointment = {
        "customer_name": customer_name,
        "date": appointment_date,
        "time": appointment_time,
        "stylist": stylist_name or "No preference"
    }
    APPOINTMENTS.append(appointment)
    
    # Store in context state for future reference
    if tool_context:
        tool_context.state['last_appointment'] = appointment
    
    return (
        f"Great! I've booked your appointment at Elegance Hair Salon & Spa.\n"
        f"Name: {customer_name}\n"
        f"Date: {appointment_date}\n"
        f"Time: {appointment_time}\n"
        f"Stylist: {appointment['stylist']}\n"
        f"Is there anything else I can help you with?"
    )


def check_availability(
    appointment_date: str,
    stylist_name: str = None,
    tool_context: ToolContext = None
) -> str:
    """
    Check available time slots for a given date and optional stylist.
    
    Args:
        appointment_date: The date to check (e.g., "2025-01-25").
        stylist_name: Optional stylist to check availability for.
        tool_context: The invocation context for state management.
    
    Returns:
        A string listing available time slots.
    """
    try:
        appt_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        if appt_date < datetime.now().date():
            return f"Hmm, {appointment_date} is in the past. Please choose a future date."
    except ValueError:
        return f"Hmm, I couldn't understand the date '{appointment_date}'."
    
    # Get booked times for this date
    booked_times = [
        appt["time"] for appt in APPOINTMENTS
        if appt["date"] == appointment_date and
        (not stylist_name or appt.get("stylist") == stylist_name)
    ]
    
    # Get available times
    available = [t for t in AVAILABLE_TIME_SLOTS if t not in booked_times]
    
    if not available:
        return f"Hmm, no time slots are available on {appointment_date}. Would you like to try another date?"
    
    stylist_info = f" with {stylist_name}" if stylist_name else ""
    return f"Available time slots{stylist_info} on {appointment_date}: {', '.join(available)}"
