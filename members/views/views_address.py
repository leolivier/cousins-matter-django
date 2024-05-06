import logging
# from pprint import pprint
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from ..models import Address
from ..forms import AddressUpdateForm

logger = logging.getLogger(__name__)

from cousinsmatter.utils import is_ajax, redirect_to_referer

class AddressDetailView(LoginRequiredMixin, generic.DetailView):
   model = Address

class AddressCreateView(LoginRequiredMixin, generic.CreateView):
   model = Address
   fields = "__all__"
   
class AddressUpdateView(LoginRequiredMixin, generic.UpdateView):
   model = Address
   fields = "__all__"

class ModalAddressCreateView(LoginRequiredMixin, generic.CreateView):
   model = Address
   fields = "__all__"
   def post(self, request, *args, **kwargs):
      if is_ajax(request):
         # create a form instance from the request and save it
         form = AddressUpdateForm(request.POST)
         # form = self.get_form()
         if form.is_valid():
            address = form.save()
            return JsonResponse({"address_id": address.id, "address_str": str(address)}, status=200)
         else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)

      return redirect_to_referer(request)

class ModalAddressUpdateView(LoginRequiredMixin, generic.UpdateView):
   model = Address
   fields = "__all__"
   def post(self, request, *args, **kwargs):
      address = get_object_or_404(Address, pk=kwargs['pk'])
      if is_ajax(request):
         # create a form instance and populate it with data from the request on existing member (or None):
         form = AddressUpdateForm(request.POST, instance=address)
         # form = self.get_form()
         if form.is_valid():
            address = form.save()
            return JsonResponse({"address_id": address.id, "address_str": str(address)}, status=200)
         else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)

      return redirect_to_referer(request)
