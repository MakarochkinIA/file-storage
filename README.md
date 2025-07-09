Simple app to store and download files

To start use:

```
cd infra
docker compose up
```

To access the swagger go to:
```
localhost:7600/api/docs/
```

Example: File Upload:

```
curl -X POST http://localhost:7600/api/v1/files/upload/ \
  -F "file=@./example.pdf"
```

.env:
SECRET_KEY
MONGO_DB_HOST
DEBUG

