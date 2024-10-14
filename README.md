# League of Legends Skins API

This project is a FastAPI-based application that provides an API for managing League of Legends champions and skins. It integrates with the DDragon API to fetch the latest data and stores it in a SQLite database.

## Requirements

The project dependencies are listed in the `requirements.txt` file

## Database Configuration

The database configuration is handled in `database_config.py`:

- Uses SQLite as the database.
- Defines a `DbContextManager` for managing database sessions.
- Provides an asynchronous `get_db` function for dependency injection in FastAPI routes.

## Models

The database models are defined in `models.py`:

- **Skin**: Represents a skin with fields for `id`, `name`, `owned`, and a foreign key to `Champion`.
- **Champion**: Represents a champion with fields for `name`, `role`, and a relationship to `Skin`.

## Services

### Skin Service

Defined in `skin_service.py`:

- `get_all_skins`: Fetches all skins except the default ones.
- `set_skin_owned_status`: Updates the owned status of a skin.
- `get_skin_by_name`: Fetches a skin by its name.

### Champion Service

Defined in `champion_service.py`:

- `get_all_champions`: Fetches all champions with their default skins.
- `get_champion_by_name`: Fetches a champion by its name along with its skins.

### DDragon Service

Defined in `ddragon_service.py`:

- `get_latest_package_version`: Fetches the latest DDragon package version.
- `get_champions_data`: Fetches champion data for a specific version.
- `filter_champion_data`: Filters and processes champion data.
- `initiate_ddragon_information`: Initiates the DDragon information and populates the database.

## Logger

Logging is configured in `logger.py` using Python's logging module.

## API Endpoints

The API endpoints are defined in `main.py`:

- `GET /version`: Returns the latest DDragon package version.
- `GET /champions`: Returns all champions.
- `GET /champions/{champion_name}`: Returns a champion by name.
- `GET /skins`: Returns all skins.
- `GET /skins/name/{skin_name}`: Returns a skin by name.
- `PUT /skins/status`: Updates the owned status of a skin.

## Running the Application

To run the application, use the following command:

```bash
uvicorn main:app --reload
```

## REST Client

The `rest-client.http` file provides example HTTP requests for testing the API endpoints.

## Alembic Configuration

The `alembic.ini` file contains the configuration for Alembic, which is used for database migrations.
