import unirest

def get_title_and_text(search_term):

    """Search news articles using the WebHose API
    and return the title and text for the first 5
    articles in a dictionary"""

    # IDEA: Add functionality to select different languages (change language=<language> in url below)
    url = "http://webhose.io/search?token=dcbf45ff-7b2f-4011-af9c-e8a1b2b1bcd0&format=json&sort=relevancy&language=english&q="
    url += search_term
    response = unirest.get(
        url,
        headers={
            "Accept": "text/plain"
        }
    )
    article_dict = {}

    count = 0
    for article in response.body['posts'][:5]:
        article_dict[count] = {
            "title": article['title'],
            "body": article['text'],
            "metadata": {
                "url": article['thread']['url'],
                "main_image": article['thread']['main_image'],
                "site_categories": article['thread']['site_categories'],
                "published_on": article['thread']['published']
            }
        }
        count += 1

    return article_dict
