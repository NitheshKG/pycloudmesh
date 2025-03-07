# pycloudmesh

`pycloudmesh` is a unified Python package for retrieving reservation costs, cost insights, and budget tracking across **AWS, Azure, and GCP**.

## 🚀 Features

- Fetch **reservation costs** for AWS, Azure, and GCP.
- Retrieve **AWS cost usage**.
- Manage **AWS budgets**.
- Get **Azure reservation order details**.
- Unified interface for multiple cloud providers.

## 📌 Installation

Install `pycloudmesh` via pip:

```sh
pip install pycloudmesh
```

To upgrade to the latest version:

```sh
pip install --upgrade pycloudmesh
```

---

## 📖 Usage

### 🔹 **Import the Package**

```python
from pycloudmesh import CloudMesh
```

### 🔹 **Initialize CloudMesh for AWS, Azure, or GCP**

#### **AWS Example**

```python
aws_client = CloudMesh(
    "aws",
    access_key="your_access_key",
    secret_key="your_secret_key",
    region="us-east-1"
)
```

#### **Azure Example**

```python
azure_client = CloudMesh(
    "azure",
    subscription_id="your_subscription_id",
    token="your_azure_token"
)
```

#### **GCP Example**

```python
gcp_client = CloudMesh(
    "gcp",
    project_id="your_project_id",
    credentials_path="path/to/credentials.json"
)
```

---

## 🔍 Fetching Cloud Data

### **1️⃣ Get Reservation Costs**

```python
cost = aws_client.get_reservation_cost()
print("AWS Reservation Cost:", cost)

cost = azure_client.get_reservation_cost()
print("Azure Reservation Cost:", cost)

cost = gcp_client.get_reservation_cost()
print("GCP Reservation Cost:", cost)
```

### **2️⃣ Get AWS Cost Data**

```python
aws_cost = aws_client.get_aws_cost()
print("AWS Cost Data:", aws_cost)
```

### **3️⃣ Get AWS Budget Data**

```python
budget_data = aws_client.list_budgets(aws_account_id="your_aws_account_id")
print("AWS Budget Data:", budget_data)
```

### **4️⃣ Get Azure Reservation Order Details**

```python
reservation_details = azure_client.get_azure_reservation_order_details()
print("Azure Reservation Details:", reservation_details)
```

---

## ❗ Error Handling

If an unsupported provider is used, an error will be raised:

```python
invalid_client = CloudMesh("unknown_provider")
# Raises: ValueError: Unsupported cloud provider: unknown_provider
```

---

## 📜 License

This project is licensed under the MIT License.

## 🙌 Contributing

Pull requests and issues are welcome! Feel free to submit improvements or bug fixes.

## 📞 Contact

For questions or support, reach out via GitHub Issues or mail me at nitheshkg18@gmail.com

