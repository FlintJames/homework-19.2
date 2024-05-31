from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product, Blog


def home(request):
    return render(request, "home.html")


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'У вас новое сообщение: {name}({phone}): {message}')
    return render(request, 'catalog/contacts.html')


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product

class BlogListView(ListView):
    model = Blog

class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object

class BlogCreateView(CreateView):
    model = Blog
    fields = ("title", "content", "image", "publication_sign", "number_of_views")
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)

class BlogUpdateView(UpdateView):
    model = Blog
    fields = ("title", "content", "image", "publication_sign", "number_of_views")
    success_url = reverse_lazy('catalog:blog_list')

    def get_success_url(self):
        return reverse('catalog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')


def toggle_publication(request, pk):
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.publication_sign:
        blog_item.publication_sign = False
    else:
        blog_item.publication_sign = True

    blog_item.save()

    return redirect(reverse('catalog:blog_list'))

