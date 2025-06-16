# Azure Activity Logs to Custom Role Generator

This script fetches Azure Activity Logs for a specified service principal and generates a custom Azure role definition JSON file based on the operations found in the logs.

## Features

- Fetches Azure Activity Logs for a specific service principal
- Extracts unique operation names from the logs
- Generates a custom Azure role definition (JSON format)
- Supports customizable time range for log analysis

## Prerequisites

- Python 3.6+
- Azure CLI installed and logged in (or proper service principal credentials configured)

### Required Python Packages:
- `azure-identity`
- `azure-mgmt-monitor`

## Installation

1. Clone this repository or download the script.

2. Install the required packages:

    ```bash
    pip install azure-identity azure-mgmt-monitor
    ```

## Usage

1. Open the script and modify the following parameters:

    - `subscription_id`: Your Azure subscription ID
    - `service_principal_name`: The service principal name to analyze
    - `role_name`: Name for your custom role
    - `role_description`: Description for your custom role
    - `start_time`: Start time for log analysis (default: last 30 days)

2. Run the script:

    ```bash
    python generate_role_from_logs.py
    ```

### Script Workflow

- Fetches activity logs for the specified service principal.
- Generates a `custom-role.json` file with the role definition.
- Prints summary information about the operations found.

## Output

The script generates a JSON file (`custom-role.json`) with the following structure:

```json
{
    "Name": "Custom Role for Service Principal",
    "Description": "Custom role containing operations performed by the service principal.",
    "Actions": [
        "Microsoft.Resources/subscriptions/resourceGroups/read",
        "Microsoft.Storage/storageAccounts/listKeys/action"
    ],
    "NotActions": [],
    "AssignableScopes": [
        "/subscriptions/4001ee16-e5a3-4b9f-bf84-d806bbedd2b9"
    ]
}
