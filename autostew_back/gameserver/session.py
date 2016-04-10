from autostew_back.gameserver.abstract_containers import AbstractAttribute, AbstractAttributeLinkedToList, \
    AbstractFlagAttribute, AbstractStatusTable, AbstractAttributeLinkedToEnum
from autostew_web_session.models.session_enums import SessionFlags, SessionState, SessionStage, SessionPhase, Privacy


class SessionAttribute(AbstractAttribute):
    type_name_in_list = 'session'
    type_name_in_method = 'session'


class SessionAttributeLinkedToList(AbstractAttributeLinkedToList):
    type_name_in_list = 'session'
    type_name_in_method = 'session'


class SessionAttributeLinkedToEnum(AbstractAttributeLinkedToEnum):
    type_name_in_list = 'session'
    type_name_in_method = 'session'


class SessionFlagAttribute(AbstractFlagAttribute):
    type_name_in_list = 'session'
    type_name_in_method = 'session'


class Session(AbstractStatusTable):
    def __init__(self, attr_list, lists, api):
        self.attr_list = attr_list

        def _session_attribute(name):
            return SessionAttribute(self._from_list(name), api)

        self.server_controls_setup = _session_attribute('ServerControlsSetup')  # bool
        self.server_controls_track = _session_attribute('ServerControlsTrack')  # bool
        self.server_controls_vehicle_class = _session_attribute('ServerControlsVehicleClass')  # bool, Remember FORCE flag
        self.server_controls_vehicle = _session_attribute('ServerControlsVehicle')  # bool, Remember FORCE flag
        self.grid_size = _session_attribute('GridSize')
        self.max_players = _session_attribute('MaxPlayers')
        self.opponent_difficulty = _session_attribute('OpponentDifficulty')
        self.flags = SessionFlagAttribute(self._from_list('Flags'), api, SessionFlags)
        self.practice1_length = _session_attribute('Practice1Length')
        self.practice2_length = _session_attribute('Practice2Length')
        self.qualify_length = _session_attribute('QualifyLength')
        self.warmup_length = _session_attribute('WarmupLength')
        self.race1_length = _session_attribute('Race1Length')
        self.race2_length = _session_attribute('Race2Length')
        self.privacy = SessionAttributeLinkedToEnum(self._from_list('Privacy'), api, Privacy)
        self.damage = SessionAttributeLinkedToList(
            self._from_list('DamageType'),
            api,
            lists[ApiListNames.damage],
            'value'
        )
        self.tire_wear = SessionAttributeLinkedToList(
            self._from_list('TireWearType'),
            api,
            lists[ApiListNames.tire_wears],
            'value'
        )
        self.fuel_usage = SessionAttributeLinkedToList(
            self._from_list('FuelUsageType'),
            api,
            lists[ApiListNames.fuel_usages],
            'value'
        )
        self.penalties = SessionAttributeLinkedToList(
            self._from_list('PenaltiesType'),
            api,
            lists[ApiListNames.penalties],
            'value'
        )
        self.allowed_views = SessionAttributeLinkedToList(
            self._from_list('AllowedViews'),
            api,
            lists[ApiListNames.allowed_views],
            'value'
        )
        self.track = SessionAttributeLinkedToList(
            self._from_list('TrackId'),
            api,
            lists[ApiListNames.tracks],
            'id'
        )
        self.vehicle_class = SessionAttributeLinkedToList(
            self._from_list('VehicleClassId'),
            api,
            lists[ApiListNames.vehicle_classes],
            'value'
        )
        self.vehicle = SessionAttributeLinkedToList(
            self._from_list('VehicleModelId'),
            api,
            lists[ApiListNames.vehicles],
            'id'
        )
        self.date_year = _session_attribute('DateYear')
        self.date_month = _session_attribute('DateMonth')
        self.date_day = _session_attribute('DateDay')
        self.date_hour = _session_attribute('DateHour')
        self.date_minute = _session_attribute('DateMinute')
        self.date_progression = _session_attribute('DateProgression')  # Multiplier, 1 to 60
        self.weather_progression = _session_attribute('ForecastProgression')  # Multiplies, 1 to 30
        self.weather_slots = _session_attribute('WeatherSlots')  # Num of slots in use, 0 = real
        self.weather_1 = SessionAttributeLinkedToList(
            self._from_list('WeatherSlot1'),
            api,
            lists[ApiListNames.weathers],
            'value',
        )
        self.weather_2 = SessionAttributeLinkedToList(
            self._from_list('WeatherSlot2'),
            api,
            lists[ApiListNames.weathers],
            'value',
        )
        self.weather_3 = SessionAttributeLinkedToList(
            self._from_list('WeatherSlot3'),
            api,
            lists[ApiListNames.weathers],
            'value',
        )
        self.weather_4 = SessionAttributeLinkedToList(
            self._from_list('WeatherSlot4'),
            api,
            lists[ApiListNames.weathers],
            'value',
        )
        self.game_mode = SessionAttributeLinkedToList(
            self._from_list('GameMode'),
            api,
            lists[ApiListNames.game_modes],
            'value'
        )
        self.track_latitude = _session_attribute('Latitude')  # * 1000
        self.track_longitude = _session_attribute('Longitude')  # * 1000
        self.track_altitude = _session_attribute('Altitude')  # in mm
        self.session_state = SessionAttributeLinkedToEnum(self._from_list('SessionState'), api, SessionState)
        self.session_stage = SessionAttributeLinkedToEnum(self._from_list('SessionStage'), api, SessionStage)
        self.session_phase = SessionAttributeLinkedToEnum(self._from_list('SessionPhase'), api, SessionPhase)
        self.session_time_elapsed = _session_attribute('SessionTimeElapsed')  # Note that this value might currently start counting during loading and otehr transitions, and then reset back to zero when the race really starts
        self.session_time_duration = _session_attribute('SessionTimeDuration')  # Time elapsed since the start of the session, in seconds
        self.num_participants_valid = _session_attribute('NumParticipantsValid')  # No. of positions?
        self.num_participants_disq = _session_attribute('NumParticipantsDisqualified')
        self.num_participants_retired = _session_attribute('NumParticipantsRetired')
        self.num_participants_dnf = _session_attribute('NumParticipantsDNF')
        self.num_participants_finished = _session_attribute('NumParticipantsFinished')
        self.current_year = _session_attribute('CurrentYear')
        self.current_month = _session_attribute('CurrentMonth')
        self.current_day = _session_attribute('CurrentDay')
        self.current_hour = _session_attribute('CurrentHour')
        self.current_minute = _session_attribute('CurrentMinute')
        self.rain_density_visual = _session_attribute('RainDensity')  # 0 - 1000, visually
        self.wetness_path = _session_attribute('WetnessOnPath')  # 0 - 1000
        self.wetness_off_path = _session_attribute('WetnessOffPath')  # 0 - 1000
        self.wetness_avg = _session_attribute('WetnessAverage')  # 0 - 1000
        self.wetness_predicted_max = _session_attribute('WetnessPredictedMax')  # 0 - 1000
        self.wetness_max_level = _session_attribute('WetnessMaxLevel')  # 0 - 1000, physically
        self.temperature_ambient = _session_attribute('TemperatureAmbient')  # Celsius * 1000
        self.temperature_track = _session_attribute('TemperatureTrack')  # Celsius * 1000
        self.air_pressure = _session_attribute('AirPressure')

    def number_of_ai_players(self):
        if SessionFlags.fill_session_with_ai not in self.flags.get_flags():
            return 0
        else:
            return self.grid_size.get() - self.max_players.get()