#!/usr/bin/python3

from mastodon import Mastodon
import os
import click
import yaml
import traceback
import hashlib

API_URL = ""
MEDIAPATH = "/opt/mastodon/media"
USERS_ENDPOINT = "/api/v1/pleroma/admin/users"
DEFAULT_SCOPES = ['read', 'write', 'follow', 'push']
ADMIN_SCOPES = DEFAULT_SCOPES + ['admin:read', 'admin:write']

def toot(mastodon, text, media):
  idempotency = hashlib.md5(mastodon.me()['id'].encode('utf-8') + text.encode('utf-8')).hexdigest()
  media = None

  if 'media' != "" and os.path.isfile("{0}/{1}".format(MEDIAPATH, media)):
    media = mastodon.media_post(media_file="{0}/{1}".format(MEDIAPATH, media))

  return mastodon.status_post(text, media_ids=media, idempotency_key=idempotency)


def create_app(login, secret_file, scopes=DEFAULT_SCOPES):
  Mastodon.create_app(
    '{0}_bot'.format(login),
    api_base_url = API_URL,
    to_file = secret_file,
    scopes=scopes
  )

  return Mastodon(
    client_id=secret_file,
    api_base_url=API_URL,
    feature_set="pleroma"
  )

def login_user(login, password, scopes=DEFAULT_SCOPES):
  secret_file = 'masto_bot/{0}.secret'.format(login)
  mastodon = create_app(login, secret_file, scopes)

  mastodon.log_in(
    username=login,
    password=password,
    to_file=secret_file,
    scopes=scopes
  )
  return mastodon

@click.command()
@click.option('--user', prompt='Username: ', help='User to toot as')
@click.option('--media', help='Media to toot')
@click.option('--config', default='/etc/mastobot/config.yaml', help='Mastobot config')
@click.option('--bootstrapconfig', default='/etc/mastobot/bootstrap.yaml', help='Mastobot Bootstrap config')
@click.argument('text')
def main(user, media, config, bootstrapconfig, text):
  """Simple program that toots texts or media as user"""

  global API_URL, MEDIAPATH

  with open(config) as f:
    mastobotconfig_dict = yaml.safe_load(f)

  with open(bootstrapconfig) as f:
    bootstrapconfig_dict = yaml.safe_load(f)

  MEDIAPATH = mastobotconfig_dict['mediapath']
  API_URL = "https://{0}".format(mastobotconfig_dict['server_name'])

  for bootstrap_user in bootstrapconfig_dict['mastodon_users']:
      if bootstrap_user['login'] == user:
          password = bootstrap_user['password']

  mastodon = login_user(user, password)
  print(toot(mastodon, text, media).url)

if __name__ == '__main__':
    main() # pylint: disable=no-value-for-parameter
