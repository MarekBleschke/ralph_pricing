# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models as db
from django.utils.translation import ugettext_lazy as _
from lck.django.choices import Choices
from lck.django.common.models import (
    EditorTrackable,
    Named,
    TimeTrackable,
    WithConcurrentGetOrCreate,
)


PRICE_DIGITS = 16
PRICE_PLACES = 6


class TeamBillingType(Choices):
    _ = Choices.Choice
    time = _('By time')
    assets_cores = _('By assets and cores count')
    assets = _('By assets count')
    distribute = _(
        'Distribute cost to other teams proportionally to members count'
    )
    average = _('Average')


class Team(TimeTrackable, EditorTrackable, Named, WithConcurrentGetOrCreate):
    show_in_report = db.BooleanField(
        verbose_name=_("Show team in report"),
        default=True,
    )
    show_percent_column = db.BooleanField(
        verbose_name=_("Show percent column in report"),
        default=False,
    )
    billing_type = db.PositiveIntegerField(
        verbose_name=_("Billing type"),
        choices=TeamBillingType(),
        null=False,
        blank=False,
        default=TeamBillingType.time.id,
    )
    excluded_services = db.ManyToManyField(
        'Service',
        verbose_name=_("Excluded services"),
        related_name='excluded_teams',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")
        app_label = 'ralph_scrooge'

    def __unicode__(self):
        return self.name


class TeamDaterange(db.Model):
    team = db.ForeignKey(
        Team,
        verbose_name=_("Team"),
        related_name="dateranges",
        limit_choices_to={
            'billing_type': TeamBillingType.time,
        },
    )
    start = db.DateField()
    end = db.DateField()

    class Meta:
        verbose_name = _("Team daterange")
        verbose_name_plural = _("Teams dateranges")
        app_label = 'ralph_scrooge'

    def __unicode__(self):
        return '{} ({} - {})'.format(
            self.team,
            self.start,
            self.end,
        )

    def clean(self):
        if self.start > self.end:
            raise ValidationError('Start greater than start')


class TeamServiceEnvironmentPercent(db.Model):
    team_daterange = db.ForeignKey(
        TeamDaterange,
        verbose_name=_("team daterange"),
        related_name="percentage",
    )
    service_environment = db.ForeignKey(
        'ServiceEnvironment',
    )
    percent = db.FloatField(
        verbose_name=_("percent"),
        validators=[
            MaxValueValidator(100.0),
            MinValueValidator(0.0)
        ]
    )

    class Meta:
        verbose_name = _("Team service environment percent")
        verbose_name_plural = _("Teams services environments percent")
        unique_together = ('team_daterange', 'service_environment')
        app_label = 'ralph_scrooge'

    def __unicode__(self):
        return '{}/{} ({} - {})'.format(
            self.team_daterange.team,
            self.service_environment,
            self.team_daterange.start,
            self.team_daterange.end,
        )


class TeamCost(db.Model):
    team = db.ForeignKey(Team, null=False, blank=False)
    members_count = db.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("members count"),
        default=0,
    )
    cost = db.DecimalField(
        max_digits=PRICE_DIGITS,
        decimal_places=PRICE_PLACES,
        default=0.00,
        verbose_name=_("cost"),
    )
    forecast_cost = db.DecimalField(
        max_digits=PRICE_DIGITS,
        decimal_places=PRICE_PLACES,
        default=0.00,
        verbose_name=_("forecast cost"),
    )
    start = db.DateField()
    end = db.DateField()

    class Meta:
        verbose_name = _("Team cost")
        verbose_name_plural = _("Teams costs")
        app_label = 'ralph_scrooge'
