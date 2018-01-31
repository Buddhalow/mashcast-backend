from django_cron import CronJobBase, Schedule
from models import Podcast


class PodcastJob(CronJobBase):
    RUN_EVERY_MINS = 120 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'mashcast.spider'    # a unique code

    def do(self):
        podcasts = Podcast.objects.all()
        for podcast in podcasts:
        	podcast.sync_episodes()
