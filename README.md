# Quickstart

### Update Configuration
Copy `example.env` to `.env` and update values

### Build and run with docker-compose or podman-compose
```bash
docker-compose build

docker-compose up
```
#### Try it out
Open your browser to http://localhost:8080

### Run outside of a container:

#### Install Dependencies
```bash
pip3 install --user pipenv

pipenv install
```

```bash
pipenv run src/app.py

## or, use the pipenv shell
pipenv shell

python src/app.py
```

#### Try with curl (so you can specify the authorized account without oauth2_proxy)
```bash
curl -H 'X-Forwarded-Email:user@example.com' http://localhost:8080
```

# Development

### Install Dependencies
```bash
pip3 install --user pipenv

pipenv install
```
### Add libraries
```bash
pipenv install library_name
```
### Use pipenv shell for your python environment
```bash
pipenv shell
```

## References

* https://bottlepy.org/
* Pipenv
* Docker / Podman

### Build Tools
* Github Source Control
* Github Actions
* Github Image Repository

### Runtime Environment
* Podman Compose or Docker Compose
* Possibly https://cloud.google.com/run

### Authentication
* https://auth0.com/
* https://github.com/oauth2-proxy/oauth2-proxy
  * see: https://developer.okta.com/blog/2022/07/14/add-auth-to-any-app-with-oauth2-proxy
