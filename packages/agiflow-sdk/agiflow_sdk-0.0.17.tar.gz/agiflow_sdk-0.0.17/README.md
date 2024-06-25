# AGIFlow SDK

## Getting Started
To get started with AGIFlow SDK, simply install the package using pip:

``` sh
pip install agiflow-sdk
```

## SDK Overview
AGIFlow SDK provides the following functionalities:

- Automatic tracing with OpenTelemetry.
- Decorators for manual tracing.
- Helpers to interact with backend APIs.

## Setup SDK
To set up the AGIFlow SDK client, initialize it once at the entry point of your application:

``` python
from agiflow import Agiflow

Agiflow.init(
  app_name="<YOUR_APP_NAME>",
  api_key="<AGIFLOW_API_KEY>"  # Or set AGIFLOW_API_KEY environment variable
)
```

You can find the API key on the Environment > Settings > API Key page of the AGIFlow Dashboard.

That's it! If you run your backend application with supported LLM frameworks, traces should be logged on the AGIFlow dashboard under Environment > Logs.

## Environment Variables
- AGIFLOW_BASE_URL: If you use AGIFlow with docker-compose for local development or self-hosting, set this to your self-hosted endpoint.
- AGIFLOW_API_KEY: Use different API keys for different environments.


NOTE: AGIFlow uses a separate global OpenTelemetry trace provider to ensure all LLM traces are sent to support user feedback. To use the default OpenTelemetry global trace provider, set the AGIFLOW_OTEL_PYTHON_TRACER_PROVIDER_GLOBAL environment variable to true.

## Documentation
For a complete guide, please visit [our documentation](https://docs.agiflow.io/python). 


