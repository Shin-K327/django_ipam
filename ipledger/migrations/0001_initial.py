# Generated by Django 3.2.6 on 2021-09-07 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HostModels',
            fields=[
                ('host_id', models.AutoField(primary_key=True, serialize=False)),
                ('hostname', models.CharField(max_length=15, unique=True)),
                ('host_description', models.CharField(blank=True, max_length=128, null=True)),
                ('kinds', models.CharField(choices=[('server', 'サーバ'), ('network', 'ルータ/スイッチ'), ('client', 'クライアント'), ('gateway', 'ゲートウェイ'), ('other', 'その他機器')], max_length=30)),
                ('change_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'hosts',
            },
        ),
        migrations.CreateModel(
            name='SegmentModels',
            fields=[
                ('segment_id', models.AutoField(primary_key=True, serialize=False)),
                ('nw_address', models.CharField(max_length=15)),
                ('prefix', models.IntegerField()),
                ('seg_description', models.CharField(blank=True, max_length=128, null=True)),
                ('register_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'segment',
            },
        ),
        migrations.CreateModel(
            name='V4addressModels',
            fields=[
                ('v4address_id', models.AutoField(primary_key=True, serialize=False)),
                ('host_address', models.CharField(max_length=15, unique=True)),
                ('address_type', models.CharField(choices=[('service', 'サービス'), ('manage', '管理'), ('storage', 'ストレージ'), ('HA', '高可用性')], max_length=32)),
                ('fore_host', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ipledger.hostmodels')),
                ('fore_segment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ipledger.segmentmodels')),
            ],
            options={
                'db_table': 'v4address',
            },
        ),
    ]
