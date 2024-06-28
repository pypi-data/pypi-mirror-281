from wise.station.publish import Publisher
from wise.station.updater import UpdaterHandler, UpdaterSet


class StationRegistry:
    def __init__(self):
        self.publishers: list[Publisher] = []
        self.updater_handlers: list[UpdaterHandler] = []
        self.periodic_updaters: UpdaterSet = UpdaterSet({})

    def add_publishers(self, publishers: list[Publisher]):
        self.publishers = publishers

    def add_updater_handlers(self, handlers: list[UpdaterHandler]):
        self.updater_handlers = handlers

    def add_periodic_updaters(self, updaters: UpdaterSet):
        self.periodic_updaters = updaters


station_registry = StationRegistry()
