from .models import Product,Category,Orders,Orderdetails,Customer
from rest_framework import serializers


class CustomProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField(source='buy_price')
    category = serializers.CharField(write_only=True)
    category_id = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'code', 'description', 'price', 'category','category_id')

    def create(self, validated_data):
        category, _ = Category.objects.get_or_create(name=validated_data['category'])
        validated_data['category'] = category
        validated_data['sell_price'] = validated_data['buy_price']
        validated_data['quantity'] = 10000
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if validated_data.has_key('category'):
            validated_data['category'] = Category.objects.get_or_create(name=validated_data['category'])[0]
        return super(CustomProductSerializer, self).update(instance, validated_data)


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='customer.firstname',required=False)
    address = serializers.CharField(max_length=100,required=False)
    status = serializers.ChoiceField(choices=('COMPLETE','CREATED'),required=True)

    class Meta:
        model = Orders
        fields = ('id','username','address','status')

    def create(self, validated_data):
        print (validated_data)

        status = str(validated_data['status'])
        if status is None or status != 'CREATED':
            raise Exception

        username = None
        if 'customer' in validated_data:
            username = self.username = validated_data['customer']['firstname']

        if username is not None:
            print (type(username),username)
            customer, _ = Customer.objects.get_or_create(firstname=username,email=(str(username) + '@gmail.com'))
            validated_data['customer'] = customer

        return Orders.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if instance.status == 'COMPLETE':
            raise Exception('cannot modify a checked out order')

        if 'customer' not in validated_data:
            validated_data['customer'] = instance.customer if self.partial else None
        if 'address' not in validated_data:
            validated_data['address'] = instance.address if self.partial else None
        if 'status' not in validated_data:
            validated_data['status'] = instance.status

        print (type(validated_data), validated_data)
        print (instance.customer)

        if validated_data['customer'] is None:
            instance.customer = None
        elif instance.customer is None:
            instance.customer = Customer.objects.get_or_create(firstname=validated_data['customer']['firstname'])[0]
        elif validated_data['customer'] != instance.customer:
            raise Exception('username conflict')

        instance.address = validated_data['address']
        instance.status = validated_data['status']

        if instance.status == 'COMPLETE' and (instance.customer is None or instance.address is None):
            raise Exception('cannot checkout without mandatory fields')
        instance.save()
        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    order_id = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField()
    price = serializers.FloatField(source='sell_price')

    class Meta:
        model = Orderdetails
        fields = ('id','order_id', 'product_id', 'price')

    def create(self, validated_data):
        order = Orders.objects.get(id=validated_data['order_id'])
        product = Orders.objects.get(id=validated_data['product_id'])
        price = Orders.objects.get(id=validated_data['price'])
        if order is None or product is None:
            raise Exception('order_id or product_id doesnt exist')
        else:
            return Orderdetails.objects.update_or_create(order=order,product=product,sell_price=price)
