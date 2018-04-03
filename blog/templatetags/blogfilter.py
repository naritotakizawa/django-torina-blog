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

import html
import html.parser
import re

from django import template
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import mark_safe, SafeData
from blog.models import Image

register = template.Library()
html_parser = html.parser.HTMLParser()
SPLIT_CHAR = html.escape('<split>')


def url(text, index):
    """[filter url]href[end]を、aタグして解釈する."""
    text = text.replace('<br />', '')
    text = text.replace('[filter url]', '').replace('[end]', '')
    if SPLIT_CHAR in text:
        url, text = text.split(SPLIT_CHAR)
        tag = '<a href="{0}" target="_blank" rel="nofollow">{1}</a>'.format(
            url, text)
    else:
        url = text
        tag = '<a href="{0}" target="_blank" rel="nofollow">{0}</a>'.format(url)
    return tag


def html(text, index):
    """[filter html]your_html[end]を、そのままHTMLとして解釈する."""
    text = text.replace('<br />', '\n')
    text = text.replace('[filter html]', '').replace('[end]', '')
    tag = html_parser.unescape(text)
    return tag


def img(text, index):
    """[filter img]src[end]を、正しいimgタグにする

    Bootstrap4に合わせたimgタグです、img-fluidを使います。
    """
    text = text.replace('<br />', '')
    text = text.replace('[filter img]', '').replace('[end]', '')
    if SPLIT_CHAR in text:
        src, alt = text.split(SPLIT_CHAR)
        tag = (
            '<a href="{0}" target="_blank" rel="nofollow"><img src="{0}" '
            'class="img-fluid" alt="{1}"></a>'
        ).format(src, alt)
    else:
        tag = (
            '<a href="{0}" target="_blank" rel="nofollow"><img src="{0}" '
            'class="img-fluid"/></a>'
        ).format(text)
    return tag


def imgpk(text, index):
    """[filter imgpk]1[end]を、正しいimgタグにする

    1の部分は、Imageモデルインスタンスのpkとなります。それ以外はimg関数と同様です。
    """
    text = text.replace('<br />', '')
    text = text.replace('[filter imgpk]', '').replace('[end]', '')
    if SPLIT_CHAR in text:
        pk, alt = text.split(SPLIT_CHAR)
    else:
        pk, alt = text, ''

    try:
        src = Image.objects.get(pk=int(pk)).src.url
    except Exception:
        tag = '<img src="">'
    else:
        tag = (
            '<a href="{0}" target="_blank" rel="nofollow"><img src="{0}" '
            'class="img-fluid" alt="{1}"></a>'
        ).format(src, alt)
    return tag


def code(text, index):
    """[filter code]コード[end]を<pre>コード</pre>に置き換える.

    google-code-prettyfyに合わせたタグです
    """
    text = text.replace('<br />', '\n')
    text = text.replace('[filter code]', '').replace('[end]', '')
    tag = '<pre class="prettyprint linenums">{}</pre>'.format(text)
    return tag


def quote(text, index):
    """[filter quote]文字[end]を<blockquote>文字</blockquote>に置き換える.

    Bootstrap4用の<blockquote>に置き換えます。
    """
    text = text.replace('[filter quote]', '').replace('[end]', '')
    if SPLIT_CHAR in text:
        p_text, footer_text = text.split(SPLIT_CHAR)
        footer_tag = '<footer class="blockquote-footer">{0}</footer>'.format(footer_text)
        tag = '<blockquote class="blockquote"><p class="mb-0">{}</p>{}</blockquote>'.format(p_text, footer_tag)
    else:
        p_text = text
        tag = '<blockquote class="blockquote"><p class="mb-0">{}</p></blockquote>'.format(p_text)
    return tag


def h2(text, index):
    """[filter h2]文字[end]を<h2 class="blog-h2">文字</h2>に置き換える."""
    text = text.replace('[filter h2]', '').replace('[end]', '')
    tag = '<h2 class="blog-h2" id="{}">{}</h2>'.format(index, text)
    return tag


def h3(text, index):
    """[filter h3]文字[end]を<h3 class="blog-h3">文字</h3>に置き換える."""
    text = text.replace('[filter h3]', '').replace('[end]', '')
    tag = '<h3 class="blog-h3" id="{}">{}</h3>'.format(index, text)
    return tag


@register.filter(is_safe=True, needs_autoescape=True)
def blog(value, autoescape=True):
    """本文中の[filter name]text[end]を、適切なHTMLタグに変換する.

    直前にlinebreaksbrを使ってください。(linebreaksbrで生成された<br />を利用するため)
    url、html、img といった別の関数へ処理を渡します。
    ここで行うのは、[filter name]text[end]が本文にあるかをチェックし
    あれば、別関数にそれらを渡して結果テキストの取得、
    その後、元の[filter name]text[end]を結果テキスト(html)に置き換えます。
    """
    autoescape = autoescape and not isinstance(value, SafeData)
    if autoescape:
        value = escape(value)
    # [filter name]text[end]を探す
    filters = re.finditer(r'\[filter (?P<tag_name>.*?)\].*?\[end\]', value)
    results = []
    # iは、何個目の[filter..]か。h2、h3等で目次を作るのに使う。
    for i, f in enumerate(filters, 1):
        filter_name = f.group('tag_name')  # name部分、urlやimg等の関数名が入る
        origin_text = f.group()  # text部分
        # 関数の取得と、呼び出し
        filter_function = globals().get(filter_name)
        if filter_function and callable(filter_function):
            result_text = filter_function(origin_text, i)
        else:
            result_text = origin_text
        results.append((origin_text, result_text))

    # 元の[filter..]を、結果htmlと置き換えていく
    for origin_text, result_text in results:
        if origin_text != result_text:
            value = value.replace(origin_text, result_text)

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
