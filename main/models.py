from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_resturent = models.BooleanField(default=False)
    is_rider = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name+ ' '+ self.last_name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True, related_name="customer_user")
    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "customer_users"

    def __str__(self):
        return self.full_name

class Division(models.Model):
    division_name = models.CharField(max_length=120,blank=True,null=True)

    class Meta:
        db_table = "division"

    def __str__(self):
        return self.division_name

class Place(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
    district_name = models.CharField(max_length=120, blank=True, null=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "place"
    
    def __str__(self):
        return self.district_name

class ResturantUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="resturant_user")
    resturant_name = models.CharField(max_length=120, blank=True, null=True)
    resturant_front = models.ImageField(upload_to="food/resturant/", null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    menu_list = models.ImageField(upload_to="food/image/", null=True)
    position = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="rest_place",blank=True,null=True)
    
    class Meta:
        db_table = "resturant_user"

    def __str__(self):
        return self.full_name + ' ' +self.resturant_name

class allowResturant(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=120, blank=True, null=True)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    resturant_name = models.CharField(max_length=120, blank=True, null=True)
    resturant_front = models.ImageField(upload_to="food/resturant/", null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    menu_list = models.ImageField(upload_to="food/add/", null=True)
    position = models.ForeignKey(Place, on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        db_table = "allow_user"

    def __str__(self):
        return self.full_name + ' ' +self.resturant_name


class Rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="rider_user")
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=120, blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "rider_profile"

    def __str__(self):
        return self.full_name


class FoodCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "categories"
    
    def __str__(self):
        return self.category_name + ' | '+str(self.category_id)

class FoodName(models.Model):
    provider = models.ForeignKey(ResturantUser, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=120,null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(null=True, blank=True)
    image_one = models.ImageField(upload_to="food/image/", null=True)
    image_two = models.ImageField(upload_to="food/image/", null=True)
    image_three = models.ImageField(upload_to="food/image/", null=True)

    class Meta:
        db_table = "food_name"
    
    def __str__(self):
        return self.slug + ' | '+str(self.pk)




class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="orders")
    date_order = models.DateField(auto_now_add=True)
    time_order = models.TimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True)
    process = models.BooleanField(default=False)
    to_rider = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = "order"

    def __str__(self):
        return self.customer.full_name

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def order_id_list(self):
        orderitems = self.orderitem_set.all()
        order_id = [item.id for item in orderitems]
        return order_id

class OrderItem(models.Model):
    food = models.ForeignKey(FoodName, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    data_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order_items"
    
    def __str__(self):
        return self.order.customer.full_name + " -> Borrowd " + str(self.quantity) +" " +self.food.name

    @property
    def get_total(self):
        total = self.food.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=120, null=True, blank=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    date_added = models.CharField(max_length=120,blank=True,null=True)

    # def __str__(self):
    #     return self.customer