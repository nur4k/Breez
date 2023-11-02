from django.db import models


class Client(models.Model):
    customer = models.CharField(verbose_name='Логин покупателя', max_length=255, null=True, blank=True)
    item = models.CharField(verbose_name='Наименование товара', max_length=255,null=True, blank=True)
    total = models.CharField(verbose_name='Cумма заказа', max_length=255, null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Kоличество товара', null=True, blank=True)
    date = models.DateTimeField(verbose_name='Дата и время регистрации заказа', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.customer} -- {self.item}'


class CSVFile(models.Model):
    csv_file = models.FileField(upload_to='csv_files/')
