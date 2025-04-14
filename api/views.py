from django.db.models import Max
from rest_framework import generics
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer,ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


class ProductListAPIView(generics.ListAPIView):
    model = Product
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer 

    def get_queryset(self):#dynamic filtering which overwrites the default queryset
        qs = super().get_queryset()
        return qs.filter(user = self.request.user)
    

class OrderListAPIView(generics.ListAPIView): #Get orders from only a specific user
    serializer_class = OrderSerializer
    queryset = Order.objects.prefetch_related('items__product').all()
    permission_classes = [IsAuthenticated]


# Using FBV
# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)
                    
# @api_view(['GET'])
# def product_detail(request, pk):
#     products = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(products)
#     return Response(serializer.data)

# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related('items__product').all()
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)
                    
@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer ({
        'products': products,
        'count' : len(products),
        'max_price' : products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)
