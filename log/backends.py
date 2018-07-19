from smtplib import SMTPAuthenticationError

import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import ServiceReturnedUnexpectedResult, ServiceUnavailable


class CeleryHealthCheckBackend(BaseHealthCheckBackend):
    #: The status endpoints will respond with a 200 status code
    #: even if the check errors.
    critical_service = False

    def check_status(self):
        from core.tasks import add
        timeout = getattr(settings, 'HEALTHCHECK_CELERY_TIMEOUT', 3)
        try:
            result = add.delay(4, 4)
            result.get(timeout=timeout)
            if result.result != 8:
                self.add_error(ServiceReturnedUnexpectedResult("Celery returned wrong result"))
        except IOError as e:
            self.add_error(ServiceUnavailable("IOError"), e)
        except BaseException as e:
            self.add_error(ServiceUnavailable("Unknown error"), e)

    def identifier(self):
        return 'Celery'


class ProfanityCheckBackend(BaseHealthCheckBackend):
    #: The status endpoints will respond with a 200 status code
    #: even if the check errors.
    critical_service = False

    def check_status(self):
        try:
            res = requests.get('http://www.purgomalum.com/service/containsprofanity?text=kickass')
            if res.status_code != 200:
                self.add_error(ServiceReturnedUnexpectedResult(
                    "Profanity service return status code: %s" % res.status_code))
        except requests.exceptions.RequestException as e:
            self.add_error(ServiceUnavailable("Unknown error"), e)

    def identifier(self):
        return 'Profanity'


class GoogleApiCheckBackend(BaseHealthCheckBackend):
    #: The status endpoints will respond with a 200 status code
    #: even if the check errors.
    critical_service = False

    def check_status(self):
        try:
            res = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?origins=jerusalem&'
                               'destinations=Tel-Aviv&mode=driving&key=AIzaSyBuVvbfu_0nMgFmagXaWdIsVyXrL41OV-U')
            if res.status_code != 200:
                self.add_error(ServiceReturnedUnexpectedResult(
                    "Google distance api service return status code: %s" % res.status_code))
        except requests.exceptions.RequestException as e:
            self.add_error(ServiceUnavailable("Unknown error"), e)

    def identifier(self):
        return 'Google distance API'


class LogoFinderCheckBackend(BaseHealthCheckBackend):
    #: The status endpoints will respond with a 200 status code
    #: even if the check errors.
    critical_service = False

    def check_status(self):
        try:
            res = requests.get('https://www.rest.co.il/restaurants/israel/?kw=zozobra')
            if res.status_code != 200:
                self.add_error(ServiceReturnedUnexpectedResult(
                    "Logo finder service return status code: %s" % res.status_code))
        except requests.exceptions.RequestException as e:
            self.add_error(ServiceUnavailable("Unknown error"), e)

    def identifier(self):
        return 'Logo finder'


class ElasticSearchBackend(BaseHealthCheckBackend):
    #: The status endpoints will respond with a 200 status code
    #: even if the check errors.
    critical_service = False

    def check_status(self):
        try:
            res = requests.get(settings.ELASTIC_SEARCH_HOST)
            if res.status_code != 200:
                self.add_error(ServiceReturnedUnexpectedResult(
                    "ElasticSearch service return status code: %s" % res.status_code))
        except requests.exceptions.RequestException as e:
            self.add_error(ServiceUnavailable("Unknown error"), e)

    def identifier(self):
        return 'ElasticSearch'


class GmailCheckBackend(BaseHealthCheckBackend):
    #: The status endpoints will respond with a 200 status code
    #: even if the check errors.
    critical_service = False

    def check_status(self):
        try:
            EmailMultiAlternatives('s', 't', 'shifty.moti@gmail.com', ['shifty.moti@gmail.com']).send()
        except SMTPAuthenticationError as e:
            self.add_error(ServiceUnavailable("SMTP error"), e)

    def identifier(self):
        return 'Gmail checker'
