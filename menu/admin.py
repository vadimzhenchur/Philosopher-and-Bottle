
from django.contrib import admin
from .models import Category, Dish, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'available')
    list_filter = ('category', 'available')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'created_at', 'total')
    inlines = [OrderItemInline]