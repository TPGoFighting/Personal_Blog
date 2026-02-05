from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Post, Category, Message


# 1. 关于页面（纯静态）
def about(request):
    return render(request, "blog/about.html")


# 2. 留言板（处理提交和显示）
def guestbook(request):
    if request.method == "POST":
        user = request.POST.get("user")
        content = request.POST.get("content")
        if user and content:
            Message.objects.create(user=user, content=content)
            return redirect('guestbook') # 提交后重定向回留言板，防止刷新重复提交
    messages = Message.objects.all().order_by("-created_at")
    return render(request, "blog/guestbook.html", {"messages": messages})


# 3. 增强 home 视图，使其支持分类筛选
def home(request):
    query = request.GET.get("q", "").strip()
    cat_id = request.GET.get("category")

    posts = Post.objects.all()

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if cat_id:
        posts = posts.filter(category_id=cat_id)

    posts = posts.distinct().order_by("-created_at")
    categories = Category.objects.all() # 确保这一行存在

    return render(request, "blog/home.html", {
        "posts": posts, 
        "query": query, 
        "categories": categories
    })
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


class PostCreateView(CreateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content"]

    def get_success_url(self):
        next_url = self.request.POST.get("next")
        return next_url if next_url and next_url != "None" else reverse_lazy("home")


class PostUpdateView(UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content"]

    def get_success_url(self):
        next_url = self.request.POST.get("next")
        return (
            next_url
            if next_url and next_url != "None"
            else reverse("post-detail", kwargs={"pk": self.object.pk})
        )


class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_delete.html"

    def get_success_url(self):
        next_url = self.request.POST.get("next")
        # 如果来源是详情页，删完回首页；否则原路返回
        if next_url and f"post/{self.object.pk}" not in next_url:
            return next_url
        return reverse_lazy("home")
