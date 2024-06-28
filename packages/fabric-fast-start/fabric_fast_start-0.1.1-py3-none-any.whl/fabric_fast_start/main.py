from fabric_fast_start.config.config_resolver import ConfigResolver
from fabric_fast_start.config.config_storage import AzureTableConfigManager

# export the ConfigResolver and AzureTableConfigManager classes for use in the main.py file

export = {ConfigResolver: ConfigResolver, AzureTableConfigManager: AzureTableConfigManager}


# config = {
#     ConfigResolver: ConfigResolver,
#     ConfigManager: AzureTableConfigManager
# }
