# Generated by Django 4.2.4 on 2023-09-11 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_alter_workplace_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='workplace',
            name='dangerous_works',
            field=models.ManyToManyField(to='company.dangerouswork', verbose_name='Работы с повышенной опасностью'),
        ),
        migrations.AddField(
            model_name='workplace',
            name='is_need_internship',
            field=models.BooleanField(default=False, verbose_name='Требуется стажировка'),
        ),
        migrations.AddField(
            model_name='workplace',
            name='is_need_knowledge_test',
            field=models.BooleanField(default=False, verbose_name='Требуется проверка знаний'),
        ),
        migrations.AddField(
            model_name='workplace',
            name='knowledge_test_period',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Периодичность проверки знаний в месяцах'),
        ),
        migrations.AddField(
            model_name='workplace',
            name='medic_works',
            field=models.ManyToManyField(to='company.medicwork', verbose_name='Работы, требующие медосмотров'),
        ),
        migrations.AlterField(
            model_name='workplace',
            name='extra_description',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Дополнительное описание'),
        ),
        migrations.AlterField(
            model_name='workplace',
            name='factors',
            field=models.ManyToManyField(through='company.WorkplaceFactor', to='company.factor', verbose_name='Вредные и опасные производственные факторы'),
        ),
    ]
