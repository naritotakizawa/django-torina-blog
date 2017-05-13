==================
django-torina-blog
==================

ブログ用のDjangoアプリケーションです。
https://torina.top/


Quick start
-----------
1. インストールする::

    pip install あとでアップする

2. settings.pyのINSTALLED_APPSに足す::

    INSTALLED_APPS = [
        ...
        'blog',
        'django.contrib.sites',
        'django.contrib.sitemaps',
    ]

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

4. MEDIA_ROOT、MEDIA_URLを例えば以下のように::

    # settings.py
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

5. urls.pyを、例えば以下のようにする::

	from django.conf import settings
	from django.conf.urls import url, include
	from django.conf.urls.static import static
	from django.contrib import admin
	 
	urlpatterns = [
	    url(r'^admin/', admin.site.urls),
	    url(r'^blog/', include('blog.urls', namespace='blog')),
	]
	# Development Environment
	if settings.DEBUG:
	    urlpatterns += static(settings.MEDIA_URL,
	                          document_root=settings.MEDIA_ROOT)

6. python manage.py migrate　でモデルを追加する.

7. python manage.py runserver 等で動かし、http://127.0.0.1:8000/admin/ から記事やカテゴリを追加する

8. http://127.0.0.1:8000/blog/ で、表示されるのを確認する

9. テンプレートを上書きしたりする。
