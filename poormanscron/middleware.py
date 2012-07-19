# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
from django.db import models
ScheduledTask = models.get_model("poormanscron", "ScheduledTask")

class PoorMansCronMiddleware(object):
    """Middleware that manages urls with subdomains
    """
    def process_response(self, request, response):
        """
        FeedBurner fetches RSS feeds every half an hour
        Google's and Yahoo's robots crawl and index webpages on a regular cycle
        """
        if 'HTTP_USER_AGENT' in request.META:
            agent = request.META['HTTP_USER_AGENT']
            # let's assume that request.is_spambot will be set to True when spammers are detected
            is_spambot = getattr(request, "is_spambot", False)
            if is_spambot or "Googlebot" in agent or "Slurp" in agent or "FeedBurner" in agent:
                now = datetime.now()
                from django.core.management import call_command
                tasks_to_execute = ScheduledTask.objects.filter(
                    is_active=True,
                    next_execution__lt=now,
                    )
                if is_spambot:
                    tasks_to_execute = tasks_to_execute.filter(is_heavy=True)
                for task in tasks_to_execute:
                    call_command(*task.command.split())
                    task.next_execution = now + timedelta(seconds = task.frequency * task.frequency_units)
                    task.save()
        return response
