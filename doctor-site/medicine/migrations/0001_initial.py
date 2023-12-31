# Generated by Django 4.2.3 on 2023-12-13 20:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('welcome', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('baseentitymodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='welcome.baseentitymodel')),
                ('title', models.CharField(max_length=15, verbose_name='Название')),
                ('end_date', models.DateField(verbose_name='Последний день приема')),
                ('today', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Принято сегодня')),
                ('amount_per_day', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Кол-во раз в день')),
                ('dosage', models.CharField(help_text='Например: 3 капсулы', max_length=30, verbose_name='Дозировка за один прием')),
                ('comments', models.TextField(verbose_name='Комментарии')),
            ],
            options={
                'verbose_name': 'Лекарство',
                'verbose_name_plural': 'Лекарства',
            },
            bases=('welcome.baseentitymodel',),
        ),
    ]