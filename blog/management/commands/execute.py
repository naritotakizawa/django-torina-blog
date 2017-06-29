"""python manage.py execute で呼ぶ処理を定義するモジュール."""
from django.core.management.base import BaseCommand
from blog.models import PopularPost
from .api import get_10_popular


class Command(BaseCommand):
    """コマンド定義のためのクラス."""

    def handle(self, *args, **options):
        """コマンド定義のための関数。実際の処理はapi.main()."""
        # 過去一週間の人気データを全て削除し、新たに作り直す
        PopularPost.objects.all().delete()
        for url, title, page_view in get_10_popular():
            PopularPost.objects.create(
                url=url, title=title, page_view=page_view)
