# -*- coding: utf-8 -*-
# Production WSGI entry point (for gunicorn etc.)
from app import app

if __name__ == "__main__":
    app.run()
