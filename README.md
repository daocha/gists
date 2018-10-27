# gists

Gists(posts) management

What it offers?

1) Authenticate with GitHub account
2) Create Gists(posts)
3) Add comments to some Gists

Disclaimer:
  To save time and avoid additional setup for DB. The access token of a authenticated user will be passed to the client side directly. This is insecure.
  Ideally on production, this access token should be saved in user db, e.g. Mongo, Mysql, etc.


How to use it?

  run: startup.sh
