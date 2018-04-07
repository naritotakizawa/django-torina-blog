"""古いバージョンのブログを使っている方は、こちらのスクリプトで修正ができます。"""
import os
import re
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from blog.models import Post


def change_comma_to_split():
    """[filter name]a,b[end]→[filter name]a<split>b[end]

    タグ1.0まで使っていた、
    [filter name]a,b[end]
    を以下に置き換えるスクリプトです。
    [filter name]a<split>b[end]
    """
    for post in Post.objects.all():
        results = []
        # img、imgpk、urlでだけ今は区切り文字を使っている
        filters = re.finditer(r'\[filter (img|imgpk|url)\].*?\[end\]', post.text, flags=re.DOTALL)
        for f in filters:
            origin_text = f.group()  # text部分
            if ',' in origin_text:
                result_text = origin_text.replace(',', '<split>')
                results.append((origin_text, result_text))

        # 元の[filter..]を、結果htmlと置き換えていく
        for origin_text, result_text in results:
            post.text = post.text.replace(origin_text, result_text)
            post.save()


def change_midasi1_to_h2():
    """[filter midasi1]text[end]→[filter h2]text[end]

    タグ1.0まで使っていた
    [filter midasi1]text[end]
    をいかに置き換えるものです。
    [filter h2]text[end]
    """
    for post in Post.objects.all():
        if '[filter midasi1]' in post.text:
            post.text = post.text.replace('[filter midasi1]', '[filter h2]')
            post.save()


def change_cord_to_code():
    """[filter cord]text[end]→[filter code]text[end]

    タグ1.0まで使っていた
    [filter cord]
    を以下に置き換えるものです。
    [filter code]
    """
    for post in Post.objects.all():
        if '[filter cord]' in post.text:
            post.text = post.text.replace('[filter cord]', '[filter code]')
            post.save()


if __name__ == '__main__':
    pass
