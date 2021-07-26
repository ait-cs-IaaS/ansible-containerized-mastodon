#!/usr/bin/python3

from mastodon import Mastodon
from os import path
import yaml
import click


@click.command()
@click.option('--user', prompt='Username: ', help='User to toot as')
@click.option('--media', help='Media to toot')
@click.option('--config', default='/etc/mastobot/config.yaml', help='Mastobot config')
@click.argument('text')
def main(user, media, config, text):
  """Simple program that toots texts or media as user"""
  with open(config) as f:
    config_dict = yaml.load(f)
  mastodon = Mastodon(
    access_token = "masto_bot/{0}.secret".format(user),
    api_base_url = "https://{0}".format(config_dict['server_name'])
  )
  if media != "" and path.isfile("{0}/{1}".format(config_dict['mediapath'], media)):
    mastodon.media_post(media_file="{0}/{1}".format(config_dict['mediapath'], media), description=text)
  else:
    mastodon.toot(text)

if __name__ == '__main__':
    main() # pylint: disable=no-value-for-parameter

