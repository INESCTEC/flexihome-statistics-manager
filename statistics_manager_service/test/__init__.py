import logging

import connexion
from flask_testing import TestCase

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from statistics_manager_service.encoder import JSONEncoder
from statistics_manager_service import Config
import unittest


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')

        connexionApp = connexion.App(__name__, specification_dir='../openapi/',
                                     options={"swagger_ui": False})
        connexionApp.app.json_encoder = JSONEncoder

        app = connexionApp.app
        app.config.from_object(Config)

        connexionApp.add_api('openapi.yaml',
                             arguments={'title': 'Statistics Manager Service'},
                             pythonic_params=True,
                             validate_responses=True)

        # Setup Flask SQLAlchemy
        db = SQLAlchemy(app)

        db.create_all()

        return app
