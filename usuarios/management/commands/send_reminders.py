import datetime
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from usuarios.views import create_notification_ionic_push_reminder
from usuarios.models import Reminder


# Class MUST be named 'Command'
class Command(BaseCommand):
    # Displayed from 'manage.py help mycommand'
    help = "Send notifications to users for reminders"

    # make_option requires options in optparse format
    option_list = BaseCommand.option_list + (
        make_option('--token', action='store',
                    dest='token',
                    default='',
                    help='Add token phone to send notifications'),
    )

    def handle(self, *app_labels, **options):
        """
        app_labels - app labels (eg. myapp in "manage.py reset myapp")
        options - configurable command line options
        """

        now = timezone.localtime(timezone.now())

        weekday = now.weekday()

        hour = now.hour
        minute = now.minute

        if weekday == 0:
            reminders = Reminder.objects.filter(monday=True, time=datetime.time(hour, minute))
        elif weekday == 1:
            reminders = Reminder.objects.filter(tuesday=True, time=datetime.time(hour, minute))
        elif weekday == 2:
            reminders = Reminder.objects.filter(wednesday=True, time=datetime.time(hour, minute))
        elif weekday == 3:
            reminders = Reminder.objects.filter(thursday=True, time=datetime.time(hour, minute))
        elif weekday == 4:
            reminders = Reminder.objects.filter(friday=True, time=datetime.time(hour, minute))
        elif weekday == 5:
            reminders = Reminder.objects.filter(saturday=True, time=datetime.time(hour, minute))
        elif weekday == 6:
            reminders = Reminder.objects.filter(sunday=True, time=datetime.time(hour, minute))
        else:
            reminders = None

        cont = 0
        for reminder in reminders:
            create_notification_ionic_push_reminder(reminder)
            cont += 1
		if cont > 0:
        	return "%s Notificaciones enviadas de recordatorios: %s" % (str(now), str(cont))
		else:
			return ""
