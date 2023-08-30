from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from ..forms import ProductImageForm
from ..models import Product, Image

class ProductListView(View):
    template_name = 'app/product/all.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, self.template_name, {'products': products})

class ProductDetailView(View):
    template_name = 'app/productsingle.html'

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        return render(request, self.template_name, {'product': product})

class ProductCreateView(View):
    template_name = 'app/product/create.html'
    form_class = ProductImageForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            images = form.cleaned_data['images']
            
            product = Product.objects.create(name=name, description=description, price=price)
            
            for image in images:
                Image.objects.create(product=product, image=image)
            
            return redirect('product_list')
        
        return render(request, self.template_name, {'form': form})
