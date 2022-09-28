import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client1.json"

from google.cloud import dialogflow_v2beta1 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "newsbot-vxss"

from gnewsclient import gnewsclient
client = gnewsclient.NewsClient()


# ###################

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result



# response = detect_intent_from_text("show me sports news from india in hindi", 12345)
# print(response)
# print(response.intent)
# print(dict(response.parameters))

#  Create a function to reply/ respond a particular query
def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)

    if response.intent.display_name == 'get_news' :
        return 'get_news', dict(response.parameters)

    else:
        return 'small_talk', response.fulfillment_text

#  News fetching using gnewsclient api

def fetch_news(parameters):
    client.language = parameters.get('language')
    client.location = parameters.get('geo-country')
    client.topic = parameters.get('topic')
    if client.language == "" :
        client.language = 'English'
    if client.location =="":
        client.location = 'India'
    if client.topic == "" or client.topic.lower() == "news":
        client.topic = 'Sports'
    return client.get_news()[:5]


topics_keyboard = [
    ['Top Stories', 'World', 'Nation'],
    ['Business', 'Technology', 'Entertainment'],
    ['Sports', 'Science', 'Health']
]





