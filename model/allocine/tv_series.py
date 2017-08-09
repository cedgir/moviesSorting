# coding:utf-8

from base import Base


class TvSeries(Base):
    __callbacks__ = {}

    def __init__(self, dictionary, info):
        super(TvSeries, self).__init__(dictionary, info)

        self.episode = info['episode']
        self.season = info['season'] if info['season'] else 1

    def get_season_and_episode(self):
        season_and_episode = ""

        if self.season:
            season_and_episode += "S" + str(self.season).zfill(2)

        if self.episode:
            season_and_episode += "E" + str(self.episode).zfill(2)

        season_and_episode.strip()

        return season_and_episode
