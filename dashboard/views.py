from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from store.models import Product


# Create your views here.
def dashboard_with_pivot(request):
    return render(request, 'dashboard/dashboard_with_pivot.html', {})


def pivot_data(request):
    dataset = Product.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)

