from wise.station.publish import Publisher
from wise.station.updater import UpdaterHandler, UpdaterSet


class StationRegistry:
    def __init__(self):
        self.publishers: list[Publisher] = []
        self.updater_handlers: list[UpdaterHandler] = []
        self.kafka_updater_handlers: dict[str, UpdaterHandler] = {}
        self.periodic_updaters: UpdaterSet = UpdaterSet({})

    def set_publishers(self, publishers: list[Publisher]):
        self.publishers = publishers

    def set_updater_handlers(self, handlers: list[UpdaterHandler]):
        self.updater_handlers = handlers

    def set_kafka_updater_handlers(
        self, handlers: dict[str, UpdaterHandler]
    ):  # topic_name -> UpdaterHandler
        self.kafka_updater_handlers = handlers

    def set_periodic_updaters(self, updaters: UpdaterSet):
        self.periodic_updaters = updaters


station_registry = StationRegistry()
