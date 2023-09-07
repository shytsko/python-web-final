# Generated by Django 4.2.4 on 2023-09-07 20:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_alter_factorcondition_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workplace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('extra_description', models.CharField(max_length=100, verbose_name='Дополнительное описание')),
                ('code', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(message='Код должен соответствовать шаблону XXXX-XXX (X - число)', regex='^\\d{4}-\\d{3}$')], verbose_name='Код должности/профессии')),
                ('is_office_worker', models.BooleanField(default=False, editable=False, verbose_name='Должность служащего')),
                ('department', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='workplaces', to='company.department')),
            ],
        ),
        migrations.CreateModel(
            name='WorkplaceFactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_class', models.CharField(choices=[('2', '2'), ('3.1', '3.1'), ('3.2', '3.2'), ('3.3', '3.3'), ('3.4', '3.4'), ('4', '4')], max_length=3, verbose_name='Класс условий труда')),
                ('factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.factor')),
                ('workplace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.workplace')),
            ],
        ),
        migrations.AddField(
            model_name='workplace',
            name='factors',
            field=models.ManyToManyField(through='company.WorkplaceFactor', to='company.factor'),
        ),
    ]