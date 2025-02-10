# Project Contributors Assignment

## Run the app

Below is the setup in order to run this application on your system.

### 1. Clone respected git repository

```
git clone git@github.com:charamis/project-contributors-assignment.git
```

### 3. Build / Run the app

```
docker compose -f docker-compose.dev.yml up --build
```

### 4. Invoke the app

Just invoke `http:/localhost:3000/api/v1/` on your API client

## Tests and other commands

### Run bash on a specific docker container to execute other commands

1. Run the app using docker compose
2. List the opened containers
   ```
   docker ps
   ```
3. Copy the ID of the API container
4. Execute bash on the specific container
   ```
   docker exec -i -t {CONTAINER_ID} bash
   ```
5. Now in this shell you can execute the commands below

### Pytest unit tests

Execute on the api container
```
./pytest.sh
```

### Generare migrations

Execute on the api container
```
./make_migrations.sh
```

### Apply Black formatting

Execute on the api container
```
./black_format.sh
```

### Add/Remove Poetry packages

Execute on the api container
```
cd ./project-contributors-api
poetry add ...
```

## Build / Run the app (Production Docker setting)

```
docker compose up --build
```