# django-torina-blog

[![Build Status](https://travis-ci.org/naritotakizawa/django-torina-blog.svg?branch=master)](https://travis-ci.org/naritotakizawa/django-torina-blog)

[![Coverage Status](https://coveralls.io/repos/github/naritotakizawa/django-torina-blog/badge.svg?branch=master)](https://coveralls.io/github/naritotakizawa/django-torina-blog?branch=master)

----
## お知らせ
ブログ用のDjangoアプリケーションです。  
大幅な更新をしたため、前のバージョンはタグ0.9のものを利用してください。  
[実際に使っているブログ](https://torina.top)  
[ちょっとした紹介](https://torina.top/detail/447/)

----
## 必要なもの
Python: 3.5以上  
Django: 2.0以上


----
## 使い方


### インストールする

    pip install -U https://github.com/naritotakizawa/django-torina-blog/archive/master.tar.gz



### settings.pyの編集
`INSTALLED_APPS`、`SITE_ID`、`TEMPLATES`の`context_processors`、`MEDIA_URL`、`MEDIA_ROOT`等の追加をしてください。

    INSTALLED_APPS = [
        'blog.apps.BlogConfig',  # add
        ...
        ...
        'django.contrib.sites',  # add
        'django.contrib.sitemaps',  # add
    ]
    SITE_ID = 1  # add
    ...
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
    ...
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

### プロジェクトのurls.pyで読み込む

    urlpatterns = [
	    path('admin/', admin.site.urls),
	    path('', include('blog.urls')),  # add
    ]



### 起動する
    python manage.py migrate
    python manage.py runserver


### データを追加する
admin管理サイトのサイトモデルから、ドメイン情報やサイト詳細情報を入力後、記事やカテゴリ、タグ等を実際に追加してください。