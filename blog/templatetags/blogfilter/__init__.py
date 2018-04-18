"""blogアプリで主に使用するフィルタ・タグ

by_the_timeタグ
人に優しい表現で、文字列を返す(n時間前)
<span class="badge badge-danger badge-pill">{% by_the_time recomment.created_at %}</span>
のようにして使います。


url_replaceタグ
キーワード検索をした際等の、他GETパラメータと?page=のページングを両立させる場合に使います。
<a href="?{% url_replace request 'page' page_obj.previous_page_number %}" aria-label="Previous">
のようにして使います。


blogフィルター
{{ post.text | linebreaksbr | blog }}
のようにして使います。
投稿画面での、[filter name]text[end]等の特殊な構文を評価するためのフィルター
"""
from django import template
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import mark_safe, SafeData
from . import filters

register = template.Library()


@register.filter(is_safe=True, needs_autoescape=True)
def blog(value, autoescape=True):
    """本文中の[filter name]text[end]を、適切なHTMLタグに変換する."""
    # html等は、一度エスケープ処理する
    autoescape = autoescape and not isinstance(value, SafeData)
    if autoescape:
        value = escape(value)

    value = filters.DefaultConverter(value).run()
    return mark_safe(value)


@register.simple_tag
def url_replace(request, field, value):
    """GETパラメータの一部を置き換える."""
    url_dict = request.GET.copy()
    url_dict[field] = value
    return url_dict.urlencode()


@register.simple_tag
def by_the_time(dt):
    """その時間が今からどのぐらい前か、人にやさしい表現で返す."""
    result = timezone.now() - dt
    s = result.total_seconds()
    hours = int(s / 3600)
    if hours >= 24:
        day = int(hours / 24)
        return '約{0}日前'.format(day)
    elif hours == 0:
        minute = int(s / 60)
        return '約{0}分前'.format(minute)
    else:
        return '約{0}時間前'.format(hours)
