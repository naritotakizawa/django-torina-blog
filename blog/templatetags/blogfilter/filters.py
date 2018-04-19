"""blogフィルター内で呼び出される、特殊構文を評価するための仕組みを提供するモジュール"""
import html as html_module
import re
from blog.models import Image


class DefaultConverter:
    """[filter name]text[end]を適切なHTMLに変換するクラス

    linebreaksbrで作られた改行(<br />)を利用しています。
    テンプレートにて、{{ post.text | linebreaksbr | blog }} のような形になっていることを確認してください。
    """
    split_char = html_module.escape('<split>')
    pattern = r'\[filter (?P<tag_name>.*?)\].*?\[end\]'

    def __init__(self, text):
        self.text = text
        self.h2_count = 0
        self.h3_count = 0

    def run(self):
        """変換の実行"""
        value = self.text
        matches = re.finditer(self.pattern, value, flags=re.DOTALL)
        for m in matches:
            filter_name = m.group('tag_name')  # name部分、urlやimg等の関数名が入る
            origin = m.group()  # [filter ...][end]までの部分
            func = getattr(self, filter_name, None)  # [filter name]のnameに対応する関数を探す
            if func:
                # 余計な部分を削る [filter name]text[end]→text
                pure_text = origin.replace(
                    '[filter {}]'.format(filter_name), ''
                )
                pure_text = pure_text.replace('[end]', '')
                # 変換後のテキストを取得し、置換する
                result = func(pure_text)
                value = value.replace(origin, result, 1)
        return value

    def url(self, text):
        """[filter url]href[end]を、aタグして解釈する

        href<split>○○へのリンク とすることで、リンクテキストを作成できます。
        """
        text = text.replace('<br />', '')
        if self.split_char in text:
            href, text = text.split(self.split_char)
            tag = '<a href="{0}" target="_blank" rel="nofollow">{1}</a>'.format(
                href, text)
        else:
            href = text
            tag = '<a href="{0}" target="_blank" rel="nofollow">{0}</a>'.format(href)
        return tag

    def html(self, text):
        """[filter html]your_html[end]を、そのままHTMLとして解釈する."""
        text = text.replace('<br />', '\n')
        tag = html_module.unescape(text)
        return tag

    def img(self, text):
        """[filter img]src[end]を、正しいimgタグにする

        Bootstrap4に合わせたimgタグです、img-fluidを使います。
        src<split>説明 とすることで、altに説明が入ります。
        """
        text = text.replace('<br />', '')
        if self.split_char in text:
            src, alt = text.split(self.split_char)
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

    def imgpk(self, text):
        """[filter imgpk]1[end]を、正しいimgタグにする

        1の部分は、Imageモデルインスタンスのpkとなります。それ以外はimg関数と同様です。
        また、<split>がなくてもImageモデルのdescription属性を使います。
        """
        text = text.replace('<br />', '')
        if self.split_char in text:
            pk, alt = text.split(self.split_char)
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

    def code(self, text):
        """[filter code]コード[end]を<pre>コード</pre>に置き換える.

        google-code-prettyfyに合わせたタグです
        """
        text = text.replace('<br />', '\n')
        tag = '<pre class="prettyprint linenums">{}</pre>'.format(text)
        return tag

    def quote(self, text):
        """[filter quote]文字[end]を<blockquote>文字</blockquote>に置き換える.

        Bootstrap4用の<blockquote>に置き換えます。
        文字<split>名前 のように使うと、名前をかっこよく表示します。
        """
        if self.split_char in text:
            p_text, footer_text = text.split(self.split_char)
            footer_tag = '<footer class="blockquote-footer">{0}</footer>'.format(footer_text)
            tag = '<blockquote class="blockquote"><p class="mb-0">{}</p>{}</blockquote>'.format(p_text, footer_tag)
        else:
            p_text = text
            tag = '<blockquote class="blockquote"><p class="mb-0">{}</p></blockquote>'.format(p_text)
        return tag

    def h2(self, text):
        """[filter h2]文字[end]を<h2 class="blog-h2">文字</h2>に置き換える."""
        self.h2_count += 1
        self.h3_count = 0
        index = 'i{}'.format(self.h2_count)
        tag = '<h2 class="blog-h2" id="{}">{}</h2>'.format(index, text)
        return tag

    def h3(self, text):
        """[filter h3]文字[end]を<h3 class="blog-h3">文字</h3>に置き換える."""
        self.h3_count += 1
        index = 'i{}-{}'.format(self.h2_count, self.h3_count)
        text = text.replace('[filter h3]', '').replace('[end]', '')
        tag = '<h3 class="blog-h3" id="{}">{}</h3>'.format(index, text)
        return tag
