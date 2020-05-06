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
            user_uuid = uuid.uuid1()
            # Creating a new Custom User object
            CustomUser.objects.create(id=user_uuid, real_name=get_random_string(),
                                      tz=random.choice(pytz.all_timezones))
            print 'Custom User object created with user_id %s' % user_uuid
