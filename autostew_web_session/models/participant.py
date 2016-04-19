from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Min

from autostew_web_enums import models as enum_models


class Participant(models.Model):
    class Meta:
        ordering = ['race_position']

    parent = models.ForeignKey('self', null=True, blank=True)
    member = models.ForeignKey('Member', null=True, blank=True)  # AI will be NULL
    session = models.ForeignKey('Session')
    still_connected = models.BooleanField()

    ingame_id = models.IntegerField()
    refid = models.IntegerField()
    name = models.CharField(max_length=200)
    is_player = models.BooleanField()
    vehicle = models.ForeignKey('Vehicle', null=True, blank=True)  # NULL because AI owner change will do that
    livery = models.ForeignKey('Livery', null=True, blank=True)  # NULL because AI owner change will do that
    accumulated_crash_points = models.IntegerField(default=0)

    grid_position = models.IntegerField()
    race_position = models.IntegerField()
    current_lap = models.IntegerField()
    current_sector = models.IntegerField()
    sector1_time = models.IntegerField()
    sector2_time = models.IntegerField()
    sector3_time = models.IntegerField()
    last_lap_time = models.IntegerField()
    fastest_lap_time = models.IntegerField()
    state = models.ForeignKey(enum_models.ParticipantState)
    headlights = models.BooleanField()
    wipers = models.BooleanField()
    speed = models.IntegerField()
    gear = models.SmallIntegerField()
    rpm = models.IntegerField()
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    position_z = models.IntegerField()
    orientation = models.IntegerField()
    total_time = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('session:participant', args=[str(self.session.id), str(self.ingame_id)])

    def create_snapshot(self, session_snapshot):
        snapshot = Participant.objects.get(pk=self.pk)
        snapshot.pk = None
        snapshot.parent = self
        snapshot.session = session_snapshot
        snapshot.save()
        return snapshot

    def send_chat(self, message, server):
        return server.send_chat(message, self.refid)

    def kick(self, server, ban_seconds):
        return server.kick(self.refid, ban_seconds)

    def gap(self):
        if self.race_position == 1:
            return None
        if self.session.session_stage.name.startswith("Race") or self.session.finished:
            if not self.total_time:
                return None
            return self.total_time - Participant.objects.get(session=self.session, race_position=1).total_time
        else:
            if not self.fastest_lap_time:
                return None
            return self.fastest_lap_time - Participant.objects.get(session=self.session, race_position=1).fastest_lap_time
