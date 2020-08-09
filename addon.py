import os
import dialogflow_v2 as dialogflow

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client.json"
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "vhugbot-gnvu"



def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result


def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)
    return "small_talk", response.fulfillment_text
topics_keyboard = [
    ['Menstrual_Cup', 'Biodegradable_pads'],
    ['Reusable_pads', 'Regular_pads'],
    ['Tampons', 'Period_pants']
]