# D1g1t Back-end Test Assignment

<!-- TOC -->
* [D1g1t Back-end Test Assignment](#d1g1t-back-end-test-assignment)
  * [Assumptions](#assumptions)
    * [Method](#method)
    * [The levels of happiness have the following ranges:](#the-levels-of-happiness-have-the-following-ranges-)
    * [High Level Solution Design](#high-level-solution-design)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
    * [How to run it?](#how-to-run-it)
      * [Go to the cloned directory:](#go-to-the-cloned-directory-)
      * [Build the application:](#build-the-application-)
      * [Apply Django migrations:](#apply-django-migrations-)
      * [Create superuser:](#create-superuser-)
      * [Run the application:](#run-the-application-)
  * [Tests](#tests)
  * [Endpoints](#endpoints)
    * [Authentication `/api/token/`](#authentication-apitoken)
      * [Response](#response)
    * [CREATE Daily Check-in `/daily/v1/api/`](#create-daily-check-in-dailyv1api)
      * [The score is calculated by summing up the responses to the following questions/criteria:](#the-score-is-calculated-by-summing-up-the-responses-to-the-following-questionscriteria-)
      * [The scale (responses):](#the-scale--responses--)
      * [Example](#example)
    * [GET Analytics `/analytics/v1/api/`](#get-analytics-analyticsv1api)
    * [Authenticated User](#authenticated-user)
      * [Response](#response-1)
    * [Analytics (Anonymous User) `/analytics/v1/api/`](#analytics--anonymous-user--analyticsv1api)
      * [Response](#response-2)
  * [Improvements](#improvements)
<!-- TOC -->

## Assumptions

* The solution implemented in this assessment has not been optimized for a live production environment with thousands of
  transactions per minute.
* The solution has not been implemented using Django async. Even though the progress done by the Django community sounds
  promising, the performance improvements are still maturing compared to sync wsgi.
* Users can get statistical information over the course of one year.
* Users can be members of more than one Team.
* Users who are not members of a team won't be able to do a daily check-in

### Method

The method chosen to measure Happiness
was [The Satisfaction with Life Scale (SWLS)](https://en.wikipedia.org/wiki/Life_satisfaction) uses a scale of 1 to 7,
where 1 represents "strongly disagree," and 7 represents "strongly agree" for statements such as "In most ways, my life
is close to my ideal."

### The levels of happiness have the following ranges:

* 31 - 35 Extremely happy
* 26 - 30 happy
* 21 - 25 Slightly happy
* 20 Neutral
* 15 - 19 Slightly unhappy
* 10 - 14 unhappy
* 5 - 9 Extremely unhappy

### High Level Solution Design

![](./monitor/daily-checkins@2x.png)

## Prerequisites

You need to install [Docker Desktop](https://www.docker.com/products/docker-desktop)
and [Docker Compose](https://docs.docker.com/compose/install/) before following the instructions below.

To install Docker Desktop on Windows Home, please follow
the [instructions](https://docs.docker.com/docker-for-windows/install-windows-home/).

## Installation

To clone the repository, run the following command

```shell
git clone https://github.com/ridiaz/d1g1t-backend-assignment.git
```

### How to run it?

We are using shared folders to enable live code reloading. Without this, Docker Compose will not start:

* Windows/MacOS: Add the cloned d1g1t-backend-assignment directory to Docker shared directories (Preferences ->
  Resources -> File
  sharing)
* Linux: No action is required, sharing is already enabled and memory for the Docker engine is not limited.

#### Go to the cloned directory:

```shell
cd d1g1t-backend-assignment
```

#### Build the application:

```shell
docker-compose build
```

#### Apply Django migrations:

```shell
docker-compose up db -d && sleep 3 && docker-compose run --rm api python3 manage.py migrate

```

#### Create superuser:

Create super user with the following command, to access the Django web Admin site

```shell
docker-compose run --rm api python3 manage.py createsuperuser

```

#### Run the application:

```shell
docker-compose up

```

Now you can access the Django web Admin on http://localhost:9001:/admin

## Tests

```shell
docker-compose run --rm api python3 pytest

```

## Endpoints

### Authentication `/api/token/`

In order to access the API endpoints that require authentication, you should include the access token in the header of
all requests.
[JSON Web Token Authentication](https://www.django-rest-framework.org/api-guide/authentication/#json-web-token-authentication)

```shell
curl --request POST \
  --url http://localhost:9001/api/token/ \
  --header 'Content-Type: application/json' \
  --data '{
"username": "<username>",
"password": "<password>"
}'

```

#### Response

```json
{
  "refresh": "<generated token>",
  "access": "<generated token>"
}
```

### CREATE Daily Check-in `/daily/v1/api/`

#### The score is calculated by summing up the responses to the following questions/criteria:

* __ In most ways my life is close to my ideal.
* __ The conditions of my life are excellent.
* __ I am satisfied with my life.
* __ So far I have gotten the important things I want in life.
* __ If I could live my life over, I would change almost nothing.

#### The scale (responses):

* 7 - Strongly agree
* 6 - Agree
* 5 - Slightly agree
* 4 - Neither agree nor disagree
* 3 - Slightly disagree
* 2 - Disagree
* 1 - Strongly disagree

#### Example

```shell
curl --request POST \
  --url http://localhost:9001/daily/v1/api/ \
  --header 'Authorization: Bearer <generated token>' \
  --header 'Content-Type: application/json' \
  --data '{
"responses": [6,6,6,5,6]
}'

```

### GET Analytics `/analytics/v1/api/`

### Authenticated User

```shell
curl --request GET \
  --url http://localhost:9001/analytics/v1/api/ \
  --header 'Authorization: Bearer <token>'

```

#### Response

Returns the list of all user's team statistics

```json
[
  {
    "name": "team_3",
    "team_statistics": [
      {
        "number_of_people": 1,
        "average_happiness": 29.0,
        "level_happiness": "Happy"
      },
      {
        "number_of_people": 1,
        "average_happiness": 22.0,
        "level_happiness": "Slightly Happy"
      }
    ],
    "average_happiness": 25.5
  }
]
```

### Analytics (Anonymous User) `/analytics/v1/api/`

```shell
curl --request GET \
  --url http://localhost:9001/analytics/v1/api/

```

#### Response

```json
[
  {
    "name": "all teams",
    "average_happiness": 29.0
  }
]
```

## Improvements

* Add cache layer
* Remove signals
* Implement task queue (i.e. Celery) to handle the loading of the data to the Analytics DB
* Writing statistical/analytics calculations with Django ORM could be difficult, sometimes is better to write raw SQL
  queries in order to take full advantage of the RDBMS engine
* Add Db indexes
* Add more type hints
* Add more tests


