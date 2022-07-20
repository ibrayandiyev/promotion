from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.http import JsonResponse
from django.utils import translation
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from backend.models import Category, Product, Banner, AboutUs

from django.core.mail import send_mail

# Create your views here.
class Index(ListView):
    model = Product
    template_name = "frontend/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actual_lang = translation.get_language()
        if actual_lang == 'es':
            idlang = 2
        elif actual_lang == 'en':
            idlang = 1
        product = Product.objects.filter(language_id=idlang, indexed=True).order_by('position')
        banner = Banner.objects.filter(language_id=idlang).order_by('position')
        parent_cate = Category.objects.filter(language_id=idlang, parent=None).order_by('position')
        for cate in parent_cate:
            cate.child = Category.objects.filter(language_id=idlang, parent=cate).order_by('position')

        context['category'] = parent_cate
        context['product'] = product
        context['banner'] = banner

        return context

class About(ListView):
    model = AboutUs
    template_name = "frontend/about.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actual_lang = translation.get_language()
        if actual_lang == 'es':
            idlang = 2
        elif actual_lang == 'en':
            idlang = 1
        about = AboutUs.objects.filter(language_id=idlang)
        context['about'] = about
        return context

class Contact(TemplateView):
    template_name = "frontend/contact.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("aaa", "########")
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            send_mail(name, message, email, ['behmpat@behmpat.com'], fail_silently= True)
            return redirect('index')

class ProductContact(TemplateView):
    template_name = "frontend/product_contact.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quantity = self.kwargs.get('quantity')
        prod_id = self.kwargs.get('prod_id')
        prod = Product.objects.get(id=prod_id)
        context["prod_name"] = prod.name
        context["min_order"] = prod.min_order
        context["quantity"] = quantity
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            product = request.POST.get('product')
            quantity = request.POST.get('quantity')
            message = request.POST.get('message')
            print(product, quantity, "######")
            send_mail(name + " ("+ product + " " + str(quantity) + ")", message, email, ['behmpat@behmpat.com'], fail_silently= True)
            return redirect('index')

def category_product(request, category, pk):
    actual_lang = translation.get_language()
    if actual_lang == 'es':
        idlang = 2
    elif actual_lang == 'en':
        idlang = 1
    cate = Category.objects.get(id=pk)
    product = Product.objects.filter(language_id=idlang, category=cate).order_by('-id')
    count = Category.objects.filter(language_id=idlang, id=cate.id).count()
    if count is not 0:
        selected_cate = Category.objects.get(language_id=idlang, id=cate.id)
        if selected_cate.parent:
            selected_cate.parent.child = Category.objects.filter(language_id=idlang, parent=selected_cate.parent).exclude(id=selected_cate.id).order_by('position')
            parent_cate = Category.objects.filter(language_id=idlang, parent=None).exclude(id=selected_cate.parent.id).order_by('position')
        else:
            parent_cate = Category.objects.filter(language_id=idlang, parent=None).exclude(id=selected_cate.id).order_by('position')
        for cate in parent_cate:
            cate.child = Category.objects.filter(language_id=idlang, parent=cate).order_by('position')
    else:
        selected_cate = None
        parent_cate = Category.objects.filter(language_id=idlang, parent=None).order_by('position')
        for cate in parent_cate:
            cate.child = Category.objects.filter(language_id=idlang, parent=cate).order_by('position')
    
    paginator = Paginator(product, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'frontend/product.html', {'product': page_obj, 'category': parent_cate, 'selected_cate': selected_cate, 'page_obj': page_obj, 'paginator': paginator})


def subcategory_product(request, category, subcategory, pk):
    actual_lang = translation.get_language()
    if actual_lang == 'es':
        idlang = 2
    elif actual_lang == 'en':
        idlang = 1

    cate = Category.objects.get(id=pk)
    product = Product.objects.filter(language_id=idlang, category=cate)
    count = Category.objects.filter(language_id=idlang, id=cate.id).count()
    if count is not 0:
        selected_cate = Category.objects.get(language_id=idlang, id=cate.id)
        if selected_cate.parent:
            selected_cate.parent.child = Category.objects.filter(language_id=idlang, parent=selected_cate.parent).exclude(id=selected_cate.id).order_by('position')
            parent_cate = Category.objects.filter(language_id=idlang, parent=None).exclude(id=selected_cate.parent.id).order_by('position')
        else:
            parent_cate = Category.objects.filter(language_id=idlang, parent=None).exclude(id=selected_cate.id).order_by('position')
        for cate in parent_cate:
            cate.child = Category.objects.filter(language_id=idlang, parent=cate).order_by('position')
    else:
        selected_cate = None
        parent_cate = Category.objects.filter(language_id=idlang, parent=None).order_by('position')
        for cate in parent_cate:
            cate.child = Category.objects.filter(language_id=idlang, parent=cate).order_by('position')
    
    paginator = Paginator(product, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'frontend/product.html', {'product': page_obj, 'category': parent_cate, 'selected_cate': selected_cate, 'page_obj': page_obj, 'paginator': paginator})

def ajax_search_front_product(request):
    search_key = request.POST.get('search_key')
    sel_cate_id = request.POST.get('sel_cate')
    actual_lang = translation.get_language()
    if actual_lang == 'es':
        idlang = 2
    elif actual_lang == 'en':
        idlang = 1
    if sel_cate_id:
        product = Product.objects.filter(language_id=idlang, name__icontains=search_key, category_id=sel_cate_id)
    else:
        product = Product.objects.filter(language_id=idlang, name__icontains=search_key)

    paginator = Paginator(product, 9)
    page_number = request.POST.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'widgets/front_ajax_product.html', {'product': page_obj, 'page_obj': page_obj, 'paginator': paginator})

class DetailProduct(ListView):
    model = Product
    template_name = "frontend/detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        actual_lang = translation.get_language()
        if actual_lang == 'es':
            idlang = 2
        elif actual_lang == 'en':
            idlang = 1
        product = Product.objects.get(id=self.kwargs.get('pk'))
        count = Category.objects.filter(language_id=idlang, id=product.category.id).count()
        if count is not 0:
            selected_cate = Category.objects.get(language_id=idlang, id=product.category.id)
            if selected_cate.parent:
                selected_cate.parent.child = Category.objects.filter(language_id=idlang, parent=selected_cate.parent).exclude(id=selected_cate.id).order_by('position')
                parent_cate = Category.objects.filter(language_id=idlang, parent=None).exclude(id=selected_cate.parent.id).order_by('position')
            else:
                parent_cate = Category.objects.filter(language_id=idlang, parent=None).exclude(id=selected_cate.id).order_by('position')
            for cate in parent_cate:
                cate.child = Category.objects.filter(language_id=idlang, parent=cate).order_by('position')
        else:
            selected_cate = None
            parent_cate = Category.objects.filter(language_id=idlang, parent=None).order_by('position')
            for cate in parent_cate:
                cate.child = Category.objects.filter(language_id=idlang, parent=cate).order_by('position')
        
        context['category'] = parent_cate
        context['product'] = product
        context['selected_cate'] = selected_cate
        return context
def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)