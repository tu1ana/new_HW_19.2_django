from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.forms import ProductForm, BlogEntryForm, VersionForm
from catalog.models import Product, BlogEntry, Version


class ProductListView(ListView):
    model = Product
    version = Version
    extra_context = {
        'title': 'Главная'
    }

    def get_queryset(self):
        return super().get_queryset()

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data['version_list'] = Version.objects.filter(product=self.kwargs.get('product'))
    #
    #     return context_data


def contacts(request):
    context = {
        'title': 'Контакты'
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have a new message from {name} ({phone}) {message}')
    return render(request, 'catalog/contacts.html', context)


class ProductDetailView(DetailView):
    model = Product
    # permission_required = ('catalog.change_description', 'catalog.set_published')


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:create_product')
    
    def form_valid(self, form):
        self.object = form.save()
        self.object.auth_user = self.request.user
        self.object.save()
        
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')
    # permission_required = ('catalog:change_description', 'catalog.change_category', 'catalog.set_published')

    def test_func(self):
        return self.request.user == self.get_object().auth_user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
    permission_required = 'catalog.delete_product'

    # def test_func(self):
    #     return self.request.user == self.get_object().auth_user


class BlogEntryCreateView(CreateView):
    model = BlogEntry
    form_class = BlogEntryForm
    # fields = ('heading', 'content',)
    success_url = reverse_lazy('catalog:blogentry_list')

    def form_valid(self, form):
        if form.is_valid():
            new_entry = form.save()
            new_entry.slug = slugify(new_entry.heading)
            new_entry.save()

        return super().form_valid(form)


class BlogEntryListView(ListView):
    model = BlogEntry

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogEntryUpdateView(UpdateView):
    model = BlogEntry
    form_class = BlogEntryForm
    # fields = ('heading', 'content',)
    # success_url = reverse_lazy('catalog:blogentry_list')

    def form_valid(self, form):
        if form.is_valid():
            new_entry = form.save()
            new_entry.slug = slugify(new_entry.heading)
            new_entry.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:view_blog', args=[self.kwargs.get('pk')])


class BlogEntryDetailView(DetailView):
    model = BlogEntry

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        object.views_count += 1
        object.save()
        return object


class BlogEntryDeleteView(DeleteView):
    model = BlogEntry
    success_url = reverse_lazy('catalog:blogentry_list')
