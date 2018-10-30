# gists

Gists(posts) management

What it offers?

  1) Authenticate with GitHub account
  2) Create Gists(posts)
  3) Add comments to some Gists

Disclaimer:
  To save time and avoid additional setup for DB. The access token of an authenticated user will be encrypted and passed to the client side directly.
  Ideally on production, this access token should be saved in user db, e.g. Mongo, Mysql, etc.


<b>How to use it?</b>

  run: startup.sh


<b>Run Unit Test?</b>

  run: test.sh

<b>Build docker image</b>

  run: docker-build.sh
