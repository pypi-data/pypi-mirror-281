# loe-simp-app-fw

A super simple python app framework that includes a logger and a config manager. This framework is also useable in Jupyter Notebook.

In addition to those function, it has a CSV IO object, a Caching object to help with common data tasks.

## Example

To get started, 

```bash
python3 -m loe_simp_app_fw init-repo
```

It will generate a project structure,

```
project directory
├── .gitignore
├── .cache
│   └── (Hashed file name)
├── config-framework.yaml
├── config-project.yaml
├── LICENSE
├── log
│   └── 2024-04-16.log
├── README.md
└── src
    ├── configuration.py
    └── main.py

```

## What happens after init

In `configuration.py`, after the initialization, it would be,

```python
from loe_simp_app_fw import BaseConfig, FrameworkConfig, Logger

class ProjectConfig(BaseConfig):
    @classmethod
    def start_developer_mode(cls) -> None:
        """
        Developer mode force the usage of the default configuration of ProjectConfig,
            i.e., the one above, rather than the one in config-project.yaml
        """
        Logger.warning(f"Project config is now in developer mode, settings from config-project.yaml will be ignored")
        return

    # Add tunable here
    example_tunable: ClassVar[str] = "ExAmPlE"

if Config.developer_mode:
    # Skip loading the config
    ProjectConfig.start_developer_mode()
else:
    # Load the config 
    ProjectConfig.load(FrameworkConfig)

# Combine two config
class Config(ProjectConfig, FrameworkConfig):
    pass

# Init logger
Logger(Config.log_directory, project_root_path = Config.project_directory, log_level = Config.log_level, buffering = Config.log_buffer_size)

Logger.info("Configuration finish initialization")
```

One may add additional tunables under ProjectConfig as a class variable.

In `main.py`, after the initialization, it would be

```python
from loe_simp_app_fw import Logger
from configuration import Config

```

## Basic Usage

### Logger usage

```python
from loe_simp_app_fw import Logger

Logger.debug("This is a debug message.")
Logger.info("This is a info message.")
Logger.warning("This is a warning message.")
Logger.error("This is a error message.")
```

### Config usage

```python
from configuration import Config

something = Config.log_level
```

## .gitignore

`.gitignore` file will be generated for the project.

In addition to the python gitignore template from GitHub, the following are also added.

```.gitignore
# Loe's Simple App Framework
playground*
database*
config*.yaml
raw
middleware
.cache*
perf/
temp
```
