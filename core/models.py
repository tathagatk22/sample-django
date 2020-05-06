from django.db import models


class CustomUser(models.Model):
    """
    This model stores information regarding Custom User
    """

    id = models.UUIDField(primary_key=True)  # This will be used as id for the Custom User object
    real_name = models.CharField(max_length=255)  # This will be used as real name for the Custom User object
    tz = models.CharField(max_length=32)  # This will be used as TimeZone for the Custom User object

    objects = models.Manager()


# hook in the New Manager to our Model
class ActivityPeriodsManager(models.Manager):
    """
    This Manager handles operations regarding Activity Period
    """

    def create_activity_period(self, user_uuid, start_time, end_time):
        """
        This method will be used to create a new Activity Period
        :param user_uuid: This determines the user_id of the following ActivityPeriod
        :param start_time: This determines the start time of the ActivityPeriod
        :param end_time: This determines the end time of the ActivityPeriod
        :return response: Will return any Exception if occurred or else a new ActivityPeriod Object
        :return error: Will return True or False
        """
        response = None
        error = True
        try:
            # Here Exception can be occurred due to unavailability of the provided user_id
            custom_user_object = CustomUser.objects.get(
                pk=user_uuid)  # Trying to fetch the customUser Model object using provided user_id
            response = self.create(user=custom_user_object, start_time=start_time, end_time=end_time)
            error = False
        except Exception as e:
            response = e
        finally:
            return response, error


class ActivityPeriods(models.Model):
    """
    This model stores information regarding Activity Period
    """
    user = models.ForeignKey(CustomUser)  # This will be used as Foreign Key for CustomUser Model
    start_time = models.CharField(max_length=255)  # This will be used as start time for the activity period object
    end_time = models.CharField(max_length=255)  # This will be used as end time for the activity period object

    objects = ActivityPeriodsManager()
