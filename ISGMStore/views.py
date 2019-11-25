from django.shortcuts import render,get_object_or_404,redirect,reverse
from . import models, forms
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict,modelform_factory
from django.http import HttpResponseBadRequest
from django.contrib import auth
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.


def default_renderer(request,template,context={}):
    categories = models.category.objects.all()
    context["categories"] = categories
    return render(request,template,context)


@login_required
@csrf_exempt
@require_http_methods(['POST'])
def checkout(request):
    checkout_items = []
    if request.method == 'POST':
        error_message = ""
        print(request.POST)
        total_types = request.POST.get('total_item_types',0)
        total_cost = 0
        for i in range(1,int(total_types)+1):
            item_id = request.POST.get('item_number_'+str(i),0)
            item = models.item.objects.get(id=item_id)
            item_dict = model_to_dict(item)
            
            quantity = int(request.POST.get('quantity_'+str(i),0))
            if quantity >= item.stock_quantity:
                error_message += " We are sorry we don't have enough in stock for the quantity of item you want to purchase. Item : "+item.item_name+" , Requested_Quantity : "+str(quantity)+" , Available_Quantity : "+str(item.stock_quantity)+". Item quantity is automatically set to maximum limit. You can change that in the quantity box"
                quantity = item.stock_quantity
            item_dict["image_url"] = item.item_image.url
            item_dict["quantity"] = quantity
            discount_amount = item.get_discount_amount()+(item.price * request.user.customer.get_discount_ratio())
            item_dict["discount_amount"] = discount_amount
            total_discount_amount = discount_amount * quantity
            item_dict["total_discount_amount"] = total_discount_amount
            total_price = (item.price-discount_amount)*quantity
            item_dict["total_price"] = total_price
            total_cost += total_price
            print(item_dict)
            checkout_items.append(item_dict) 
        return default_renderer(request, "ISGMStore/checkout.html", {'checkout_items':checkout_items,'total_cost':total_cost,'error_message':error_message})
    else:
        return HttpResponseBadRequest("Accept Only POST Method With Necessary Data.")


@login_required
def index(request):
    error_message = request.GET.get("error_message","")
    query = "select * from ISGMStore_item i, ISGMStore_purchase_order po where i.id=po.item_id and i.discount >= 10 order by count(po.item_id) limit 9"
    item_list = models.item.objects.filter(discount__gte=10).order_by('-discount')[:9]
    return default_renderer(request, "ISGMStore/inde.html",{"error_message":error_message,"item_list":item_list})


@login_required
@require_http_methods(['POST'])
def confirm_checkout(request):
    if request.method=="POST":
        error_message = ""
        total_orders = int(request.POST.get('total_order', 0))
        confirmed_order = models.confirmed_order()
        confirmed_order.user = request.user
        confirmed_order.save()
        print(confirmed_order.id)
        for i in range(1,total_orders+1):
            item_id = int(request.POST.get('item_id_'+str(i),0))
            item = get_object_or_404(models.item,pk=item_id)
            quantity = int(request.POST.get('quantity_'+str(i),0))
            if quantity > item.stock_quantity:
                error_message += " We are sorry we don't have enough in stock for the quantity of item you want to purchase. Item : "+item.item_name+" , Requested_Quantity : "+quantity+" , Available_Quantity : "+item.stock_quantity
                
            else:
                order = models.order_history()
                order.item = item
                order.original_price = request.POST.get('price_'+str(i),0)
                order.discount = request.POST.get('discount_'+str(i),0)
                order.quantity = quantity
                order.confirmed_order = confirmed_order
                order.save()
        return default_renderer(request, "ISGMStore/result.html", {"redirect_url":reverse("ISGMStore:invoice",args=(confirmed_order.id,)),"error_message":error_message})
    else:
        return HttpResponseBadRequest("Accept Only POST Method With Necessary Data.")


@login_required
def invoices(request):
    invoices = models.confirmed_order.objects.filter(user=request.user)
    return default_renderer(request, "ISGMStore/invoices.html", {'invoices':invoices})


@login_required
def invoice(request, pk):
    invoice = models.confirmed_order.objects.get(pk=pk, user=request.user)
    total_price = 0
    for order in invoice.order_history_set.all():
        total_price += order.total_price()
    return default_renderer(request, "ISGMStore/invoice.html", {'invoice':invoice,'total_cost':total_price})


@login_required
def category(request,id):
    category = get_object_or_404(models.category,pk=id)
    all_item_list = category.item_set.all().order_by('id')
    paginator = Paginator(all_item_list,12)
    page_no = request.GET.get('page_no',1)
    item_list = paginator.page(page_no)
    print(item_list.paginator.num_pages)
    return default_renderer(request, "ISGMStore/products.html", {'category':category,'items':item_list})


@login_required
@require_http_methods(["GET","POST"])
def user_profile(request):
    user = request.user
    user_form = forms.UserForm(instance=user)
    # password_form = auth.forms.PasswordChangeForm(user=user)
    customer_form = modelform_factory(models.customer, fields=['name'])
    if request.method == 'GET':
        return default_renderer(request, "ISGMStore/profile.html",{'user_form':user_form,'password_form':None,'customer_form':customer_form(instance=user.customer)})
    else : 
        user_form = forms.UserForm(request.POST,instance=user)
        # password_form = auth.forms.PasswordChangeForm(request.POST,instance=user)
        customer_form = customer_form(request.POST,instance=user.customer)
        # password_form.is_valid() and
        if user_form.is_valid() and customer_form.is_valid():
            print("Fields Are Valid")
            user_form.save()
            customer_form.save()
            #password_form.save()
        print("Saved")
        return redirect(reverse("ISGMStore:user_profile"))


@require_http_methods(["GET","POST"])
def login(request):
    if request.user.is_authenticated:
        return redirect(reverse("ISGMStore:index"))
    login_form = auth.forms.AuthenticationForm
    user_form = forms.UserCreateForm
    customer_form = modelform_factory(models.customer,fields=['name'])
    if request.method=="GET":
        return render(request, "ISGMStore/login.html",{'login_form':login_form(),'user_form':user_form(),'customer_form':customer_form()} )
    else:
        login_form = login_form(request=request, data=request.POST)
        if login_form.is_valid():
            print(login_form.get_user())
            auth.login(request, login_form.get_user())
            return redirect(reverse("ISGMStore:index"))
        else:
            return render(request, "ISGMStore/login.html",{'login_form':login_form,'user_form':user_form(),'customer_form':customer_form()} )


def logout(request):
    auth.logout(request)
    return redirect(reverse("ISGMStore:login"))


@require_http_methods(["POST"])
def register(request):
    print("Here Here")
    user_form = forms.UserCreateForm
    customer_form = modelform_factory(models.customer,fields=["name"])
    user_form = user_form(request.POST)
    customer_form = customer_form(request.POST)
    print(user_form.is_valid())
    if user_form.is_valid():
        user = user_form.save()
        
        if customer_form.is_valid():
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.discount = 0
            customer.credits = 0
            customer.save()
            auth.login(request,user)
            return redirect(reverse("ISGMStore:index"))
    return redirect(reverse("ISGMStore:login"))


