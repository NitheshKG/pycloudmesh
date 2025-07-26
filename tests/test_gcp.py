#!/usr/bin/env python3
"""
Test file for GCP cloud functionality using unittest framework.
"""

import sys
import os
import unittest
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pycloudmesh import gcp_client
from pycloudmesh.pycloudmesh import GCPProvider
from pycloudmesh.providers.gcp import (
    GCPReservationCost, GCPBudgetManagement, GCPCostManagement,
    GCPFinOpsOptimization, GCPFinOpsGovernance, GCPFinOpsAnalytics
)

# Load environment variables
load_dotenv()

# Configuration flag for response storage
RESPONSE_STORE = True  # Set to False to disable response storage

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
GCP_CREDENTIAL_PATH = os.environ.get("GCP_CREDENTIAL_PATH")
GCP_BILLING_ACCOUNT = os.environ.get("GCP_BILLING_ACCOUNT_ID")
BQ_PROJECT_ID = GCP_PROJECT_ID
BQ_DATASET = os.environ.get("GCP_BQ_DATASET")
BQ_TABLE = os.environ.get("GCP_BQ_TABLE")

class TestGCPClient(unittest.TestCase):
    """Test cases for GCP client functionality."""

    @classmethod
    def setUpClass(cls):
        cls.gcp = gcp_client(GCP_PROJECT_ID, GCP_CREDENTIAL_PATH)
        cls.gcp_provider = GCPProvider(GCP_PROJECT_ID, GCP_CREDENTIAL_PATH)
        cls.budget_client = GCPBudgetManagement(GCP_PROJECT_ID, GCP_CREDENTIAL_PATH)
        cls.cost_client = GCPCostManagement(GCP_PROJECT_ID, GCP_CREDENTIAL_PATH)
        cls.reservation_client = GCPReservationCost(GCP_PROJECT_ID, GCP_CREDENTIAL_PATH)
        cls.optimization_client = GCPFinOpsOptimization(GCP_PROJECT_ID, GCP_CREDENTIAL_PATH)
        cls.governance_client = GCPFinOpsGovernance(GCP_PROJECT_ID, GCP_CREDENTIAL_PATH)
        cls.analytics_client = GCPFinOpsAnalytics(GCP_PROJECT_ID, GCP_CREDENTIAL_PATH)
        cls.test_results = {
            "test_suite": "GCP Cloud Tests",
            "timestamp": datetime.datetime.now().isoformat(),
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "test_details": []
        }

    def setUp(self):
        self.test_start_time = datetime.datetime.now()
        self.test_response = None

    def tearDown(self):
        test_end_time = datetime.datetime.now()
        test_duration = (test_end_time - self.test_start_time).total_seconds()
        test_result = {
            "test_name": self._testMethodName,
            "status": "PASSED",
            "duration": test_duration,
            "error_message": None,
            "response": self.test_response if RESPONSE_STORE else None
        }
        self.test_results["test_details"].append(test_result)

    def test_gcp_client_creation(self):
        try:
            gcp = gcp_client(GCP_PROJECT_ID, GCP_CREDENTIAL_PATH)
            self.assertIsInstance(gcp, GCPProvider)
            self.test_response = {
                "client_type": type(gcp).__name__,
                "has_required_attributes": hasattr(gcp, 'reservation_client') and hasattr(gcp, 'cost_client') and hasattr(gcp, 'budget_client'),
                "available_clients": [attr for attr in dir(gcp) if attr.endswith('_client')]
            }
            print("✅ GCP client creation successful")
        except Exception as e:
            self.fail(f"GCP client creation failed: {str(e)}")

    def test_gcp_required_methods(self):
        required_methods = [
            'get_reservation_cost',
            'get_reservation_recommendation',
            'list_budgets',
            'get_cost_data',
            'get_cost_analysis',
            'get_cost_trends',
            'get_resource_costs',
            'get_optimization_recommendations',
            'get_cost_forecast',
            'get_cost_anomalies',
            'get_cost_efficiency_metrics',
            'generate_cost_report',
            'get_governance_policies',
            'create_budget',
            'get_budget_alerts',
            'get_machine_type_recommendations',
            'get_idle_resource_recommendations'
        ]
        missing_methods = []
        available_methods = []
        for method in required_methods:
            if hasattr(self.gcp_provider, method):
                available_methods.append(method)
            else:
                missing_methods.append(method)
        self.test_response = {
            "total_required_methods": len(required_methods),
            "available_methods": available_methods,
            "missing_methods": missing_methods,
            "all_methods_present": len(missing_methods) == 0
        }
        self.assertEqual(len(missing_methods), 0, f"Missing required methods: {missing_methods}")

    def test_gcp_list_budgets(self):
        try:
            result = self.budget_client.list_budgets(GCP_BILLING_ACCOUNT, max_results=50)
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP budget listing successful")
        except Exception as e:
            self.fail(f"GCP budget listing failed: {str(e)}")

    def test_gcp_create_budget(self):
        try:
            budget_name = f"Test_pycloudmesh_budget_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            result = self.budget_client.create_budget(
                billing_account=GCP_BILLING_ACCOUNT,
                budget_name=budget_name,
                amount=1.0,
                currency_code="USD"
            )
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP budget creation successful")
        except Exception as e:
            self.fail(f"GCP budget creation failed: {str(e)}")

    def test_gcp_get_budget_alerts(self):
        try:
            result = self.budget_client.get_budget_alerts(
                billing_account=GCP_BILLING_ACCOUNT,
                budget_display_name="pycloudmesh_budget"
            )
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP budget alerts retrieval successful")
        except Exception as e:
            self.fail(f"GCP budget alerts retrieval failed: {str(e)}")

    def test_gcp_get_cost_data(self):
        try:
            result = self.cost_client.get_cost_data(
                start_date="2025-06-01",
                end_date="2025-07-03",
                granularity="DAILY",
                group_by=["service.description"],
                bq_project_id=BQ_PROJECT_ID,
                bq_dataset=BQ_DATASET,
                bq_table=BQ_TABLE
            )
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP cost data retrieval successful")
        except Exception as e:
            self.fail(f"GCP cost data retrieval failed: {str(e)}")

    def test_gcp_get_cost_analysis(self):
        try:
            result = self.cost_client.get_cost_analysis(
                start_date="2025-06-01",
                end_date="2025-07-03",
                bq_project_id=BQ_PROJECT_ID,
                bq_dataset=BQ_DATASET,
                bq_table=BQ_TABLE
            )
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP cost analysis successful")
        except Exception as e:
            self.fail(f"GCP cost analysis failed: {str(e)}")

    def test_gcp_get_cost_trends(self):
        try:
            result = self.cost_client.get_cost_trends(
                start_date="2025-06-01",
                end_date="2025-07-03",
                granularity="DAILY",
                bq_project_id=BQ_PROJECT_ID,
                bq_dataset=BQ_DATASET,
                bq_table=BQ_TABLE
            )
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP cost trends retrieval successful")
        except Exception as e:
            self.fail(f"GCP cost trends retrieval failed: {str(e)}")

    def test_gcp_get_resource_costs(self):
        try:
            result = self.cost_client.get_resource_costs(
                resource_name="pycloudmesh",
                bq_project_id=BQ_PROJECT_ID,
                bq_dataset=BQ_DATASET,
                bq_table=BQ_TABLE
            )
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP resource costs retrieval successful")
        except Exception as e:
            self.fail(f"GCP resource costs retrieval failed: {str(e)}")

    def test_gcp_get_reservation_cost(self):
        try:
            result = self.reservation_client.get_reservation_cost(
                bq_project_id=BQ_PROJECT_ID,
                bq_dataset=BQ_DATASET,
                bq_table=BQ_TABLE,
                start_date="2025-06-01",
                end_date="2025-07-03"
            )
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP reservation cost retrieval successful")
        except Exception as e:
            self.fail(f"GCP reservation cost retrieval failed: {str(e)}")

    def test_gcp_get_reservation_recommendation(self):
        try:
            result = self.reservation_client.get_reservation_recommendation()
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP reservation recommendation retrieval successful")
        except Exception as e:
            self.fail(f"GCP reservation recommendation retrieval failed: {str(e)}")

    def test_gcp_get_optimization_recommendations(self):
        try:
            result = self.optimization_client.get_optimization_recommendations()
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP optimization recommendations retrieval successful")
        except Exception as e:
            self.fail(f"GCP optimization recommendations retrieval failed: {str(e)}")

    def test_gcp_get_machine_type_recommendations(self):
        try:
            result = self.optimization_client.get_machine_type_recommendations()
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP machine type recommendations retrieval successful")
        except Exception as e:
            self.fail(f"GCP machine type recommendations retrieval failed: {str(e)}")

    def test_gcp_get_idle_resource_recommendations(self):
        try:
            result = self.optimization_client.get_idle_resource_recommendations()
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP idle resource recommendations retrieval successful")
        except Exception as e:
            self.fail(f"GCP idle resource recommendations retrieval failed: {str(e)}")

    def test_gcp_get_cost_allocation_tags(self):
        try:
            result = self.governance_client.get_cost_allocation_tags(
                bq_project_id=BQ_PROJECT_ID,
                bq_dataset=BQ_DATASET,
                bq_table=BQ_TABLE
            )
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP cost allocation tags retrieval successful")
        except Exception as e:
            self.fail(f"GCP cost allocation tags retrieval failed: {str(e)}")

    def test_gcp_get_policy_compliance(self):
        try:
            result = self.governance_client.get_policy_compliance()
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP policy compliance retrieval successful")
        except Exception as e:
            self.fail(f"GCP policy compliance retrieval failed: {str(e)}")

    def test_gcp_get_cost_policies(self):
        try:
            result = self.governance_client.get_cost_policies(
                gcp_billing_account=GCP_BILLING_ACCOUNT
            )
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP cost policies retrieval successful")
        except Exception as e:
            self.fail(f"GCP cost policies retrieval failed: {str(e)}")

    def test_gcp_get_cost_anomalies(self):
        try:
            result = self.analytics_client.get_cost_anomalies(
                bq_project_id=BQ_PROJECT_ID,
                bq_dataset=BQ_DATASET,
                bq_table=BQ_TABLE
            )
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP cost anomalies retrieval successful")
        except Exception as e:
            self.fail(f"GCP cost anomalies retrieval failed: {str(e)}")

    def test_gcp_get_cost_efficiency_metrics(self):
        try:
            result = self.analytics_client.get_cost_efficiency_metrics(
                bq_project_id=BQ_PROJECT_ID,
                bq_dataset=BQ_DATASET,
                bq_table=BQ_TABLE
            )
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP cost efficiency metrics retrieval successful")
        except Exception as e:
            self.fail(f"GCP cost efficiency metrics retrieval failed: {str(e)}")

    def test_gcp_generate_cost_report(self):
        try:
            result = self.analytics_client.generate_cost_report(
                bq_project_id=BQ_PROJECT_ID,
                bq_dataset=BQ_DATASET,
                bq_table=BQ_TABLE
            )
            self.test_response = result
            self.assertIsInstance(result, dict)
            print(f"✅ GCP cost report generation successful")
        except Exception as e:
            self.fail(f"GCP cost report generation failed: {str(e)}")

    @classmethod
    def tearDownClass(cls):
        cls.generate_test_report()

    @classmethod
    def generate_test_report(cls):
        total_tests = len(cls.test_results["test_details"])
        passed = sum(1 for test in cls.test_results["test_details"] if test["status"] == "PASSED")
        failed = sum(1 for test in cls.test_results["test_details"] if test["status"] == "FAILED")
        cls.test_results["total_tests"] = total_tests
        cls.test_results["passed"] = passed
        cls.test_results["failed"] = failed
        cls.test_results["success_rate"] = (passed / total_tests * 100) if total_tests > 0 else 0
        reports_dir = Path("tests/test_reports")
        reports_dir.mkdir(exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gcp_{timestamp}_test.json"
        filepath = reports_dir / filename
        with open(filepath, 'w') as f:
            json.dump(cls.test_results, f, indent=2, default=str)
        print("\n" + "=" * 60)
        print(f"{'GCP Test Results Summary':^60}")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {cls.test_results['success_rate']:.1f}%")
        print(f"Report saved to: {filepath}")
        print("=" * 60)
        print("\nDetailed Test Results:")
        print("-" * 60)
        for test in cls.test_results["test_details"]:
            status_icon = "✅" if test["status"] == "PASSED" else "❌"
            print(f"{status_icon} {test['test_name']:<40} {test['status']:<8} ({test['duration']:.2f}s)")
            if test["error_message"]:
                print(f"    Error: {test['error_message']}")
        return filepath

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGCPClient)
    class TestResultCollector(unittest.TestResult):
        def __init__(self):
            super().__init__()
            self.test_results = []
        def addSuccess(self, test):
            super().addSuccess(test)
            response_data = getattr(test, 'test_response', None) if RESPONSE_STORE else None
            self.test_results.append({
                "test_name": test._testMethodName,
                "status": "PASSED",
                "error_message": None,
                "response": response_data
            })
        def addFailure(self, test, err):
            super().addFailure(test, err)
            response_data = getattr(test, 'test_response', None) if RESPONSE_STORE else None
            self.test_results.append({
                "test_name": test._testMethodName,
                "status": "FAILED",
                "error_message": str(err[1]),
                "response": response_data
            })
        def addError(self, test, err):
            super().addError(test, err)
            response_data = getattr(test, 'test_response', None) if RESPONSE_STORE else None
            self.test_results.append({
                "test_name": test._testMethodName,
                "status": "FAILED",
                "error_message": str(err[1]),
                "response": response_data
            })
    result_collector = TestResultCollector()
    suite.run(result_collector)
    TestGCPClient.test_results["test_details"] = result_collector.test_results
    return result_collector.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
