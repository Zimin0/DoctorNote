from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from welcome.models import BaseEntityModel
from django.utils import timezone
import datetime

class ActiveMedicineManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_ended=False).order_by('-end_date')

class Medicine(BaseEntityModel):
    class Meta:
        verbose_name = "Лекарство"
        verbose_name_plural = "Лекарства"

    title = models.CharField(verbose_name='Название', max_length=15)
    end_date = models.DateField(verbose_name='Последний день приема')
    today = models.IntegerField(verbose_name="Принято сегодня", default=0, validators=[MinValueValidator(0), ])
    amount_per_day = models.IntegerField(verbose_name='Кол-во раз в день', validators=[MinValueValidator(0),] )
    dosage = models.CharField(verbose_name='Дозировка за один прием', max_length=30, help_text='Например: 3 капсулы')
    comments = models.TextField(verbose_name='Комментарии')

    objects = models.Manager()
    active_medicine_sorted = ActiveMedicineManager()

    def __str__(self) -> str:
        return f'{self.title}: до {self.end_date}'
    
    def clean(self):
        if self.today > self.amount_per_day:
            raise ValidationError({'today': f'Значение должно быть не больше {self.amount_per_day}'})

    def save(self, *args, **kwargs):
        self.is_ended = self.is_medicine_over
        self.full_clean()  # Вызов clean() для валидации перед сохранением
        super(Medicine, self).save(*args, **kwargs)

    @property
    def is_medicine_over(self) -> bool:
        """ Проверяет, закончился ли прием лекарства. """
        current_timezone = timezone.get_current_timezone()
        current_date = timezone.now()
        medicine_date = self.end_date
        medicine_datetime = datetime.datetime.combine(medicine_date, datetime.time(0, 0), tzinfo=current_timezone)
        return medicine_datetime < current_date
