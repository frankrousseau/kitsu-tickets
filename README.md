# Tickets - Zou Example Plugin

A reference plugin for developers who want to build their own Zou/Kitsu
plugins. It implements a simple ticket management system (issues on tasks) and
demonstrates all the key parts of the plugin architecture:

- **manifest.toml** - Plugin metadata, version, and frontend flags.
- **models.py** - SQLAlchemy models using `db.Model`, `BaseMixin`, and `SerializerMixin`.
- **services.py** - Business logic separated from resources.
- **resources.py** - Flask-RESTful endpoints with JWT authentication and Pydantic validation.
- **__init__.py** - Route registration and lifecycle hooks.
- **migrations/** - Alembic database migrations scoped to the plugin's tables.
- **frontend/** - Nuxt 4 app embedded in Kitsu via iframe.

Use this plugin as a starting point: copy the structure, rename `tickets` to
your plugin ID, and adapt the models and resources to your needs.

Reference: [Kitsu Plugin Development](https://dev.kitsu.cloud/kitsu-plugins/development.html)

## Installation

Reference: [Kitsu Plugin Installation](https://dev.kitsu.cloud/kitsu-plugins/installation.html)

### From a local folder

```bash
git clone https://github.com/cgwire/kitsu-tickets.git
zou install-plugin --path ./kitsu-tickets
```

### From the Git repository

```bash
zou install-plugin --path https://github.com/cgwire/kitsu-tickets.git
```

Then restart the Zou server.

## Plugin structure

```
tickets/
  manifest.toml          # Plugin ID, name, version, frontend flags
  __init__.py             # Routes and lifecycle hooks (pre/post install/uninstall)
  models.py               # SQLAlchemy models (db.Model, BaseMixin, SerializerMixin)
  services.py             # Business logic
  resources.py            # Flask-RESTful endpoints (GET, POST, PUT, DELETE)
  migrations/
    alembic.ini           # Alembic config
    env.py                # Migration env scoped to plugin tables
    versions/             # Auto-generated migration scripts
  frontend/
    app/
      app.vue             # Nuxt root component
      app.config.ts       # Nuxt UI theme config
      pages/
        debug.vue         # Example page using useKitsu() composable
  logo.png                # Plugin icon shown in Kitsu
```

## Tables

| Table | Description |
|-------|-------------|
| `plugin_tickets_tickets` | Tickets (title, text, status, task_id, project_id, episode_id, person_id, assignee_id) |

## API routes

All routes are prefixed by **`/api/plugins/tickets`**. JWT authentication is
required.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/tickets` | List all tickets |
| POST | `/tickets` | Create a ticket |
| GET | `/tickets/<ticket_id>` | Get a ticket |
| PUT | `/tickets/<ticket_id>` | Update a ticket |
| DELETE | `/tickets/<ticket_id>` | Delete a ticket |

## Key concepts for plugin developers

### Manifest

`manifest.toml` declares your plugin's identity. Set `frontend_project_enabled`
and `frontend_studio_enabled` to `true` if your plugin ships a frontend. The
`icon` field accepts a Lucide icon name.

### Models

Use `db.Model` with `BaseMixin` and `SerializerMixin`. Prefix table names with
`plugin_<id>_` to avoid collisions. `BaseMixin` provides helper methods:

| Method | Description |
|--------|-------------|
| `Model.get(id)` | Get by primary key |
| `Model.get_by(**kwargs)` | Get first match by column values |
| `Model.get_all()` | Get all rows |
| `Model.create(**kwargs)` | Create and commit |
| `instance.update(dict)` | Update fields and commit |
| `instance.delete()` | Delete and commit |

Define a `present()` method on your models for API serialization.

### Services

Keep business logic in `services.py`, separate from resources. This makes
the code easier to test and reuse.

### Resources

Extend `flask_restful.Resource` and `ArgsMixin`. Protect endpoints with
`@jwt_required()`. Use `self.check_id_parameter(uuid)` to validate UUID
parameters.

### Lifecycle hooks

`__init__.py` exposes `pre_install`, `post_install`, `pre_uninstall`, and
`post_uninstall` hooks that run during `zou install-plugin` /
`zou uninstall-plugin`.

### Migrations

Run `zou migrate-plugin --path .` to auto-generate and apply Alembic
migrations. The migration env in `migrations/env.py` automatically discovers
your models.

### Frontend

The frontend is a standalone Nuxt 4 app. Kitsu embeds it in an iframe and
passes context via query parameters (`production_id`, `episode_id`,
`dark_theme`). Use the `useKitsu()` composable to access the Kitsu API client.

## Testing

Tests use Zou's `ApiDBTestCase` base class. Always run tests against a test
database:

```bash
DB_DATABASE=zoudb-test python -m pytest tests/ -v
```
