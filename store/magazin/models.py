from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class SliderProduct(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200, default='')
    image = models.ImageField(upload_to='sliders/', verbose_name='Фото товара')

    def __str__(self):
        return self.title


class Tovari(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара')
    image = models.ImageField(upload_to='tovari/', verbose_name='Фото товара')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена товара')
    count = models.IntegerField(verbose_name='Количество товара')
    sliders = models.ManyToManyField(SliderProduct, related_name='slider_product', default=None)

    def __str__(self):
        return f'Название: {self.title} Категория: {self.category.name} '

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'


class Client(models.Model):
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    balance = models.IntegerField(default=0, verbose_name='Баланс')

    def __str__(self):
        return self.login


class Status(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Tovari, related_name='order_products')
    total_price = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(Status, related_name='orderstatus', on_delete=models.CASCADE)
