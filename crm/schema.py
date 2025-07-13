import graphene
from graphene_django import DjangoObjectType
from crm.models import Product, Customer, Order

# GraphQL Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'

class OrderType(DjangoObjectType):
    total_amount = graphene.Decimal()
    
    class Meta:
        model = Order
        fields = '__all__'
    
    def resolve_total_amount(self, info):
        return self.total_amount

# Query Class
class Query(graphene.ObjectType):
    hello = graphene.String()
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)

    def resolve_hello(self, info):
        return "Hello, GraphQL!"

    def resolve_customers(self, info):
        return Customer.objects.all()

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_orders(self, info):
        return Order.objects.all()

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        dummy = graphene.Boolean()

    updated = graphene.List(graphene.String)
    message = graphene.String()

    def mutate(self, info, dummy=False):
        low_stock = Product.objects.filter(stock__lt=10)
        names = []
        for p in low_stock:
            p.stock += 10
            p.save()
            names.append(f"{p.name} (new stock: {p.stock})")
        return UpdateLowStockProducts(updated=names, message="Restocked products successfully")

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
