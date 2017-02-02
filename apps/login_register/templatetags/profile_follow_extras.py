from django import template
from django.contrib.auth.models import User
register = template.Library()

@register.filter(name='profile_already_follow')
def already_follow(user, follow_user_id):
    print "*"*50
    print "IN FOLLOW EXTRA"
    print "*"*50
    follow_profile_id = User.objects.get(id=follow_user_id).profile.id
    if user.profile.follows.filter(id=follow_profile_id).exists():
        return True
    elif user.profile.id == follow_profile_id:
        return True
    else:
        return False
