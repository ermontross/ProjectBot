[![Build Status](https://travis-ci.org/taylorjandrews/ProjectBot.svg?branch=master)](https://travis-ci.org/taylorjandrews/ProjectBot)

ProjectBot
=============

[![Build Status](https://travis-ci.org/ermontross/ProjectBot.svg?branch=master)](https://travis-ci.org/ermontross/ProjectBot)

## Overview
A Slack-bot designed for my CS Senior Project Team's Slack. Features:
-  Read members' daily stand-up messages and store what they committed to for the day
-  Tell member what he/she committed to upon request
-  Give member the daily and/or weekly schedule upon request
-  Let members know what tasks remain to complete the project

Based on the python-starter-bot from and hosted on [Beep Boop](https://beepboophq.com/docs/article/overview)

## Prereqs
1. You have already signed up with [Beep Boop](https://beepboophq.com) and have a local fork of this project.
* You have sufficient rights in your Slack team to configure a bot and generate/access a Slack API token.

## Usage

### Run locally
Install dependencies ([virtualenv](http://virtualenv.readthedocs.org/en/latest/) is recommended.)

	pip install -r requirements.txt
	export SLACK_TOKEN=<YOUR SLACK TOKEN>; python ./bot/app.py

If you want change the logging level, prepend `export LOG_LEVEL=<your level>; ` to the `python ./bot/app.py` command.

### Run locally in Docker
	docker build -t starter-python-bot .
	docker run --rm -it -e SLACK_TOKEN=<YOUR SLACK API TOKEN> starter-python-bot

### Run in BeepBoop
If you have linked your local repo with the Beep Boop service (check [here](https://beepboophq.com/0_o/my-projects)), changes pushed to the remote master branch will automatically deploy.

## Code Organization
If you want to add or change an event that the bot responds (e.g. when the bot is mentioned, when the bot joins a channel, when a user types a message, etc.), you can modify the `_handle_by_type` method in `event_handler.py`.

If you want to change the responses, then you can modify the `messenger.py` class, and make the corresponding invocation in `event_handler.py`.

The `slack_clients.py` module provides a facade of two different Slack API clients which can be enriched to access data from Slack that is needed by your Bot:

1. [slackclient](https://github.com/slackhq/python-slackclient) - Realtime Messaging (RTM) API to Slack via a websocket connection.
2. [slacker](https://github.com/os/slacker) - Web API to Slack via RESTful methods.

The `slack_bot.py` module implements and interface that is needed to run a multi-team bot using the Beep Boop Resource API client, by implementing an interface that includes `start()` and `stop()` methods and a function that spawns new instances of your bot: `spawn_bot`.  It is the main run loop of your bot instance that will listen to a particular Slack team's RTM events, and dispatch them to the `event_handler`.

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
