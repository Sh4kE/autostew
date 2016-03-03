import logging

from autostew_back.plugins import laptimes, crash_monitor, motd, db, db_reader, db_writer
from autostew_back.setups import prl_s4_r2_zolder_casual

logging.getLogger().setLevel(logging.INFO)
logging.getLogger('django.db.backends').setLevel(logging.INFO)


class Settings:
    host_name = "Host1"
    server_name = "Server1"
    config_file = "/home/joan/.steam/steam/SteamApps/common/Project CARS Dedicated Server/server.cfg"
    url = "http://localhost:9000"
    event_poll_period = 1
    full_update_period = 5

    setup_rotation = [
        prl_s4_r2_zolder_casual
    ]

    plugins = [
        db,
        db_reader,
        db_writer,
        laptimes,
        crash_monitor,
        motd,
    ]

