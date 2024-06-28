from unittest.mock import MagicMock, patch

from fabric_fast_start.config.config_storage import AzureTableConfigManager


def test_initialization():
    with patch("fabric_fast_start.config.config_storage.TableServiceClient") as mock_table_service_client:
        mock_table_service_client.from_connection_string.return_value.create_table.side_effect = None
        manager = AzureTableConfigManager("fake_table_name", connection_string="fake_connection_string")
        mock_table_service_client.from_connection_string.assert_called_with("fake_connection_string")
        assert manager.connection_string == "fake_connection_string"
        assert manager.table_name == "fake_table_name"


def test_store_config():
    with patch.object(AzureTableConfigManager, "_get_table_client", return_value=MagicMock()):
        manager = AzureTableConfigManager("fake_table_name", "fake_account_name", "fake_account_key")
        manager.store_config("project", "context", "config_str")
        manager.table_client.upsert_entity.assert_called_with({"PartitionKey": "project", "RowKey": "context", "ConfigData": "config_str"})


def test_retrieve_config():
    with patch.object(AzureTableConfigManager, "_get_table_client", return_value=MagicMock()) as mock_get_table_client:
        mock_get_table_client.return_value.get_entity.return_value = {"ConfigData": "config_str"}
        manager = AzureTableConfigManager("fake_table_name", "fake_account_name", "fake_account_key")
        config = manager.retrieve_config("project", "context")
        assert config == "config_str"


def test_retrieve_config_not_found():
    with patch.object(AzureTableConfigManager, "_get_table_client", return_value=MagicMock()) as mock_get_table_client:
        mock_get_table_client.return_value.get_entity.side_effect = Exception
        manager = AzureTableConfigManager("fake_table_name", "fake_account_name", "fake_account_key")
        config = manager.retrieve_config("project", "context")
        assert config is None


def test_resolve_config():
    with patch("fabric_fast_start.config.config_storage.TableServiceClient.from_connection_string") as mock_from_conn_str:
        # Mock the from_connection_string method to return a mock TableServiceClient instance
        mock_table_service_client = MagicMock()
        mock_from_conn_str.return_value = mock_table_service_client
        # Mock the _get_table_client method to return the mock TableServiceClient instance
        mock_table_service_client.create_table.return_value = None

        with patch.object(AzureTableConfigManager, "retrieve_config", return_value="resources:\n  keyvault: my-keyvault"):
            manager = AzureTableConfigManager("fake_table_name", connection_string="fake_connection_string")
            # Proceed with the rest of your test logic
            config = manager.resolve_config("project", "context")
            # Assuming resolve_config returns a ConfigResolver instance with a 'config' attribute
            # Filter the config to only include expected keys for the test
            filtered_config = {key: config.config[key] for key in ["resources"]}
            assert filtered_config == {"resources": {"keyvault": "my-keyvault"}}
            # Ensure retrieve_config was called with the correct arguments


def test_resolve_config_with_env_vars():
    with patch("fabric_fast_start.config.config_storage.TableServiceClient.from_connection_string") as mock_from_conn_str:
        # Mock the from_connection_string method to return a mock TableServiceClient instance
        mock_table_service_client = MagicMock()
        mock_from_conn_str.return_value = mock_table_service_client
        # Mock the _get_table_client method to return the mock TableServiceClient instance
        mock_table_service_client.create_table.return_value = None

        with patch.object(AzureTableConfigManager, "retrieve_config", return_value="resources:\n  keyvault: my-keyvault") as mock_retrieve_config:
            manager = AzureTableConfigManager("fake_table_name", connection_string="fake_connection_string")
            # Proceed with the rest of your test logic
            config = manager.resolve_config("project", "context", {"DB_HOST": "localhost"})
            # Assuming resolve_config returns a ConfigResolver instance with a 'config' attribute
            # Filter the config to only include expected keys for the test
            filtered_config = {key: config.config[key] for key in ["resources"]}
            assert filtered_config == {"resources": {"keyvault": "my-keyvault"}}
            # Ensure retrieve_config was called with the correct arguments
            assert mock_retrieve_config.call_args == (("project", "context"),)
            # Ensure the ConfigResolver was updated with the provided environment variables
            assert config.config["DB_HOST"] == "localhost"


def test_resolve_config_not_found():
    with patch("fabric_fast_start.config.config_storage.TableServiceClient.from_connection_string") as mock_from_conn_str:
        # Mock the from_connection_string method to return a mock TableServiceClient instance
        mock_table_service_client = MagicMock()
        mock_from_conn_str.return_value = mock_table_service_client
        # Mock the _get_table_client method to return the mock TableServiceClient instance
        mock_table_service_client.create_table.return_value = None

        with patch.object(AzureTableConfigManager, "retrieve_config", return_value=None):
            manager = AzureTableConfigManager("fake_table_name", "fake_connection_string")
            try:
                manager.resolve_config("project", "context")
                assert False, "ValueError expected"
            except ValueError as e:
                assert str(e) == "Configuration for project 'project' and context 'context' not found"
