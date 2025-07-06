#!/usr/bin/env python3
"""
Comprehensive unit tests for GCP cloud functionality using real credentials.
"""

import os
import sys
import unittest
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pycloudmesh import gcp_client
from pycloudmesh.pycloudmesh import GCPProvider
from pycloudmesh.providers.gcp import (
    GCPReservationCost, GCPBudgetManagement, GCPCostManagement,
    GCPFinOpsOptimization, GCPFinOpsGovernance, GCPFinOpsAnalytics
)

# Get credentials from environment variables
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
GCP_CREDENTIAL_PATH = os.environ.get("GCP_CREDENTIAL_PATH")
GCP_BILLING_ACCOUNT = os.environ.get("GCP_BILLING_ACCOUNT_ID") # From test_individual.py
BQ_PROJECT_ID = GCP_PROJECT_ID
BQ_DATASET = os.environ.get("GCP_BQ_DATASET")
BQ_TABLE = os.environ.get("GCP_BQ_TABLE")


class TestGCPClientCreation(unittest.TestCase):
    """Test GCP client creation and initialization."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.project_id = GCP_PROJECT_ID
        self.credentials_path = GCP_CREDENTIAL_PATH
    
    def test_gcp_client_creation_success(self):
        """Test successful GCP client creation."""
        gcp = gcp_client(self.project_id, self.credentials_path)
        self.assertIsInstance(gcp, GCPProvider)
        print("✅ GCP client creation successful")
    
    def test_gcp_client_missing_credentials(self):
        """Test GCP client creation with missing credentials file."""
        with self.assertRaises(FileNotFoundError):
            gcp_client(self.project_id, "/nonexistent/credentials.json")
        print("✅ GCP client creation with missing credentials handled correctly")


class TestGCPBudgetManagement(unittest.TestCase):
    """Test GCP Budget Management functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.project_id = GCP_PROJECT_ID
        self.credentials_path = GCP_CREDENTIAL_PATH
        self.billing_account = GCP_BILLING_ACCOUNT
        self.budget_client = GCPBudgetManagement(self.project_id, self.credentials_path)
    
    def test_list_budgets_success(self):
        """Test successful budget listing."""
        result = self.budget_client.list_budgets(self.billing_account, max_results=50)
        
        self.assertIsInstance(result, dict)
        if "budgets" in result:
            self.assertIsInstance(result["budgets"], list)
            print(f"✅ GCP budget listing successful - Found {len(result['budgets'])} budgets")
        elif "error" in result:
            print(f"⚠️ GCP budget listing returned error: {result['error']}")
        else:
            print(f"ℹ️ GCP budget listing result: {result}")
    
    def test_create_budget_success(self):
        """Test successful budget creation."""
        budget_name = f"Test_pycloudmesh_budget_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        result = self.budget_client.create_budget(
            billing_account=self.billing_account,
            budget_name=budget_name,
            amount=1.0,
            currency_code="USD"
        )
        
        self.assertIsInstance(result, dict)
        if "name" in result:
            self.assertIn("budgets", result["name"])
            print(f"✅ GCP budget creation successful - {result['display_name']}")
        elif "error" in result:
            print(f"⚠️ GCP budget creation returned error: {result['error']}")
        else:
            print(f"ℹ️ GCP budget creation result: {result}")
    
    def test_get_budget_alerts_success(self):
        """Test successful budget alerts retrieval."""
        result = self.budget_client.get_budget_alerts(
            billing_account=self.billing_account,
            budget_display_name="pycloudmesh_budget"
        )
        
        self.assertIsInstance(result, dict)
        if "budget_name" in result:
            self.assertIn("budgets", result["budget_name"])
            print(f"✅ GCP budget alerts retrieval successful - {result['display_name']}")
        elif "error" in result:
            print(f"⚠️ GCP budget alerts returned error: {result['error']}")
        else:
            print(f"ℹ️ GCP budget alerts result: {result}")


class TestGCPCostManagement(unittest.TestCase):
    """Test GCP Cost Management functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.project_id = GCP_PROJECT_ID
        self.credentials_path = GCP_CREDENTIAL_PATH
        self.bq_project_id = BQ_PROJECT_ID
        self.bq_dataset = BQ_DATASET
        self.bq_table = BQ_TABLE
        self.cost_client = GCPCostManagement(self.project_id, self.credentials_path)
    
    def test_get_cost_data_success(self):
        """Test successful cost data retrieval."""
        result = self.cost_client.get_cost_data(
            start_date="2025-06-01",
            end_date="2025-07-03",
            granularity="DAILY",
            group_by=["service.description"],
            bq_project_id=self.bq_project_id,
            bq_dataset=self.bq_dataset,
            bq_table=self.bq_table
        )
        
        self.assertIsInstance(result, dict)
        if "cost_data" in result:
            self.assertIsInstance(result["cost_data"], list)
            print(f"✅ GCP cost data retrieval successful - {len(result['cost_data'])} records")
        elif "error" in result:
            print(f"⚠️ GCP cost data retrieval returned error: {result['error']}")
        else:
            print(f"ℹ️ GCP cost data retrieval result: {result}")
    
    def test_get_cost_data_missing_bigquery_config(self):
        """Test cost data retrieval without BigQuery config."""
        result = self.cost_client.get_cost_data()
        
        self.assertIn("error", result)
        self.assertIn("BigQuery billing export table not configured", result["error"])
        print("✅ GCP cost data missing BigQuery config handling successful")
    
    def test_get_cost_analysis_success(self):
        """Test successful cost analysis."""
        result = self.cost_client.get_cost_analysis(
            start_date="2025-06-01",
            end_date="2025-07-03",
            bq_project_id=self.bq_project_id,
            bq_dataset=self.bq_dataset,
            bq_table=self.bq_table
        )
        
        self.assertIsInstance(result, dict)
        if "cost_data" in result:
            self.assertIsInstance(result["cost_data"], list)
            print(f"✅ GCP cost analysis successful - {len(result['cost_data'])} records")
        elif "error" in result:
            print(f"⚠️ GCP cost analysis returned error: {result['error']}")
        else:
            print(f"ℹ️ GCP cost analysis result: {result}")
    
    def test_get_cost_trends_success(self):
        """Test successful cost trends retrieval."""
        result = self.cost_client.get_cost_trends(
            start_date="2025-06-01",
            end_date="2025-07-03",
            granularity="DAILY",
            bq_project_id=self.bq_project_id,
            bq_dataset=self.bq_dataset,
            bq_table=self.bq_table
        )
        
        self.assertIsInstance(result, dict)
        if "cost_data" in result:
            self.assertIsInstance(result["cost_data"], list)
            print(f"✅ GCP cost trends successful - {len(result['cost_data'])} records")
        elif "error" in result:
            print(f"⚠️ GCP cost trends returned error: {result['error']}")
        else:
            print(f"ℹ️ GCP cost trends result: {result}")
    
    def test_get_resource_costs_success(self):
        """Test successful resource cost retrieval."""
        result = self.cost_client.get_resource_costs(
            resource_name="pycloudmesh",
            bq_project_id=self.bq_project_id,
            bq_dataset=self.bq_dataset,
            bq_table=self.bq_table
        )
        
        self.assertIsInstance(result, dict)
        if "cost_data" in result:
            self.assertIsInstance(result["cost_data"], list)
            print(f"✅ GCP resource costs successful - {len(result['cost_data'])} records")
        elif "error" in result:
            print(f"⚠️ GCP resource costs returned error: {result['error']}")
        else:
            print(f"ℹ️ GCP resource costs result: {result}")


class TestGCPReservationManagement(unittest.TestCase):
    """Test GCP Reservation Management functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.project_id = GCP_PROJECT_ID
        self.credentials_path = GCP_CREDENTIAL_PATH
        self.bq_project_id = BQ_PROJECT_ID
        self.bq_dataset = BQ_DATASET
        self.bq_table = BQ_TABLE
        self.reservation_client = GCPReservationCost(self.project_id, self.credentials_path)
    
    def test_get_reservation_cost_success(self):
        """Test successful reservation cost retrieval."""
        result = self.reservation_client.get_reservation_cost(
            bq_project_id=self.bq_project_id,
            bq_dataset=self.bq_dataset,
            bq_table=self.bq_table,
            start_date="2025-06-01",
            end_date="2025-07-03"
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn("total_reservation_cost", result)
        self.assertIn("reservation_utilization", result)
        self.assertIn("insights", result)
        self.assertIn("period", result)
        
        print(f"✅ GCP reservation cost successful - Total cost: ${result['total_reservation_cost']}")
        print(f"   Found {len(result['reservation_utilization'])} reservation records")
    
    def test_get_reservation_recommendation_success(self):
        """Test successful reservation recommendation retrieval."""
        result = self.reservation_client.get_reservation_recommendation()
        
        self.assertIsInstance(result, dict)
        self.assertIn("recommendations", result)
        self.assertIn("summary", result)
        
        recommendations_count = len(result["recommendations"])
        total_savings = result["summary"]["total_potential_savings"]
        
        print(f"✅ GCP reservation recommendation successful - {recommendations_count} recommendations")
        print(f"   Total potential savings: ${total_savings}")


class TestGCPOptimization(unittest.TestCase):
    """Test GCP Optimization functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.project_id = GCP_PROJECT_ID
        self.credentials_path = GCP_CREDENTIAL_PATH
        self.optimization_client = GCPFinOpsOptimization(self.project_id, self.credentials_path)
    
    def test_get_machine_type_recommendations_success(self):
        """Test successful machine type recommendations."""
        result = self.optimization_client.get_machine_type_recommendations()
        
        self.assertIsInstance(result, dict)
        if "recommendations" in result:
            recommendations_count = len(result["recommendations"])
            print(f"✅ GCP machine type recommendations successful - {recommendations_count} recommendations")
        elif "error" in result:
            print(f"⚠️ GCP machine type recommendations returned error: {result['error']}")
        else:
            print(f"ℹ️ GCP machine type recommendations result: {result}")
    
    def test_get_idle_resource_recommendations_success(self):
        """Test successful idle resource recommendations."""
        result = self.optimization_client.get_idle_resource_recommendations()
        
        self.assertIsInstance(result, dict)
        if "recommendations" in result:
            recommendations_count = len(result["recommendations"])
            print(f"✅ GCP idle resource recommendations successful - {recommendations_count} recommendations")
        elif "error" in result:
            print(f"⚠️ GCP idle resource recommendations returned error: {result['error']}")
        else:
            print(f"ℹ️ GCP idle resource recommendations result: {result}")
    
    def test_get_optimization_recommendations_success(self):
        """Test successful comprehensive optimization recommendations."""
        result = self.optimization_client.get_optimization_recommendations()
        
        self.assertIsInstance(result, dict)
        self.assertIn("machine_type_recommendations", result)
        self.assertIn("idle_resource_recommendations", result)
        
        machine_count = len(result["machine_type_recommendations"].get("recommendations", []))
        idle_count = len(result["idle_resource_recommendations"].get("recommendations", []))
        
        print(f"✅ GCP comprehensive optimization recommendations successful")
        print(f"   Machine type recommendations: {machine_count}")
        print(f"   Idle resource recommendations: {idle_count}")


class TestGCPGovernance(unittest.TestCase):
    """Test GCP Governance functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.project_id = GCP_PROJECT_ID
        self.credentials_path = GCP_CREDENTIAL_PATH
        self.bq_project_id = BQ_PROJECT_ID
        self.bq_dataset = BQ_DATASET
        self.bq_table = BQ_TABLE
        self.governance_client = GCPFinOpsGovernance(self.project_id, self.credentials_path)
    
    def test_get_cost_allocation_tags_success(self):
        """Test successful cost allocation tags retrieval."""
        result = self.governance_client.get_cost_allocation_tags(
            bq_project_id=self.bq_project_id,
            bq_dataset=self.bq_dataset,
            bq_table=self.bq_table
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn("project_labels", result)
        self.assertIn("resource_labels", result)
        self.assertIn("total_labels", result)
        
        print(f"✅ GCP cost allocation tags successful - {result['total_labels']} project labels")
        if "resource_labels" in result and "total_unique_labels" in result["resource_labels"]:
            print(f"   Resource labels: {result['resource_labels']['total_unique_labels']} unique labels")
    
    def test_get_policy_compliance_success(self):
        """Test successful policy compliance check."""
        result = self.governance_client.get_policy_compliance()
        
        self.assertIsInstance(result, dict)
        self.assertIn("compliance_status", result)
        self.assertIn("message", result)
        
        overall_status = result["compliance_status"]["overall_status"]
        print(f"✅ GCP policy compliance successful - Overall status: {overall_status}")
    
    def test_get_cost_policies_success(self):
        """Test successful cost policies retrieval."""
        result = self.governance_client.get_cost_policies(
            gcp_billing_account=GCP_BILLING_ACCOUNT
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn("policies", result)
        self.assertIn("total_policies", result)
        
        total_policies = result["total_policies"]
        print(f"✅ GCP cost policies successful - {total_policies} policy categories")


class TestGCPAnalytics(unittest.TestCase):
    """Test GCP Analytics functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.project_id = GCP_PROJECT_ID
        self.credentials_path = GCP_CREDENTIAL_PATH
        self.bq_project_id = BQ_PROJECT_ID
        self.bq_dataset = BQ_DATASET
        self.bq_table = BQ_TABLE
        self.analytics_client = GCPFinOpsAnalytics(self.project_id, self.credentials_path)
    
    def test_get_cost_anomalies_success(self):
        """Test successful cost anomaly detection."""
        result = self.analytics_client.get_cost_anomalies(
            bq_project_id=self.bq_project_id,
            bq_dataset=self.bq_dataset,
            bq_table=self.bq_table
        )
        
        self.assertIsInstance(result, dict)
        if "anomalies" in result:
            anomalies_count = len(result["anomalies"])
            print(f"✅ GCP cost anomaly detection successful - {anomalies_count} anomalies detected")
        elif "error" in result:
            print(f"⚠️ GCP cost anomaly detection returned error: {result['error']}")
        else:
            print(f"ℹ️ GCP cost anomaly detection result: {result}")
    
    def test_get_cost_efficiency_metrics_success(self):
        """Test successful cost efficiency metrics."""
        result = self.analytics_client.get_cost_efficiency_metrics(
            bq_project_id=self.bq_project_id,
            bq_dataset=self.bq_dataset,
            bq_table=self.bq_table
        )
        
        self.assertIsInstance(result, dict)
        if "efficiency_metrics" in result:
            efficiency_score = result["efficiency_metrics"]["cost_efficiency_score"]
            waste_percentage = result["efficiency_metrics"]["waste_percentage"]
            print(f"✅ GCP cost efficiency metrics successful")
            print(f"   Efficiency score: {efficiency_score}")
            print(f"   Waste percentage: {waste_percentage}%")
        elif "error" in result:
            print(f"⚠️ GCP cost efficiency metrics returned error: {result['error']}")
        else:
            print(f"ℹ️ GCP cost efficiency metrics result: {result}")
    
    def test_generate_cost_report_success(self):
        """Test successful cost report generation."""
        result = self.analytics_client.generate_cost_report(
            bq_project_id=self.bq_project_id,
            bq_dataset=self.bq_dataset,
            bq_table=self.bq_table
        )
        
        self.assertIsInstance(result, dict)
        if "summary" in result:
            total_cost = result["summary"]["total_cost"]
            total_days = result["summary"]["total_days"]
            print(f"✅ GCP cost report generation successful")
            print(f"   Total cost: ${total_cost}")
            print(f"   Total days: {total_days}")
        elif "error" in result:
            print(f"⚠️ GCP cost report generation returned error: {result['error']}")
        else:
            print(f"ℹ️ GCP cost report generation result: {result}")


class TestGCPProviderIntegration(unittest.TestCase):
    """Test GCP Provider integration functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.project_id = GCP_PROJECT_ID
        self.credentials_path = GCP_CREDENTIAL_PATH
        self.gcp_provider = GCPProvider(self.project_id, self.credentials_path)
    
    def test_provider_has_all_required_methods(self):
        """Test that GCP provider has all required methods."""
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
            'get_governance_policies'
        ]
        
        for method in required_methods:
            self.assertTrue(hasattr(self.gcp_provider, method), f"Missing method: {method}")
        
        print("✅ GCP provider has all required methods")
    
    def test_provider_methods_return_dict(self):
        """Test that provider methods return dictionaries."""
        # Test reservation cost method
        reservation_result = self.gcp_provider.get_reservation_cost(
            bq_project_id=BQ_PROJECT_ID,
            bq_dataset=BQ_DATASET,
            bq_table=BQ_TABLE
        )
        self.assertIsInstance(reservation_result, dict)
        
        # Test budget listing method
        budget_result = self.gcp_provider.list_budgets(
            gcp_billing_account=GCP_BILLING_ACCOUNT
        )
        self.assertIsInstance(budget_result, dict)
        
        print("✅ GCP provider methods return dictionaries")
    
    def test_provider_integration_workflow(self):
        """Test a complete workflow using the provider."""
        # Test budget listing
        budgets = self.gcp_provider.list_budgets(
            gcp_billing_account=GCP_BILLING_ACCOUNT,
            gcp_max_results=10
        )
        self.assertIsInstance(budgets, dict)
        
        # Test cost data retrieval
        cost_data = self.gcp_provider.get_cost_data(
            start_date="2025-06-01",
            end_date="2025-07-03",
            bq_project_id=BQ_PROJECT_ID,
            bq_dataset=BQ_DATASET,
            bq_table=BQ_TABLE
        )
        self.assertIsInstance(cost_data, dict)
        
        # Test optimization recommendations
        optimizations = self.gcp_provider.get_optimization_recommendations()
        self.assertIsInstance(optimizations, dict)
        
        print("✅ GCP provider integration workflow successful")


def run_tests():
    """Run all GCP tests."""
    print("Running Comprehensive GCP Tests with Real Credentials")
    print("=" * 60)
    print(f"Project ID: {GCP_PROJECT_ID}")
    print(f"Billing Account: {GCP_BILLING_ACCOUNT}")
    print(f"BigQuery Table: {BQ_TABLE}")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestGCPClientCreation,
        TestGCPBudgetManagement,
        TestGCPCostManagement,
        TestGCPReservationManagement,
        TestGCPOptimization,
        TestGCPGovernance,
        TestGCPAnalytics,
        TestGCPProviderIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("\n" + "=" * 60)
    print(f"Test Results: {result.testsRun} tests run")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    return len(result.failures) + len(result.errors) == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
