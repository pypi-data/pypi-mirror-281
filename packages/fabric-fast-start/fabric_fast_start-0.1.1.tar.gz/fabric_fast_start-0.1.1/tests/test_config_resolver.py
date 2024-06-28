import datetime

from fabric_fast_start.config.config_resolver import ConfigResolver


def test_init():
    config_str = """
    resources:
        keyvault: my_keyvault
    """
    resolver = ConfigResolver(config_str)
    assert isinstance(resolver, ConfigResolver), "Initialization failed"


def test_get_with_nested_path():
    config_str = """
    resources:
        keyvault: my_keyvault
        database:
            credentials:
                username: admin
                password: secret
    """
    resolver = ConfigResolver(config_str)
    username = resolver.get("resources.database.credentials.username")
    assert username == "admin", "Failed to get nested config value"


def test_resolve_value_without_secret():
    config_str = """
    resources:
        keyvault: my_keyvault
    """
    resolver = ConfigResolver(config_str)
    value = resolver.resolve_value("simple_value")
    assert value == "simple_value", "Failed to resolve simple value"


def test_resolve_value_with_quotes():
    config_str = """
    resources:
        keyvault: my_keyvault
    """
    resolver = ConfigResolver(config_str)
    value = resolver.resolve_value('"quoted_value"')
    assert value == "quoted_value", "Failed to strip quotes from value"


def test_resolve_number_value():
    config_str = """
    resources:
        days: 7
    """
    resolver = ConfigResolver(config_str)
    value = resolver.get("resources.days")
    assert value == 7, "Failed to resolve number value"


def test_resolve_date_value():
    config_str = """
    resources:
        start_date: 2021-01-01
    """
    resolver = ConfigResolver(config_str)
    value = resolver.get("resources.start_date")
    assert value == datetime.date(2021, 1, 1), "Failed to resolve date value"


def test_get_secret_not_found(mocker):
    # Mocking mssparkutils.credentials.getSecret to raise an exception
    mocker.patch("fabric_fast_start.config.config_resolver.mssparkutils.credentials.getSecret", side_effect=Exception("Secret not found"))

    config_str = """
    resources:
        keyvault: my_keyvault
    """
    resolver = ConfigResolver(config_str)
    try:
        resolver.get_secret("my_keyvault", "nonexistent_secret")
        assert False, "Expected an exception for a nonexistent secret"
    except Exception as e:
        assert str(e) == "Secret not found", "Unexpected exception message"


def test_resolve_config_with_invalid_syntax():
    config_str = """
    resources:
        keyvault: my_keyvault
        database:
            credentials:
                username: admin
                password: {secret:db-password
    """
    try:
        ConfigResolver(config_str)
        assert False, "Expected an exception for invalid YAML syntax"
    except Exception as e:
        assert "while parsing a flow mapping" in str(e) or "expected ',' or '}'" in str(e), "Unexpected exception message"


def test_resolve_config_with_undefined_placeholder():
    config_str = """
    resources:
        keyvault: my_keyvault
    database:
        credentials:
            username: admin
            password: "{undefined:db-password}"
    undefined:
        some-key: some-value
    """
    try:
        ConfigResolver(config_str)
        assert False, "Expected an exception for an undefined placeholder"
    except ValueError as e:
        assert "Undefined placeholder value: db-password for type undefined" in str(e), f"Unexpected exception message: {str(e)}"
