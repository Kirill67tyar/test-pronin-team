from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Payment(models.Model):
    comment = models.CharField(max_length=50, verbose_name="Комментарий к платежу")
    owner = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Владелец платежа",
    )
    collection = models.ForeignKey(
        to="fees.Collect",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Оплата сбора",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2, 
        verbose_name="Сумма пожертвования",
    )
    created_at = models.DateTimeField(verbose_name="Время оплаты", auto_now_add=True,)
    updated_at = models.DateTimeField(verbose_name="Время оплаты", auto_now=True,)
    
    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ("created_at",)
        default_related_name = "payments"

class Collect(models.Model):

    class Cause(models.TextChoices):
        BIRTHDAY = "BD"
        WEDDING = "WD"
        PARTY = "PT"
        MEDICINE = "MD"
        ART = "AR"
    
    name = models.CharField(max_length=50, verbose_name="Название сбора")
    author = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="collections",
        verbose_name="Владелец сбора",
    )
    cause = models.CharField(
        max_length=2, 
        choices=Cause, 
        default=Cause.ART, 
        verbose_name="Повод сбора",
        )
    description = models.TextField(verbose_name="Описание сбора",)
    planned_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2, 
        verbose_name="Планируемая сумма сбора",
        )
    # current_amount = models.DecimalField(
    #     max_digits=10,
    #     decimal_places=2, 
    #     verbose_name="Текущая сумма сбора",
    # )
    # count_supporters = models.PositiveSmallIntegerField(verbose_name="Сколько человек уже сделало пожертвования",)
    image = models.ImageField(upload_to='collects/images/',null=True, blank=True, verbose_name="Обложка сбора",)
    closing_to = models.DateTimeField(verbose_name="Дата и время завершения сбора",)
    
    # @property
    # def list_supported(self):
    #     ls_supported = [self.payments.select_related("owner")]
    #     pass
