# Generated by Django 4.2.4 on 2023-09-04 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_alter_dangerouswork_company_alter_dangerouswork_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicwork',
            name='medical_period',
            field=models.SmallIntegerField(choices=[(None, 'Не требуется'), (1, '1 год'), (2, '2 года'), (3, '3 года')], default=2, verbose_name='Периодичность медосмотров'),
            preserve_default=False,
        ),
    ]
