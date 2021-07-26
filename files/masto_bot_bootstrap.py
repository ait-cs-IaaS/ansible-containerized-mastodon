#!/usr/bin/python3

from mastodon import Mastodon
import os
import click
import yaml

API_URL = ""
MEDIAPATH = "/opt/mastodon/media"

def initialize_toots(mastodon, initial_toots=[]):
  for toot in initial_toots:
    if 'media' in toot and os.path.isfile("{0}/{1}".format(MEDIAPATH, toot['media'])):
      mastodon.media_post(media_file="{0}/{1}".format(MEDIAPATH, toot['media']), description=toot['text'])
    else:
      mastodon.toot(toot['text'])


def initialize_follows(mastodon, follow=[]):
  for uid in follow:
    mastodon.follows(uri=uid)


def update_account(mastodon, account):
  if 'display_name' in account:
    mastodon.account_update_credentials(display_name=account['display_name'])
  if 'bio' in account:
    mastodon.account_update_credentials(note=account['bio'])
  if 'avatar' in account:
    mastodon.account_update_credentials(avatar="{0}/{1}".format(MEDIAPATH, account['avatar']))
  if 'header' in account:
    mastodon.account_update_credentials(header="{0}/{1}".format(MEDIAPATH, account['header']))


def create_app(login, secret_file):
  Mastodon.create_app(
    '{0}_bot'.format(login),
    api_base_url = API_URL,
    to_file = secret_file
  )

  return Mastodon(
    client_id = secret_file,
    api_base_url = API_URL
  )

def register_user(login, email, password):
  secret_file = 'masto_bot/{0}.secret'.format(login)
  if os.path.isfile(secret_file):
    return login_user(login, email, password)

  mastodon = create_app(login, secret_file)

  mastodon.create_account(
      username=login,
      password=password,
      email=email,
      agreement=True,
      to_file=secret_file
  )
  return mastodon

def login_user(login, email, password):
  secret_file = 'masto_bot/{0}.secret'.format(login)
  mastodon = create_app(login, secret_file)

  mastodon.log_in(
    username=login,
    password=password,
    to_file=secret_file
  )
  return mastodon


@click.command()
@click.option('--mastobotconfig', default='/etc/mastobot/config.yaml', help='Mastobot config')
@click.option('--bootstrapconfig', default='/etc/mastobot/bootstrap.yaml', help='Mastobot Bootstrap config')
def main(mastobotconfig, bootstrapconfig):
  global API_URL, MEDIAPATH

  with open(mastobotconfig) as f:
    mastobotconfig_dict = yaml.safe_load(f)

  MEDIAPATH = mastobotconfig_dict['mediapath']
  API_URL = "https://{0}".format(mastobotconfig_dict['server_name'])

  is_bootstrapped = "{0}/../.masto_bot_bootstrapped".format(MEDIAPATH)
  if os.path.isfile(is_bootstrapped):
    exit(0)

  with open(bootstrapconfig) as f:
    config_dict = yaml.safe_load(f)

  login_user(config_dict['admin_user'].split('@')[0], config_dict['admin_user'], config_dict['admin_password'])

  for user in config_dict['mastodon_users']:
    try:
      mastodon = register_user(
        user['login'],
        user['email'],
        user.get('password', 'password')
      )
      if mastodon != None:
        initialize_toots(mastodon, user.get('initial_toots', []))
        initialize_follows(mastodon, user.get('follow', []))
        update_account(mastodon, user.get('account', []))
    except Exception as err:
      print("Error setting up: {0}\n{1}".format(user['login'], err))

    open(is_bootstrapped, 'a').close()


if __name__ == '__main__':
  main() # pylint: disable=no-value-for-parameter

