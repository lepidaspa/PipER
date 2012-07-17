from datetime import datetime
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.db import models
from django.conf import settings

FREQUENCY_UNIT_CHOICES = (
    (1, _("s")),
    (60, _("min")),
    (3600, _("h")),
    (3600 * 24, _("d")),
    (3600 * 24 * 7, _("wk")),
)

class ScheduledTask(models.Model):
    command = models.CharField(_("command"), help_text=_("management command with its parameters, i.e. 'flush --noinput'"), max_length=255)
    next_execution = models.DateTimeField(_("next execution"), default=datetime.now)
    frequency = models.IntegerField(_("frequency"))
    frequency_units = models.IntegerField(_("frequency units"), choices=FREQUENCY_UNIT_CHOICES)
    is_active = models.BooleanField(_("active"))
    is_heavy = models.BooleanField(_("heavy"), help_text=_("Does it require long time to execute? Heavy tasks will be triggered only by bad bots."))

    class Meta:
        verbose_name = _("scheduled task")
        verbose_name_plural = _("scheduled tasks")
        ordering = ("command",)
    
    def __unicode__(self):
        return force_unicode(self.command)
    
    def frequency_admin_display(self):
        return ugettext("Every %s %s") % (
            self.frequency,
            self.get_frequency_units_display(),
            )
    frequency_admin_display.short_description = _("frequency")

    def ready_admin_display(self):
        return datetime.now() > self.next_execution and """<img alt="1" src="/admin/media/img/admin/icon-yes.gif"/>""" or """<img alt="0" src="/admin/media/img/admin/icon-no.gif"/>"""
    ready_admin_display.short_description = _("ready to be called")
    ready_admin_display.allow_tags = True
