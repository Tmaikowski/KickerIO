from summarizer import *
from getarticles import *

fs = FrequencySummarizer()

def get_summarized_text(search_term):
    summary_dict = {}
    for key, val in get_title_and_text(search_term).iteritems():
        summary_dict[key] = {
            "title": val['title'],
            "summary_sentences": [x for x in fs.summarize(val['body'], 2)],
            "meta": {
                "url": val['metadata']['url'],
                "main_image": val['metadata']['main_image'],
                "site_categories": val['metadata']['site_categories'],
                "published_on": val['metadata']['published_on']
            }
        }
    return summary_dict
