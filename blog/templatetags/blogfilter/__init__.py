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
投稿画面での、[filter name]text[end]という特殊な構文を評価するためのフィルター
blogアプリケーションでは、linebreaksbrでの自動改行と、blogフィルターでの特殊構文評価を使っています。
linebreaksbrは便利ですが、自動生成された<br />タグが一部の処理で邪魔になっています。

[filter img]
http://...
[end]

linebreaksによって、以下のようになります。

[filter img]<br>
http://...<br>
[end]<br>

[filter img]を正しくimgタグにするには、[filter img]内の<br>を消す必要があります。
同様に、[filter imgpk]や[filter url]も<br />が消されます。

[filter html]や[filter code]などは、<br />を\nにすることで、元々のhtmlやプログラミングコードの形を保っています。

[filter h2]や[filter h3]、[filter quote]など、内部に<br />があってもおかしくない場合は、<br />をそのままにしています。
"""
import re

from django import template
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import mark_safe, SafeData
from . import functions

register = template.Library()


@register.filter(is_safe=True, needs_autoescape=True)
def blog(value, autoescape=True):
    """本文中の[filter name]text[end]を、適切なHTMLタグに変換する.

    直前にlinebreaksbrを使ってください。(linebreaksbrで生成された<br />を利用するため)
    url、html、img といった別の関数へ処理を渡します。
    まず[filter name]text[end]が本文にあるかをチェックし
    あれば、別関数にそれらを渡して結果テキストの取得、
    その後、元の[filter name]text[end]を結果テキスト(html)に置き換えます。
    """
    # functionsモジュールの属性をリセット...上手いやり方を探している
    functions.h2_count = 0
    functions.h3_count = 0

    # html等は、一度エスケープ処理する
    autoescape = autoescape and not isinstance(value, SafeData)
    if autoescape:
        value = escape(value)

    # [filter name]text[end]を探す
    filters = re.finditer(r'\[filter (?P<tag_name>.*?)\].*?\[end\]', value, flags=re.DOTALL)

    for f in filters:
        filter_name = f.group('tag_name')  # name部分、urlやimg等の関数名が入る
        origin_text = f.group()  # 元のtext部分
        # [filter name]のnameに対応する関数を呼び出し、結果テキストの取得
        result_text = functions.convert(filter_name, origin_text)
        if result_text:
            value = value.replace(origin_text, result_text, 1)

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
