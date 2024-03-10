from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse


from .models import Categories, Product, Order, OrderDetail

# Create your views here.

def WaitersPage(request, message=None):

    all_products = {}
    categories=Categories.objects.all()
    for cat in categories:
        prods = Product.objects.filter(category=cat.id)
        all_products[cat.name] = prods
        
    return render(request, "Mizuki_app/waiters.html", {'all_products': all_products, 'message':message})

def AddProd(request):
    products_list = request.session.get('added_products')

    if(products_list == None):
        products_list = []
    
    pk = request.POST['add_prod']
    quantity = request.POST['Quantity']
    product = Product.objects.get(pk=pk)
    print(product)
    for prod in products_list:
        if(prod['name']==product.name):
            prod['quantity'] += int(quantity)
            request.session['added_products'] = products_list
            return HttpResponseRedirect(reverse('Mizuki_app:waitersPage'))
    
    products_list.append({'id':product.id,'name': product.name, 'price':product.price,'quantity': int(quantity)})
    request.session['added_products'] = products_list
    return HttpResponseRedirect(reverse('Mizuki_app:waitersPage'))

def DelProd(request):
    products_list = request.session.get('added_products')
    prod_to_delete = request.POST['Del_prod']
    for i, prod in enumerate(products_list):
        if(prod['id']==int(prod_to_delete)):
            products_list.pop(i)
    if(len(products_list)==0):
        request.session['added_products'] = None
    
    return HttpResponseRedirect(reverse('Mizuki_app:waitersPage'))

def CancelOrder(request):
    request.session['added_products'] = None
    return HttpResponseRedirect(reverse('Mizuki_app:waitersPage'))

def PlaceOrder(request):
    if(request.session['added_products'] == None):
        return HttpResponseRedirect(reverse('Mizuki_app:waitersPageMessage', args=('Añade al menos un producto para realizar el pedido',)))
    
    newOrder=Order(tableNumber=request.POST['table'])
    newOrder.save()
    for item in request.session['added_products']:
        order_detail = OrderDetail(orderID=newOrder, productID=Product(pk=item['id']), quantity=item['quantity'])
        order_detail.save()
    request.session['added_products'] = None
    return HttpResponseRedirect(reverse('Mizuki_app:waitersPageMessage', args=('Pedido realizado con éxito',)))


def KitchenPage(request):
    dic_append = {'id':' ','table': ' ', 'Prods':[]}
    orders_display=[]
    orders = Order.objects.filter(waitingPayment=False)
    
    for order in orders:
        dic_append['id'] = order.pk
        dic_append['table'] = order.tableNumber
        details = OrderDetail.objects.filter(orderID=order.pk)
        for detail in details:
            dic_append['Prods'].append({'name':Product.objects.get(pk=detail.productID.pk).name, 'quantity': detail.quantity})
        orders_display.append(dic_append)
        dic_append = {'id':' ', 'Prods':[]}
    return render(request, "Mizuki_app/kitchen.html", {'orders': orders_display})

def CompleteOrder(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.SetWaitingPayment()
    order.save()
    return HttpResponseRedirect(reverse('Mizuki_app:kitchenPage'))

def CashiersPage(request):
    return render(request, "Mizuki_app/cashier.html")

def PaymentPage(request):
    return render(request, "Mizuki_app/payment.html")