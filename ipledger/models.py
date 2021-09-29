from django.db import models

from django.core.exceptions import ValidationError
# Create your models here.

UNIT_KINDS = (
    ('server', 'サーバ'),
    ('network', 'ルータ/スイッチ'),
    ('client/static', 'クライアント/静的割当'),
    ('client/DHCP', 'クライアント/DHCP'),
    ('gateway', 'ゲートウェイ'),
    ('other', 'その他機器'),
)

ADDRESS_TYPE = (
    ('service', 'サービス'),
    ('manage', '管理'),
    ('storage', 'ストレージ'),
    ('HA', '高可用性')
)


class SegmentModels(models.Model):

    class Meta:
        db_table = 'segment'

    segment_id = models.AutoField(primary_key=True)
    segment_name = models.CharField(verbose_name='ネットワーク名', null=True, blank=True, max_length=64)
    nw_address = models.CharField(verbose_name='ネットワークアドレス', max_length=15, null=False, unique=True)
    prefix = models.IntegerField(verbose_name='プレフィックス長', null=False)
    seg_description = models.CharField(verbose_name='ネットワークの説明', max_length=128, null=True, blank=True)
    register_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.segment_id}_{self.nw_address}'


class HostModels(models.Model):
    class Meta:
        db_table = 'hosts'

    host_id = models.AutoField(primary_key=True)
    hostname = models.CharField(unique=True, max_length=15)
    host_description = models.CharField(null=True, blank=True, max_length=128)
    kinds = models.CharField(choices=UNIT_KINDS, max_length=30)
    change_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.host_id}_{self.hostname}'


class V4addressModels(models.Model):

    class Meta:
        db_table = 'v4address'

    v4address_id = models.AutoField(primary_key=True)
    host_address = models.CharField(unique=True, max_length=15)
    address_type = models.CharField(choices=ADDRESS_TYPE, max_length=32)
    fore_segment = models.ForeignKey(SegmentModels, null=True, blank=True, on_delete=models.CASCADE)
    fore_host = models.ForeignKey(HostModels, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.v4address_id}_{self.host_address}'
