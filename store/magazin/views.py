from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.template.loader import get_template
from django.conf import settings

from .models import *


def index(request):
    tovari = Tovari.objects.order_by('-count').all()

    return render(request, 'index.html', context={'tovari': tovari})


def catalog(request):
    tovari = Tovari.objects.order_by('-count').all()

    return render(request, 'product/catalog.html', context={'tovari': tovari})


def panel(request):
    if 'login' in request.session:
        id_client = Client.objects.filter(login=request.session['login']).first().id
        client = get_object_or_404(Client, id=id_client)
        if request.method == 'POST' and request.FILES['avatar']:
            path = ''
            if 'avatar' in request.FILES:
                file = request.FILES['avatar']
                fs = FileSystemStorage()
                fs.save('avatars/' + file.name, file)
                path = 'avatars/' + file.name
            email = request.POST['email']
            phone = request.POST['phone']

            client.email = email
            client.phone = phone
            if path != '':
                client.avatar = path
            client.save()

        data = Client.objects.filter(login=request.session['login']).first()
        orders = Order.objects.filter(client=client)
        return render(request, 'user/panel.html', context={'data': data, 'orders': orders})
    return redirect('/auth')


def cart(request):
    products = []
    all_total_price = 0
    if 'products' in request.session:
        products_id = request.session['products'].split(',')
        products_n = {}
        for id in products_id:
            if id != '':
                id = int(id)
                if id in products_n:
                    products_n[id] += 1
                else:
                    products_n[id] = 1

        for key, value in products_n.items():
            all_total_price += (value * Tovari.objects.filter(id=int(key)).first().price)
            products.append({
                'id': key,
                'count': value,
                'product': Tovari.objects.filter(id=int(key)).first(),
                'total': value * Tovari.objects.filter(id=int(key)).first().price,
            })

    return render(request, 'product/cart.html', context={'products': products, 'all_total': all_total_price})


def order(request):
    if 'login' in request.session:
        if request.method == 'POST':
            login = request.session['login']
            all_total = request.POST['all_total']
            client = get_object_or_404(Client, login=login)
            ids_new = []
            error = ''
            if 'products' in request.session:
                current_client = Client.objects.filter(login=request.session['login']).first()
                if current_client.balance >= int(all_total):
                    ids = str(request.session['products']).split(',')
                    for id in ids:
                        if id != '':
                            ids_new.append(int(id))
                    products_new = Tovari.objects.filter(id__in=ids_new)

                    new_order = Order()

                    new_order.client = client
                    new_order.total_price = int(all_total)
                    s_1 = Status.objects.filter(title='На складе').first()
                    new_order.status = s_1
                    new_order.save()

                    new_order.products.add(*products_new)

                    Client.objects.filter(pk=current_client.id).update(balance=current_client.balance - int(all_total))
                    del request.session['products']
                    # print(request.session['products'])
                    send_message(new_order.id, current_client.email, int(all_total), current_client.login)
                else:
                    error = 'Недостаточно средств на счету!'

            return redirect('/cart')


def del_product(request):
    if request.method == 'POST':
        id_tovar = request.POST['id']
        products_id = request.session['products'].split(',')
        for id in products_id:
            if id != '':
                if id == id_tovar:
                    products_id.remove(id)
                    break
        del request.session['products']
        request.session['products'] = ','.join(products_id)

    return HttpResponse(1)


def get_products(products):
    res = ''
    for product in products:
        res += f'''<div class="product_item">
                   <h2>{product.title}</h2>
                   <p>
                       <img src="/media/{product.image}" width="100%" height="250px">
                   </p>
                   <p>
                       {product.price} руб.
                   </p>
                   <p>
                       Кол-во: {product.count}
                   </p>
                   <p>
                       <button class="btn btn-buy" data="{product.id}">Купить</button>
                       <a class="btn" href="/product/{product.id}">Подробнее</a>
                   </p>
               </div>'''

    return res


def filter_catalog(request):
    if request.method == 'POST':
        mode = request.POST['mode']
        sort = request.POST['sort']
        if mode == 'price':
            if sort == 'sort_1':
                products = Tovari.objects.order_by('price')
            else:
                products = Tovari.objects.order_by('-price')

            res = get_products(products)
            return HttpResponse(res)

        elif mode == 'count':
            if sort == 'count_1':
                products = Tovari.objects.order_by('count')
            else:
                products = Tovari.objects.order_by('-count')
            res = get_products(products)
            return HttpResponse(res)

        elif mode == 'name':
            search = sort
            products = Tovari.objects.filter(title__icontains=search)
            res = get_products(products)
            return HttpResponse(res)


def gettotal(request):
    if request.method == 'POST':
        all_total_price = 0
        if 'products' in request.session:
            products_id = request.session['products'].split(',')
            products_n = {}
            for id in products_id:
                if id != '':
                    id = int(id)
                    if id in products_n:
                        products_n[id] += 1
                    else:
                        products_n[id] = 1

            for key, value in products_n.items():
                all_total_price += (value * Tovari.objects.filter(id=int(key)).first().price)

        return HttpResponse(all_total_price)


def product_id(request, id):
    product = Tovari.objects.filter(id=id).first()

    return render(request, 'product/tovar_description.html', context={'product': product})


def order_id(request, id):
    order = Order.objects.filter(id=id).first()

    return render(request, 'order/order_description.html', context={'order': order})


def add_product(request):
    if request.method == 'POST':
        id = request.POST['id']
        count = 0
        if 'products' in request.session:
            products = request.session['products'] + "," + str(id)
            request.session['products'] = products
            count = len(str(request.session['products']).split(',')) - 1
        else:
            request.session['products'] = str(id) + ','
            count = 1

    return HttpResponse(count)


def tovar_description(request):
    return render(request, 'tovar_description.html')


def reg(request):
    suc = ''
    r = ''
    if request.method == 'POST':
        login = request.POST['login']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        reppassword = request.POST['reppassword']
        if len(login) < 5 or len(password) < 5:
            suc = 'Пустые или слишком короткие значения логина и/или пароля.'
        if Client.objects.filter(login=login).exists():
            suc = 'Такой логин занят.'
        if Client.objects.filter(login=phone).exists():
            suc = 'Такой номер телефона уже используется.'
        if Client.objects.filter(login=email).exists():
            suc = 'Такой адрес электронной почты уже используется.'
        if password != reppassword:
            suc = 'Пароли не совподают.'
        if not suc:
            client = Client()
            client.login = login
            client.email = email
            client.phone = phone
            client.password = password
            client.save()
            r = 'Успешная регистация'

    return render(request, 'user/reg.html', context={'suc': suc, 'r': r})


def auth(request):
    suc = ''
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        if Client.objects.filter(login=login, password=password).exists():
            request.session['login'] = login
            return redirect('/panel')
        else:
            suc = 'Ошибка авторизации!'

    return render(request, 'user/auth.html', context={'suc': suc})


def logout(request):
    if 'login' in request.session:
        del request.session['login']
    return redirect('/')


def send_message(id_order, email, summa, name):
    html = get_template('mail/message.html')
    context = {'id_order': id_order, 'summa': summa, 'name': name}
    subject = 'Оформлен новый заказ с №' + str(id_order)
    from_email = settings.EMAIL_HOST_USER
    html_content = html.render(context)
    msg = EmailMultiAlternatives(subject, html_content, from_email, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
