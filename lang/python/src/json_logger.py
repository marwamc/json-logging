import logging
import logging.config
import os
import time

global_indent: bool = False


class RequestIdFilter(logging.Filter):
    """
    We use this class to add key-value pairs to the log record json
    """

    service_name = "UNKNOWN"
    service_version = "NONE"
    service_step = "UNKNOWN"
    environment = "UNKNOWN"
    process_id = "NONE"
    request_uuid = "NONE"
    request_number = "NONE"
    request_uuid_unique = "NONE"
    request_status = "NONE"
    entity_name = "NONE"
    error_type = "NONE"

    def filter(self, record):
        record.service_name = self.service_name
        record.service_version = self.service_version
        record.service_step = self.service_step
        record.environment = self.environment
        record.process_id = self.process_id
        record.request_uuid = self.request_uuid
        record.request_number = self.request_number
        record.request_uuid_unique = self.request_uuid_unique
        record.request_status = self.request_status
        record.entity_name = self.entity_name
        record.error_type = self.error_type
        return True


class UTCFormatter(logging.Formatter):
    converter = time.gmtime


def get_format_str(format_type):
    formats = {
        "json": "{"
        '"service_name": "%(service_name)s", '
        '"service_version": "%(service_version)s", '
        '"service_step": "%(service_step)s", '
        '"environment": "%(environment)s", '
        '"process_id": "%(process_id)s", '
        '"request_uuid": "%(request_uuid)s", '
        '"request_number": "%(request_number)s", '
        '"request_uuid_unique": "%(request_uuid_unique)s", '
        '"request_status": "%(request_status)s", '
        '"entity_name": "%(entity_name)s", '
        '"error_type": "%(error_type)s", '
        '"timestamp": "%(asctime)s", '
        '"log_level": "%(levelname)s", '
        '"file_name:lineno": "%(filename)s:%(lineno)s", '
        '"message": "%(message)s" }',
        "flat": "%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(entity_name)s|%(message)s",
    }
    return formats[format_type]


def setup_logging(
    default_level=logging.INFO,
    log_prefix="",
    format_type="json",
    indent=False,
    service_name=os.getenv("SERVICE_NAME", "NONE"),
    service_step=os.getenv("SERVICE_STEP", "NONE"),
    environment_name=os.getenv("ENV_NAME", "NONE")
):
    global global_indent
    global_indent = indent

    """Setup logging configuration """
    RequestIdFilter.environment = environment_name or os.getenv("ENVIRONMENT_NAME", "UNKNOWN")
    RequestIdFilter.service_name = service_name or os.getenv("APPLICATION_NAME", "UNKNOWN")
    RequestIdFilter.service_step = service_step or "UNKNOWN"
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "utc": {"()": UTCFormatter, "format": get_format_str(format_type=format_type),}
        },
        "filters": {"request_id": {"()": RequestIdFilter}},
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "utc",
                "stream": "ext://sys.stdout",
                "filters": ["request_id"],
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }
    logging.config.dictConfig(log_config)


def set_log_record_field(
    service_name=None,
    service_version=None,
    service_step=None,
    environment=None,
    process_id=None,
    request_uuid=None,
    request_number=None,
    request_status=None,
    entity_name=None,
    error_type=None,
):
    RequestIdFilter.service_name = service_name or RequestIdFilter.service_name
    RequestIdFilter.service_version = service_version or RequestIdFilter.service_version
    RequestIdFilter.service_step = service_step or RequestIdFilter.service_step
    RequestIdFilter.environment = environment or RequestIdFilter.environment
    RequestIdFilter.request_uuid = request_uuid or RequestIdFilter.request_uuid
    RequestIdFilter.request_number = request_number or RequestIdFilter.request_number
    RequestIdFilter.request_uuid_unique = (
        f"{RequestIdFilter.request_uuid}_{str(RequestIdFilter.request_number)}"
    )
    RequestIdFilter.process_id = process_id or RequestIdFilter.process_id
    RequestIdFilter.request_status = request_status or RequestIdFilter.request_status
    RequestIdFilter.entity_name = entity_name or RequestIdFilter.entity_name
    RequestIdFilter.error_type = error_type or RequestIdFilter.error_type


def reset_log_record_fields():
    RequestIdFilter.request_uuid = "NONE"
    RequestIdFilter.request_number = "NONE"
    RequestIdFilter.request_uuid_unique = "NONE"
    RequestIdFilter.process_id = "NONE"
    RequestIdFilter.request_status = "NONE"
    RequestIdFilter.entity_name = "NONE"
    RequestIdFilter.error_type = "NONE"


def unset_log_record_fields(field_list: list):
    for f in field_list:
        setattr(RequestIdFilter, f, "NONE")
