# Generated by Django 4.0.1 on 2022-03-19 09:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_userinput_is_modified'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinput',
            options={'get_latest_by': 'invoice_num', 'ordering': ['invoice_num']},
        ),
        migrations.AddField(
            model_name='userinput',
            name='igst_percent',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
