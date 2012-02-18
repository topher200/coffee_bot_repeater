# CoffeeBot Repeater

## Introduction
A new addition at FarSounder is CoffeeBot, an Android app that tweets when a
new pot of coffee is being brewed. This invention is widely regarded at a
historic moment in the history of mankind.

However, the glorious CoffeeBot just isn't good enough for SOME people. For
them, the CoffeeBot Repeater adds additional functionality.


## Usage
CoffeeBot Repeater runs as a small app on Heroku. It polls for updates from
@FSCoffeeBot, and repeats these updates as Twitter Direct Messages to
registered users.

Why not just have the tweets? Great question! Twitter DMs cause immediate
phone alerts, which is appearently very important to people are interested in
timely updates about coffee.


## Setup
The app will not run without these environment variables being set:

  - REDIS_HOST (ex: asdf.redistogo.com)
  - REDIS_PASS (ex: MyPasswordIs12345)
  - REDIS_PORT (ex: 9001)
  - SUPERTWEET_USER (ex: SuperTweetUsername)
  - SUPERTWEET_PASS (ex: SuperSecretPassword)

The easiest way to set these variables is using Foreman with a '.env' file;
this allows identical variables to be used locally and in production. More
information can be found in the Heroku documentation:
http://devcenter.heroku.com/articles/config-vars#local_setup


## Changelog 
v1.00: Initial release!


## Source
The source for this project is available on Github:
https://github.com/topher200/coffee_bot_repeater


## License
Copyright Topher Brown <topher200@gmail.com>, 2012. Released under the MIT 
license.
