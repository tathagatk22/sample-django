import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from core.models import ActivityPeriods


class Command(BaseCommand):
    """
    This class will be used to create new Activity Period Objects
    """

    help = 'Create random activity period for custom user'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=str,
                            help='Indicates the user_id of a user for whom activity period needs to be created.')

    def handle(self, *args, **kwargs):
        # This determines the user_id of the CustomUser.
        user_id = kwargs['user_id']
        # Random end_time will be generated from start_time.
        start_time = datetime.now().strftime("%B %d %Y %I:%M %p")
        end_time = (datetime.now() + timedelta(minutes=random.randint(10, 60))).strftime("%B %d %Y %I:%M %p")
        # Creating a new Activity Period object
        response, error = ActivityPeriods.objects.create_activity_period(user=user_id,
                                                                         start_time=start_time, end_time=end_time)
        if error:
            raise Exception(response)
        else:
            print 'Activity Period object created with id %s for user_id %s' % (response.id, user_id)
