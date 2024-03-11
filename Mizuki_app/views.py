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
    orders_display=[]
    orders = Order.objects.filter(waitingPayment=False)
    
    for order in orders:
        dic_append = {'id':' ','table': ' ', 'Prods':[]}
        dic_append['id'] = order.pk
        dic_append['table'] = order.tableNumber
        details = OrderDetail.objects.filter(orderID=order.pk)
        for detail in details:
            dic_append['Prods'].append({'name':Product.objects.get(pk=detail.productID.pk).name, 'quantity': detail.quantity})
        orders_display.append(dic_append)
    return render(request, "Mizuki_app/kitchen.html", {'orders': orders_display})

def CompleteOrder(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.SetWaitingPayment()
    order.save()
    return HttpResponseRedirect(reverse('Mizuki_app:kitchenPage'))

def CashiersPage(request):
    orders_display = GetOrdersToDisplay()
    history_display = GetHistoryToDisplay()
    return render(request, "Mizuki_app/cashier.html",{'orders':orders_display, 'history':history_display})

def GetOrdersToDisplay():
    orders_display=[]
    orders = Order.objects.filter(waitingPayment=True).filter(complete=False)
    
    for order in orders:
        dic_append = {'id':' ','table': ' ', 'Prods':[]}
        dic_append['id'] = order.pk
        dic_append['table'] = order.tableNumber
        details = OrderDetail.objects.filter(orderID=order.pk)
        for detail in details:
            dic_append['Prods'].append({'name':Product.objects.get(pk=detail.productID.pk).name, 'quantity': detail.quantity})
        orders_display.append(dic_append)
    return orders_display

def GetHistoryToDisplay():
    orders_display=[]
    orders = Order.objects.filter(waitingPayment=True).filter(complete=True).order_by('-id')
    order_total = 0
    for order in orders:
        dic_append = {'id':' ','table': ' ', 'order_total': 1, 'Prods':[]}
        dic_append['id'] = order.pk
        dic_append['table'] = order.tableNumber
        details = OrderDetail.objects.filter(orderID=order.pk)
        for detail in details:
            prod = Product.objects.get(pk=detail.productID.pk)
            total = int(prod.price) * int(detail.quantity)
            order_total += total
            dic_append['Prods'].append({'product': prod, 'quantity': detail.quantity, 'total': total})
        dic_append['order_total'] = order_total
        orders_display.append(dic_append)
    return orders_display

def PayOrDelete(request, order_id):
    pay = request.POST.get('pay_order', 0)
    delete = request.POST.get('remove_order', 0)
    if(pay != 0):
        return HttpResponseRedirect(reverse('Mizuki_app:paymentPage', args=(order_id,)))
    elif(delete !=0 ):
        order = Order.objects.get(pk=order_id)
        order.delete()
        return HttpResponseRedirect(reverse('Mizuki_app:cashierPage'))

def PaymentPage(request, order_id):
    order_total = 0
    prods_list = []
    prod_dict = {'detail_id':'', 'prod':1, 'quantity': 1, 'total': 1}
    order = Order.objects.get(pk=order_id)
    details = OrderDetail.objects.filter(orderID=order.id)
    for detail in details:
        prod_dict['detail_id'] = detail.id
        prod_dict['prod'] = Product.objects.get(pk=detail.productID.pk)
        prod_dict['quantity'] = detail.quantity
        prod_dict['total'] = int(prod_dict['prod'].price) * int(detail.quantity)
        order_total += prod_dict['total']
        prods_list.append(prod_dict)
        prod_dict = {'id':'', 'prod':1}
        
    return render(request, "Mizuki_app/payment.html",{'order':order,'prods_list':prods_list, 'order_total':order_total})

def PaymentDone(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.SetCompleted()
    order.save()
    return HttpResponseRedirect(reverse('Mizuki_app:cashierPage'))

def DeleteOrderProduct(request, detail_id):
    detail = OrderDetail.objects.get(pk=detail_id)
    order_id = detail.orderID.pk
    detail.delete()
    prods = OrderDetail.objects.filter(orderID=order_id)
    if not prods:
        Order.objects.get(pk=detail.orderID.pk).delete()
        return HttpResponseRedirect(reverse('Mizuki_app:cashierPage'))
    
    return HttpResponseRedirect(reverse('Mizuki_app:paymentPage',args=(order_id,)))
    