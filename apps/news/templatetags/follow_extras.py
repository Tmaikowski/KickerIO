from django import template
from django.contrib.auth.models import User
register = template.Library()

@register.filter(name='already_follow')
def already_follow(user, follow_user_id):
    print "HERE"
    print "HERE*************************"
    print "MADE A CHANGE!!!!!!"
    follow_profile_id = User.objects.get(id=follow_user_id).profile.id
    print "*"*50
    print "Follow_Profile: {}".format(follow_profile_id)
    print "*"*50
    if user.profile.follows.filter(id=follow_profile_id).exists():
        print "*"*50
        print "FOLLOWING"
        print "*"*50
        return True
    elif user.profile.id == follow_profile_id:
        print "-"*50
        print "THIS IS YOU"
        print "-"*50
        return True
    else:
        print "*"*50
        print "NOT FOLLOWING"
        print "*"*50
        return False
