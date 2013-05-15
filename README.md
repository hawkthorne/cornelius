# Cornelius

REST API for Journey to the Center of Hawkthorne. LOVE lacks SSL support, so
this server provides endpoints for tasks that require SSL.

## Error Reporting

Whenever the game encoutners an error, it's reported and shipped off to Sentry.

```
POST /errors HTTP/1.1
Host: api.projecthawkthrone.com
Content-Type: application/json

{
  "message": "An error has occured",
  "tags": {
    "version": "0.0.0"
  }
}
```
