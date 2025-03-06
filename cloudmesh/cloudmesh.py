from cloudmesh.aws import AWSReservationCost
from cloudmesh.azure import AzureReservationCost
from cloudmesh.gcp import GCPReservationCost

class CloudMesh:
    def __init__(self, provider, **kwargs):
        if provider == "aws":
            self.client = AWSReservationCost(kwargs["access_key"], kwargs["secret_key"], kwargs["region"])
        elif provider == "azure":
            self.client = AzureReservationCost(kwargs["subscription_id"], kwargs["token"])
        elif provider == "gcp":
            self.client = GCPReservationCost(kwargs["project_id"], kwargs["credentials_path"])
        else:
            raise ValueError("Unsupported cloud provider")

    def get_reservation_cost(self):
        return self.client.get_reservation_cost()
