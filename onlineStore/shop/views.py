from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from shop.models import Product


class AddProductToCartView(LoginRequiredMixin, AccessMixin, View):
    def check(self, pk):
        return Product.objects.filter(pk=pk).exists() and self.request.user != Product.objects.get(pk=pk).user

    def get(self, request, pk):
        if not self.check(pk):
            self.handle_no_permission()
        product = get_object_or_404(Product, pk=pk)
        request.user.cart.add(product)
        return redirect(reverse('shop:products'))


class DeleteProductFromCartView(LoginRequiredMixin, AccessMixin, View):
    def check(self, pk):
        return Product.objects.filter(pk=pk).exists() and self.request.user.cart.filter(pk=pk).exists()

    def get(self, request, pk):
        if not self.check(pk):
            self.handle_no_permission()
        product = get_object_or_404(Product, pk=pk)
        request.user.cart.remove(product)
        return redirect(reverse('shop:cart'))


class ProductListView(ListView):
    template_name = 'shop/products.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)
    paginate_by = 3


class CreateProductView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'shop/create_product.html'
    fields = 'name', 'description', 'price', 'discount', 'count', 'image'
    success_url = reverse_lazy('shop:products')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductEditView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        product = self.get_object()
        return self.request.user == product.user

    model = Product
    template_name = 'shop/product_edit.html'
    context_object_name = 'product'
    fields = 'name', 'description', 'price', 'discount', 'count', 'image'

    def get_success_url(self):
        return reverse('shop:product_details', kwargs={'pk': self.object.pk})


class ProductDetailsView(DetailView):
    model = Product


class ProductDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        product = self.get_object()
        return self.request.user == product.user

    model = Product
    success_url = reverse_lazy('shop:products')


class CartDetailsView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'shop/cart_detail.html'

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(CartDetailsView, self).get_context_data(**kwargs)
        context['bill'] = self.request.user.cart.aggregate(Sum('price')).get('price__sum')
        return context


class CartClearView(LoginRequiredMixin, View):
    def get(self, request):
        request.user.cart.clear()
        return redirect(reverse('shop:cart'))


class BuyView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'shop/buy.html')

    def post(self, request):
        for product in request.user.cart.all():
            product.count -= 1
            if product.count == 0:
                product.archived = True
            product.save()
        request.user.cart.clear()
        return redirect(reverse('shop:products'))
