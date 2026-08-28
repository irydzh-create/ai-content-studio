# Custom GPT Integration Plan

The first version runs locally as a Python CLI. The next version can expose the
same generator through a small API, then connect that API to a Custom GPT action.

## Action Flow

1. User asks the Custom GPT for tomorrow's AI content.
2. Custom GPT calls the local or deployed API.
3. API generates a content package.
4. API saves the result to SQLite.
5. Custom GPT returns the final script, carousel, prompts, caption, and hashtags.

## First API Endpoints

- `POST /content-pack`: generate and optionally save one content package.
- `GET /content-pack/{id}`: fetch a saved content package.
- `GET /calendar`: list planned content items.

