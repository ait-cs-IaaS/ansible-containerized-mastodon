#!/usr/bin/python3

from mastodon import Mastodon

Mastodon.create_app(
  'masto_bot',
  api_base_url = "https://{{ server_name }}",
  to_file = 'masto_bot.secret'
)

mastodon = Mastodon(
    client_id = 'masto_bot.secret',
    api_base_url = 'https://{{ server_name }}'
)
mastodon.log_in(
    '{{ admin_user }}',
    '{{ admin_password }}',
    to_file = 'masto_bot.secret'
)

mastodon.toot('Cyber Cyber Cyber')
