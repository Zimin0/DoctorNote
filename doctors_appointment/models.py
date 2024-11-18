from django.db import models
from django.contrib.auth.models import User
from welcome.models import BaseEntityModel
from django.utils import timezone
import datetime

class ActiveAppointmentManager(models.Manager):
    """ Возвращает только неархивированные записи """
    def get_queryset(self):
        return super().get_queryset().filter(archived=False).order_by('-date', '-time')

class Appointment(BaseEntityModel):
    class Meta:
        verbose_name = "Запись к врачу"
        verbose_name_plural = "Записи к врачу"
         
    doctor = models.CharField(verbose_name="Врач", max_length=14, blank=False)  
    date = models.DateField(verbose_name="Дата", help_text="Формат: XX.XX.XXXX", blank=False)
    time = models.TimeField(verbose_name="Время", help_text="Формат: XX:XX", blank=False)
    address = models.CharField(verbose_name="Адрес", max_length=80, blank=False)
    office_number = models.CharField(verbose_name="Кабинет", max_length=6, blank=False)
    health_troubles = models.TextField(verbose_name="Жалобы", blank=True, null=True)
    report = models.TextField(verbose_name="Отчет после приема", blank=True, null=True)

    objects = models.Manager() # базовый 
    active_appointments_sorted = ActiveAppointmentManager() # кастомный 

    def __str__(self):
        return f'{self.doctor}: {self.date} в {self.time}'
    
    def save(self, *args, **kwargs):
        self.is_ended = self.is_appointment_over
        super(Appointment, self).save(*args, **kwargs)
    
    @property
    def is_report_was_added(self) -> bool:
        """ Был ли загружен отчет. """
        formatted = self.report.strip().strip('.').strip(',')
        return len(formatted) >= 3

    @property
    def is_appointment_over(self) -> bool:
        """ Проверяет, прошла ли встреча у доктора исходя из назначенного времени."""
        current_timezone = timezone.get_current_timezone()
        current_datetime = timezone.now()
        appointment_datetime = datetime.datetime.combine(self.date, self.time)
        appointment_datetime = appointment_datetime.replace(tzinfo=current_timezone)
        return appointment_datetime < current_datetime