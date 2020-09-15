from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Home page',
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # nếu không set biến này thì default nó sẽ lấy view theo đường dẫn [app]/[model]_<viewtype>, vd: blog/post_list.html
    context_object_name = 'posts' # đây là tên biến context để truyền vào view hiển thị, nếu không set biến này thì default là object
    ordering = ['-date_posted'] #để dấu "-" đằng trước để nó đảo thứ tự sắp xếp
    paginate_by = 2

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # nếu không set biến này thì default nó sẽ lấy view theo đường dẫn [app]/[model]_<viewtype>, vd: blog/post_list.html
    context_object_name = 'posts' # đây là tên biến context để truyền vào view hiển thị, nếu không set biến này thì default là object
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    # template_name = 'blog/post_detail.html'

# Verify that the current user is authenticated. -> Yêu cầu login mới được post
class PostCreateView(LoginRequiredMixin, CreateView): 
    model = Post
    fields = ['title', 'content']
    # template_name: sẽ dùng theo mẫu [app]/[model]_form vì nó dùng chung cho cả UpdateView
    
    def form_valid(self, form):
        # thêm tác giả cho bài post vì trong form không có phần này, nên trước khi valid thì thêm vào data này
        form.instance.author = self.request.user   
        return super().form_valid(form)

# Verify that the current user is authenticated. -> Yêu cầu login mới được post
# UserPassesTestMixin: Deny a request with a permission error if the test_func() method returns False.
# -> hàm test_func phải trả về true thì mới được đi tiếp, 1 dạng middleware
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Post
    fields = ['title', 'content']
    # template_name: sẽ dùng theo mẫu [app]/[model]_form vì nó dùng chung cho cả UpdateView
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    #hàm này dùng để test xem người dùng có phải là chủ post hay không, kế thừa từ UserPassesTestMixin
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html')
