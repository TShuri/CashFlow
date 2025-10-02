from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название статуса")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название типа")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Тип операции")

    def __str__(self):
        return f"{self.name} ({self.type})"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ['name', 'type']


class Subcategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название подкатегории")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        unique_together = ['name', 'category']


class Transaction(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    operation_date = models.DateField(verbose_name="Дата операции")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма")
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.operation_date} - {self.amount} руб. - {self.category}"

    class Meta:
        verbose_name = "Денежная операция"
        verbose_name_plural = "Денежные операции"
        ordering = ['-operation_date']
