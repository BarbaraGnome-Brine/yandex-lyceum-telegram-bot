import os
import sys
from datetime import datetime
from pathlib import Path

import pytest

from bot.config import (
    admin_parse,
    parse_int,
    parse_float,
    parse_bool,
    parse_list_of_strings,
    parse_list_of_ints,
    load_settings,
    ValidationSettings,
    Settings,
    DatabaseSettings,
    MonitoringSettings,
    NotificationSettings,
)


def test_admin_parse_normal():
    assert admin_parse("123,456,789") == [123, 456, 789]


def test_admin_parse_with_spaces():
    assert admin_parse(" 123 , 456 , 789 ") == [123, 456, 789]


def test_admin_parse_single():
    assert admin_parse("123") == [123]


def test_admin_parse_empty_string():
    with pytest.raises(ValueError):
        admin_parse("")


def test_admin_parse_negative_id():
    with pytest.raises(ValueError):
        admin_parse("-123,456")


def test_admin_parse_invalid_format():
    with pytest.raises(ValueError):
        admin_parse("abc,def")


def test_admin_parse_empty_after_clean():
    with pytest.raises(ValueError):
        admin_parse(",,,")


def test_admin_parse_trailing_comma():
    assert admin_parse("123,456,") == [123, 456]


def test_admin_parse_leading_comma():
    assert admin_parse(",123,456") == [123, 456]


def test_admin_parse_zero_id():
    with pytest.raises(ValueError, match="positive number"):
        admin_parse("0")


def test_admin_parse_mixed_valid_positive():
    assert admin_parse("  42 , 7 , 100 ") == [42, 7, 100]


def test_admin_parse_large_ids():
    assert admin_parse("999999999999999,1000000000000000") == [999999999999999, 1000000000000000]



def test_admin_parse_newline_separated():
    assert admin_parse("123\n456") == [123, 456]


def test_admin_parse_unicode_ids():
    with pytest.raises(ValueError):
        admin_parse("१२३,४५६")


def test_admin_parse_tab_separated():
    assert admin_parse("123\t456") == [123, 456]


def test_admin_parse_multiple_commas():
    assert admin_parse("1,,2,,,3") == [1, 2, 3]


def test_admin_parse_only_commas():
    with pytest.raises(ValueError):
        admin_parse(",")


def test_parse_int_valid():
    assert parse_int("42") == 42
    assert parse_int("-5") == -5


def test_parse_int_with_spaces():
    assert parse_int("  123  ") == 123


def test_parse_int_invalid():
    with pytest.raises(ValueError, match="Invalid integer"):
        parse_int("abc")


def test_parse_int_empty():
    with pytest.raises(ValueError):
        parse_int("")


def test_parse_int_float_string():
    with pytest.raises(ValueError):
        parse_int("3.14")


def test_parse_int_custom_name():
    with pytest.raises(ValueError, match="PORT"):
        parse_int("no", "PORT")


def test_parse_int_leading_zeros():
    assert parse_int("00123") == 123


def test_parse_int_plus_sign():
    assert parse_int("+42") == 42


def test_parse_int_max_int():
    assert parse_int(str(2 ** 63 - 1)) == 2 ** 63 - 1


def test_parse_int_min_int():
    assert parse_int(str(-2 ** 63)) == -2 ** 63


def test_parse_int_whitespace_only():
    with pytest.raises(ValueError):
        parse_int("   ")


def test_parse_int_hex():
    with pytest.raises(ValueError):
        parse_int("0xFF")


def test_parse_float_valid():
    assert parse_float("3.14") == 3.14
    assert parse_float("-2.5") == -2.5
    assert parse_float("0.0") == 0.0


def test_parse_float_integer_string():
    assert parse_float("42") == 42.0


def test_parse_float_with_spaces():
    assert parse_float("  1.23  ") == 1.23


def test_parse_float_invalid():
    with pytest.raises(ValueError, match="Invalid float"):
        parse_float("abc")


def test_parse_float_empty():
    with pytest.raises(ValueError):
        parse_float("")


def test_parse_float_scientific_notation():
    assert parse_float("1e-5") == 1e-5
    assert parse_float("2.5e3") == 2500.0


def test_parse_float_nan():
    with pytest.raises(ValueError):
        parse_float("nan")


def test_parse_float_inf():
    with pytest.raises(ValueError):
        parse_float("inf")


def test_parse_float_whitespace_only():
    with pytest.raises(ValueError):
        parse_float("   ")


@pytest.mark.parametrize(
    "value,expected",
    [
        ("true", True),
        ("True", True),
        ("TRUE", True),
        ("1", True),
        ("yes", True),
        ("Yes", True),
        ("YES", True),
        ("false", False),
        ("False", False),
        ("FALSE", False),
        ("0", False),
        ("no", False),
        ("No", False),
        ("NO", False),
    ],
)
def test_parse_bool_valid(value, expected):
    assert parse_bool(value) == expected


def test_parse_bool_with_spaces():
    assert parse_bool("  true  ") == True
    assert parse_bool("  0  ") == False


def test_parse_bool_invalid():
    with pytest.raises(ValueError, match="Invalid boolean"):
        parse_bool("maybe")


def test_parse_bool_empty():
    with pytest.raises(ValueError):
        parse_bool("")


def test_parse_bool_whitespace():
    with pytest.raises(ValueError):
        parse_bool("   ")


def test_parse_bool_other_languages():
    with pytest.raises(ValueError):
        parse_bool("да")


def test_parse_list_of_strings_normal():
    assert parse_list_of_strings("a,b,c") == ["a", "b", "c"]


def test_parse_list_of_strings_with_spaces():
    assert parse_list_of_strings(" a , b , c ") == ["a", "b", "c"]


def test_parse_list_of_strings_empty_input():
    assert parse_list_of_strings("") == []
    assert parse_list_of_strings("   ") == []


def test_parse_list_of_strings_custom_separator():
    assert parse_list_of_strings("x;y;z", separator=";") == ["x", "y", "z"]


def test_parse_list_of_strings_empty_parts():
    assert parse_list_of_strings("a,,b") == ["a", "b"]


def test_parse_list_of_strings_trailing_separator():
    assert parse_list_of_strings("a,b,") == ["a", "b"]


def test_parse_list_of_strings_leading_separator():
    assert parse_list_of_strings(",a,b") == ["a", "b"]


def test_parse_list_of_strings_newline():
    assert parse_list_of_strings("a\nb\nc") == ["a", "b", "c"]


def test_parse_list_of_strings_tab():
    assert parse_list_of_strings("a\tb\tc") == ["a", "b", "c"]


def test_parse_list_of_strings_multiple_separators():
    assert parse_list_of_strings("a,,b,,c") == ["a", "b", "c"]


def test_parse_list_of_strings_unicode():
    assert parse_list_of_strings("привет,мир") == ["привет", "мир"]


def test_parse_list_of_ints_normal():
    assert parse_list_of_ints("1,2,3") == [1, 2, 3]


def test_parse_list_of_ints_with_spaces():
    assert parse_list_of_ints(" 10 , 20 , 30 ") == [10, 20, 30]


def test_parse_list_of_ints_empty():
    assert parse_list_of_ints("") == []


def test_parse_list_of_ints_empty_after_strip():
    assert parse_list_of_ints("   ") == []


def test_parse_list_of_ints_custom_separator():
    assert parse_list_of_ints("4;5;6", separator=";") == [4, 5, 6]


def test_parse_list_of_ints_negative_number():
    with pytest.raises(ValueError, match="positive"):
        parse_list_of_ints("1,-2,3")



def test_parse_list_of_ints_invalid_number():
    with pytest.raises(ValueError, match="Invalid integer in list"):
        parse_list_of_ints("1,abc,3")


def test_parse_list_of_ints_skip_empty():
    assert parse_list_of_ints("1,,3") == [1, 3]


def test_parse_list_of_ints_leading_trailing():
    assert parse_list_of_ints(",1,2,") == [1, 2]


def test_parse_list_of_ints_large():
    assert parse_list_of_ints("9999999999999") == [9999999999999]


def test_parse_list_of_ints_newline():
    assert parse_list_of_ints("1\n2\n3") == [1, 2, 3]


def make_settings(bot_token="123:abc", admin_ids=None, anomaly_threshold=2.0):
    if admin_ids is None:
        admin_ids = [111]
    return Settings(
        bot_token=bot_token,
        bot_name="TestBot",
        database=DatabaseSettings(),
        monitoring=MonitoringSettings(anomaly_threshold=anomaly_threshold),
        notifications=NotificationSettings(admin_ids=admin_ids),
    )


def test_validation_settings_valid():
    settings = make_settings()
    ValidationSettings(settings)


def test_validation_settings_missing_token():
    settings = make_settings(bot_token="")
    with pytest.raises(ValueError, match="Incorrect bot token"):
        ValidationSettings(settings)


def test_validation_settings_invalid_token_format():
    settings = make_settings(bot_token="not_a_token")
    with pytest.raises(ValueError, match="Incorrect bot token"):
        ValidationSettings(settings)


def test_validation_settings_missing_admin_ids():
    settings = make_settings(admin_ids=[])
    with pytest.raises(ValueError, match="No admins were given"):
        ValidationSettings(settings)


def test_validation_settings_non_positive_threshold():
    settings = make_settings(anomaly_threshold=0)
    with pytest.raises(ValueError, match="positive number"):
        ValidationSettings(settings)

    settings = make_settings(anomaly_threshold=-1.0)
    with pytest.raises(ValueError, match="positive number"):
        ValidationSettings(settings)


MINIMAL_ENV = {
    "BOT_TOKEN": "123:testtoken",
    "ADMIN_IDS": "111,222",
}


def test_load_settings_minimal(monkeypatch):
    for key, val in MINIMAL_ENV.items():
        monkeypatch.setenv(key, val)
    for var in [
        "BOT_NAME", "DATABASE_PATH", "COLLECTION_INTERVAL", "ANOMALY_THRESHOLD",
        "MIN_DATA_POINTS", "METRICS_RETENTION_DAYS", "TRACKED_METRICS",
        "ALERTS_ENABLED", "ALERTS_COOLDOWN_MINUTES", "DIGEST_TIME", "DIGEST_ENABLED",
        "LOG_LEVEL", "LOG_FILE", "LOG_FORMAT",
    ]:
        monkeypatch.delenv(var, raising=False)

    settings = load_settings()
    assert settings.bot_token == "123:testtoken"
    assert settings.notifications.admin_ids == [111, 222]
    assert settings.bot_name == "MonitoringBot"
    assert settings.database.path == "data/bot_stats.db"
    assert settings.monitoring.collection_interval == 60
    assert settings.monitoring.anomaly_threshold == 2.0
    assert settings.monitoring.min_data_points == 10
    assert settings.monitoring.metrics_retention_days == 30
    assert settings.monitoring.tracked_metrics == []
    assert settings.notifications.alerts_enabled == True
    assert settings.notifications.alerts_cooldown_minutes == 60
    assert settings.notifications.digest_time == 9
    assert settings.notifications.digest_enabled == False


def test_load_settings_missing_token(monkeypatch):
    monkeypatch.delenv("BOT_TOKEN", raising=False)
    with pytest.raises(ValueError, match="No token was found"):
        load_settings()


def test_load_settings_invalid_admin_ids(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "123:token")
    monkeypatch.setenv("ADMIN_IDS", "abc,def")
    with pytest.raises(ValueError, match="Error in the ADMIN_IDS"):
        load_settings()


def test_load_settings_custom_values(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "5")
    monkeypatch.setenv("BOT_NAME", "CustomBot")
    monkeypatch.setenv("DATABASE_PATH", "custom/path.db")
    monkeypatch.setenv("COLLECTION_INTERVAL", "30")
    monkeypatch.setenv("ANOMALY_THRESHOLD", "3.5")
    monkeypatch.setenv("MIN_DATA_POINTS", "20")
    monkeypatch.setenv("METRICS_RETENTION_DAYS", "7")
    monkeypatch.setenv("TRACKED_METRICS", "cpu,mem,disk")
    monkeypatch.setenv("ALERTS_ENABLED", "false")
    monkeypatch.setenv("ALERTS_COOLDOWN_MINUTES", "15")
    monkeypatch.setenv("DIGEST_TIME", "18")
    monkeypatch.setenv("DIGEST_ENABLED", "true")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("LOG_FILE", "custom.log")
    monkeypatch.setenv("LOG_FORMAT", "custom-format")

    settings = load_settings()
    assert settings.bot_name == "CustomBot"
    assert settings.database.path == "custom/path.db"
    assert settings.monitoring.collection_interval == 30
    assert settings.monitoring.anomaly_threshold == 3.5
    assert settings.monitoring.min_data_points == 20
    assert settings.monitoring.metrics_retention_days == 7
    assert settings.monitoring.tracked_metrics == ["cpu", "mem", "disk"]
    assert settings.notifications.alerts_enabled == False
    assert settings.notifications.alerts_cooldown_minutes == 15
    assert settings.notifications.digest_time == 18
    assert settings.notifications.digest_enabled == True
    assert settings.log_level == "DEBUG"
    assert settings.log_file == "custom.log"
    assert settings.log_format == "custom-format"


def test_load_settings_bool_variants(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    for val in ("true", "True", "1", "yes", "Yes"):
        monkeypatch.setenv("ALERTS_ENABLED", val)
        s = load_settings()
        assert s.notifications.alerts_enabled == True
    for val in ("false", "False", "0", "no", "No"):
        monkeypatch.setenv("ALERTS_ENABLED", val)
        s = load_settings()
        assert s.notifications.alerts_enabled == False


def test_load_settings_tracked_metrics_empty(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("TRACKED_METRICS", "   ")
    settings = load_settings()
    assert settings.monitoring.tracked_metrics == []


def test_load_settings_parse_int_invalid(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("COLLECTION_INTERVAL", "not_an_int")
    with pytest.raises(ValueError, match="Invalid integer"):
        load_settings()


def test_load_settings_parse_float_invalid(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("ANOMALY_THRESHOLD", "not_a_number")
    with pytest.raises(ValueError, match="Invalid float"):
        load_settings()


def test_load_settings_missing_admin_ids_env(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.delenv("ADMIN_IDS", raising=False)
    with pytest.raises(ValueError, match="ADMIN_IDS can't be empty"):
        load_settings()


def test_load_settings_empty_admin_ids(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "")
    with pytest.raises(ValueError, match="ADMIN_IDS can't be empty"):
        load_settings()


def test_load_settings_admin_ids_whitespace(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "   ")
    with pytest.raises(ValueError, match="ADMIN_IDS can't be empty"):
        load_settings()


def test_load_settings_database_path_absolute(monkeypatch, tmp_path):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    abs_path = str(tmp_path / "test.db")
    monkeypatch.setenv("DATABASE_PATH", abs_path)
    settings = load_settings()
    assert settings.database.path == abs_path


def test_load_settings_database_path_relative(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("DATABASE_PATH", "relative/path.db")
    settings = load_settings()
    assert settings.database.path.endswith("relative/path.db")


def test_load_settings_empty_tracked_metrics(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("TRACKED_METRICS", "")
    settings = load_settings()
    assert settings.monitoring.tracked_metrics == []


def test_load_settings_tracked_metrics_single(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("TRACKED_METRICS", "cpu")
    settings = load_settings()
    assert settings.monitoring.tracked_metrics == ["cpu"]


def test_load_settings_invalid_cooldown(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("ALERTS_COOLDOWN_MINUTES", "abc")
    with pytest.raises(ValueError, match="Invalid integer"):
        load_settings()


def test_load_settings_invalid_digest_time(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("DIGEST_TIME", "24")  # still valid int, no range check
    settings = load_settings()
    assert settings.notifications.digest_time == 24


def test_load_settings_negative_digest_time(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("DIGEST_TIME", "-5")
    settings = load_settings()
    assert settings.notifications.digest_time == -5


def test_load_settings_invalid_min_data_points(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("MIN_DATA_POINTS", "not_int")
    with pytest.raises(ValueError, match="Invalid integer"):
        load_settings()


def test_load_settings_invalid_retention_days(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("METRICS_RETENTION_DAYS", "thirty")
    with pytest.raises(ValueError, match="Invalid integer"):
        load_settings()


def test_load_settings_digest_enabled_variants(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("DIGEST_ENABLED", "1")
    s = load_settings()
    assert s.notifications.digest_enabled == True
    monkeypatch.setenv("DIGEST_ENABLED", "0")
    s = load_settings()
    assert s.notifications.digest_enabled == False


def test_load_settings_alerts_enabled_variants(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("ALERTS_ENABLED", "yes")
    s = load_settings()
    assert s.notifications.alerts_enabled == True
    monkeypatch.setenv("ALERTS_ENABLED", "no")
    s = load_settings()
    assert s.notifications.alerts_enabled == False


def test_load_settings_log_level_default(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    s = load_settings()
    assert s.log_level == "INFO"


def test_load_settings_log_file_default(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.delenv("LOG_FILE", raising=False)
    s = load_settings()
    assert s.log_file == "bot.log"


def test_load_settings_log_format_default(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.delenv("LOG_FORMAT", raising=False)
    s = load_settings()
    assert s.log_format == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def test_load_settings_tracked_metrics_with_custom_separator(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("TRACKED_METRICS", "cpu;mem;disk")
    settings = load_settings()
    assert settings.monitoring.tracked_metrics == ["cpu;mem;disk"]


def test_load_settings_very_large_interval(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("COLLECTION_INTERVAL", "999999999")
    settings = load_settings()
    assert settings.monitoring.collection_interval == 999999999


def test_load_settings_negative_threshold(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("ANOMALY_THRESHOLD", "-5.0")
    settings = load_settings()
    assert settings.monitoring.anomaly_threshold == -5.0


def test_validation_settings_with_negative_threshold():
    settings = make_settings(anomaly_threshold=-0.1)
    with pytest.raises(ValueError, match="positive number"):
        ValidationSettings(settings)


def test_validation_settings_with_large_threshold():
    settings = make_settings(anomaly_threshold=1e9)
    ValidationSettings(settings)


def test_validation_settings_token_without_colon():
    settings = make_settings(bot_token="123")
    with pytest.raises(ValueError, match="Incorrect bot token"):
        ValidationSettings(settings)


def test_validation_settings_token_with_multiple_colons():
    settings = make_settings(bot_token="123:abc:def")
    ValidationSettings(settings)


def test_admin_parse_mixed_valid_invalid():
    with pytest.raises(ValueError):
        admin_parse("123,abc,456")


def test_admin_parse_duplicate_ids():
    assert admin_parse("123,123") == [123, 123]


def test_admin_parse_whitespace_only():
    with pytest.raises(ValueError):
        admin_parse("   ")


def test_parse_int_very_negative():
    assert parse_int("-999999999999999999") == -999999999999999999


def test_parse_int_leading_plus():
    assert parse_int("+123") == 123


def test_parse_float_large_exponent():
    assert parse_float("1e100") == 1e100


def test_parse_float_negative_exponent():
    assert parse_float("1e-100") == 1e-100


def test_parse_bool_mixed_case():
    assert parse_bool("TrUe") == True
    assert parse_bool("FaLsE") == False
    assert parse_bool("YeS") == True
    assert parse_bool("No") == False


def test_parse_list_of_strings_very_long():
    long_str = ",".join(["item" + str(i) for i in range(1000)])
    result = parse_list_of_strings(long_str)
    assert len(result) == 1000
    assert result[0] == "item0"
    assert result[999] == "item999"


def test_parse_list_of_ints_very_long():
    long_str = ",".join(str(i) for i in range(1000))
    result = parse_list_of_ints(long_str)
    assert len(result) == 1000
    assert result[0] == 0
    assert result[999] == 999


def test_parse_list_of_strings_custom_separator_newline():
    assert parse_list_of_strings("a\nb\nc", separator="\n") == ["a", "b", "c"]


def test_parse_list_of_strings_empty_custom_separator():
    assert parse_list_of_strings("", separator=";") == []


def test_parse_list_of_ints_custom_separator_newline():
    assert parse_list_of_ints("1\n2\n3", separator="\n") == [1, 2, 3]


def test_load_settings_all_env_vars_ints_at_limits(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("ADMIN_IDS", "1")
    monkeypatch.setenv("COLLECTION_INTERVAL", str(2 ** 31 - 1))
    monkeypatch.setenv("ANOMALY_THRESHOLD", "1e6")
    monkeypatch.setenv("MIN_DATA_POINTS", str(2 ** 31 - 1))
    monkeypatch.setenv("METRICS_RETENTION_DAYS", str(2 ** 31 - 1))
    monkeypatch.setenv("ALERTS_COOLDOWN_MINUTES", str(2 ** 31 - 1))
    monkeypatch.setenv("DIGEST_TIME", str(2 ** 31 - 1))
    settings = load_settings()
    assert settings.monitoring.collection_interval == 2 ** 31 - 1
    assert settings.monitoring.anomaly_threshold == 1e6
    assert settings.monitoring.min_data_points == 2 ** 31 - 1
    assert settings.monitoring.metrics_retention_days == 2 ** 31 - 1
    assert settings.notifications.alerts_cooldown_minutes == 2 ** 31 - 1
    assert settings.notifications.digest_time == 2 ** 31 - 1
