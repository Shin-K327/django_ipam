from django import forms

import ipaddress
import re

from .models import SegmentModels, HostModels, V4addressModels

V4ADDRESS_PATTERN = r'^([\d]{1,3}\.){3}[\d]{1,3}$'
HOSTNAME_PATTERN = r'^[a-zA-Z][0-9a-zA-Z\-]{0,14}$'


class IpNetworkForm(forms.models.ModelForm):

    class Meta:
        model = SegmentModels
        fields = ('segment_name', 'nw_address', 'prefix', 'seg_description')

    segment_name = forms.CharField(max_length=64)
    nw_address = forms.CharField(max_length=15)
    prefix = forms.IntegerField()
    seg_description = forms.CharField(max_length=128)

    def clean_nw_address(self):
        nw_address = self.cleaned_data['nw_address']

        if re.fullmatch(V4ADDRESS_PATTERN, nw_address) is None:
            raise forms.ValidationError(
                '正しいIPv4アドレスフォーマットで入力してください'
            )
        return nw_address

    def clean_prefix(self):
        prefix = self.cleaned_data['prefix']
        # 1677万件のレコード登録に対応できなさそうなのでクラスフルAセグメントの作成を制限中
        if prefix <= 15 or prefix >= 32:
            raise forms.ValidationError(
                'プレフィックスは16-31の間の値を指定してください'
            )
        return prefix

    def clean(self):
        nw_address = self.cleaned_data.get('nw_address')
        prefix = self.cleaned_data.get('prefix')

        try:
            host_object = ipaddress.ip_network(f'{nw_address}/{str(prefix)}').hosts()

            self.cleaned_data['hosts'] = [host.__str__() for host in host_object]

            if V4addressModels.objects.filter(host_address__in=self.cleaned_data['hosts']).exists():
                raise forms.ValidationError(
                    'ネットワーク範囲の重複が発生しています'
                )

        except ValueError as ve:
            raise forms.ValidationError(
                'ネットワークとプレフィックスの組み合わせが不適切です'
            )
        else:
            return self.cleaned_data


class HostnameForm(forms.ModelForm):

    class Meta:
        model = HostModels
        fields = ('hostname', 'host_description', 'kinds')

    hostname = forms.CharField(max_length=15)
    host_description = forms.CharField(max_length=128)

    def clean_hostname(self):
        hostname = self.cleaned_data['hostname']

        if re.fullmatch(HOSTNAME_PATTERN, hostname) is None:
            raise forms.ValidationError(
                'ホスト名は文字を先頭に英数及びハイフン(-)のみを使用し、15字以内で入力してください'
            )
        elif HostModels.objects.filter(hostname=hostname).exists():
            raise forms.ValidationError(
                '既に存在するホスト名は登録できません'
            )
        else:
            return hostname


class HostChoiceForm(forms.ModelForm):

    class Meta:
        model = V4addressModels
        fields = ('fore_host',)
