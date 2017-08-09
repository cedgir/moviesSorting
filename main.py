#!/usr/bin/env python
# coding:utf-8

import os
import shutil
import sys

import syslog

import settings
from model.allocine.movie import Movie
from model.allocine.tv_series import TvSeries
from search.allocine_search import AllocineSearch
from utils import mail
from utils import notification
from utils import utils

syslog.openlog('TorrentsSorting', 0, syslog.LOG_LOCAL0)

FILE_EXIST = 1

@Movie.register('start_treatment')
def treat_movie(movie):
    file_path = settings.MOVIE_HD_PATH + movie.genre[0]['$']
    file_name = utils.get_valid_filename(movie.title) + movie.info_file['extension']

    cur_file = torrent_dir + '/' + torrent_name
    new_file = file_path + '/' + file_name

    if os.path.isfile(new_file):
        return FILE_EXIST

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    shutil.copyfile(cur_file, new_file)

    mail_subject = u"[Torrents] Téléchargement du film \"" + movie.title + u"\" terminé !"
    mail_text = u"Le téléchargement du film \"" + movie.title + u"\" vient de se terminer."
    mail_html = u"""\
    <html>
      <head></head>
      <body>
        <a href="{movie_url}" style="text-decoration: none; color: #4A4A4A;">
          <table>
            <tr>
              <td>
                <img src="{image_url}"   height="300"/>
              </td>
              <td>
                <p style="font-size: 18px; padding: 0 0 0 5px;">
                  Le téléchargement de "{movie_title}" est maintenant terminé.
                </p>
              </td>
            </tr>
          </table>
        </a>
      </body>
    </html>
    """.format(movie_url=movie.link[0]['href'], image_url=movie.poster['href'], movie_title=movie.title)

    mail.send_mail(mail_subject, mail_text, mail_html)

    notif_subject = u"Téléchargement terminé !"
    notif_message = u"""\
    Le téléchargement du film "{movie_title}" est fini.
    """.format(movie_title=movie.title)

    notification.send_notif(notif_subject, notif_message, movie.link[0]['href'])

    syslog.syslog("Traitement du film \"" + movie.title + "\" termine.")


@TvSeries.register('start_treatment')
def treat_tvseries(tvseries):
    file_path = settings.TVSERIES_PATH + utils.get_valid_filename(tvseries.title) + '/Saison ' + str(tvseries.season)
    file_name = utils.get_valid_filename(
        tvseries.title) + ' - ' + tvseries.get_season_and_episode() + ' - ' + utils.get_valid_filename(
        tvseries.episode_info['title']) + tvseries.info_file['extension']

    cur_file = torrent_dir + '/' + torrent_name
    new_file = file_path + '/' + file_name

    if os.path.isfile(new_file):
        return FILE_EXIST

    if not os.path.exists(file_path):
        os.makedirs(file_path)
    shutil.copyfile(cur_file, new_file)

    mail_subject = u"[Torrents] Téléchargement de l'épisode \"" + tvseries.title + tvseries.get_season_and_episode() + u"\" terminé !"
    mail_text = u"Le téléchargement de l'épisode \"" + tvseries.title + u"\" vient de se terminer."
    mail_html = u"""\
        <html>
          <head></head>
          <body>
            <a href="{tvseries_url}" style="text-decoration: none; color: #4A4A4A;">
              <table>
                <tr>
                  <td>
                    <img src="{image_url}"   height="300"/>
                  </td>
                  <td>
                    <p style="font-size: 18px; padding: 0 0 0 5px;">
                      Le téléchargement de "{tvseries_title} saison {tvseries_season} épisode {tvseries_episode}" est maintenant terminé.
                    </p>
                  </td>
                </tr>
              </table>
            </a>
          </body>
        </html>
        """.format(tvseries_url=tvseries.link[0]['href'], image_url=tvseries.poster['href'],
                   tvseries_title=tvseries.title, tvseries_season=tvseries.season, tvseries_episode=tvseries.episode)

    mail.send_mail(mail_subject, mail_text, mail_html)

    notif_subject = u"Téléchargement terminé !"
    notif_message = u"""\
        Le téléchargement de l'épisode "{tvseries_title} {tvseries_season}" est fini.
        """.format(tvseries_title=tvseries.title, tvseries_season=tvseries.get_season_and_episode())

    notification.send_notif(notif_subject, notif_message, tvseries.link[0]['href'])

    syslog.syslog("Traitemnt de la serie \"" + tvseries.title + " " + tvseries.get_season_and_episode() + "\" termine.")


def treat_other():
    mail_subject = u"[Torrents] Téléchargement du fichier \"" + torrent_name + u"\" terminé !"
    mail_text = u"Le téléchargement du fichier \"" + torrent_name + u"\" vient de se terminer, mais n'a pas pu être traité automatiquement."
    mail_html = u"""\
       <html>
         <head></head>
         <body>
           <p style="font-size: 18px; padding: 0 0 0 5px;">
             Le téléchargement du fichier "{torrent_name}" est vient de se terminer, mais n'a pas pu être traité automatiquement.
           </p>
         </body>
       </html>
       """.format(torrent_name=torrent_name)

    mail.send_mail(mail_subject, mail_text, mail_html)

    notif_subject = u"Téléchargement terminé !"
    notif_message = u"""\
           Le téléchargement du fichier "{torrent_name}" est fini, mais il n'a pas pu être traité.
           """.format(torrent_name=torrent_name)

    notification.send_notif(notif_subject, notif_message)

    syslog.syslog("Traitement du fichier \"" + torrent_name + "\" termine.")


torrent_name = ''
torrent_path = ''
torrent_dir  = ''

if len(sys.argv) == 2:
    torrent_path = sys.argv[1]
    torrent_name = os.path.basename(torrent_path)
    torrent_dir = os.path.dirname(torrent_path)
elif len(sys.argv) == 3:
    torrent_name = sys.argv[1]
    torrent_dir = sys.argv[2]
    torrent_path = torrent_dir + '/' + torrent_name

if not torrent_name:
    torrent_name = torrent_dir

search = AllocineSearch()
media = None

if os.path.isdir(torrent_path):
    for file_basename in os.listdir(torrent_path):
        file = torrent_path + '/' + file_basename
        torrent_name = file_basename
        torrent_dir = torrent_path

        if os.path.isfile(file):
            media = search.find(file_basename)

            if media:
                media.treat('start_treatment')
else:
    media = search.find(torrent_name)

    if media:
        media.treat('start_treatment')
    else:
        treat_other()
