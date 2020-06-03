# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import uuid
from datetime import datetime, timedelta

import pytz
from django.http import JsonResponse
# Create your views here.
from django.utils.crypto import get_random_string
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


@api_view(['POST'])
def create_user(request):
    """
    This API will be used to fetch data for all custom users
    """
    json_response = {
        'ok': True,
        'member_details': {}
    }
    try:
        user_uuid = uuid.uuid1()
        tz = random.choice(pytz.all_timezones)
        random_string = get_random_string()
        # Creating a new Custom User object
        CustomUser.objects.create(id=user_uuid, real_name=random_string,
                                  tz=tz)

        json_response.update({'member_details': {
            'id': user_uuid,
            'real_name': random_string,
            'tz': tz,
            'activity_periods': []
        }})

    except Exception:

        json_response.update({'ok': False})

    finally:

        return JsonResponse(json_response, safe=False)

@api_view(['POST'])
def create_activity_period(request):
    activity_period_details = []
    json_response = {
        'ok': True,
        'activity_period_details': []
    }
    try:
        all_objects = CustomUser.objects.all()
        user_object_list = list(all_objects)
        # If length of list 0 then no users are present
        if len(user_object_list) > 0:
            for index in range(10):
                # Random CustomUser object will be chosen for activity period.
                custom_user_object = user_object_list[random.randint(0, len(user_object_list) - 1)]
                user_uuid = custom_user_object.id
                start_time = datetime.now().strftime("%B %d %Y %I:%M %p")
                end_time = (datetime.now() + timedelta(minutes=random.randint(10, 60))).strftime(
                    "%B %d %Y %I:%M %p")
                # Creating a new Activity Period object
                response, error = ActivityPeriods.objects.create_activity_period(user_uuid=user_uuid,
                                                                                 start_time=start_time,
                                                                                 end_time=end_time)
                if error:
                    raise Exception(response)
                else:
                    activity_period_details.append({'user_uuid': user_uuid,
                                                    'start_time': start_time,
                                                    'end_time': end_time})
            json_response.update({'activity_period_details': activity_period_details})
    except Exception:

        json_response.update({'ok': False})

    finally:

        return JsonResponse(json_response, safe=False)
