import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print("Cart:",cart)
    items = []
    order = {'get_cart_items':0,'get_cart_total':0}
    for i in cart:
        try:
            order['get_cart_items'] += cart[i]["quantity"]
            product = FoodName.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            item = {
                'food':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image_one':product.image_one,
                    'category':{
                        'category_name':product.category.category_name,
                    }
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
            }
            items.append(item)
        except:
            pass
    return {"order":order,"items":items}

def cartData(request):
    if request.user.is_authenticated and request.user.is_customer:
        customer = Customer.objects.get(user=request.user.pk)
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        cookieData = cookieCart(request)
        order = cookieData['order']
        items = cookieData['items']
    
    return {"order":order, "items":items}

def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    user = User(
        username = name,
        email = email,
        first_name = name,
        last_name = "_",
        is_customer = True,
    )
    user.set_password("12345")
    user.save()
    customer, created = Customer.objects.get_or_create(
        user = user,
        full_name = name,
        phone_no=data['shipping']['phone'],
    )
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = FoodName.objects.get(id=item['food']['id'])
        orderItem = OrderItem.objects.create(
            food=product,
            order=order,
            quantity=item['quantity'],

        )
    return customer, order
