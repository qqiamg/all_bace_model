# Generated by Django 2.2 on 2020-01-16 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaceManber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名字')),
                ('year', models.CharField(max_length=20, verbose_name='年份')),
                ('work', models.CharField(max_length=20, verbose_name='工作')),
                ('place', models.CharField(max_length=20, verbose_name='地址')),
            ],
        ),
    ]
