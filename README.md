# Ansible Role: mastodon

Ansible Module to install [mastodon](https://github.com/tootsuite/mastodon) via docker-compose.

## Requirements

- Ansible 2.10+
- Debian-based linux-distribution

## Configuration example

```yaml
- name: Configure mastodon
  hosts: mastodon
  roles: 
    - mastodon
  vars:
    mastodon_users:
      - login: "cert"
        email: "cert@fullscope.at"
        password: "certpassword"
        initial_toots:
          - text: "Cyber Cyber Cyber"
          - text: "Hello Masto"
          - text: "My cat"
            media: "katze.jpg"
        follow: ["user1", "user2"]
        account:
          bio: "CERT Protecting the Cyber"
          display_name: "Fullscope CERT"
          header: "eso1907a.jpg"
          avatar: "cs.jpg"
  tasks:
    - name: Deploy mastodon media
      become: true
      copy:
        src: mastodon_media/
        dest: "{{ mastodon_deploy_dir }}/media/"
```

## Role Variables

```yaml
instance_name: "AIT Mastodon"
```

```yaml
server_name: mastodon.local
```

```yaml
admin_user: ait@cyberrange.at
```

```yaml
admin_password: "password"
```

```yaml
# Has do be deployed to this location seperatly
ca_cert: "/usr/local/share/ca-certificates/ca.crt"
ssl_cert: "/etc/ssl/mastodon.crt"
ssl_key: "/etc/ssl/mastodon.key"
```

```yaml
mastodon_deploy_dir: /opt/mastodon
```

```yaml
# Initial User and toot creation see exmaple config
mastodon_users:
```

## Dependencies

None.

## Licence

GPL-3.0

## Author information

Benjamin Akhras
