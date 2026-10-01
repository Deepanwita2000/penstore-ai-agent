from django.db import models

# Create your models here.
class PenProduct(models.Model):
    name = models.CharField(max_length=225)
    price = models.IntegerField(default=0)
    scheme = models.CharField(max_length=225)
    quantity_condition = models.CharField(max_length=225)
     
class ProductImage(models.Model):
    product = models.ForeignKey(PenProduct , on_delete=models.CASCADE, related_name="images")
    image = models.FileField(upload_to="product_images/", blank=True, null=True)



# class OrderDetails(models.Model):
#     user_id = models.CharField(max_length=100,blank=True , null=True)
#     product = models.ForeignKey(PenProduct , on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)



# class OrderDetails(models.Model):
#     user = models.ForeignKey(User,max_length=100,blank=True , null=True)
#     product = models.ForeignKey(PenProduct , on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
    