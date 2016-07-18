# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.utils import timezone


class Address(models.Model):
    street1 = models.CharField(max_length=45, blank=True, null=True)
    street2 = models.CharField(max_length=45, blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    country = models.CharField(max_length=45, blank=True, null=True)
    zipcode = models.CharField(max_length=45, blank=True, null=True)
    mobile = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Address'


class Category(models.Model):
    name = models.CharField(unique=True, max_length=45, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Category'


class Customer(models.Model):
    email = models.CharField(max_length=45)
    company_name = models.CharField(max_length=45, blank=True, null=True)
    firstname = models.CharField(max_length=45,unique=True)
    lastname = models.CharField(max_length=45, blank=True, null=True)
    contact = models.CharField(max_length=45, blank=True, null=True)
    current_add = models.ForeignKey(Address, models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Customer'


class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, models.CASCADE)
    add_code = models.ForeignKey(Address, models.CASCADE, db_column='add_code')

    class Meta:
        managed = False
        db_table = 'Customer_Address'
        unique_together = (('customer', 'add_code'),)


class Orderdetails(models.Model):
    order = models.ForeignKey('Orders', models.CASCADE)
    product = models.ForeignKey('Product', models.CASCADE)
    quantity = models.IntegerField()
    sell_price = models.FloatField()

    class Meta:
        managed = False
        db_table = 'OrderDetails'
        unique_together = (('order', 'product'),)


class Orders(models.Model):
    customer = models.ForeignKey(Customer, models.CASCADE, blank=True, null=True)
    time_created = models.DateTimeField(default=timezone.now())
    status = models.CharField(max_length=45,blank=False, null=False)
    address = models.CharField(max_length=100,blank=True,null=True)
    payment_mode = models.CharField(max_length=45,default='COD')
    payment_status = models.CharField(max_length=45,default='NOT_MADE')
    deleted = models.IntegerField(blank=False, null=False,default=False)

    class Meta:
        managed = False
        db_table = 'Orders'


class Product(models.Model):
    category = models.ForeignKey(Category, models.CASCADE)
    code = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    buy_price = models.FloatField()
    sell_price = models.FloatField()
    quantity = models.BigIntegerField()
    deleted = models.IntegerField(default=True)

    class Meta:
        managed = False
        db_table = 'Product'


class AuditLog(models.Model):
    audit_id = models.AutoField(primary_key=True)
    time_created = models.DateTimeField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    params = models.CharField(max_length=200, blank=True, null=True)
    response_code = models.BigIntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    request_type = models.CharField(max_length=45, blank=True, null=True)
    request_duration_ms = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_log'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
