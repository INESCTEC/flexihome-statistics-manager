#!/usr/bin/env python3

from waitress import serve
from statistics_manager_service import connexionApp, app
from statistics_manager_service.event_consumer.thread import EventConsumer


def main():
    # Register our API in connexion
    connexionApp.add_api('openapi.yaml',
                         arguments={'title': 'Statistics Manager Service'},
                         pythonic_params=True,
                         validate_responses=True)

    ec = EventConsumer()
    ec.start()

    # Start web server to serve our REST API (the program waits until an exit signal is received)
    serve(app, host='0.0.0.0', port=8080)
    # app.run(host='0.0.0.0', port=8080)

    ec.stop()

if __name__ == '__main__':
    main()
