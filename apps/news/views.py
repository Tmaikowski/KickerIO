from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
import json

from .forms import SummaryArticles
from .models import Article, Category, Like
from ..login_register .models import User

from NLTK.getlinks import *

# Create your views here.
def index(request):
    print "*"*50
    print request.user.id
    print "*"*50
    form = SummaryArticles()
    profile = User.objects.get(id=request.user.id)
    context = {
        'profile': profile,
        'SummaryForm': form
    }
    return render(request, 'news/index.html', context)

def get_new_articles(request):
    if request.method == "POST":
        bound_form = SummaryArticles(request.POST)
        search_term = bound_form['search_term'].value()
        summary_dict = get_summarized_text(search_term)
        context = {
            'summary_dict': summary_dict
        }
        request.session['user_articles'] = summary_dict
    return redirect(reverse("news:index"))

def share(request, id):
    if request.method == "POST":
        shared = request.session['user_articles'][str(id)]
        user = User.objects.get(id=request.user.id)
        article = Article(
            title=shared['title'],
            summarized_text=" ".join(shared['summary_sentences']),
            url=shared['meta']['url'],
            published_on=shared['meta']['published_on'],
            main_image=shared['meta']['main_image'],
            creator_id=request.user.id
        )
        article.save()
        article.users.add(user)
        categories = " ".join(shared['meta']['site_categories'])
        category = Category(name=categories)
        category.save()
        category.articles.add(article)
    return redirect(reverse("news:newsreel"))

def newsreel(request):
    user_profile = User.objects.get(id=request.user.id).profile
    #get the user_id of everyone the logged in user is following
    network_ids = [am_following.user_id for am_following in user_profile.follows.all()]
    articles = Article.objects.filter(Q(creator__in=network_ids) | Q(creator=request.user.id))
    context = {
        'articles': articles
    }
    return render(request, 'news/newsreel.html', context)

def like_article(request, id):
    #NEED to validate that like doesn't already exist in the DB
    user = User.objects.get(id=request.user.id)
    article = Article.objects.get(id=id)
    like = Like.objects.create(
        user=user,
        article=article
    )
    article_likes = article.like_set.count()
    # return redirect(reverse("news:newsreel"))
    return HttpResponse(
        json.dumps(article_likes),
        content_type="application/json"
    )

def unlike(request, id):
    user = User.objects.get(id=request.user.id)
    article = Article.objects.get(id=id)
    like_obj = Like.objects.get(
        Q(user=user),
        Q(article=article)
    )
    like_obj.delete()
    article_likes = article.like_set.count()
    # return redirect(reverse("news:newsreel"))
    return HttpResponse(
        json.dumps(article_likes),
        content_type="application/json"
    )
