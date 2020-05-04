# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view


@api_view(['GET'])
def health_check(request):
    response = {"Status": True}
    return JsonResponse(response, safe=False)
