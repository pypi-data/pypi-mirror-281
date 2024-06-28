import os
import tempfile

from django.apps import AppConfig
from django.conf import settings

from wise.utils.sentry import SentryHandler


class WiseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wise"

    def ready(self):
        self._install_additional_app()
        self._configure_project_settings()
        self._configure_celery_settings()
        self._configure_prometheus_settings()
        self._configure_sentry()

    @staticmethod
    def _install_additional_app():
        additional_apps = [
            "django_prometheus",
            "django_celery_results",
            "django_celery_beat",
        ]

        for app in additional_apps:
            if app not in settings.INSTALLED_APPS:
                settings.INSTALLED_APPS.append(app)

    @staticmethod
    def _configure_project_settings():
        if not hasattr(settings, "ENV"):
            return
        env = settings.ENV
        if not hasattr(settings, "DEBUG"):
            settings.DEBUG = env.debug
        if not hasattr(settings, "SECRET_KEY"):
            settings.SECRET_KEY = env.secret_key

    @staticmethod
    def _configure_celery_settings():
        if not hasattr(settings, "ENV"):
            return

        env = settings.ENV
        if hasattr(env, "celery") and env.celery.enabled:
            if not hasattr(settings, "CELERY_TASK_DEFAULT_QUEUE"):
                settings.CELERY_TASK_DEFAULT_QUEUE = (
                    env.celery.default_queue
                    if env.celery.default_queue
                    else f"{settings.ENV.service_name}-celery"
                )  # TODO
            if not hasattr(settings, "CELERY_RESULT_BACKEND"):
                settings.CELERY_RESULT_BACKEND = "django-db"
            if not hasattr(settings, "CELERY_BEAT_SCHEDULER"):
                settings.CELERY_BEAT_SCHEDULER = (
                    "django_celery_beat.schedulers:DatabaseScheduler"
                )

            if hasattr(settings, "TESTING") and settings.TESTING:
                settings.CELERY_BROKER_URL = "memory://"
                settings.CELERY_ALWAYS_EAGER = True
                settings.CELERY_TASK_EAGER_PROPAGATES = True

            else:
                settings.CELERY_BROKER_URL = env.celery.broker_url
                settings.CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

    @staticmethod
    def _configure_prometheus_settings():
        if not hasattr(settings, "ENV"):
            return

        env = settings.ENV
        if hasattr(env, "prometheus") and env.prometheus.enabled:
            if (
                "django_prometheus.middleware.PrometheusBeforeMiddleware"
                not in settings.MIDDLEWARE
            ):
                settings.MIDDLEWARE.insert(
                    0, "django_prometheus.middleware.PrometheusBeforeMiddleware"
                )
            if (
                "django_prometheus.middleware.PrometheusAfterMiddleware"
                not in settings.MIDDLEWARE
            ):
                settings.MIDDLEWARE.append(
                    "django_prometheus.middleware.PrometheusAfterMiddleware"
                )

            coordination_dir = env.prometheus.multiproc_dir
            if not coordination_dir:
                coordination_dir = tempfile.gettempdir() + "/prometheus-multiproc-dir/"
            os.makedirs(coordination_dir, exist_ok=True)
            os.environ["PROMETHEUS_MULTIPROC_DIR"] = coordination_dir

    @staticmethod
    def _configure_sentry():
        if not hasattr(settings, "ENV"):
            return
        env = settings.ENV
        if hasattr(env, "sentry"):
            SentryHandler.setup_sentry(env.sentry)
