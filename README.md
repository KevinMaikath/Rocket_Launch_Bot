# Rocket Launch Bot

This project consists of a Telegram bot inside a [Django]((https://www.djangoproject.com)) API that guesses the exact
frame in which a rocket is launched in the video [Falcon Heavy Test Flight](https://www.youtube.com/watch?v=wbSwFU6tY1c)
with the help of the user the bot is talking with. This Telegram Bot is managed by a webhook inside a RESTful API
developed with Django.

This API retrieves the video information and the frame images from
the [FrameX API](https://framex-dev.wadrid.net/api/video/). The Telegram bot is then able to interact with the user
sending these images and asking whether the rocket has been launched yet or not. The exact frame in which the rocket is
launched is calculated using the [bisection method](https://en.wikipedia.org/wiki/Bisection_method) with the help of the
users answers.

## Why Django ?

Before answering that question comes another one: "Why a RESTful API?".

A Telegram bot can be developed with a single python script. Using
the [python-telegram-bot](https://pypi.org/project/python-telegram-bot/) library you can even run a simple HTTP server
in order to set a webhook. However, running a whole project in a single script isn't usually a good practice, no matter
how small it is. Setting up a small RESTful API to manage a webhook might be a better idea.

Then again: Why Django in particular ?

Thanks to the python-telegram-bot library it is really easy to manage a Telegram bot using python, and with the
[django-rest-framework](https://www.django-rest-framework.org) you can manage to build a Django RESTful API project in a
matter of minutes. I developed this project using both of them, and this brought me the following advantages against the
single-script solution:

* Scalability: this is the main reason why I used a framework like Django. All the bot-related code is encapsulated in a
  Django "app" inside the project. This way, it would be possible to add more apps in order to enrich the overall
  project and bring more features easily.
* Data persistence: it is easier to manage a database connection inside an API with multiple scripts rather than a
  "spaghetti-code" solution.
* Deployment: it is easier and safer to deploy an API with the settings and security that brings a framework like
  Django.

## Project set-up

In order to reproduce this project with a full operational bot, you will need to:

1. Create and connect a telegram bot
2. Install the project dependencies
3. Set-up a database

### Telegram bot

A Telegram bot can be easily created following the official [Telegram bot documentation](https://core.telegram.org/bots)
.

Once you've created your bot, you can connect it to the Django API as follows:

1. In the Django API, you just need to set the bot token provided by the BotFather. This project is prepared for doing
   this with environment variables, so you can just run the API with an environment variable called `TELEGRAM_BOT_TOKEN`
   or just replace it wherever is needed inside the project.

2. Using the Telegram bot API, set the webhook URL for your bot. This way Telegram will know where to send a request (
   via HTTP POST) everytime a user sends a message to your bot. You can set the webhook by sending an HTTP GET request
   to:

```html
https://api.telegram.org/bot
<TELEGRAM_BOT_TOKEN>/setWebhook?url=
    <URL_TO_YOUR_API_WEBHOOK>
```

### Dependencies

This project has been developed using a virtual environment. The following steps will help you to install all the
project dependencies in a virtual environment called "venv":

1. Install [pip](https://pypi.org/project/pip/) if necessary.
2. Install [virtualenv](https://pypi.org/project/virtualenv/) if necessary. Open your terminal and run the next command:

```Shell
pip install virtualenv
```

3. Inside the project's root directory, create a new virtual environment.

```Shell
virtualenv venv
```

4. Inside "venv", install the project dependencies.

```Shell
pip install -r requirements.txt
```

### Database

In order to be able to manage the state of multiple conversations at the same time as well as saving those states in a
persistent way, this projects uses a simple MongoDB connection using [djongo](https://pypi.org/project/djongo/).

You just need to set the following environment variables to set up a connection to a MongoDB cluster:

* `MONGO_CLUSTER`
* `MONGO_USERNAME`
* `MONGO_PASSWORD`

If the cluster is successfully connected to the project, the Django API will automatically create a collection
named `chats` where it will save the state of the chats.

As this project consists mainly in the Telegram bot management, no authentication is needed. Therefore, there's no need
to execute the usual initial database migration of Django apps.

## API usage

In order to run the Django API, you will need to set all of the following environment variables:

* `SECRET_KEY`: your Django project secret key.
* `API_URL`: URL denoting where is your API hosted. Needed for including it in the settings allowed-hosts.
* `MONGO_CLUSTER`, `MONGO_USERNAME`, `MONGO_PASSWORD`: database connection.
* `TELEGRAM_BOT_TOKEN`

Optional variables:

* `DEBUG_MODE`: if set to "True", the Django app will run in debug mode.

Once all the environment variables are set up, you can start the app by running the following command in the project
root directory:

```shell
python manage.py runserver
```

## API Deploy

This project is fully prepared to be deployed using [Heroku](https://www.heroku.com). Just follow the official
documentation and remember to set up all the environment variables needed for this project before deploying it.
