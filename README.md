# Documents

## Data

All services data is contained in docker images to avoid damaging data in a local datastore.

```bash
docker compose up -d
```

---

## API

### Run

#### Grab the data from S3

```bash
aws --profile production s3 cp s3://cpr-production-rds/admin-service/dump-2025-02-12-navigator-production.sql sql-init/dump-2025-02-12-navigator-production.sql
```

#### Run the API

```bash
cd api
poetry install
poetry run fastapi dev
```

#### Deleting data and starting again

```bash
docker volume rm documents_navigator_postgres_data
docker compose up -d
```

#### Generating nicer API docs

```bash
# When the API is running
npx @redocly/cli build-docs http://127.0.0.1:8000/openapi.json
```

Then just open the `redoc-static.html` file in your browser.

---

## CMS ([Strapi](https://docs.strapi.io))
