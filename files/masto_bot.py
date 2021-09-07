#!/usr/bin/python3

from mastodon import Mastodon
import os
import click
import yaml
import traceback

API_URL = ""
MEDIAPATH = "/opt/mastodon/media"
USERS_ENDPOINT = "/api/v1/pleroma/admin/users"
DEFAULT_SCOPES = ['read', 'write', 'follow', 'push']
ADMIN_SCOPES = DEFAULT_SCOPES + ['admin:read', 'admin:write']

def toot(mastodon, text, media):
  if 'media' != "" and os.path.isfile("{0}/{1}".format(MEDIAPATH, media)):
    mastodon.media_post(media_file="{0}/{1}".format(MEDIAPATH, media), description=text)
  else:
    mastodon.toot(text)


def login_user(login, scopes=DEFAULT_SCOPES):
  secret_file = '../masto_bot/{0}.secret'.format(login)

  return Mastodon(
    client_id=secret_file,
    api_base_url=API_URL,
    feature_set="pleroma"
  )

@click.command()
@click.option('--user', prompt='Username: ', help='User to toot as')
@click.option('--media', help='Media to toot')
@click.option('--config', default='/etc/mastobot/config.yaml', help='Mastobot config')
@click.option('--bootstrapconfig', default='/etc/mastobot/bootstrap.yaml', help='Mastobot Bootstrap config')
@click.argument('text')
def main(user, media, config, text):
  """Simple program that toots texts or media as user"""

  global API_URL, MEDIAPATH

  with open(config) as f:
    mastobotconfig_dict = yaml.safe_load(f)

  MEDIAPATH = mastobotconfig_dict['mediapath']
  API_URL = "https://{0}".format(mastobotconfig_dict['server_name'])

  mastodon = login_user(user)
  toot(mastodon, text, media)

if __name__ == '__main__':
    main() # pylint: disable=no-value-for-parameter
