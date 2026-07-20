# Week 8 — Resources

Bookmark this file. You will return to it every time you call a new API.

---

## Official Python docs

- **`json` module** — <https://docs.python.org/3/library/json.html>
  The standard-library reference for `json.loads`, `json.dumps`, `json.load`, `json.dump`, and the `JSONDecodeError` exception. Read the "Encoders and Decoders" section if you ever need to (de)serialize a custom type.
- **`urllib.parse`** — <https://docs.python.org/3/library/urllib.parse.html>
  When you need to URL-encode a query string by hand (`quote`, `urlencode`) or split a URL into parts (`urlparse`). `requests` does this for you in `params=`, but knowing the primitives helps.
- **`http.HTTPStatus`** — <https://docs.python.org/3/library/http.html#http.HTTPStatus>
  Named constants for every status code in the IANA registry. Use `HTTPStatus.NOT_FOUND` instead of the magic number `404`.

---

## Third-party HTTP libraries

- **`requests`** — <https://requests.readthedocs.io/>
  The de-facto HTTP client for Python. We use it for every example this week. Read at minimum the *Quickstart* and *Advanced Usage* pages.
- **`httpx`** — <https://www.python-httpx.org/>
  A modern alternative with the same `requests`-style API plus async support and HTTP/2. If you ever need to fire 100 requests in parallel, switch to `httpx.AsyncClient`.
- **`urllib3`** — <https://urllib3.readthedocs.io/>
  The connection-pool library that `requests` uses under the hood. You will see it in stack traces; knowing what it is removes the mystery.

---

## API playgrounds (free, no key needed)

These services exist so you can practice without signing up for anything:

- **httpbin.org** — <https://httpbin.org/>
  Echoes back whatever you send. Endpoints: `/get`, `/post`, `/headers`, `/status/{code}`, `/delay/{n}`, `/basic-auth/{user}/{pass}`. We use it in Exercises 01, 03, and 05.
- **PokeAPI** — <https://pokeapi.co/>
  Free Pokémon database. No auth. We use it in Exercise 02.
- **JSONPlaceholder** — <https://jsonplaceholder.typicode.com/>
  Fake but realistic REST API for blogs (posts, comments, users). Great for practicing CRUD.
- **Open-Meteo** — <https://open-meteo.com/>
  Free weather and geocoding API, **no key required** for non-commercial use. Mini-project uses this.
- **Frankfurter** — <https://www.frankfurter.app/>
  Free currency-conversion API backed by European Central Bank data. Challenge 01.
- **GitHub REST API** — <https://docs.github.com/en/rest>
  Public endpoints (`/users/:name`, `/users/:name/repos`) work without a token, just at a lower rate limit. Exercise 04 and Challenge 02.
- **The Cat API** — <https://thecatapi.com/>
  Random cat pictures. Yes really. Bonus practice if you finish early.

---

## HTTP & REST reference

- **MDN — HTTP overview** — <https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview>
  Best single page on the web for understanding HTTP if you have never seen it before.
- **MDN — HTTP status codes** — <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status>
  Every code, with definitions and links to the relevant RFCs. Keep this open while you debug.
- **MDN — HTTP request methods** — <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods>
  GET/POST/PUT/PATCH/DELETE/HEAD/OPTIONS explained with idempotency notes.
- **RFC 9110 — HTTP semantics** — <https://www.rfc-editor.org/rfc/rfc9110.html>
  The current authoritative spec for HTTP. You do not need to read it cover to cover, but it is *the* source of truth when MDN and Stack Overflow disagree.
- **REST API tutorial** — <https://restfulapi.net/>
  Plain-English explanation of REST conventions, resources, idempotency, and HATEOAS.

---

## Authentication & secrets

- **`python-dotenv`** — <https://github.com/theskeptics/python-dotenv> (canonical: <https://pypi.org/project/python-dotenv/>)
  Load `.env` files into `os.environ`.
- **OWASP cheat sheet — secrets management** — <https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html>
  How professionals handle API keys in real projects. Read at least the "Application secrets" section.
- **`git secrets`** — <https://github.com/awslabs/git-secrets>
  A pre-commit hook that refuses to let you accidentally commit an AWS key.

---

## Real Python articles

Beginner-friendly long-form tutorials:

- **Python's `requests` library guide** — <https://realpython.com/python-requests/>
- **Python and REST APIs** — <https://realpython.com/api-integration-in-python/>
- **JSON in Python** — <https://realpython.com/python-json/>
- **Working with environment variables** — <https://realpython.com/python-dotenv/>

---

## Tools every API developer uses

- **`curl`** — already on macOS and Linux. Try `curl -i https://httpbin.org/get` once before you ever write Python. The `-i` flag prints headers; `-v` prints everything.
- **HTTPie** — <https://httpie.io/cli> — `curl` with sane defaults and color output. `http GET httpbin.org/get`.
- **Postman** — <https://www.postman.com/> — GUI for crafting and saving requests. Great for exploring an API before you write code.
- **Insomnia** — <https://insomnia.rest/> — Open-source Postman alternative.
- **`jq`** — <https://jqlang.org/> — Command-line JSON processor. `curl ... | jq '.users[].name'` is a developer superpower.

---

## Going deeper (optional)

- **"HTTP: The Definitive Guide"** by David Gourley & Brian Totty. Old (2002) but the protocol has not changed much.
- **"REST in Practice"** by Webber, Parastatidis, Robinson. The HATEOAS bible.
- **GraphQL official site** — <https://graphql.org/learn/> — when REST stops being the right answer.
