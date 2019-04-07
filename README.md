# Simple App that shortens links from any given size to fixed length

## How to run

```
$ docker-compose build
```
```
$ docker-compose run web python manage.py migrate
```
```
$ docker-compose up
```

## Tests
```
$ docker-compose run web python manage.py test
```

## Link statistics
```
$ http://localhost:8000/link/get_link/<link_shortcut>/stats
```

## Set shortcut length
```
$ http://localhost:8000/link/shortcut_length
```
