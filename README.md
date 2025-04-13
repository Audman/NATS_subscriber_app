# NATS Subscriber App

A 3-layered Python application that subscribes to a NATS topic and stores incoming messages into a PostgreSQL database.

## ⚙️ Architecture

- **NATS**: Message broker
- **PostgreSQL**: Persistent data storage
- **Python App**: Subscribes to `messages` topic, stores content + timestamp in DB
- **Layers**:
  - **API layer**: subscribes to NATS and receives messages
  - **Service layer**: handles the logic of subscribing and parsing messages
  - **Data layer**: manages database models and access
  - **Tests**: verify functionality of both layers

---

## 📦 Requirements

- Python 3.11
- NATS server
- PostgreSQL 15
- `nats-py`, `sqlalchemy`, `psycopg2-binary`, `python-dotenv`

---

## 📁 Project Structure

```
.
├── app
│   ├── api
│   │   └── nats_client.py
│   ├── data
│   │   ├── database.py
│   │   ├── models.py
│   │   └── repositories.py
│   └── service
│       └── message_service.py
├── docker-compose.yml
├── Dockerfile
├── main.py
├── migrations
│   └── init_db.sql
├── requirements.txt
├── tests
│   ├── test_repository.py
│   └── test_service.py
├── README.md
└── .env
```

---

## 🐋 Run with Docker

#### 1. Clone the repo

```bash
git clone https://github.com/Audman/NATS_subscriber_app
cd NATS_subscriber_app
```

#### 2. Build and start the containers

```bash
docker-compose up --build
```
This will launch:
> - NATS server on port `4222`
> - PostgreSQL on port `5432`
> - The Python app, listening for NATS messages

#### 3. Create the database schema

If your database schema isn't created automatically by the app, mention how to run the SQL script manually:
```bash
docker exec -i nats-subscriber-db-1 psql -U postgres -d nuts_db < migrations/init_db.sql
```



---

## 📤 Publish a test message

In a separate terminal, use the official NATS CLI to send a message:

```bash
docker run --rm -it --network=nats-subscriber_default natsio/nats-box nats pub messages "Test message" --server nats://nats:4222
```

---

## 📥 Verify the data

You can check the saved messages via psql:

```bash
docker exec -it nats-subscriber-db-1 psql -U postgres -d nuts_db -c "SELECT * FROM messages;"
```

---

## 🧪 Run tests (outside Docker)

#### 1. Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Run the tests

```bash
PYTHONPATH=. pytest
```

---

## 🧩 Environment Variables

Set in `docker-compose.yml`, but you can also use a `.env` file if running locally:

```
NATS_URL=nats://localhost:4222
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/nuts_db
```

> **Note**: If running outside Docker, ensure NATS and PostgreSQL are running locally and accessible via the URLs set in the `.env` or environment variables.

---

## 🔧 Common Issues

#### ❗ `psycopg2` fails to install during `docker-compose build`
**Error:**
```
Error: pg_config executable not found.
```

**Fix:**
Use `psycopg2-binary` instead of `psycopg2`:

---

#### ❗ `ERROR: relation "messages" does not exist` when querying the DB

**Cause:**
The `messages` table has not been created.

**Fixes:**
- Ensure your application runs the DB schema creation on startup, *or*
- Manually execute the SQL script:
  ```bash
  docker exec -i nats-subscriber-db-1 psql -U postgres -d nuts_db < migrations/init_db.sql
  ```

---

#### ❗ `port is already allocated` on 4222 or 5432

**Cause:**
Another process (e.g., a local Postgres instance or previously crashed NATS container) is using the same port.

**Fix:**

Stop existing containers or services:
```bash
docker ps
```

Find the **container_id**

```bash
docker stop <container_id>
```

Or kill processes using the port:

```bash
sudo lsof -i :5432
```

Find the **PID**

```bash
sudo kill <pid>
```

---

#### ❗ `nats: no servers available for connection`

**Cause:**
- You're publishing messages from a container outside the correct Docker network.
- The hostname `nats` is not resolvable from your client.

**Fix:**
Use the correct `--network` and `--server` when running the publisher:

```bash
docker run --rm -it --network=nats-subscriber_default natsio/nats-box nats pub messages "Test" --server nats://nats:4222
```

---

#### ❗ `lookup nats on ... no such host`

**Cause:**
DNS resolution failed from a container not in the same Docker network.

**Fix:**
Use the `--network` flag when running containers like `nats-box`.

---

## 🐛 Troubleshooting

#### Port already in use
Make sure no other process is using port `4222` (NATS) or `5432` (PostgreSQL).
You can stop containers with:
```bash
docker-compose down
```

#### NATS client error: no servers available
Ensure you're using the correct Docker network.
The `nats` hostname only works inside the `nats-subscriber_default` network.

#### `psycopg2` build error
If you install locally, use `psycopg2-binary` instead of `psycopg2`.

---

## 🔒 Security Note

This project uses default credentials in `docker-compose.yml`.
**Change the database password**, and **avoid exposing services directly to the internet**.

---
