import requests

class AzureReservationCost:
    def __init__(self, subscription_id, token):
        self.subscription_id = subscription_id
        self.token = token
        self.base_url = "https://management.azure.com"

    def get_reservation_cost(self):
        """Fetch reservation cost details from Azure."""
        url = f"{self.base_url}/subscriptions/{self.subscription_id}/providers/Microsoft.Consumption/reservationSummaries?api-version=2022-10-01"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}

    def get_reservation_recommendation(self, subscription_id: str):
        """Fetch the reservation recommendation"""
        url = f"{self.base_url}/subscriptions/{subscription_id}/providers/Microsoft.Advisor/recommendations?api-version=2020-01-01"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        all_response = []

        try:
            while url:
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    response_json = response.json()
                    all_response.extend(response_json.get("value", []))

                    url = response_json.get("nextLink")
                else:
                    return {"error": f"Failed to fetch data. Status: {response.status_code}, Message: {response.text}"}

            return {"recommendations": all_response}

        except requests.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}


    def get_azure_reservation_order_details(self):
        """Fetch reservation order details from Azure."""
        url = f"{self.base_url}/providers/Microsoft.Capacity/reservationOrders?api-version=2022-11-01"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}

    def get_azure_reservation_details(self, reservation_order_id: str, reservation_id: str, grain:str ="monthly"):
        """Get the reservation details for the subscriptions based on the reservation order id"""
        url = f"{self.base_url}/providers/Microsoft.Capacity/reservationorders/{reservation_order_id}/reservations/{reservation_id}/providers/Microsoft.Consumption/reservationSummaries?grain={grain}&api-version=2024-08-01"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers)
        return response.json() if response.status_code == 200 else {"error": response.text}

