from http_api.api import app
import settings

if __name__ == '__main__':
    app.run(host=settings.HTTP_API_LISTEN,
        port=settings.HTTP_API_PORT)