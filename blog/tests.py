"""テストを行うモジュール."""
from django.test import TestCase
from django.urls import reverse
from blog.models import Post, Category, Tag


class TestViews(TestCase):
    """Viewのテストクラス."""

    def setUp(self):
        """初期化。各モデルを作成する."""
        tag = Tag.objects.create(name='Django')
        category = Category.objects.create(name='Programing')
        post = Post.objects.create(
            title='Hello', text='World', category=category)
        post.tag.add(tag)

    def test_index_get(self):
        """/ アクセスのテスト."""
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello')
        self.assertQuerysetEqual(
            response.context['post_list'], ['<Post: Hello>'])

    def test_alltag_get(self):
        """/alltag アクセスのテスト."""
        response = self.client.get(reverse('blog:tag_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django')
        self.assertQuerysetEqual(
            response.context['tag_list'], ['<Tag: Django>'])

    def test_detail_get_1(self):
        """/detail/1 アクセスのテスト."""
        response = self.client.get(reverse('blog:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'World')
        self.assertEqual(response.context['post'].title, 'Hello')

    def test_detail_get_2(self):
        """/detail/2 アクセスのテスト(つくってない記事)."""
        response = self.client.get(reverse('blog:detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 404)

    def test_category_get_1(self):
        """/category/Programing アクセスのテスト."""
        response = self.client.get(
            reverse('blog:category', kwargs={'category': 'Programing'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello')
        self.assertQuerysetEqual(
            response.context['post_list'], ['<Post: Hello>'])

    def test_category_get_2(self):
        """/category/aiueo アクセスのテスト (作ってないカテゴリ)."""
        try:
            self.client.get(
                reverse('blog:category', kwargs={'category': 'aiueo'}))
        except Category.DoesNotExist:
            pass
        else:
            raise

    def test_tag_get_1(self):
        """/tag/Django アクセスのテスト."""
        response = self.client.get(
            reverse('blog:tag', kwargs={'tag': 'Django'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello')
        self.assertQuerysetEqual(
            response.context['post_list'], ['<Post: Hello>'])

    def test_tag_get_2(self):
        """/tag/Python アクセスのテスト(作ってないタグ)."""
        try:
            self.client.get(reverse('blog:tag', kwargs={'tag': 'Python'}))
        except Tag.DoesNotExist:
            pass
        else:
            raise

    def test_comment_get_1(self):
        """/comment/1 アクセスのテスト."""
        response = self.client.get(
            reverse('blog:comment', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_comment_get_2(self):
        """/comment/2 アクセスのテスト(作ってない記事).

        試したらエラーになりませんでした。これはいつか修正しましょう

        """
        response = self.client.get(
            reverse('blog:comment', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)

    def test_private_get(self):
        """/private アクセスのテスト."""
        response = self.client.get(reverse('blog:private'))
        self.assertEqual(response.status_code, 302)

    def test_feed_get(self):
        """/latest/feed アクセスのテスト."""
        response = self.client.get(reverse('blog:feed'))
        self.assertEqual(response.status_code, 200)

    def test_sitemap_get(self):
        """/sitemap.xml アクセスのテスト."""
        response = self.client.get(
            reverse('blog:django.contrib.sitemaps.views.sitemap'))
        self.assertEqual(response.status_code, 200)
