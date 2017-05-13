from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sitemaps import ping_google
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponsePermanentRedirect, Http404
from django.shortcuts import redirect
from django.views import generic
from .forms import PostSerachForm, CommentCreateForm
from .models import Post, Comment


class BaseListView(generic.ListView):
    paginate_by = 10

    def get_queryset(self):

        # 公開フラグがTrue、作成日順
        queryset = Post.objects.filter(
            is_publick=True).order_by('-created_at')
        return queryset


class PostIndexView(BaseListView):
    """トップページ、クイックサーチ"""

    def get_queryset(self):

        global_form = PostSerachForm(self.request.GET)
        global_form.is_valid()
        keyword = global_form.cleaned_data['keyword']
        queryset = super().get_queryset()

        # 大文字小文字の区別なく、タイトル、本文に含むかのor検索
        if keyword:
            for word in keyword.split():
                queryset = queryset.filter(
                    Q(title__icontains=word) | Q(text__icontains=word))

        return queryset


class PostPrivateIndexView(LoginRequiredMixin, BaseListView):
    """非公開の記事一覧"""

    def get_queryset(self):

        # 公開フラグがFalse、作成日順
        queryset = Post.objects.filter(
            is_publick=False).order_by('-created_at')
        return queryset


class CategoryView(BaseListView):
    """カテゴリのリンククリック"""

    def get_queryset(self):
        category = self.kwargs['category']
        queryset = super().get_queryset().filter(category__name=category)
        return queryset


class TagView(BaseListView):
    """タグのリンククリック"""

    def get_queryset(self):
        tag = self.kwargs['tag']
        queryset = super().get_queryset().filter(tag__name=tag)
        return queryset


class PostDetailView(generic.DetailView):
    """記事詳細ページ"""

    model = Post
    def get_object(self, queryset=None):
        post = super().get_object()
        
        # その記事が公開か、ユーザがログインしていればよし 
        if post.is_publick or self.request.user.is_authenticated():
            return post
        else:
            raise Http404

class CommentCreateView(generic.CreateView):
    """コメント投稿画面

    '^comment/(?P<pk>[0-9]+)/$'のようにして、記事のpkも受け取っている
    このpkをcontextへ渡し前へ戻るリンクに利用したり、targetに指定する記事を取得するのに使う
    """

    model = Comment
    form_class = CommentCreateForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['post_pk'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.target = Post.objects.get(pk=post_pk)
        self.object.save()
        return redirect('blog:detail', pk=post_pk)


@login_required
def ping(request):
    """Googleへpingを送信する"""

    try:
        url = reverse_lazy('blog:django.contrib.sitemaps.views.sitemap')
        ping_google(sitemap_url=url)
    except Exception:
        raise
    else:
        return redirect('blog:index', permanent=True)


def redirect_main(request, pk):
    """旧URLである/mainの、/detailへのリダイレクト。後々消す"""

    return redirect('blog:detail', permanent=True, pk=pk)
