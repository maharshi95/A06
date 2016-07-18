from django.shortcuts import render
from django import http
from django.db import connection
from rest_framework import viewsets,response,status
import json
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.decorators import api_view


@api_view(['GET'])
def health(request):
    # return http.HttpResponse()
    return response.Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_products_summary(request):
    query_former = "select Category.`id` as category_id, count(Product.`id`) as count " \
                   "from Category,Product " \
                   "where Category.`id` = Product.`category_id` ";

    query_opt = "and Category.`name` = %s"

    query_latter = "group by Category.`id`"

    name = request.GET['name'] if 'name' in request.GET else None
    query = query_former
    if name is not None:
        query += query_opt.replace('%s', name)
    query += query_latter
    print query
    cursor = connection.cursor()
    cursor.execute(query)
    rows = [item for item in cursor.fetchall()]
    data = []
    for row in rows:
        summary = {
            'category_id': row[0],
            'count': row[1]
        }
        data.append(summary)
    output = json.dumps({"data": data})
    output = json.dumps(json.loads(output), indent=4)
    return http.HttpResponse(output, content_type='application/json')


@api_view(['GET'])
def get_orders_summary(request):
    output = None

    if 'group_by' not in request.GET:
        output = get_orders_count()
    elif request.GET['group_by'] == 'product_id':
        output = get_orders_summary_by_product()
    elif request.GET['group_by'] == 'product_id':
        output = get_orders_summary_by_product()

    if output is None:
        return response.Response(status=status.HTTP_400_BAD_REQUEST)
    return http.HttpResponse(output, content_type='application/json')


def get_orders_summary_by_product():
    query = "select count(OrderDetails.`id`) as count, Product.`id` as product_id " \
            "from OrderDetails,Product " \
            "where OrderDetails.`product_id` = Product.`id` " \
            "group by product_id"

    print (query)
    cursor = connection.cursor()
    cursor.execute(query)
    rows = [item for item in cursor.fetchall()]
    data = []
    for row in rows:
        summary = {
            'count': row[0],
            'product_id': row[1]
        }
        data.append(summary)
    output = json.dumps({"data": data})
    output = json.dumps(json.loads(output), indent=4)
    return output


def get_orders_summary_by_category():
    query = "select count(OrderDetails.`id`) as count, Product.`category_id` as category_id " \
            "from OrderDetails,Product " \
            "where OrderDetails.`product_id` = Product.`id` " \
            "group by category_id"

    print (query)
    cursor = connection.cursor()
    cursor.execute(query)
    rows = [item for item in cursor.fetchall()]
    data = []
    for row in rows:
        summary = {
            'count': row[0],
            'category_id': row[1]
        }
        data.append(summary)
    output = json.dumps({"data": data})
    output = json.dumps(json.loads(output), indent=4)
    return output


def get_orders_count():
    query = "select count(OrderDetails.`id`) as count " \
            "from OrderDetails"
    print (query)
    cursor = connection.cursor()
    cursor.execute(query)
    rows = [item for item in cursor.fetchall()]
    output = json.dumps({"count": rows[0][0]})
    output = json.dumps(json.loads(output), indent=4)
    return output


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(deleted=False).all()
    serializer_class = CustomProductSerializer

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.filter(deleted=False).all()
    serializer_class = OrderSerializer

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return response.Response(serializer.data)
        except:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)


class OrderItemViewSet(viewsets.ModelViewSet):

    serializer_class = OrderItemSerializer

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        queryset = Orderdetails.objects.filter(order__deleted=False,order_id=order_id)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data['order_id'] = kwargs['order_id']
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except :
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
