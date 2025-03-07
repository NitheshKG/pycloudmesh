from pycloudmesh.providers.aws import AWSBudgetManagement
from pycloudmesh.providers.aws import AWSCostManagement
from pycloudmesh.providers.aws import AWSReservationCost
from pycloudmesh.providers.azure import AzureReservationCost
from pycloudmesh.providers.gcp import GCPReservationCost


class CloudMesh:
    """
    CloudMesh provides a unified interface for fetching reservation costs,
    cost usage, and budget details across AWS, Azure, and GCP.
    """
    def __init__(self, provider: str, **kwargs):
        """
        Initializes CloudMesh based on the selected cloud provider.

        :param provider: Cloud provider ("aws", "azure", or "gcp").
        :param kwargs: Provider-specific authentication details.
        """
        self.provider = provider.lower()

        if self.provider == "aws":
            self.aws_reservation_client = AWSReservationCost(
                kwargs["access_key"], kwargs["secret_key"], kwargs["region"]
            )
            self.aws_cost_client = AWSCostManagement(
                kwargs["access_key"], kwargs["secret_key"], kwargs["region"]
            )
            self.aws_budget_client = AWSBudgetManagement(
                kwargs["access_key"], kwargs["secret_key"], kwargs["region"]
            )

        elif self.provider == "azure":
            self.azure_reservation_client = AzureReservationCost(kwargs["subscription_id"], kwargs["token"])

        elif self.provider == "gcp":
            self.gcp_reservation_client = GCPReservationCost(kwargs["project_id"], kwargs["credentials_path"])

        else:
            raise ValueError(f"Unsupported cloud provider: {provider}")

    def get_reservation_cost(self):
        """Fetch reservation cost for the selected cloud provider."""
        if self.provider == "aws":
            return self.aws_reservation_client.get_reservation_cost()
        elif self.provider == "azure":
            return self.azure_reservation_client.get_reservation_cost()
        elif self.provider == "gcp":
            return self.gcp_reservation_client.get_reservation_cost()

    def get_reservation_recommendation(self,
                                       /,
                                       *,
                                       subscription_id: str = None):
        """Fetch reservation recommendation for the selected cloud provider."""
        if self.provider == "aws":
            return self.aws_reservation_client.get_reservation_recommendation()
        elif self.provider == "azure":
            return self.azure_reservation_client.get_reservation_recommendation(subscription_id)
        elif self.provider == "gcp":
            return self.gcp_reservation_client.get_reservation_recommendation()

    def get_azure_reservation_order_details(self):
        """Fetch reservation order details (Only available for Azure)."""
        if self.provider == "azure":
            return self.azure_reservation_client.get_azure_reservation_order_details()
        raise AttributeError("get_azure_reservation_order_details() is only available for Azure.")

    def get_aws_cost(self):
        """Fetch the AWS cost usage (Only available for AWS)."""
        if self.provider == "aws":
            return self.aws_cost_client.get_aws_cost_data()
        raise AttributeError("get_aws_cost() is only available for AWS.")

    def list_budgets(self, aws_account_id: str, max_results: int = None, next_token: str = None):
        """Fetch AWS budget details (Only available for AWS)."""
        if self.provider == "aws":
            return self.aws_budget_client.list_budgets(
                aws_account_id,
                max_results=max_results,
                next_token=next_token
            )
        raise AttributeError("list_budgets() is only available for AWS.")
