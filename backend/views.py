from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView, RedirectView, View

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, TemplateView
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.utils import translation
from django.http import HttpResponse, HttpResponseRedirect

from .models import User, Category, LanguageCampaign, Product, Banner, AboutUs
from .forms import UserForm, ProductForm, BannerForm

import json
# Create your views here.
class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "backend/login_page.html"
    
    def get_success_url(self):
        return reverse_lazy('admin-index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())

        return super(LoginView, self).form_valid(form)

class LogoutView(RedirectView):
    url = '/admin/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class Index(ListView):
    model = Category
    template_name = "backend/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        actual_lang = translation.get_language()
        if actual_lang == 'es':
            idlang = 2
        elif actual_lang == 'en':
            idlang = 1
        parent_cate = Category.objects.filter(language_id=idlang, parent=None).order_by('position')
        for cate in parent_cate:
            product_count = Product.objects.filter(category=cate).count()
            child_cate = Category.objects.filter(language_id=idlang, parent=cate).order_by('position')

            sum_child_product_count = product_count
            for child in child_cate:
                child_product_count = Product.objects.filter(category=child).count()
                child.product_count = child_product_count
                sum_child_product_count = sum_child_product_count + child_product_count
                print(child_product_count)
            cate.child = child_cate
            cate.product_count = sum_child_product_count

        index_product = Product.objects.filter(language_id=idlang, indexed=True).order_by('position')

        context['category'] = parent_cate
        context['products'] = index_product
        return context


@method_decorator(login_required, name='dispatch')
class Profile(UpdateView):
    model = User
    form_class = UserForm
    template_name = "backend/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs.get('pk'))
        return context
    def get_success_url(self):

        return reverse('profile', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class About(ListView):
    model = User
    template_name = "backend/about_us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actual_lang = translation.get_language()
        if actual_lang == 'es':
            idlang = 2
        elif actual_lang == 'en':
            idlang = 1
        context['about'] = AboutUs.objects.filter(language_id=idlang)
        return context

def ajax_save_about(request):
    description = request.POST.get('description')
    actual_lang = translation.get_language()
    if actual_lang == 'es':
        idlang = 2
    elif actual_lang == 'en':
        idlang = 1
    count = AboutUs.objects.filter(language_id=idlang).count()
    if count == 0:
        new_about = AboutUs(description=description, language_id=idlang)
        new_about.save()
    else:
        saved_about = AboutUs.objects.get(language_id=idlang)
        saved_about.description = description
        saved_about.save()

    return JsonResponse({'status': 'ok'})
@method_decorator(login_required, name='dispatch')
class CategoryPage(ListView):
    model = Category
    template_name = "backend/category.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actual_lang = translation.get_language()
        if actual_lang == 'es':
            idlang = 2
        elif actual_lang == 'en':
            idlang = 1
        parent_cate = Category.objects.filter(language_id=idlang, parent=None).order_by('position')
        for cate in parent_cate:
            cate.child = Category.objects.filter(language_id=idlang, parent=cate).order_by('position')

        context['category'] = parent_cate
        return context

def ajax_add_category(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    cate_id = request.POST.get('cate_id')
    if cate_id == "-1":
        language_campaign = LanguageCampaign.objects.get(value_language=request.POST.get('lang'))
        cate = Category(name=name, description=description, language=language_campaign)
        cate.save()
    else:
        cate = Category.objects.get(id=cate_id)
        cate.name = name
        cate.description = description
        cate.save()
    return JsonResponse({'id': cate.id, 'name': cate.name, 'description':cate.description, 'position':cate.position, 'parent': cate.parent_id})
 
def ajax_order_category(request):
    new_order = request.POST.get('new_order')
    new_order_json = json.loads(new_order)
    new_position = 1
    for obj in new_order_json:
        cate = Category.objects.get(id=obj['id'])
        cate.position = new_position
        cate.parent = None
        cate.save()
        new_position += 1
        if 'children' in obj:
            for obj_child in obj['children']:
                print(obj_child['id'])
                cate = Category.objects.get(id=obj_child['id'])
                cate.parent = Category.objects.get(id=obj['id'])
                cate.position = new_position
                cate.save()
                new_position += 1
    return JsonResponse({'status': 'ok'})
def ajax_delete_category(request):
    cate_id = request.POST.get('cate_id')
    cate = Category.objects.get(id=cate_id)
    cate.delete()
    return JsonResponse({'status': 'ok'})

def ajax_get_subcategory(request):
    cate_id = request.POST.get('cate_id')
    actual_lang = translation.get_language()
    if actual_lang == 'es':
        idlang = 2
    elif actual_lang == 'en':
        idlang = 1
    cate = Category.objects.filter(language_id=idlang, parent_id=cate_id).values('id', 'name').order_by('position')
    return JsonResponse({'category': list(cate)})
   
@method_decorator(login_required, name='dispatch')
class ProductPage(ListView):
    model = Product
    template_name = "backend/product.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actual_lang = translation.get_language()
        if actual_lang == 'es':
            idlang = 2
        elif actual_lang == 'en':
            idlang = 1
        product = Product.objects.filter(language_id=idlang)
        parent_cate = Category.objects.filter(language_id=idlang, parent=None).order_by('position')
        for cate in parent_cate:
            cate.child = Category.objects.filter(language_id=idlang, parent=cate).order_by('position')

        context['category'] = parent_cate
        context['product'] = product
        return context
        
@method_decorator(login_required, name='dispatch')
class CategoryProduct(ListView):
    model = Product
    template_name = "backend/category_product.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actual_lang = translation.get_language()
        if actual_lang == 'es':
            idlang = 2
        elif actual_lang == 'en':
            idlang = 1
        product = Product.objects.filter(language_id=idlang, category_id=self.kwargs.get('pk'))
        count = Category.objects.filter(language_id=idlang, id=self.kwargs.get('pk')).count()
        if count is not 0:
            selected_cate = Category.objects.get(language_id=idlang, id=self.kwargs.get('pk'))
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
            product = Product.objects.filter(language_id=idlang)
        

        context['category'] = parent_cate
        context['product'] = product
        context['selected_cate'] = selected_cate
        return context

class ProductNew(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "backend/product_new.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actual_lang = translation.get_language()
        if actual_lang == 'es':
            idlang = 2
        elif actual_lang == 'en':
            idlang = 1
        parent_cate = Category.objects.filter(language_id=idlang, parent=None).order_by('position')
        context['category'] = parent_cate
        context['actual_lang'] = idlang
        return context
    def get_success_url(self):
        return reverse('products')

class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "backend/product_new.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actual_lang = translation.get_language()
        if actual_lang == 'es':
            idlang = 2
        elif actual_lang == 'en':
            idlang = 1
        parent_cate = Category.objects.filter(language_id=idlang, parent=None).order_by('position')
        context['category'] = parent_cate
        context['actual_lang'] = idlang
        product = Product.objects.get(pk=self.kwargs.get('pk'))
        context['product'] = product
        return context
    def get_success_url(self):
        product = Product.objects.get(pk=self.kwargs.get('pk'))
        exist1 = self.request.POST.get('exist1')
        exist2 = self.request.POST.get('exist2')
        exist3 = self.request.POST.get('exist3')
        exist4 = self.request.POST.get('exist4')
        existPDF = self.request.POST.get('existPDF')
        if exist1=='NO':
            product.picture1=''
        if exist2=='NO':
            product.picture2=''
        if exist3=='NO':
            product.picture3=''
        if exist4=='NO':
            product.picture4=''
        if existPDF=='NO':
            product.pdf=''
        product.save()
        return reverse('products')

def ajax_delete_product(request):
    prod_id = request.POST.get('prod_id')
    prod = Product.objects.get(id=prod_id)
    prod.delete()
    return JsonResponse({'status': 'ok'})

def ajax_order_index_product(request):
    new_order = request.POST.get('new_order')
    new_order_json = json.loads(new_order)
    new_position = 1
    for obj in new_order_json:
        prod = Product.objects.get(id=obj['id'])
        prod.position = new_position
        prod.save()
        new_position += 1
    return JsonResponse({'status': 'ok'})

def ajax_remove_index_product(request):
    prod_id = request.POST.get('prod_id')
    prod = Product.objects.get(id=prod_id)
    prod.indexed = False
    prod.save()
    return JsonResponse({'status': 'ok'})
def ajax_search_product(request):
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
    return render(request, 'widgets/product_list.html', {'product': product})

@method_decorator(login_required, name='dispatch')
class BannerPage(ListView):
    model = Banner
    template_name = "backend/banner.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actual_lang = translation.get_language()
        if actual_lang == 'es':
            idlang = 2
        elif actual_lang == 'en':
            idlang = 1
        banner = Banner.objects.filter(language_id=idlang).order_by('position')
        
        context['banner'] = banner
        context['actual_lang'] = idlang
        return context

def ajax_add_banner(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    bann_id = request.POST.get('bann_id')
    
    if bann_id == "-1":
        bann = BannerForm(request.POST, request.FILES)
        bann.save()
    else:
        print(bann_id)
        bann = Banner.objects.get(id=bann_id)
        print(bann)
        bann.name = name
        bann.picture = request.FILES.get('picture')
        bann.save()
    return HttpResponse('ok')

def ajax_order_banner(request):
    new_order = request.POST.get('new_order')
    new_order_json = json.loads(new_order)
    new_position = 1
    for obj in new_order_json:
        bann = Banner.objects.get(id=obj['id'])
        bann.position = new_position
        bann.save()
        new_position += 1
    return JsonResponse({'status': 'ok'})

def ajax_delete_banner(request):
    bann_id = request.POST.get('bann_id')
    bann = Banner.objects.get(id=bann_id)
    bann.delete()
    return JsonResponse({'status': 'ok'})
