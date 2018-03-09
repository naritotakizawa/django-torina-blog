==================
django-torina-blog
==================
.. image:: https://travis-ci.org/naritotakizawa/django-torina-blog.svg?branch=master
    :target: https://travis-ci.org/naritotakizawa/django-torina-blog

.. image:: https://coveralls.io/repos/github/naritotakizawa/django-torina-blog/badge.svg
    :target: https://coveralls.io/github/naritotakizawa/django-torina-blog

https://torina.top/

ブログ用のDjangoアプリケーションです。大幅な更新をしたため、前のバージョンはタグ0.9のものを利用してください。

Requirement
--------------

:Python: 3.5以上
:Django: 2.0以上


Quick start
-----------
1. インストールする::

    pip install -U https://github.com/naritotakizawa/django-torina-blog/archive/master.tar.gz

2. settings.pyのINSTALLED_APPSに足し、SITE_ID=1も書く::

    INSTALLED_APPS = [
        'blog.apps.BlogConfig',  # add
        ...
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
	    path('admin/', admin.site.urls),
	    path('', include('blog.urls')),  # add
	]

6. python manage.py migrate

7. python manage.py runserver 等で動かし、admin管理サイトのサイトモデルから、サイトのドメインやサイト詳細情報を入力後、記事やカテゴリを追加する。

8. http://127.0.0.1:8000/blog/ で、表示されるのを確認する

9. テンプレートを上書きしたりする。


過去1週間の人気記事を取得する場合(Google Analytics)
----------------------------------------------------------

1. インストールする::

    pip install google-api-python-client
    pip install pyopenssl

2. settings.pyに追記::

    SERVICE_ACCOUNT_EMAIL = 'your@account'
    KEY_FILE_LOCATION = os.path.join(BASE_DIR, 'client_secrets.p12')
    VIEW_ID = 'your view id'

3. python manage.py execute で取得開始(cron等で呼び出すようにするとgood)