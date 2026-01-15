
from django.contrib import admin
from .models import Category, Dish, Order, OrderItem, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'available', 'weight')
    list_filter = ('category', 'available')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'total', 'created_at')
    inlines = [OrderItemInline]

admin.site.register(Review)