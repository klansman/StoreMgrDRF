from django.db.models import Max
from rest_framework import generics
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer,ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView


class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all() 

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_url_kwarg ='product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['DELETE', 'PATCH', 'PUT']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):#dynamic filtering which overwrites the default queryset
        qs = super().get_queryset()
        return qs.filter(user = self.request.user)
    

class OrderListAPIView(generics.ListAPIView): #Get orders from only a specific user
    serializer_class = OrderSerializer
    queryset = Order.objects.prefetch_related('items__product').all()

class ProductInfoAPIView(APIView):
    def get(self,request): 
        products = Product.objects.all()
        serializer = ProductInfoSerializer ({
            'products': products,
            'count' : len(products),
            'max_price' : products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)

    


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
                    
# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer ({
#         'products': products,
#         'count' : len(products),
#         'max_price' : products.aggregate(max_price=Max('price'))['max_price']
#     })
#     return Response(serializer.data)
