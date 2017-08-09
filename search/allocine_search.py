# coding:utf-8

import os
import PTN
import re
import settings

from lib.allocine import allocine
from model.allocine.movie import Movie
from model.allocine.tv_series import TvSeries


class AllocineSearch:
    api = None

    def __init__(self):
        self.api = allocine()
        self.api.configure(settings.ALLOCINE_SELF_CODE, settings.ALLOCINE_PARTNER_CODE)

    def find(self, filename):
        root_name = os.path.splitext(filename)[0]
        file_ext = os.path.splitext(filename)[1]

	search_name = self.cleanName(root_name)

        info_file = PTN.parse(search_name)
        info_file['extension'] = file_ext

        media_type = self.get_type(info_file)

        if media_type == settings.TYPE_TVSERIES:
            search_tvseries = self.api.search(info_file['title'], settings.TYPE_TVSERIES)

            if search_tvseries['feed']['totalResults'] > 0:
                tvseries = TvSeries(
                    self.api.tvseries(search_tvseries['feed'][settings.TYPE_TVSERIES][0]['code'], 'small')[
                        settings.TYPE_TVSERIES], info_file)
                seasons = self.api.tvseries(search_tvseries['feed'][settings.TYPE_TVSERIES][0]['code'], 'large')[
                    settings.TYPE_TVSERIES]['season']
                tvseries.season_info = filter(lambda season: season['seasonNumber'] == tvseries.season, seasons)[0]

                episodes = self.api.season(tvseries.season_info['code'], 'large')['season']['episode']
                tvseries.episode_info = \
                    filter(lambda episode: episode['episodeNumberSeason'] == tvseries.episode, episodes)[0]

                if 'title' not in tvseries.episode_info:
                    tvseries.episode_info['title'] = tvseries.episode_info['originalTitle']

                return tvseries

        elif media_type == settings.TYPE_MOVIE:
            search_movie = self.api.search(info_file['title'], settings.TYPE_MOVIE)

            if search_movie['feed']['totalResults'] > 0:
                movie = Movie(
                    self.api.movie(search_movie['feed'][settings.TYPE_MOVIE][0]['code'], 'small')[settings.TYPE_MOVIE],
                    info_file)
                return movie
        return False

    @staticmethod
    def get_type(info):
        if 'episode' in info or 'season' in info:
            return settings.TYPE_TVSERIES
        else:
            return settings.TYPE_MOVIE

    @staticmethod
    def cleanName(name):
        return re.sub(r'\[[^\]]*\]\s*(.*)', r'\1', name)
