"""
run.py

Application Entry Point

Usage
-----
Development:
    python run.py

Production:
    gunicorn run:app

Author : Team AIgnition
Version : 1.0.0
"""

import os

from app import app

from settings import (

    HOST,

    PORT,

    DEBUG

)

############################################################
# Main
############################################################

def main():

    print()

    print("=" * 70)

    print("Marketing Intelligence Platform")

    print("=" * 70)

    print(f"Environment : {os.getenv('APP_ENV', 'development')}")

    print(f"Host        : {HOST}")

    print(f"Port        : {PORT}")

    print(f"Debug       : {DEBUG}")

    print("=" * 70)

    print()

    app.run(

        host=HOST,

        port=PORT,

        debug=DEBUG,

        threaded=True

    )


############################################################

if __name__ == "__main__":

    main()

