from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Страва"
        verbose_name_plural = "Страви"

    def __str__(self):
        return self.title

class Order(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} — {self.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(1, default=1)
    def __str__(self):
        return f"Order #{self.order} — {self.quantity}"

class Review(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    text_review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    def __str__(self):
        return


