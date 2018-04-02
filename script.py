import os
import re
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from blog.models import *


def change_comma_to_split():
    """[filter name]a,b[end]→[filter name]a<split>b[end]"""
    for post in Post.objects.all():
        results = []
        # img、imgpk、urlでだけ今は区切り文字を使っている
        filters = re.finditer(r'\[filter (img|imgpk|url)\].*?\[end\]', post.text)
        for f in filters:
            origin_text = f.group()  # text部分
            if ',' in origin_text:
                result_text = origin_text.replace(',', '<split>')
                results.append((origin_text, result_text))
    
        # 元の[filter..]を、結果htmlと置き換えていく
        for origin_text, result_text in results:
            post.text = post.text.replace(origin_text, result_text)
            post.save()



if __name__ == '__main__':
    pass
