# Generated by Django 3.2.8 on 2021-11-17 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('btitle', models.CharField(max_length=20, verbose_name='名称')),
                ('bpub_data', models.DateField(verbose_name='发布日期')),
                ('bread', models.IntegerField(default=0, verbose_name='阅读量')),
                ('bcomment', models.IntegerField(default=0, verbose_name='评论量')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
            ],
            options={
                'verbose_name': '图书',
                'verbose_name_plural': '图书',
                'db_table': 'tb_books',
            },
        ),
        migrations.CreateModel(
            name='Cal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_a', models.FloatField(max_length=10)),
                ('value_b', models.FloatField(max_length=10)),
                ('result', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='用户名')),
                ('pwd', models.CharField(max_length=20, verbose_name='密码')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'db_table': 'user_pwd',
            },
        ),
        migrations.CreateModel(
            name='HeroInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hname', models.CharField(max_length=20, verbose_name='姓名')),
                ('hgender', models.SmallIntegerField(choices=[(0, 'male'), (1, 'female')], default=0, verbose_name='性别')),
                ('hcomment', models.CharField(max_length=200, null=True, verbose_name='描述信息')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('hbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_1.bookinfo', verbose_name='图书')),
            ],
            options={
                'verbose_name': '英雄',
                'verbose_name_plural': '英雄',
                'db_table': 'tb_heros',
            },
        ),
    ]
