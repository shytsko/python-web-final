# Generated by Django 4.2.4 on 2023-09-02 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_factor_alter_dangerouswork_name_alter_medicwork_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dangerouswork',
            name='company',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='dangerous_works', to='company.company'),
        ),
        migrations.AlterField(
            model_name='dangerouswork',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='department',
            name='company',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='departments', to='company.company'),
        ),
        migrations.AlterField(
            model_name='factor',
            name='company',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='factors', to='company.company'),
        ),
        migrations.AlterField(
            model_name='factorcondition',
            name='condition_class',
            field=models.CharField(choices=[('2', '2'), ('3.1', '3.1'), ('3.2', '3.2'), ('3.3', '3.3'), ('3.4', '3.4'), ('4', '4')], max_length=250, verbose_name='Класс условий труда'),
        ),
        migrations.AlterField(
            model_name='factorcondition',
            name='factor',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='conditions', to='company.factor', verbose_name='Фактор'),
        ),
        migrations.AlterField(
            model_name='medicwork',
            name='company',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='medic_works', to='company.company'),
        ),
        migrations.AlterField(
            model_name='medicwork',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
        migrations.AlterUniqueTogether(
            name='dangerouswork',
            unique_together={('company', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='factor',
            unique_together={('company', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='medicwork',
            unique_together={('company', 'name')},
        ),
    ]