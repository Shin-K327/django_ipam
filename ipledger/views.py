from django.db.utils import IntegrityError
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import V4addressModels, SegmentModels, HostModels
from .forms import IpNetworkForm, HostnameForm, HostChoiceForm


# Viewの並びはCRUD順で、Indexだけトップに
class IndexView(TemplateView):
    template_name = 'index.html'


class SegmentGenericView(CreateView):
    template_name = 'create-seg.html'
    model = SegmentModels
    form_class = IpNetworkForm
    success_url = reverse_lazy('ipledger:seglist')

    def form_valid(self, form):
        record = form.save()
        hosts_object = []
        for i in form.cleaned_data.get('hosts'):
            hosts_object.append(V4addressModels(fore_segment_id=record.segment_id, host_address=i))

        V4addressModels.objects.bulk_create(hosts_object)

        return super().form_valid(form)


class HostGenericView(CreateView):
    template_name = 'create-host.html'
    model = HostModels
    form_class = HostnameForm
    success_url = reverse_lazy('ipledger:hostassign')


class HostGenericOnlyView(CreateView):
    template_name = 'create-host.html'
    model = HostModels
    form_class = HostnameForm
    success_url = reverse_lazy('ipledger:hostlist')


class IpBaseListView(ListView):
    template_name = 'iplist.html'
    model = V4addressModels


class SegBaseListView(ListView):
    template_name = 'seglist.html'
    model = SegmentModels


class HostListView(ListView):
    template_name = 'host-list.html'
    model = HostModels


class SegDetailView(ListView):
    template_name = 'seg-detail.html'
    model = V4addressModels

    def get(self, request, *args, **kwargs):
        self.filter_element = kwargs['pk']
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        filtered_model = self.model.objects.filter(fore_segment_id=self.filter_element)
        return filtered_model

    def post(self, request, *args, **kwargs):
        unassign_list = request.POST.getlist('unassign')
        self.model.objects.filter(pk__in=unassign_list).update(fore_host=None)
        messages.success(request, '選択したホストの割当を解除しました')
        return redirect('ipledger:segdetail', kwargs['pk'])

    def get_context_data(self):
        context = super().get_context_data()
        context['page_title'] = SegmentModels.objects.get(segment_id=self.filter_element).segment_name
        return context


class HostDetailView(DeleteView):
    template_name = 'host-detail.html'
    model = HostModels


class HostAssignView(UpdateView):
    template_name = 'hostassign.html'
    model = V4addressModels
    form_class = HostChoiceForm

    def get_success_url(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        refer_detail = V4addressModels.objects.get(v4address_id=pk).fore_segment.segment_id
        return reverse('ipledger:segdetail', kwargs={'pk': refer_detail})


class SegDeleteView(DeleteView):
    template_name = 'seg-delete.html'
    model = SegmentModels
    success_url = reverse_lazy('ipledger:seglist')


class HostDeleteView(DeleteView):
    template_name = 'host-delete.html'
    model = HostModels
    success_url = reverse_lazy('ipledger:hostlist')