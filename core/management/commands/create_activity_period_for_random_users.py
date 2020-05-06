import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from core.models import ActivityPeriods, CustomUser


class Command(BaseCommand):
    """
    This class will be used to create new Activity Period Objects
    """

    help = 'Create random activity period for random Custom Users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int,
                            help='Indicates the number of activity period will be created for random custom users')

    def handle(self, *args, **kwargs):
        # This determines the total number of the Activity Periods needs to be created.
        total = kwargs['total']
        if total < 0:
            raise Exception('Please provide positive integer.')
        all_objects = CustomUser.objects.all()
        user_object_list = list(all_objects)
        # If length of list 0 then no users are present
        if len(user_object_list) > 0:
            for index in range(total):
                # Random CustomUser object will be chosen for activity period.
                custom_user_object = user_object_list[random.randint(0, len(user_object_list)-1)]
                user_uuid = custom_user_object.id
                start_time = datetime.now().strftime("%B %d %Y %I:%M %p")
                end_time = (datetime.now() + timedelta(minutes=random.randint(10, 60))).strftime("%B %d %Y %I:%M %p")
                # Creating a new Activity Period object
                response, error = ActivityPeriods.objects.create_activity_period(user_uuid=user_uuid,
                                                                                 start_time=start_time,
                                                                                 end_time=end_time)
                if error:
                    raise Exception(response)
                else:
                    print 'Activity Period object created with id %s for user_id %s' % (response.id, user_uuid)
        else:
            raise Exception('Currently no users are present, please add some users.')
