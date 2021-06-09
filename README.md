# Squawker

Squawker is a web application that allows a Twitter user to organize the people they follow into groups (known as "flocks") and view their timeline filtered by these groups. For example, a user may create a flock for "news" and another for "sports".

## How it's made
This application is created in the Python language using the Flask micro-framework. A WSGI server runs on a Digital Ocean droplet and uses a PostgreSQL database.

### Dependencies
1. Flask
2. Flask-SQLAlchemy
3. Tweepy

## Data Protection
No personal data is gathered in this application. The user logs in with Twitter directly using the OAuth workflow.

## Potential Future Features

Below are features that could be added to further enhance the application.

### Setup Page:
* Alphabetize your friends by (screen_name) or (name)
* When moving a friend from right to left, they go back to their alphabetized location
* Animate the friends below "sliding up" to fill the space when a friend moves to the other side

### Tweet Object:
* Replace URL, hashtag, mention by index instead of regular expression. This fixes the bug where 'Foo' is hyperlinked in a @FooBaz mention, for example.

### Login Page:
* Offer the following options:
  * Logout: Clears the session and redirects the user to the login page
  * Clear from this Browser: Clears the ID and key stored in the user's browser
  * Purge data (name TBD): Removes user's entry in the database

