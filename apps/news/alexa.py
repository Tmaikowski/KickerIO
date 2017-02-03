from django_alexa.api import fields, intent, ResponseBuilder
from NLTK.getlinks import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from models import *
#ISSUE: Alexa times out while calling the API. Need to rewrite for only 1 result or find
#another way to get news data
print "-"*50
print "-"*50
print Article.objects.all().annotate(num_likes=Count('like')).order_by("-num_likes")[:1][0].title
print "-"*50
print "-"*50
#./ ngrok http 8000
#python manage.py runserver

#had to manually add the app ideas to environment variables in the settings.py file
#ISSUE: turned off csrf verification in settings.py. Figure this out to turn back on

# IDEA: Populate the SEARCHES list with each users' top search terms/most frequently searched terms
SEARCHES = ("soccer", "computers", "trump", "google", "taco bell")
print SEARCHES

#Alexa Config
ALEXA_APP_ID_DEFAULT="amzn1.ask.skill.f4e917c3-fc1b-45ea-a7f1-4ad4db881cff"
# ALEXA_APP_ID_OTHER="amzn1.ask.skill.f4e917c3-fc1b-45ea-a7f1-4ad4db881cff"
ALEXA_REQUEST_VERIFICATON=True # Enables/Disable request verification

@intent
def LaunchRequest(session):
    """
    Starting the news app
    ---
    launch
    start
    run
    begin
    open
    """

    print "LAUNCHREQUEST"
    return ResponseBuilder.create_response(message="Welcome to Kicker... ... ...What can I help you with?",
                                        #    reprompt="What can I help you with?",
                                           end_session=False,
                                           launched=True)

@intent
def HelpIntent(session):
    msg = """Kicker is a social web application for breaking news based on your interests... ... ... ...
             You can ask me to search for a news story or read some of your top stories that you have shared with your network... ...
             ... ... ...What would you like to do?"""
    return ResponseBuilder.create_response(message=msg,
                                           end_session=False)

class SearchTerm(fields.AmazonSlots):
    print "IN THE CLASS"
    search_term = fields.AmazonCustom(label="SEARCHES_LIST", choices=SEARCHES)

@intent(slots=SearchTerm)
def ReadTopStory(session, search_term):
    """
    Get the top news story
    ---
    {search_term}
    search {search_term}
    tell me about {search_term}
    """

    top_story = get_summarized_text(search_term)[0]
    story_title = top_story['title']
    sentences = " ".join(top_story['summary_sentences']).encode('ascii', errors='ignore')

    kwargs = {}
    # kwargs['message'] = "{0} points added to house {1}.".format(points, house)

    kwargs['message'] = "{}... ... ...{}.".format(story_title.encode(), sentences)
    if session.get('launched'):
        kwargs['reprompt'] = "What would you like me to search?"
        kwargs['end_session'] = False
        kwargs['launched'] = session['launched']
    return ResponseBuilder.create_response(**kwargs)

@intent
def CancelIntent(session):
    return ResponseBuilder.create_response(message="You canceled. Thanks!",
                                           end_session=True)

@intent
def StopIntent(session):
    return ResponseBuilder.create_response(message="Ok ... ... See you later",
                                           end_session=True)
