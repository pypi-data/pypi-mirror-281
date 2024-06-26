# b-utils-infra

`b-utils-infra` is a collection of utility functions and classes designed to streamline and enhance your Python
projects. The
library is organized into several modules, each catering to different categories of utilities, including logging, client
interactions, data manipulation with pandas, and general-purpose functions.

## Installation

You can install `b-utils-infra` using pip:

```bash
pip install b-utils-infra
```

## Structure

The library is organized into the following modules:

1. logging.py
   This module provides utilities for logging with SlackAPI and writing to a file.
2. ai.py
   This module contains utilities for working with AI models, such as token count, tokenization, and text generation.
3. translation.py
   This module offers utilities for working with translation APIs, such as Google Translate and DeepL.
4. services.py
   This module contains services-related utilities, such as creating google service.
5. pandas.py
   This module offers utilities for working with pandas dataframes, including data cleaning, insertion into databases,
   and other common dataframe operations.
6. generic.py
   This module includes miscellaneous utilities that don't fit into the other specific categories. These functions are
   designed to be broadly useful across different parts of your codebase.

## Usage

Below are examples of how to use some of the utilities provided by b-utils.

Logging Utilities

```python
from b_utils_infra.logging import SlackLogger

logger = SlackLogger(project_name="your-project-name", slack_token="your-slack-token", slack_channel_id="channel-id")
logger.info("This is an info message")
logger.error(exc=Exception, header_message="Header message appears above the exception message in the Slack message")
```

Client Utilities

```python
from b_utils_infra.clients import SlackAPI

slack_client = SlackAPI(token="your-slack-token")
slack_client.send_message(channel="#general", message="Hello, Slack!")
```

Pandas Utilities

```python
import pandas as pd
from b_utils_infra.pandas import clean_dataframe

df = pd.read_csv("data.csv")
clean_df = clean_dataframe(df)
```

Generic Utilities

```python
from b_utils_infra.generic import retry_with_timeout, validate_numeric_value


@retry_with_timeout(retries=3, timeout=5)
def fetch_data():
    # function logic here
    pass


is_valid = validate_numeric_value(123)
print(is_valid)  # Output: True
```

## Changelog

For all the changes and version history, see the [CHANGELOG](CHANGELOG.md).

## License

This project is licensed under the MIT License. See the LICENSE file for details.