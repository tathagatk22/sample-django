# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view

from core.models import CustomUser, ActivityPeriods


@api_view(['GET'])
def health_check(request):
    """
    This API will be used to get health status of the application
    """
    response = {"Status": True}
    return JsonResponse(response, safe=False)


@api_view(['GET'])
def fetch_data(request):
    """
    This API will be used to fetch data for all custom users
    """
    json_response = {
        'ok': True,
        'members': []
    }
    try:

        user_json_list = []
        # all CustomUser object will be fetched
        all_objects = CustomUser.objects.all()
        user_object_list = list(all_objects)
        for user_object in user_object_list:
            user_json = {}
            # All ActivityPeriod objects will be fetched using custom user object as a foreign key
            all_objects = ActivityPeriods.objects.filter(user=user_object)
            activity_periods_object_list = list(all_objects)
            activity_periods_list = []
            for activity_periods_object in activity_periods_object_list:
                activity_periods_list.append({
                    'start_time': activity_periods_object.start_time,
                    'end_time': activity_periods_object.end_time,
                })
            user_json.update({
                'id': user_object.id,
                'real_name': user_object.real_name,
                'tz': user_object.tz,
                'activity_periods': activity_periods_list
            })
            user_json_list.append(user_json)
        json_response.update({'members': user_json_list})

    except Exception:

        json_response.update({'ok': False})

    finally:

        return JsonResponse(json_response, safe=False)
