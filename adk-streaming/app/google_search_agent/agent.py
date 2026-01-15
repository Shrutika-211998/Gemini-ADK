import os
import uuid
import logging
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.cloud import dialogflowcx_v3 as dialogflow
from google.api_core.exceptions import GoogleAPIError
from dotenv import load_dotenv

# --------------------------------------------------
# Load environment variables (IMPORTANT for ADK CLI)
# --------------------------------------------------
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------------------------------------
# Dialogflow CX Client Wrapper
# --------------------------------------------------
class DialogflowCXTool:
    def __init__(self):
        self.project_id = os.getenv("DIALOGFLOW_PROJECT_ID")
        self.location = os.getenv("DIALOGFLOW_LOCATION", "global")
        self.agent_id = os.getenv("DIALOGFLOW_AGENT_ID")
        self.language_code = os.getenv("DIALOGFLOW_LANGUAGE", "en")

        self.session_client = dialogflow.SessionsClient(
            client_options={
                "api_endpoint": f"{self.location}-dialogflow.googleapis.com"
            }
        )

        self.session_path_template = (
            f"projects/{self.project_id}/locations/{self.location}"
            f"/agents/{self.agent_id}/sessions/{{session_id}}"
        )

        logger.info("✅ Dialogflow CX client initialized")

    def detect_intent(self, text: str, session_id: str) -> str:
        try:
            session_path = self.session_path_template.format(
                session_id=session_id
            )

            query_input = dialogflow.QueryInput(
                text=dialogflow.TextInput(text=text),
                language_code=self.language_code,
            )

            request = dialogflow.DetectIntentRequest(
                session=session_path,
                query_input=query_input,
            )

            response = self.session_client.detect_intent(request=request)
            result = response.query_result

            responses = []
            for msg in result.response_messages:
                if msg.text:
                    responses.extend(msg.text.text)

            return " ".join(responses) if responses else "Sorry, I didn’t understand."

        except GoogleAPIError as e:
            logger.error(f"Dialogflow CX error: {e}")
            return "There was a system error. Please try again."

# --------------------------------------------------
# Global instances (IMPORTANT)
# --------------------------------------------------
cx_tool = DialogflowCXTool()
SESSION_ID = None  # ADK-safe session handling

# --------------------------------------------------
# ADK Tool Function (SINGLE PARAM, SINGLE RETURN)
# --------------------------------------------------
def query_dialogflow_cx(user_message: str) -> str:
    """
    ADK-compatible tool:
    - ONE input parameter
    - Returns ONLY string
    """
    global SESSION_ID

    if SESSION_ID is None:
        SESSION_ID = str(uuid.uuid4())

    return cx_tool.detect_intent(
        text=user_message,
        session_id=SESSION_ID
    )

# --------------------------------------------------
# Root ADK Agent
# --------------------------------------------------
root_agent = Agent(
    name="dialogflow_cx_voice_agent",
    model="gemini-2.5-flash-native-audio-preview-12-2025",
    instruction="""
You are a voice assistant powered by Dialogflow CX.

STRICT RULES:
- ALWAYS call the tool query_dialogflow_cx
- Pass ONLY the user's spoken text
- Do NOT invent parameters
- Do NOT retry tool calls
- Do NOT answer on your own
""",
    tools=[
        FunctionTool(query_dialogflow_cx)
    ],
)
