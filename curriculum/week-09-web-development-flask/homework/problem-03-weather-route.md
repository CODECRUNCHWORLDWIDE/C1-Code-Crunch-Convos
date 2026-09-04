# Homework Problem 3 — Weather route

> **Topic:** `request.args` and the query string, one thin view over borrowed logic, and a single error type that turns into a flash message
> **Lecture:** [03 — Forms, Sessions, Deployment](../lecture-notes/03-forms-sessions-deployment.md) · [02 — Templates and Static Files](../lecture-notes/02-templates-and-static.md)
> **Difficulty:** Intermediate
> **Target time:** 1 hour 15 minutes
> **Why this one:** this is the first time your blog talks to the outside world, and the outside world is unreliable. The whole problem is about a seam: the part that fetches weather knows nothing about the web, and the part that answers the browser knows nothing about weather. Get that seam right once and every later "call an API from a page" is a copy of it.

## The Brief

In Week 8 you wrote a small program that ran in the terminal, asked an API
about the weather, and printed the answer. It worked. The only problem is
that nobody can visit a terminal.

So put a door on it.

Think of your Week 8 code as a vending machine that already works. You are
not rebuilding the machine. You are cutting a hole in the wall of your blog,
sliding the machine behind it, and putting a little slot out front where
somebody types a city name. The machine does the same job it always did. It
just has a customer now instead of a programmer.

The ask, in one sentence: add a `GET /weather` page that shows a search box,
and — when somebody has typed a city — shows that city's current weather
under the box.

Two things go wrong out there, and both are normal:

- **The person typed a city that does not exist.** `Nowheresville` is not a
  place.
- **The internet did not answer in time.** The weather service is slow, or
  down, or your wifi blinked.

Neither of those is a crash. A crash is when your program falls over and
Python dumps a wall of red text — a *traceback*, the list of every line the
program was inside when it died. On a web page, a traceback is worse than
useless: it is scary to the visitor and it leaks your file paths and your
code to a stranger. So both of those failures come out as one calm sentence
on the page, and the search box stays there so the person can try again.

The way you get that is a **seam** — one clean line between two halves that
agree on exactly one thing. Here the agreement is: *the fetching half is
allowed to fail in exactly one way, and it must fail with a sentence a human
can read.* You give that one way a name — `WeatherError` — and then the view
only ever needs one `except`.

One honest note about the shipped answer beside this page: a downloaded file
cannot depend on your wifi, so its `fetch_current_weather` reads from a tiny
offline table instead of calling a real API. The seam is identical. Your
real fetcher goes behind the same function name, raises the same
`WeatherError`, and the view does not change by one character. That is the
proof that the seam works — the web half could not tell the difference.

## Starter

Save this as `problem-03-weather-route.py` in your `homework/` folder. It runs as
pasted: `/weather` comes up, the flash widget works, and every lookup
politely fails. Your job is the four `TODO`s.

```python
"""problem-03-weather-route.py — starter: a /weather route that cannot fetch yet.

Run with: python problem-03-weather-route.py
"""

import os

from flask import Flask, flash, render_template, request
from jinja2 import DictLoader

# TODO 1: decide what CurrentWeather looks like — city, temp, unit,
#         description at minimum. A dataclass keeps the template honest.
# TODO 2: fill in fetch_current_weather. In your blog this is your Week 8
#         code: requests.get(..., timeout=5.0), check the response, read the
#         JSON. Every failure it can hit leaves as WeatherError, carrying a
#         sentence written for a person.
# TODO 3: finish the view. No ?city= in the query string -> just the form.
#         A city -> try the fetch; on WeatherError, flash the message and
#         re-render the form. The view gets no other job.
# TODO 4: finish weather.html: the search form always, the reading only when
#         there is one, and the box remembering what was typed.

#: Your API key, if the service you chose needs one. It is read from the
#: environment at start-up and never written in this file. See Constraints.
API_KEY: str | None = os.environ.get("WEATHER_API_KEY")

#: templates/base.html — a minimal layout with the flash widget.
BASE_HTML: str = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{% block title %}Crunch Blog{% endblock %}</title>
  </head>
  <body>
    <main>
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          <ul class="flashes">
            {% for category, message in messages %}
              <li class="flash flash-{{ category }}">{{ message }}</li>
            {% endfor %}
          </ul>
        {% endif %}
      {% endwith %}
      {% block content %}{% endblock %}
    </main>
  </body>
</html>
"""

#: templates/weather.html — one page, two states.
WEATHER_HTML: str = """\
{% extends "base.html" %}

{% block content %}
  <h2>Weather</h2>
  <p>TODO 4: a GET form with a "city" box, then the reading if there is one.</p>
{% endblock %}
"""


class WeatherError(RuntimeError):
    """Anything that should become a flash message rather than a traceback."""


def fetch_current_weather(city: str):
    """TODO 2: return the current weather for *city*, or raise WeatherError."""
    raise WeatherError("The weather lookup is not written yet.")


app: Flask = Flask(__name__)
app.jinja_loader = DictLoader({"base.html": BASE_HTML, "weather.html": WEATHER_HTML})
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-not-a-real-secret")


@app.route("/weather")
def weather() -> str:
    city = request.args.get("city", "").strip()
    if not city:
        return render_template("weather.html", current=None)

    # TODO 3: try the fetch here, and let WeatherError become a flash.
    flash("Not wired up yet.", "error")
    return render_template("weather.html", current=None)


if __name__ == "__main__":
    app.run(debug=True)  # local development only — never in production
```

In your own blog this is the same code across real files: `weather.html`
joins `templates/`, the fetcher lives in its own module beside `app.py`, and
the route is the only new thing in `app.py`.

## Requirements

1. `GET /weather` with no query string shows the search form and nothing
   else — no reading, no error.
2. `GET /weather?city=London` shows London's current temperature and a short
   description, with the search form still on the page.
3. The form is a `GET` form pointing at `/weather` itself, with one input
   named `city`, so submitting it produces exactly the URL in requirement 2.
4. The search box comes back holding what was typed, so a person correcting
   a typo does not start from an empty field.
5. A city that does not exist flashes one clean sentence and re-renders the
   form. No traceback reaches the browser, with `debug` off.
6. A slow or dead weather service does the same thing, with its own
   sentence. Both paths leave the fetcher as `WeatherError`.
7. The API key, if your service needs one, is read from `os.environ` and
   appears nowhere in your source.
8. The view is thin: read the query string, call one function, catch one
   exception type, render one template. Nothing about HTTP or JSON parsing
   lives in it.

## Constraints

- **The API key comes from `os.environ`, never from the file.** A key typed
  into your source is in your git history within the hour, and public the
  moment you push. Git does not forget: deleting the line later leaves the
  key sitting in an old commit. `os.environ.get("WEATHER_API_KEY")` reads it
  from outside the repository, so the repository never has it to leak.
- **Every `requests.get` carries `timeout=`.** Without it `requests` waits
  forever by default. "Forever" means one dead weather server can freeze a
  page of your site until you restart it. Five seconds is generous.
- **One exception type crosses the seam.** The fetcher raises `WeatherError`
  and nothing else. If `requests.Timeout` or a `KeyError` were allowed
  through, the view would need a growing list of `except` clauses that all
  do the same thing — and the day you swap the weather service, that list is
  wrong. One type in, one `except` out.
- **The message inside `WeatherError` is written for a person, not a
  programmer.** "No city called 'Nowheresville' was found." is a sentence.
  `HTTPError: 404 Client Error for url=...` is not. The view flashes the
  message unchanged, so the quality of the sentence is decided where the
  failure happens.
- **The form is `GET`, not `POST`.** A search is a question, not a change —
  it puts the answer in the URL, so `/weather?city=Miami` can be bookmarked,
  shared, and reloaded without the browser asking "resend this form?".
  `POST` is for things that change something on the server.
- **No traceback in the browser, ever.** Test with `debug` off. Flask's
  debug page is a development convenience; on a real host it hands a visitor
  your source code and a Python prompt.

## Expected output

Real stdout from the shipped file, captured on CPython 3.13.2 with Flask
3.1.0:

```text
$ python problem-03-weather-route.py
GET /weather                    -> 200 (the search form, nothing else)
GET /weather?city=London        -> 200
  <h3>London, United Kingdom</h3>
  <p class="temp">18.4°C</p>
  <p>Partly cloudy</p>
  the search box keeps the typed city: True
GET /weather?city=Nowheresville -> 200 (a flash, never a traceback)
  <li class="flash flash-error">No city called &#39;Nowheresville&#39; was found.</li>
GET /weather?city=timeout       -> 200 (the requests.Timeout branch)
  <li class="flash flash-error">The weather service timed out. Try again.</li>
```

## Steps

1. Copy the starter into `problem-03-weather-route.py` and run it. Visit
   `/weather` and confirm the form-only state and the flash widget both
   work before you fetch anything.
2. Write the `CurrentWeather` dataclass — `city`, `country`, `temp`, `unit`,
   `description`. Naming the shape once stops the template guessing.
3. Fill in `fetch_current_weather` with your Week 8 code. Give it a
   `timeout=`, and wrap the call so that a timeout, a network failure, and
   an unknown city all `raise WeatherError("...")` with their own sentence.
4. Call it straight from a terminal first — `python -c "import
   hw03_weather_route as w; print(w.fetch_current_weather('London'))"`. Get
   it right with no web app in the way.
5. Finish the view: `request.args.get("city", "").strip()`, the empty case,
   then `try` / `except WeatherError` / `flash` / re-render.
6. Finish `weather.html`. The form goes at the top with
   `value="{{ request.args.get('city', '') }}"`, the reading goes below it
   inside `{% if current %}`.
7. Try all four states in the browser: no city, a real city, a nonsense
   city, and the service failing. For the last one, point your fetcher at a
   deliberately wrong address for a moment.
8. Turn `debug` off and repeat the two failures. If a traceback appears, the
   `except` is missing or too narrow.

## The Solution

```python
"""problem-03-weather-route-solution.py — the Week 8 weather CLI, behind a route.

The lesson of this problem is the seam: the fetching code raises one
exception type, ``WeatherError``, with a message written for a human, and the
view does exactly one thing with it — flash it and re-render. The view never
knows how the weather is fetched; the fetcher never knows it is inside a web
app.

One honest substitution so this download runs anywhere: a shipped answer
cannot depend on your wifi, so ``fetch_current_weather`` below reads from a
small offline table instead of calling the Open-Meteo API with ``requests``.
The seam is identical — your real fetcher goes behind the same function name,
raises the same ``WeatherError`` for a timeout, a network failure, or an
unknown city, and the view does not change by one character. The city name
``timeout`` is wired to fail the way ``requests.Timeout`` would, so the error
path is demonstrable offline too.

The template travels inside the file via a ``DictLoader``, and the app is
driven by ``app.test_client()`` — Flask's in-process fake browser — instead
of ``app.run()``.

Run it with::

    python problem-03-weather-route-solution.py
"""

import os
from dataclasses import dataclass

from flask import Flask, flash, render_template, request
from jinja2 import DictLoader

#: templates/base.html — a minimal layout with the flash widget.
BASE_HTML: str = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Crunch Blog{% endblock %}</title>
  </head>
  <body>
    <header>
      <h1><a href="{{ url_for('weather') }}">Crunch Blog</a></h1>
    </header>
    <main>
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          <ul class="flashes">
            {% for category, message in messages %}
              <li class="flash flash-{{ category }}">{{ message }}</li>
            {% endfor %}
          </ul>
        {% endif %}
      {% endwith %}
      {% block content %}{% endblock %}
    </main>
  </body>
</html>
"""

#: templates/weather.html — one page serving both states: form, and form+reading.
WEATHER_HTML: str = """\
{% extends "base.html" %}

{% block title %}
  {%- if current -%}
    Weather in {{ current.city }} — Crunch Blog
  {%- else -%}
    Weather — Crunch Blog
  {%- endif -%}
{% endblock %}

{% block content %}
  <h2>Weather</h2>

  <form class="search" method="get" action="{{ url_for('weather') }}">
    <label for="city">City</label>
    <input type="search" id="city" name="city" placeholder="London"
           value="{{ request.args.get('city', '') }}" required>
    <button type="submit">Look up</button>
  </form>

  {% if current %}
    <article>
      <h3>{{ current.city }}{% if current.country %}, {{ current.country }}{% endif %}</h3>
      <p class="temp">{{ current.temp }}{{ current.unit }}</p>
      <p>{{ current.description }}</p>
    </article>
  {% endif %}
{% endblock %}
"""


class WeatherError(RuntimeError):
    """Anything that should become a flash message rather than a traceback."""


@dataclass
class CurrentWeather:
    """One reading, shaped for the template."""

    city: str
    country: str
    temp: float
    unit: str
    description: str


#: The offline stand-in for the API. Your real build replaces the body of
#: fetch_current_weather with the Week 8 requests calls; nothing else moves.
OFFLINE_WEATHER: dict[str, CurrentWeather] = {
    "london": CurrentWeather("London", "United Kingdom", 18.4, "°C", "Partly cloudy"),
    "miami": CurrentWeather("Miami", "United States", 31.2, "°C", "Thunderstorm"),
    "nairobi": CurrentWeather("Nairobi", "Kenya", 24.0, "°C", "Clear sky"),
}


def fetch_current_weather(city: str) -> CurrentWeather:
    """Return the current weather for *city*, or raise WeatherError.

    The real version geocodes the name and calls the forecast API with
    ``requests.get(..., timeout=5.0)``, translating requests.Timeout and
    requests.RequestException into WeatherError. This offline version keeps
    every failure mode; it just does not need the network to show them.
    """
    key = city.strip().lower()
    if not key:
        raise WeatherError("Please enter a city name.")
    if key == "timeout":  # the requests.Timeout branch, demonstrable offline
        raise WeatherError("The weather service timed out. Try again.")
    if key not in OFFLINE_WEATHER:
        raise WeatherError(f"No city called {city!r} was found.")
    return OFFLINE_WEATHER[key]


app: Flask = Flask(__name__)
app.jinja_loader = DictLoader({"base.html": BASE_HTML, "weather.html": WEATHER_HTML})
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-not-a-real-secret")


@app.route("/weather")
def weather() -> str:
    """Thin wrapper around the weather logic. Eleven lines, on purpose."""
    city = request.args.get("city", "").strip()
    if not city:
        return render_template("weather.html", current=None)

    try:
        current = fetch_current_weather(city)
    except WeatherError as exc:
        # A user-caused or network-caused failure is a flash, never a traceback.
        flash(str(exc), "error")
        return render_template("weather.html", current=None)

    return render_template("weather.html", current=current)


def line_with(page: str, needle: str) -> str:
    """Return the first line of *page* containing *needle*, stripped."""
    for line in page.splitlines():
        if needle in line:
            return line.strip()
    return f"(no line contains {needle!r})"


def main() -> None:
    """Drive both states and every failure path, and print each one."""
    client = app.test_client()

    response = client.get("/weather")
    print(f"GET /weather                    -> {response.status_code} (the search form, nothing else)")

    response = client.get("/weather?city=London")
    body = response.get_data(as_text=True)
    print(f"GET /weather?city=London        -> {response.status_code}")
    print(f"  {line_with(body, '<h3>')}")
    print(f"  {line_with(body, 'class=\"temp\"')}")
    print(f"  {line_with(body, 'Partly cloudy')}")
    print(f"  the search box keeps the typed city: {'value=\"London\"' in body}")

    response = client.get("/weather?city=Nowheresville")
    body = response.get_data(as_text=True)
    print(f"GET /weather?city=Nowheresville -> {response.status_code} (a flash, never a traceback)")
    print(f"  {line_with(body, 'class=\"flash ')}")

    response = client.get("/weather?city=timeout")
    body = response.get_data(as_text=True)
    print(f"GET /weather?city=timeout       -> {response.status_code} (the requests.Timeout branch)")
    print(f"  {line_with(body, 'class=\"flash ')}")


if __name__ == "__main__":
    main()
```

**The view is eleven lines because it is a receptionist, not a worker.** It
does four things: read what was asked, hand it to the specialist, catch the
one failure the specialist is allowed to have, render. Every line about
HTTP, JSON, units, or API keys lives in `fetch_current_weather`. That is why
the shipped file can read from an offline table and still be the correct
answer — swapping the specialist changes nothing out front.

**`request.args` is the query string, already taken apart.** The bit of a
URL after `?` — `?city=London` — arrives as something that behaves like a
dictionary. Use `.get("city", "")` and never `["city"]`: `.get` with a
default hands you an empty string when nobody typed anything, which is the
*normal* first visit, not an error. Square brackets raise instead, and Flask
turns that raise into a `400 Bad Request` — an error page for a page load
that was perfectly fine.

**`.strip()` earns its place.** A space typed before a city name, or a stray
`?city=%20` in a shared link, would otherwise count as "they typed
something" and send a lookup for a blank city. Trim first, then decide.

**`current=None` is the whole "two pages in one file" trick.** The template
always draws the form. It draws the reading only inside `{% if current %}`.
So the empty first visit and the failed lookup render the exact same page
and there is no second template to keep in step.

**One `except`, and the message passes through untouched.**
`except WeatherError as exc: flash(str(exc), "error")` is the entire error
handling. It works because the fetcher already decided what a human should
read. The view is not translating anything — translation is where wording
goes stale.

**The box remembers what was typed** because the template reads
`request.args.get('city', '')` back into the input's `value`. Flask makes
`request` available to every template without you passing it. A person
fixing `Lodnon` to `London` edits four characters instead of retyping.

**`app.secret_key` from the environment, with a loud development default.**
Flash messages ride in the session cookie, and Flask signs that cookie with
the secret key — no key, no flash, just
`RuntimeError: The session is unavailable because no secret key was set`.
The default is named `dev-only-not-a-real-secret` so that shipping it is
embarrassing rather than silent.

**The `timeout` city is not a joke, it is a test fixture.** The failure that
actually hurts in production — the service not answering — is the hardest
one to trigger on purpose. Wiring one input to that branch means you can
prove the calm-message path works, today, offline, without unplugging
anything.

## Run it

Copy the worked answer on this page into `problem-03-weather-route.py` and run it:

```bash
python problem-03-weather-route.py
```

It needs Flask installed and nothing else — no API key, no network — and it
exits on its own. In your own build the same shape lands as a `/weather`
route in `app.py`, a `templates/weather.html`, and your Week 8 fetcher
behind `fetch_current_weather`.

The `-solution` in the filename keeps this file from colliding with your own
`problem-03-weather-route.py`.

## Common bugs to catch

- **`werkzeug.exceptions.BadRequestKeyError: 400 Bad Request: KeyError:
  'city'`.** You wrote `request.args["city"]`. A first visit has no `city`
  at all, and that is the normal case, not a bad request. Use
  `request.args.get("city", "")`.

- **The page hangs and the browser spinner never stops.** A `requests.get`
  with no `timeout=`. `requests` waits forever by default, and forever is a
  long time to hold a worker. Add `timeout=5.0` and give the timeout its own
  `WeatherError` message.

- **A wall of red text in the browser instead of a message.** Either the
  `try` does not wrap the fetch, or the fetcher lets something out that is
  not a `WeatherError` — often a `KeyError` while reading the JSON, because
  the error response has a different shape than the success one. Catch it
  where it happens and re-raise it as `WeatherError`.

- **`RuntimeError: The session is unavailable because no secret key was
  set.`** `flash()` needs `app.secret_key`. The line exists in the starter;
  it usually gets lost in a copy-paste.

- **`jinja2.exceptions.UndefinedError: 'current' is undefined`.** One
  `render_template` call forgot to pass `current`. Every path through the
  view passes it — `None` on the empty and failed paths, the reading on the
  happy one.

- **The temperature is right and the units are nonsense** — 64 degrees in
  London, in Celsius. The API returned Fahrenheit because you did not ask
  for anything else. Send the unit parameter explicitly and store the unit
  next to the number instead of assuming it.

- **Your key is in the repository.** `git log -S "your-key-here"` finds it
  even after you delete the line. If it ever landed in a commit, treat it as
  public: revoke the key on the provider's dashboard and issue a new one.
  Nothing else is a fix.

- **`ModuleNotFoundError: No module named 'requests'`** when your fetcher
  runs.

  ```text
  Traceback (most recent call last):
    File "problem-03-weather-route.py", line 8, in <module>
      import requests
  ModuleNotFoundError: No module named 'requests'
  ```

  Your virtual environment is not the one you installed into. Activate it,
  then `pip install requests`.

## Under the hood

<details>
<summary>Under the hood — why `request.args` is not a plain dict</summary>

A URL is allowed to repeat a key: `?city=London&city=Miami` is legal. A
plain dictionary cannot hold that, so Werkzeug — the library underneath
Flask that handles the raw HTTP — gives you a `MultiDict`.

It behaves like a dictionary for the common case: `.get("city")` returns the
**first** value. When you actually want them all, `.getlist("city")` returns
`["London", "Miami"]`.

It is also immutable. `request.args["city"] = "Paris"` raises, on purpose:
the query string is a record of what the browser sent, and rewriting the
record would make your logs lie about the request.

Two other bags on the same object, shaped the same way: `request.form` for
`POST` bodies, and `request.values`, which searches both. Prefer the
specific one — a route that reads `request.values` accepts a form field
where it meant to read a URL, which is a small hole with a long history.

</details>

<details>
<summary>Under the hood — what `timeout=5.0` actually times</summary>

It is not "the whole request must finish in five seconds". A single float
sets two separate clocks:

- the **connect** timeout — how long to wait for the far end to pick up the
  phone, and
- the **read** timeout — how long to wait *between* chunks of the answer
  once it has.

So a server that dribbles data out slowly, one byte every four seconds, can
legally keep you on the line far longer than five seconds and never trip
either clock. `timeout=(3.0, 5.0)` sets the two independently.

If you genuinely need a hard ceiling on total time, no timeout argument will
give it to you — that needs a worker-level limit outside `requests`, such as
gunicorn's `--timeout`. What `timeout=` buys is protection against the
common failure: a host that has simply stopped answering.

</details>

<details>
<summary>Under the hood — why the seam is one exception type, not several</summary>

The rule has a name: the view depends on an *interface*, not on an
implementation. `WeatherError` is the whole interface for failure.

Watch what happens without it. The view grows
`except (requests.Timeout, requests.ConnectionError, requests.HTTPError,
KeyError, ValueError)` — five types, one body, all doing the same flash.
Now swap Open-Meteo for a provider whose client library raises its own
classes, or cache to a file that raises `OSError`. Every one of those tuples
across your app is now quietly incomplete, and the symptom is a traceback in
front of a visitor.

With the seam, the fetcher owns the translation. The five `except` clauses
live in one function, next to the code that knows what each failure means,
and they produce sentences instead of class names.

This is the same idea as an adapter or a port in bigger designs, and it is
why the shipped file can serve a dictionary rather than the internet without
touching a line of the view. That substitution *is* the test of the seam: if
the web half had to change, the seam was in the wrong place.

</details>

<details>
<summary>Under the hood — a five-minute cache in eight lines, and why not to keep it</summary>

The Stretch asks for a per-city cache. The shape:

```python
import time

_CACHE: dict[str, tuple[float, CurrentWeather]] = {}
TTL_SECONDS = 300.0


def cached_weather(city: str) -> CurrentWeather:
    key = city.strip().lower()
    hit = _CACHE.get(key)
    if hit is not None and time.monotonic() - hit[0] < TTL_SECONDS:
        return hit[1]
    reading = fetch_current_weather(key)
    _CACHE[key] = (time.monotonic(), reading)
    return reading
```

`time.monotonic()` rather than `time.time()`: a monotonic clock only ever
counts forward, so a machine syncing its clock or crossing a daylight-saving
boundary cannot make an entry look five minutes old — or a year in the
future — by accident.

The lowercased key means `London`, `london`, and `  LONDON ` are one entry
instead of three.

Two reasons this is a demonstration and not a production cache. It lives in
one process's memory, so four gunicorn workers keep four separate copies and
your hit rate is a quarter of what you think. And it never shrinks — every
city anyone ever asks for stays forever, which is a slow memory leak that a
bored visitor can turn into a fast one. Real answers: bound it with
`functools.lru_cache(maxsize=128)` plus a time bucket, or move it out of the
process into something shared like Redis.

</details>

## Acceptance checklist

- [ ] `/weather` with no query string shows the search form and nothing
      else.
- [ ] `/weather?city=London` shows the temperature and a description, with
      the form still on the page.
- [ ] Submitting the form produces the URL in the line above — a `GET` form,
      not a `POST`.
- [ ] The box still holds what was typed after any submission.
- [ ] A nonsense city flashes one clean sentence, with `debug` off, and no
      traceback reaches the browser.
- [ ] A failing service does the same, with its own sentence, and you
      triggered it on purpose rather than assuming it works.
- [ ] `grep -rn "api_key\|API_KEY" .` shows the key being read from
      `os.environ` and never written down.
- [ ] Every outbound call carries a `timeout=`.
- [ ] The view is a dozen lines or fewer and mentions neither HTTP nor JSON.

## Stretch

- Cache each city's reading for five minutes in a module-level dict so that
  ten refreshes cost one API call. The Under the hood block above has the
  shape and the two traps.
- Let the visitor pick Celsius or Fahrenheit with a second query parameter,
  `?units=f`, defaulting to Celsius. Keep the unit next to the number so the
  template never has to guess.
- Remember the last five cities looked up in the session and show them as
  links under the form. Sessions are Lecture 03, and the links are just
  `url_for('weather', city=name)`.
- Give the fetcher one retry, once, on a timeout only — and wait a second
  before it. Then read about why retrying a `500` is fine and retrying a
  `400` is pointless: one is the server having a bad moment, the other is
  your request being wrong, and it will be just as wrong next time.
