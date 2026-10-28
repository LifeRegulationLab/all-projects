# Postiz on the Mac

Repo: https://github.com/gitroomhq/postiz-app (gitroomhq, v1.47.0, AGPL-3.0).
Postiz runs in Docker. The repo's docker-compose.yaml starts Postiz, Postgres, Redis, Temporal and Elasticsearch. You do not build anything; the app image is pulled ready-made.

Allow about 6 GB of disk for the images and 15 minutes the first time.

## 1. Install Docker Desktop (skip if already installed)

```zsh
brew install --cask docker
open -a Docker
```

Wait until the whale icon in the menu bar stops animating. Check it is ready:

```zsh
docker compose version
```

## 2. Get the repo

```zsh
git clone --depth 1 https://github.com/gitroomhq/postiz-app ~/postiz
cd ~/postiz
```

## 3. Set a secret

The compose file ships with a placeholder JWT secret. Replace it with a random one:

```zsh
sed -i '' "s|JWT_SECRET: '.*'|JWT_SECRET: '$(openssl rand -hex 32)'|" docker-compose.yaml
grep JWT_SECRET docker-compose.yaml
```

## 4. Start it

```zsh
docker compose up -d
```

The first run downloads the images. When `docker compose ps` shows every container as running or healthy, open:

http://localhost:4007

Register with any email and password. There is no email service configured, so the account is activated at once. After your own account is made you can close registration by changing `DISABLE_REGISTRATION: 'false'` to `'true'` in docker-compose.yaml and running `docker compose up -d` again.

## Day to day

| Do | Command (from ~/postiz) |
| --- | --- |
| Stop | `docker compose down` |
| Start again | `docker compose up -d` |
| Update to the latest | `docker compose pull && docker compose up -d` |
| See logs | `docker compose logs -f postiz` |
| Remove everything, including data | `docker compose down -v` |

Data lives in Docker volumes (postgres-volume, postiz-uploads, postiz-config), so `docker compose down` keeps it.

## Connecting channels

Self-hosted Postiz needs your own developer app for each platform (X, LinkedIn, YouTube, Facebook, Instagram, TikTok, Threads, Bluesky, Mastodon and so on). Each one is a client id and secret pasted into the `Social Media API Settings` block of docker-compose.yaml, then `docker compose up -d`. Reference: https://docs.postiz.com/providers. Meta, YouTube and TikTok approval can take weeks; X, LinkedIn, Bluesky and Mastodon are quick.

Keep the client secrets in `Desktop/Private - not in cloud/`, not in a project folder.

## Other ports it uses

4007 (Postiz), 7233 (Temporal), 8080 (Temporal UI), 8969 (Spotlight). If one is already taken on the Mac, change the left-hand number of that `ports:` line in docker-compose.yaml.
