from django import template

register = template.Library()

@register.filter(name='already_liked')
def already_liked(article, user_id):
    u_id = int(user_id)
    if article.like_set.filter(user_id=u_id).exists():
        return True
    else:
        return False
