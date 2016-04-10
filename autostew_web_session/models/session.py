from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import QuerySet, Max, Min

import autostew_web_session.models.participant
from autostew_web_enums import models as enum_models
from autostew_web_session.models.member import Member, MemberSnapshot
from autostew_web_session.models import models as session_models


class SessionSetup(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=100, blank=True)
    is_template = models.BooleanField()

    server_controls_setup = models.BooleanField(
        help_text="If true, players won't be able to control the race setup")
    server_controls_track = models.BooleanField(
        help_text="If true, players won't be able to control track selection")
    server_controls_vehicle_class = models.BooleanField(
        help_text="If true, players won't be acle to control vehicle class selection")
    server_controls_vehicle = models.BooleanField(
        help_text="If true, players won't be able to access vehicle selection")
    grid_size = models.IntegerField(
        help_text="How many cars can be on the field, don't set it higher than the track's grid size")
    max_players = models.IntegerField(
        help_text="How many human players can join the game")
    opponent_difficulty = models.IntegerField(
        help_text="AI difficulty, 0 to 100")

    force_identical_vehicles = models.BooleanField()
    allow_custom_vehicle_setup = models.BooleanField()
    force_realistic_driving_aids = models.BooleanField()
    abs_allowed = models.BooleanField(
        help_text="Won't have any effect if force realistic driving aids is on")
    sc_allowed = models.BooleanField(
        help_text="Won't have any effect if force realistic driving aids is on")
    tcs_allowed = models.BooleanField(
        help_text="Won't have any effect if force realistic driving aids is on")
    force_manual = models.BooleanField(
        help_text="If true, only manual transmission will be allowed")
    rolling_starts = models.BooleanField(
        help_text="If true, the race will have a rolling start")
    force_same_vehicle_class = models.BooleanField()
    fill_session_with_ai = models.BooleanField()
    mechanical_failures = models.BooleanField()
    auto_start_engine = models.BooleanField()
    timed_race = models.BooleanField(
        "If true, race length will be measured in minutes")
    ghost_griefers = models.BooleanField()
    enforced_pitstop = models.BooleanField()

    practice1_length = models.IntegerField(help_text="In minutes")
    practice2_length = models.IntegerField(help_text="In minutes")
    qualify_length = models.IntegerField(help_text="In minutes")
    warmup_length = models.IntegerField(help_text="In minutes")
    race1_length = models.IntegerField(help_text="In laps or minutes")
    race2_length = models.IntegerField(help_text="In laps or minutes (this setting does not have any effect (yet?)")

    public = models.BooleanField(
        help_text="If true, this game will be listed in the multiplayer server search (implies friends_can_join)")
    friends_can_join = models.BooleanField(help_text="If true, the players' friend will be able to join")
    damage = models.ForeignKey('autostew_web_enums.DamageDefinition', null=True)
    tire_wear = models.ForeignKey('autostew_web_enums.TireWearDefinition', null=True)
    fuel_usage = models.ForeignKey('autostew_web_enums.FuelUsageDefinition', null=True)
    penalties = models.ForeignKey('autostew_web_enums.PenaltyDefinition', null=True)
    allowed_views = models.ForeignKey('autostew_web_enums.AllowedViewsDefinition', null=True)
    track = models.ForeignKey('Track', null=True, blank=True)
    vehicle_class = models.ForeignKey('VehicleClass', null=True, blank=True,
        help_text="Only has a real effect if force_same_vehicle_class")
    vehicle = models.ForeignKey('Vehicle', null=True, blank=True,
        help_text="Only has a real effect if force_same_vehicle")
    date_year = models.IntegerField(help_text="Race date, set to 0 for 'real date'")
    date_month = models.IntegerField(help_text="Race date, set to 0 for 'real date'")
    date_day = models.IntegerField(help_text="Race date, set to 0 for 'real date'")
    date_hour = models.IntegerField()
    date_minute = models.IntegerField()
    date_progression = models.IntegerField(
        help_text="Time multiplier, unconfirmed allowed values: 0, 1, 2, 5, 10, 30, 60"
    )
    weather_progression = models.IntegerField(
        help_text="Weather progression multiplier, unconfirmed allowed values: 0, 1, 2, 5, 10, 30, 60"
    )
    weather_slots = models.IntegerField(
        help_text="Set to 0 for 'real weather'"
    )
    weather_1 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True, blank=True)
    weather_2 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True, blank=True)
    weather_3 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True, blank=True)
    weather_4 = models.ForeignKey('autostew_web_enums.WeatherDefinition', related_name='+', null=True, blank=True)
    game_mode = models.ForeignKey('autostew_web_enums.GameModeDefinition', related_name='+', null=True, blank=True)
    track_latitude = models.IntegerField(
        help_text="Setting this value won't have any effect")  # TODO this should be on track model
    track_longitude = models.IntegerField(
        help_text="Setting this value won't have any effect")  # TODO this should be on track model
    track_altitude = models.IntegerField(
        help_text="Setting this value won't have any effect")  # TODO this should be on track model

    def get_track_url(self):
        if self.force_identical_vehicles:
            get = '?vehicle={}'.format(self.vehicle.ingame_id)
        elif self.force_same_vehicle_class:
            get = '?vehicle_class={}'.format(self.vehicle_class.ingame_id)
        else:
            get = ''
        return "{}{}".format(self.track.get_absolute_url(), get)

    def get_absolute_url(self):
        return reverse('session:setup', args=[str(self.id)])

    def get_fields(self):
        return [(field.verbose_name, field._get_val_from_obj(self)) for field in self.__class__._meta.fields]

    def __str__(self):
        return "{} ({})".format(self.name, "template" if self.is_template else "instance")


class Session(models.Model):
    class Meta:
        ordering = ['start_timestamp']

    server = models.ForeignKey('Server')
    setup_template = models.ForeignKey(SessionSetup, limit_choices_to={'is_template': True}, related_name='+',
                                       help_text="This setup is feeded to the game")
    setup_actual = models.ForeignKey(SessionSetup, limit_choices_to={'is_template': False}, related_name='+',
                                     null=True, blank=True,
                                     help_text="This setup is read from the game once the race starts")

    start_timestamp = models.DateTimeField(auto_now_add=True,  # TODO remove auto_now_add
                                           help_text="Time when the race starts/started")
    last_update_timestamp = models.DateTimeField(auto_now=True)
    planned = models.BooleanField(help_text="If true, this race was/is scheduled")
    schedule_time = models.TimeField(null=True, blank=True, help_text="Time this schedule will run")
    schedule_date = models.DateField(null=True, blank=True,
                                     help_text="Date this schedule will run, if blank will run daily")
    running = models.BooleanField(help_text="If true, this race is currently running")
    finished = models.BooleanField(help_text="If true, this race finished")

    max_member_count = models.IntegerField(null=True, blank=True)

    first_snapshot = models.ForeignKey("SessionSnapshot", null=True, blank=True, related_name='+')
    current_snapshot = models.ForeignKey("SessionSnapshot", null=True, blank=True, related_name='+')
    starting_snapshot_lobby = models.ForeignKey("SessionSnapshot", null=True, blank=True, related_name='+')
    starting_snapshot_to_track = models.ForeignKey("SessionSnapshot", null=True, blank=True, related_name='+')

    def get_absolute_url(self):
        return reverse('session:session', args=[str(self.id)])

    def __str__(self):
        return "{} - {}".format(self.id, self.setup_actual.name)

    def get_members_who_finished_race(self) -> QuerySet:
        results_stage = self.get_race_stage()
        if results_stage is None or results_stage.result_snapshot is None:
            return None
        snapshots = results_stage.result_snapshot.member_snapshots.all()
        return Member.objects.filter(membersnapshot__in=snapshots)

    def get_members_who_participated(self):
        participants = autostew_web_session.models.participant.Participant.objects.filter(lap__in=self.lap_set.all())
        return Member.objects.filter(participant__in=participants)

    def get_race_stage(self):
        try:
            results_stage = SessionStage.objects.get(
                session=self,
                stage__name="Race1"
            )
            return results_stage
        except SessionStage.DoesNotExist:
            return None


class SessionSnapshot(models.Model):
    class Meta:
        ordering = ['timestamp']

    session = models.ForeignKey(Session)
    is_result = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session_state = models.ForeignKey("autostew_web_enums.SessionState")
    session_stage = models.ForeignKey("autostew_web_enums.SessionStage")
    session_phase = models.ForeignKey("autostew_web_enums.SessionPhase")
    session_time_elapsed = models.BigIntegerField()
    session_time_duration = models.IntegerField()
    num_participants_valid = models.IntegerField()
    num_participants_disq = models.IntegerField()
    num_participants_retired = models.IntegerField()
    num_participants_dnf = models.IntegerField()
    num_participants_finished = models.IntegerField()
    current_year = models.IntegerField()
    current_month = models.IntegerField()
    current_day = models.IntegerField()
    current_hour = models.IntegerField()
    current_minute = models.IntegerField()
    rain_density_visual = models.IntegerField()
    wetness_path = models.IntegerField()
    wetness_off_path = models.IntegerField()
    wetness_avg = models.IntegerField()
    wetness_predicted_max = models.IntegerField()
    wetness_max_level = models.IntegerField()
    temperature_ambient = models.IntegerField()
    temperature_track = models.IntegerField()
    air_pressure = models.IntegerField()

    def get_absolute_url(self):
        return reverse('session:snapshot', args=[str(self.id)])

    def reorder_by_best_time(self):
        participants_with_fastest_lap_set = self.participantsnapshot_set.filter(fastest_lap_time__gt=0)
        for i, v in enumerate(participants_with_fastest_lap_set.order_by('fastest_lap_time')):
            v.race_position = i + 1
            v.save()
        positions_without_laptime = len(participants_with_fastest_lap_set) + 1
        for v in self.participantsnapshot_set.filter(fastest_lap_time=0):
            v.race_position = positions_without_laptime
            v.save()

    @property
    def previous_in_session(self):
        try:
            previous_timestamp = SessionSnapshot.objects.filter(
                timestamp__lt=self.timestamp,
                session=self.session,
            ).aggregate(Max('timestamp'))['timestamp__max']
            return SessionSnapshot.objects.get(
                timestamp=previous_timestamp,
                session=self.session
            )
        except self.DoesNotExist:
            return None

    @property
    def next_in_session(self):
        try:
            next_timestamp = SessionSnapshot.objects.filter(
                timestamp__gt=self.timestamp,
                session=self.session,
            ).aggregate(Min('timestamp'))['timestamp__min']
            return SessionSnapshot.objects.get(
                timestamp=next_timestamp,
                session=self.session
            )
        except self.DoesNotExist:
            return None


class SessionStage(models.Model):
    session = models.ForeignKey(Session, related_name='stages')
    stage = models.ForeignKey(enum_models.SessionStage)
    starting_snapshot = models.ForeignKey(SessionSnapshot, related_name='starting_of', null=True, blank=True)
    result_snapshot = models.ForeignKey(SessionSnapshot, related_name='result_of', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('session:session_stage', args=[str(self.session.id), str(self.stage.name)])