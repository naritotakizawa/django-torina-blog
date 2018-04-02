"""blogアプリで主に使用するフィルタ."""
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


def url(text):
    """[filter url]http://...[end]を、aタグして解釈する.

    >>> url('[filter url]https://torina.top[end]')
    '<a target="_blank" rel="nofollow" href="https://torina.top" \
    rel="nofollow">https://torina.top</a>'

    """
    text = text.replace('<br />', '\n')
    text = text.replace('[filter url]', '').replace('[end]', '')
    if SPLIT_CHAR in text:
        url, text = text.split(SPLIT_CHAR)
        tag = '<a href="{0}" target="_blank" rel="nofollow">{1}</a>'.format(
            url, text)
    else:
        url = text
        tag = '<a href="{0}" target="_blank" rel="nofollow">{0}</a>'.format(url)
    return tag


def html(text):
    """[filter html]your_html[end]を、そのままHTMLとして解釈する.

    >>> html('[filter html]&lt;h1&gt;ヘロー&lt;/h1&gt;[end]')
    '<h1>ヘロー</h1>'

    """
    text = text.replace('<br />', '\n')
    text = text.replace('[filter html]', '').replace('[end]', '')
    tag = html_parser.unescape(text)
    return tag


def img(text):
    """http://spam.png等の画像URLを、imgタグに置換する.

    Bootstrap4に合わせたタグです

    >>> img('[filter img]https://torina.top/a.png[end]')
    '<a href="https://torina.top/a.png" target="_blank" rel="nofollow">\
    <img src="https://torina.top/a.png" class="img-fluid"/></a>'

    """
    text = text.replace('<br />', '\n')
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


def imgpk(text):
    """[filter imgpk]1[end]を、正しいimgタグにする

    1の部分は、Imageモデルインスタンスのpkとなります。
    """
    text = text.replace('<br />', '\n')
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


def cord(text):
    """<pre>コード</pre>に置き換える.

    google-code-prettyfyに合わせたタグです

    >>> cord('[filter cord]hello<br />narito[end]')
    '<pre class="prettyprint linenums">hello\\nnarito</pre>'

    """
    text = text.replace('<br />', '\n')
    text = text.replace('[filter cord]', '').replace('[end]', '')
    tag = '<pre class="prettyprint linenums">{}</pre>'.format(text)
    return tag


def quote(text):
    """<blockquote>文字</blockquote>に置き換える.

    Bootstrap4にあわせたタグです

    >>> quote('[filter quote]narito[end]')
    '<blockquote class="blockquote"><p>narito</p></blockquote>'

    """
    text = text.replace('[filter quote]', '').replace('[end]', '')
    tag = '<blockquote class="blockquote"><p>{}</p></blockquote>'.format(text)
    return tag


def h2(text):
    """<h2 class="blog-h2">文字</h2>に置き換える."""
    text = text.replace('[filter h2]', '').replace('[end]', '')
    tag = '<h2 class="blog-h2">{0}</h2>'.format(text)
    return tag


@register.filter(is_safe=True, needs_autoescape=True)
def blog(value, autoescape=True):
    """本文中の[filter name]text[end]を、適切なHTMLタグに変換する.

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
    for f in filters:
        filter_name = f.group('tag_name')  # name部分、urlやimg等の関数名が入る
        origin_text = f.group()  # text部分
        # 関数の取得と、呼び出し
        filter_function = globals().get(filter_name)
        if filter_function and callable(filter_function):
            result_text = filter_function(origin_text)
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
    """GETパラメータを一部を置き換える."""
    url_dict = request.GET.copy()
    url_dict[field] = value
    return url_dict.urlencode()


@register.simple_tag
def hilight(text, key_word):
    """ハイライトした文章を返す.

    >>> hilight('oh my oh', 'oh')
    '<span class="under-line">oh</span> my <span class="under-line">oh</span>'

    """
    result = text
    case = (key_word, key_word.title(), key_word.capitalize())
    for word in case:
        html_tag = '<span class="under-line">{0}</span>'.format(word)
        result = result.replace(word, html_tag)

    return result


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
