business logic for shop (Store service, Order domain, Product domain)

### install dependencies

```
poetry install --no-root
```

### run app

```
poetry run python app/main.py
```

### run tests

```
poetry run coverage run -m pytest --verbose app/tests
```

### run tests coverage

```
poetry run coverage report -m
```
