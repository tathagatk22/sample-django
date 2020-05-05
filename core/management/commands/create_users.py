import random
import uuid
import pytz

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from core.models import CustomUser


class Command(BaseCommand):
    """
    This class will be used to create new Custom User Objects
    """

    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of custom users to be created')

    def handle(self, *args, **kwargs):

        total = kwargs['total']
        if total < 0:
            raise Exception('Please provide positive integer')
        for index in range(total):
            # Random user_id, real_name and timezones will be allotted to a new CustomUser Object
            user_id = uuid.uuid1()
            timezones = tuple(pytz.common_timezones)
            # Creating a new Custom User object
            response, error = CustomUser.objects.create_user(user_id=user_id, real_name=get_random_string(),
                                                             tz=random.choice(timezones))
            if error:
                raise Exception(response)
            else:
                print 'Custom User object created with user_id %s' % user_id
