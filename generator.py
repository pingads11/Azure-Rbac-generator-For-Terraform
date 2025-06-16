import json
from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient


def fetch_activity_logs(subscription_id, service_principal_name, start_time, end_time):
    """
    Fetches Azure Activity Logs for a specific service principal.
    
    Args:
        subscription_id (str): Azure subscription ID.
        service_principal_name (str): The service principal name to filter logs.
        start_time (datetime): The start time for fetching logs.
        end_time (datetime): The end time for fetching logs.
    
    Returns:
        list: List of activity log records.
    """
    try:
        # Authenticate using DefaultAzureCredential (ensure you are logged in to Azure CLI or environment variables are set)
        credential = DefaultAzureCredential()

        # Initialize the Monitor Management Client
        monitor_client = MonitorManagementClient(credential, subscription_id)

        # Query Activity Logs
        logs = monitor_client.activity_logs.list(
            filter=(
                f"eventTimestamp ge {start_time.strftime('%Y-%m-%dT%H:%M:%SZ')} and "
                f"eventTimestamp le {end_time.strftime('%Y-%m-%dT%H:%M:%SZ')}"
                # f"caller eq '{service_principal_name}'"
            )
        )

        return list(logs)

    except Exception as e:
        print(f"Error fetching activity logs: {e}")
        return []


def generate_role_definition(subscription_id, activity_logs, role_name, role_description):
    """
    Generates a custom Azure role definition JSON based on extracted activity logs.
    
    Args:
        subscription_id (str): Azure subscription ID.
        activity_logs (list): List of activity logs to process.
        role_name (str): Name of the custom Azure role.
        role_description (str): Description of the custom Azure role.
    
    Returns:
        str: Path to the generated role definition file.
    """
    try:
        # Extract unique operation names from the activity logs
        operation_names = set()
        for log in activity_logs:
            operation_name = log.operation_name.value if log.operation_name else None
            if operation_name:
                operation_names.add(operation_name)

        # Create a CRD (Custom Role Definition template)
        custom_role = {
            "Name": role_name,
            "Description": role_description,
            "Actions": sorted(operation_names),  # Sorted for consistency
            "NotActions": [],
            "AssignableScopes": [f"/subscriptions/{subscription_id}"]
        }

        # Output the custom role JSON to a file
        output_file = "custom-role.json"
        with open(output_file, "w") as json_file:
            json.dump(custom_role, json_file, indent=4)

        print(f"Custom role definition created and saved to '{output_file}'")
        print(f"Total number of unique operations: {len(operation_names)}")

        return output_file

    except Exception as e:
        print(f"Error generating role definition: {e}")
        return None


if __name__ == "__main__":
    # Input parameters
    subscription_id = "xxxx"            # Replace with your subscription ID
    service_principal_name = "AZR-xxxx"   # Replace with your service principal name
    role_name = "Custom Role for Service Principal"
    role_description = "Custom role containing operations performed by the service principal."
    start_time = datetime.utcnow() - timedelta(days=30)   # Last 30 days
    end_time = datetime.utcnow()

    # Step 1: Fetch activity logs for the service principal
    print(f"Fetching activity logs for service principal '{service_principal_name}'...")
    activity_logs = fetch_activity_logs(subscription_id, service_principal_name, start_time, end_time)
    print(f"Total activity logs fetched: {len(activity_logs)}")

    if not activity_logs:
        print("No activity logs found for the specified service principal.")
    else:
        # Step 2: Generate the role definition JSON
        print("Generating custom role definition...")
        generate_role_definition(subscription_id, activity_logs, role_name, role_description)
