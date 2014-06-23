#!/bin/bash

gpg --passphrase $PASSWORD -o ~/.ssh/id_rsa -d scripts/deploy_rsa.gpg
cp scripts/known_hosts ~/.ssh/known_hosts

case "$TRAVIS_BRANCH" in
  master)
    git remote add heroku git@heroku.com:bce-simulation.git
    git push heroku master 
    ;;
esac

