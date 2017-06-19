==================
django-torina-blog
==================
.. image:: https://travis-ci.org/naritotakizawa/django-torina-blog.svg?branch=master
    :target: https://travis-ci.org/naritotakizawa/django-torina-blog

.. image:: https://coveralls.io/repos/github/naritotakizawa/django-torina-blog/badge.svg
    :target: https://coveralls.io/github/naritotakizawa/django-torina-blog

ブログ用のDjangoアプリケーションです。

https://torina.top/



Requirement
--------------

:Python: 3.5以上
:Django: 1.10以上


Quick start
-----------
1. インストールする::

    pip install -U https://github.com/naritotakizawa/django-torina-blog/archive/master.tar.gz

2. settings.pyのINSTALLED_APPSに足す::

    INSTALLED_APPS = [
        ...
        'blog',  # add
        'django.contrib.sites',
        'django.contrib.sitemaps',
    ]
    
    SITE_ID = 1  # add

3. settings.pyのcontext_processorsに'blog.context_processors.common'を足す::

	TEMPLATES = [
	    {
	        'BACKEND': 'django.template.backends.django.DjangoTemplates',
	        'DIRS': [],
	        'APP_DIRS': True,
	        'OPTIONS': {
	            'context_processors': [
	                'django.template.context_processors.debug',
	                'django.template.context_processors.request',
	                'django.contrib.auth.context_processors.auth',
	                'django.contrib.messages.context_processors.messages',
	                'blog.context_processors.common',  # add
	            ],
	        },
	    },
	]

4. MEDIA_ROOT、MEDIA_URLを設定する::

    # settings.py
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

5. ルートのurls.pyに足す::

	urlpatterns = [
	    url(r'^admin/', admin.site.urls),
	    url(r'^blog/', include('blog.urls', namespace='blog')),  # add
	]

6. python manage.py migrate　でモデルを追加する.

7. python manage.py runserver 等で動かし、http://127.0.0.1:8000/admin/ から記事やカテゴリを追加する

8. http://127.0.0.1:8000/blog/ で、表示されるのを確認する

9. テンプレートを上書きしたりする。
