# Generated by Django 2.1.4 on 2019-05-06 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]