==================
django-torina-blog
==================
.. image:: https://travis-ci.org/naritotakizawa/django-torina-blog.svg?branch=master
    :target: https://travis-ci.org/naritotakizawa/django-torina-blog

.. image:: https://coveralls.io/repos/github/naritotakizawa/django-torina-blog/badge.svg
    :target: https://coveralls.io/github/naritotakizawa/django-torina-blog

ブログ用のDjangoアプリケーションです。

`実際に使っているブログ <https://torina.top>`_
`ちょっとした紹介 <https://torina.top/detail/447/>`_

お知らせ
--------
`新しいブログ<https://github.com/naritotakizawa/naritoblog/>`_ができました。こちらのほうが洗練されています。

Requirement
--------------

:Python: 3.5以上
:Django: 2.0以上


Quick start
-----------
1. インストールする。現状PyPIにはありません。::

    # 安定版
    pip install -U https://github.com/naritotakizawa/django-torina-blog/archive/master.tar.gz

    # 開発版。ある程度の期間https://torina.topで使って問題がなければ、masterにマージされます。
    pip install -U https://github.com/naritotakizawa/django-torina-blog/archive/develop.tar.gz


2. settings.pyにINSTALLED_APPS、SITE_ID、TEMPLATESのcontext_processors、MEDIA_URL、MEDIA_ROOT等の追加::

    INSTALLED_APPS = [
        'blog.apps.BlogConfig',  # add
        ...
        'django.contrib.sites',  # add
        'django.contrib.sitemaps',  # add
    ]
    
    SITE_ID = 1  # add
    ...
    ...
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
    ...
    ...
    # 各種メディアファイル
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

3. プロジェクトのurls.pyに足す::

    from django.conf import settings
    from django.contrib import admin
    from django.urls import path, include
    from django.conf.urls.static import static

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('blog.urls')),  # add
    ]

    # 開発環境でのメディアファイルの配信設定
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

4. 動かす::

    python manage.py migrate
    python manage.py runserver
    python manage.py createsuperuser

5. データを追加する。admin管理サイトのサイトモデルから、ドメイン情報やサイト詳細情報を入力後、記事やカテゴリ、タグ等を実際に追加してください。



過去1週間の人気記事を取得する場合(Google Analytics)
----------------------------------------------------------
`参考1 <https://torina.top/detail/357/>`_
`参考2 <https://torina.top/detail/355/>`_

1. インストールする::

    pip install google-api-python-client
    pip install pyopenssl

2. settings.pyに追記::

    SERVICE_ACCOUNT_EMAIL = 'your@account'
    KEY_FILE_LOCATION = os.path.join(BASE_DIR, 'client_secrets.p12')
    VIEW_ID = 'your view id'

3. python manage.py execute で取得開始(cron等で呼び出すようにするとgood)
