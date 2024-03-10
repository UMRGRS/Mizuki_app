from django.db import models

# Create your models here.

class Categories(models.Model):
    name = models.CharField(('Nombre'), max_length = 50)
    
    def __str__(self):
        return(self.name)

class Product(models.Model):
    name = models.CharField(('Nombre'), max_length = 100)
    price = models.PositiveIntegerField(('Precio'))
    category = models.ForeignKey(Categories, on_delete = models.CASCADE)
    
    def __str__(self):
        return(self.name)

class Order(models.Model):
    tableNumber = models.PositiveIntegerField(('Numero de mesa'))
    waitingPayment = models.BooleanField(('Orden por cobrar'), default=False)
    complete = models.BooleanField(('Orden completada'), default=False)
    
    def SetWaitingPayment(self):
        self.waitingPayment = True
    
    def SetCompleted(self):
        self.completed = True
        
    def __str__(self):
        return(f'{self.tableNumber}')
    
class OrderDetail(models.Model):
    orderID = models.ForeignKey(Order, on_delete = models.CASCADE)
    productID = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField('Cantidad')
    
    def GetTotal(self):
        prod = Product.objects.get(pk=self.productID)
        return prod.price*self.quantity
    
    def __str__(self):
        return(f'{self.orderID}, {self.productID}, {self.quantity}')