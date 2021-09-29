from django.urls import path

from .views import *

app_name = 'ipledger'

urlpatterns = [
    path('', IndexView.as_view(), name='index' ),
    path('iplist/', IpBaseListView.as_view(), name='iplist'),
    path('seglist/', SegBaseListView.as_view(), name='seglist'),
    path('hostlist/', HostListView.as_view(), name='hostlist'),
    path('segcreate/', SegmentGenericView.as_view(), name='segcreate'),
    path('segdetail/<int:pk>', SegDetailView.as_view(), name='segdetail'),
    path('segdelete/<int:pk>', SegDeleteView.as_view(), name='segdelete'),
    path('hostdetail/<int:pk>', HostDetailView.as_view(), name='hostdetail'),
    path('hostcreate/', HostGenericView.as_view(), name='hostcreate'),
    path('hostupdate/<int:pk>', HostAssignView.as_view(), name='hostassign'),
    path('hostdelete/<int:pk>', HostDeleteView.as_view(), name='hostdelete')
]
