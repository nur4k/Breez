import csv
from io import TextIOWrapper
from django.db.models import Sum, Count

from rest_framework import status
from rest_framework import serializers

from mainapp.models import Client, CSVFile


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'customer', 'item', 'total', 'quantity', 'date')


class CSVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVFile
        fields = ('id', 'csv_file')

    def create(self, validated_data):
        csv_file = validated_data.get('csv_file')
        if not csv_file:
            raise serializers.ValidationError({'csv_file': 'В процессе обработки файла произошла ошибка.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            csv_text = TextIOWrapper(csv_file.file, encoding='utf-8')
            csv_reader = csv.DictReader(csv_text)
            for row in csv_reader:
                client_data = {
                    'customer': row['customer'],
                    'item': row['item'],
                    'total': row['total'],
                    'quantity': row['quantity'],
                    'date': row['date']
                }
                client_serializer = ClientSerializer(data=client_data)
                client_serializer.is_valid(raise_exception=True)
                client_serializer.save()
            return CSVFile.objects.create(csv_file=csv_file)
        except Exception as e:
            raise serializers.ValidationError({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ClientCSVDataSerializer(serializers.ModelSerializer):
    top_customers = serializers.SerializerMethodField()

    class Meta:
        model = Client
        exclude = ('customer', 'item', 'total', 'quantity', 'date',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['top_customers'] = self.get_top_customers(instance) 
        return data

    def get_top_customers(self, instance):  
        top_customers = Client.objects.values('customer').annotate(spent_money=Sum('total')).order_by('-spent_money')[:5]
        top_items = Client.objects.values('item').annotate(num_customers=Count('customer')).filter(num_customers__gte=2)

        top_customer_data = []
        for customer in top_customers:
            customer_data = {
                'username': customer['customer'],
                'spent_money': customer['spent_money'],
                'gems': self.get_customer_gems(customer['customer'], top_items)
            }
            top_customer_data.append(customer_data)

        return top_customer_data

    def get_customer_gems(self, customer, top_items):
        customer_gems = []
        for item in top_items:
            if Client.objects.filter(customer=customer, item=item['item']).count() >= 2:
                customer_gems.append(item['item'])
        return customer_gems
