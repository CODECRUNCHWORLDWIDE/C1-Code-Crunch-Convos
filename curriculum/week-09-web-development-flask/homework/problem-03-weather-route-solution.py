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
