import html
from blog.models import Image

# いくつかの関数で使われる区切り文字。関数には区切り文字がエスケープされて渡される
# 区切り文字があるかどうかの確認は、エスケープした状態で比較しなければならない
SPLIT_CHAR = html.escape('<split>')

# {'url': url関数オブジェクト} のような辞書。
name_function = {}


def register(func):
    """関数を登録するデコレータ

    [filter name]text[end]では、nameに対応する関数が呼び出されます。
    その関数を登録するのに使うデコレータです。
    """
    name_function[func.__name__] = func


def convert(name, text):
    """[filter name]text[end]を評価する"""
    func = name_function.get(name)
    if func:
        return func(text)


@register
def url(text):
    """[filter url]href[end]を、aタグして解釈する."""
    text = text.replace('<br />', '')
    text = text.replace('[filter url]', '').replace('[end]', '')
    if SPLIT_CHAR in text:
        href, text = text.split(SPLIT_CHAR)
        tag = '<a href="{0}" target="_blank" rel="nofollow">{1}</a>'.format(
            href, text)
    else:
        href = text
        tag = '<a href="{0}" target="_blank" rel="nofollow">{0}</a>'.format(href)
    return tag


@register
def html(text):
    """[filter html]your_html[end]を、そのままHTMLとして解釈する."""
    text = text.replace('<br />', '\n')
    text = text.replace('[filter html]', '').replace('[end]', '')
    tag = html.unescape(text)
    return tag


@register
def img(text):
    """[filter img]src[end]を、正しいimgタグにする

    Bootstrap4に合わせたimgタグです、img-fluidを使います。
    """
    text = text.replace('<br />', '')
    text = text.replace('[filter img]', '').replace('[end]', '')
    if SPLIT_CHAR in text:
        src, alt = text.split(SPLIT_CHAR)
        tag = (
            '<a href="{0}" target="_blank" rel="nofollow"><img data-original="{0}" '
            'class="img-fluid lazy" alt="{1}"></a>'
        ).format(src, alt)
    else:
        tag = (
            '<a href="{0}" target="_blank" rel="nofollow"><img data-original="{0}" '
            'class="img-fluid lazy"/></a>'
        ).format(text)
    return tag


@register
def imgpk(text):
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
        image = Image.objects.get(pk=int(pk))
    except Image.DoesNotExist:
        tag = '<img src="">'
    else:
        src = image.src.url
        tag = (
            '<a href="{0}" target="_blank" rel="nofollow"><img data-original="{0}" '
            'class="img-fluid lazy" alt="{1}"></a>'
        ).format(src, alt or image.title)  # <split>があればそれ優先、なければImageのタイトル属性
    return tag


@register
def code(text):
    """[filter code]コード[end]を<pre>コード</pre>に置き換える.

    google-code-prettyfyに合わせたタグです
    """
    text = text.replace('<br />', '\n')
    text = text.replace('[filter code]', '').replace('[end]', '')
    tag = '<pre class="prettyprint linenums">{}</pre>'.format(text)
    return tag


@register
def quote(text):
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


h2_count = 0
h3_count = 0


@register
def h2(text):
    """[filter h2]文字[end]を<h2 class="blog-h2">文字</h2>に置き換える."""
    global h2_count, h3_count
    h2_count += 1
    h3_count = 0
    index = 'i{}-{}'.format(h2_count, h3_count)
    text = text.replace('[filter h2]', '').replace('[end]', '')
    tag = '<h2 class="blog-h2" id="{}">{}</h2>'.format(index, text)
    return tag


@register
def h3(text):
    """[filter h3]文字[end]を<h3 class="blog-h3">文字</h3>に置き換える."""
    global h3_count
    h3_count += 1
    index = 'i{}-{}'.format(h2_count, h3_count)
    text = text.replace('[filter h3]', '').replace('[end]', '')
    tag = '<h3 class="blog-h3" id="{}">{}</h3>'.format(index, text)
    return tag
