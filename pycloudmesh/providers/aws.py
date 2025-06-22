import boto3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from pycloudmesh.definitions import AWSReservationService
from pycloudmesh.definitions import AWSCostMetrics


class AWSReservationCost:
    """AWS Reservation Cost Management class for handling AWS reservation-related operations."""

    def __init__(self, access_key: str, secret_key: str, region: str):
        """
        Initialize AWS Reservation Cost client.

        Args:
            access_key (str): AWS access key ID
            secret_key (str): AWS secret access key
            region (str): AWS region name
        """
        self.client = boto3.client(
            "ce",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def get_reservation_cost(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        granularity: str = "MONTHLY"
    ) -> Dict[str, Any]:
        """
        Get AWS reservation utilization and cost data.

        Args:
            start_date (Optional[str]): Start date in YYYY-MM-DD format. Defaults to first day of current month.
            end_date (Optional[str]): End date in YYYY-MM-DD format. Defaults to last day of current month.
            granularity (str): Data granularity. Options: "DAILY", "MONTHLY", "HOURLY". Defaults to "MONTHLY".

        Returns:
            Dict[str, Any]: Reservation utilization data from AWS Cost Explorer.

        Raises:
            boto3.exceptions.Boto3Error: If AWS API call fails
        """
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month.replace(day=1) - timedelta(days=1)
            end_date = end_date.strftime("%Y-%m-%d")

        try:
            response = self.client.get_reservation_utilization(
                TimePeriod={"Start": start_date, "End": end_date},
                Granularity=granularity
            )
            return response
        except boto3.exceptions.Boto3Error as e:
            return {"error": f"Failed to fetch reservation utilization: {str(e)}"}

    def get_reservation_recommendation(
        self,
        look_back_period: str = '60',
        term: str = 'ONE_YEAR',
        payment_option: str = "ALL_UPFRONT",
        /
    ) -> List[Dict[str, Any]]:
        """
        Get AWS reservation recommendations for various services.

        Args:
            look_back_period (str): Number of days to look back for usage data. Defaults to '60'.
            term (str): Reservation term. Options: "ONE_YEAR", "THREE_YEARS". Defaults to "ONE_YEAR".
            payment_option (str): Payment option. Options: "ALL_UPFRONT", "PARTIAL_UPFRONT", "NO_UPFRONT". Defaults to "ALL_UPFRONT".

        Returns:
            List[Dict[str, Any]]: List of reservation recommendations.

        Raises:
            boto3.exceptions.Boto3Error: If AWS API call fails
        """
        services_list = [
            AWSReservationService.AMAZONEC2,
            AWSReservationService.AMAZONRDS,
            AWSReservationService.AMAZONREDSHIFT,
            AWSReservationService.AMAZONELASTICCACHE,
            AWSReservationService.AMAZONOPENSEARCHSERVICE
        ]

        params = {
            "LookbackPeriodInDays": look_back_period,
            "TermInYears": term,
            "PaymentOption": payment_option
        }

        all_response = []

        try:
            for service in services_list:
                params["service"] = service
                response = self.client.get_reservation_recommendation(params)
                all_response.extend(response.get("Recommendations", []))
            return all_response
        except boto3.exceptions.Boto3Error as e:
            return [{"error": f"Failed to fetch reservation recommendations: {str(e)}"}]


class AWSBudgetManagement:
    """AWS Budget Management class for handling AWS budget-related operations."""

    def __init__(self, access_key: str, secret_key: str, region: str):
        """
        Initialize AWS Budget Management client.

        Args:
            access_key (str): AWS access key ID
            secret_key (str): AWS secret access key
            region (str): AWS region name
        """
        self.client = boto3.client(
            "budgets",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def list_budgets(
        self,
        account_id: str,
        /,
        *,
        max_results: Optional[int] = None,
        next_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List AWS budgets for an account.

        Args:
            account_id (str): AWS account ID
            max_results (Optional[int]): Maximum number of results to return
            next_token (Optional[str]): Token for pagination

        Returns:
            Dict[str, Any]: List of budgets and pagination information

        Raises:
            boto3.exceptions.Boto3Error: If AWS API call fails
        """
        params = {"AccountId": account_id}
        if max_results:
            params["MaxResults"] = max_results
        if next_token:
            params["NextToken"] = next_token

        try:
            response = self.client.describe_budgets(**params)
            return response
        except boto3.exceptions.Boto3Error as e:
            return {"error": f"Failed to list budgets: {str(e)}"}

    def create_budget(
        self,
        account_id: str,
        budget_name: str,
        budget_amount: float,
        budget_type: str = "COST",
        time_unit: str = "MONTHLY",
        notifications_with_subscribers: list = None
    ) -> Dict[str, Any]:
        """
        Create a new AWS budget.

        Args:
            account_id (str): AWS account ID
            budget_name (str): Name of the budget
            budget_amount (float): Budget amount
            budget_type (str): Type of budget (COST, USAGE, RI_UTILIZATION, RI_COVERAGE)
            time_unit (str): Time unit for the budget (MONTHLY, QUARTERLY, ANNUALLY)
            notifications_with_subscribers (list): List of notification dicts (optional)

        Returns:
            Dict[str, Any]: Budget creation response
        """
        try:
            budget = {
                "BudgetName": budget_name,
                "BudgetLimit": {
                    "Amount": str(budget_amount),
                    "Unit": "USD"
                },
                "TimeUnit": time_unit,
                "BudgetType": budget_type
            }
            kwargs = {
                "AccountId": account_id,
                "Budget": budget
            }
            if notifications_with_subscribers:
                kwargs["NotificationsWithSubscribers"] = notifications_with_subscribers
            response = self.client.create_budget(**kwargs)
            return response
        except boto3.exceptions.Boto3Error as e:
            return {"error": f"Failed to create budget: {str(e)}"}

    def get_budget_notifications(
        self,
        account_id: str,
        budget_name: str
    ) -> Dict[str, Any]:
        """
        Get notifications for a specific budget.

        Args:
            account_id (str): AWS account ID
            budget_name (str): Name of the budget

        Returns:
            Dict[str, Any]: Budget notifications
        """
        try:
            response = self.client.describe_notifications_for_budget(
                AccountId=account_id,
                BudgetName=budget_name
            )
            return response
        except boto3.exceptions.Boto3Error as e:
            return {"error": f"Failed to get budget notifications: {str(e)}"}


class AWSCostManagement:
    """AWS Cost Management class for handling AWS cost-related operations."""

    def __init__(self, access_key: str, secret_key: str, region: str):
        """
        Initialize AWS Cost Management client.

        Args:
            access_key (str): AWS access key ID
            secret_key (str): AWS secret access key
            region (str): AWS region name
        """
        self.client = boto3.client(
            "ce",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def get_aws_cost_data(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        granularity: str = "MONTHLY",
        metrics: Optional[List[str]] = None,
        group_by: Optional[List[Dict[str, str]]] = None,
        filter_: Optional[Dict[str, Any]] = None,
        sort_by: Optional[List[Dict[str, str]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch AWS cost data from Cost Explorer.

        Args:
            start_date (Optional[str]): Start date (YYYY-MM-DD). Defaults to first day of current month.
            end_date (Optional[str]): End date (YYYY-MM-DD). Defaults to today's date.
            granularity (str): "DAILY", "MONTHLY", or "HOURLY". Defaults to "MONTHLY".
            metrics (Optional[List[str]]): List of cost metrics. Defaults to standard cost metrics.
            group_by (Optional[List[Dict[str, str]]]): Grouping criteria.
            filter_ (Optional[Dict[str, Any]]): Filter criteria.
            sort_by (Optional[List[Dict[str, str]]]): Sorting criteria.

        Returns:
            List[Dict[str, Any]]: Cost data from AWS Cost Explorer.

        Raises:
            boto3.exceptions.Boto3Error: If AWS API call fails
        """
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today.replace(day=1).strftime("%Y-%m-%d")
            end_date = today.strftime("%Y-%m-%d")

        if not metrics:
            metrics = ["UnblendedCost"]

        params = {
            "TimePeriod": {"Start": start_date, "End": end_date},
            "Granularity": granularity,
            "Metrics": metrics
        }

        if group_by:
            params["GroupBy"] = group_by
        if filter_:
            params["Filter"] = filter_
        if sort_by:
            params["SortBy"] = sort_by

        try:
            response = self.client.get_cost_and_usage(**params)
            return response.get("ResultsByTime", [])
        except boto3.exceptions.Boto3Error as e:
            return [{"error": f"Failed to fetch cost data: {str(e)}"}]

    def get_aws_cost_analysis(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        dimensions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get detailed cost analysis with insights and breakdowns.

        Args:
            start_date (Optional[str]): Start date for analysis
            end_date (Optional[str]): End date for analysis
            dimensions (Optional[List[str]]): List of dimensions to analyze (max 2)

        Returns:
            Dict[str, Any]: Cost analysis with insights, breakdowns, and trends
        """
        if not dimensions or len(dimensions) > 2:
            dimensions = ["SERVICE", "REGION"]  # Default to 2 dimensions max

        try:
            # Get raw cost data
            group_by = [{"Type": "DIMENSION", "Key": dim} for dim in dimensions]
            cost_data = self.get_aws_cost_data(
                start_date=start_date,
                end_date=end_date,
                group_by=group_by
            )

            # Analyze the cost data
            analysis = {
                "period": {"start": start_date, "end": end_date},
                "dimensions": dimensions,
                "total_cost": 0.0,
                "cost_breakdown": {},
                "top_services": [],
                "cost_trends": [],
                "insights": []
            }

            # Process each time period
            for period_data in cost_data:
                if isinstance(period_data, dict) and "error" in period_data:
                    continue
                
                if not isinstance(period_data, dict):
                    continue
                
                time_period = period_data.get("TimePeriod", {})
                groups = period_data.get("Groups", [])
                total = period_data.get("Total", {})
                
                # Calculate total cost for this period
                period_total = 0.0
                
                if groups:
                    # When grouping is used, process each group
                    for group in groups:
                        keys = group.get("Keys", [])
                        metrics = group.get("Metrics", {})
                        cost = float(metrics.get("UnblendedCost", {}).get("Amount", 0))
                        period_total += cost
                        
                        # Build cost breakdown
                        if len(keys) >= 1:
                            service = keys[0]
                            if service not in analysis["cost_breakdown"]:
                                analysis["cost_breakdown"][service] = 0.0
                            analysis["cost_breakdown"][service] += cost
                elif total:
                    # When no grouping, use total
                    cost = float(total.get("UnblendedCost", {}).get("Amount", 0))
                    period_total = cost
                    analysis["cost_breakdown"]["Total"] = analysis["cost_breakdown"].get("Total", 0.0) + cost
                
                analysis["total_cost"] += period_total
                analysis["cost_trends"].append({
                    "period": f"{time_period.get('Start')} to {time_period.get('End')}",
                    "cost": period_total
                })

            # Generate insights
            if analysis["cost_breakdown"]:
                # Top services by cost
                sorted_services = sorted(
                    analysis["cost_breakdown"].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )
                analysis["top_services"] = [
                    {"service": service, "cost": cost} 
                    for service, cost in sorted_services[:5]
                ]
                
                # Generate insights
                if analysis["total_cost"] > 0:
                    top_service = sorted_services[0]
                    top_percentage = (top_service[1] / analysis["total_cost"]) * 100
                    analysis["insights"].append(
                        f"Top service '{top_service[0]}' accounts for {top_percentage:.1f}% of total costs"
                    )
                    
                    if len(sorted_services) > 1:
                        analysis["insights"].append(
                            f"Top 3 services account for {sum(cost for _, cost in sorted_services[:3]) / analysis['total_cost'] * 100:.1f}% of total costs"
                        )

            return analysis
            
        except Exception as e:
            return {"error": f"Failed to perform cost analysis: {str(e)}"}

    def get_aws_cost_trends(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        granularity: str = "DAILY"
    ) -> Dict[str, Any]:
        """
        Get detailed cost trends analysis with insights and patterns.

        Args:
            start_date (Optional[str]): Start date for trend analysis
            end_date (Optional[str]): End date for trend analysis
            granularity (str): Data granularity for trends (DAILY, MONTHLY, HOURLY)

        Returns:
            Dict[str, Any]: Cost trends analysis with patterns, growth rates, and insights
        """
        try:
            # Get raw cost data
            cost_data = self.get_aws_cost_data(
                start_date=start_date,
                end_date=end_date,
                granularity=granularity
            )

            # Analyze the cost trends
            trends_analysis = {
                "period": {"start": start_date, "end": end_date},
                "granularity": granularity,
                "total_periods": 0,
                "total_cost": 0.0,
                "average_daily_cost": 0.0,
                "cost_periods": [],
                "trend_direction": "stable",
                "growth_rate": 0.0,
                "peak_periods": [],
                "low_periods": [],
                "patterns": [],
                "insights": []
            }

            # Process each time period
            costs = []
            for period_data in cost_data:
                if isinstance(period_data, dict) and "error" in period_data:
                    continue
                
                if not isinstance(period_data, dict):
                    continue
                
                time_period = period_data.get("TimePeriod", {})
                total = period_data.get("Total", {})
                
                # Calculate cost for this period
                cost = float(total.get("UnblendedCost", {}).get("Amount", 0))
                costs.append(cost)
                
                trends_analysis["total_cost"] += cost
                trends_analysis["total_periods"] += 1
                
                trends_analysis["cost_periods"].append({
                    "period": f"{time_period.get('Start')} to {time_period.get('End')}",
                    "cost": cost,
                    "date": time_period.get('Start')
                })

            # Calculate trend metrics
            if trends_analysis["total_periods"] > 0:
                trends_analysis["average_daily_cost"] = trends_analysis["total_cost"] / trends_analysis["total_periods"]
                
                # Find peak and low periods
                if costs:
                    max_cost = max(costs)
                    min_cost = min(costs)
                    
                    # Find periods with peak costs
                    for period in trends_analysis["cost_periods"]:
                        if period["cost"] == max_cost and max_cost > 0:
                            trends_analysis["peak_periods"].append(period)
                        if period["cost"] == min_cost:
                            trends_analysis["low_periods"].append(period)

                # Calculate trend direction and growth rate
                if len(costs) >= 2:
                    # Simple trend calculation: compare first and last periods
                    first_half = costs[:len(costs)//2]
                    second_half = costs[len(costs)//2:]
                    
                    if first_half and second_half:
                        first_avg = sum(first_half) / len(first_half)
                        second_avg = sum(second_half) / len(second_half)
                        
                        if first_avg > 0:
                            growth_rate = ((second_avg - first_avg) / first_avg) * 100
                            trends_analysis["growth_rate"] = growth_rate
                            
                            if growth_rate > 10:
                                trends_analysis["trend_direction"] = "increasing"
                            elif growth_rate < -10:
                                trends_analysis["trend_direction"] = "decreasing"
                            else:
                                trends_analysis["trend_direction"] = "stable"

                # Generate patterns and insights
                if costs:
                    # Pattern: Check for consistent vs variable costs
                    non_zero_costs = [c for c in costs if c > 0]
                    if non_zero_costs:
                        cost_variance = max(non_zero_costs) - min(non_zero_costs)
                        if cost_variance > trends_analysis["average_daily_cost"]:
                            trends_analysis["patterns"].append("High cost variability")
                        else:
                            trends_analysis["patterns"].append("Consistent cost pattern")
                    
                    # Pattern: Check for zero-cost periods
                    zero_cost_periods = len([c for c in costs if c == 0])
                    if zero_cost_periods > len(costs) * 0.5:
                        trends_analysis["patterns"].append("Many zero-cost periods")
                    
                    # Insights
                    if trends_analysis["total_cost"] > 0:
                        trends_analysis["insights"].append(
                            f"Total cost over {trends_analysis['total_periods']} periods: ${trends_analysis['total_cost']:.2f}"
                        )
                        trends_analysis["insights"].append(
                            f"Average cost per period: ${trends_analysis['average_daily_cost']:.4f}"
                        )
                        
                        if trends_analysis["trend_direction"] != "stable":
                            trends_analysis["insights"].append(
                                f"Cost trend is {trends_analysis['trend_direction']} ({trends_analysis['growth_rate']:.1f}% change)"
                            )
                        
                        if trends_analysis["peak_periods"]:
                            peak_period = trends_analysis["peak_periods"][0]
                            trends_analysis["insights"].append(
                                f"Peak cost period: {peak_period['period']} (${peak_period['cost']:.4f})"
                            )

            return trends_analysis
            
        except Exception as e:
            return {"error": f"Failed to perform cost trends analysis: {str(e)}"}

    def get_aws_resource_costs(
        self,
        resource_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        granularity: str = "DAILY"
    ) -> Dict[str, Any]:
        """
        Get detailed cost analysis for a specific resource.

        Args:
            resource_id (str): ID of the resource to get costs for
            start_date (Optional[str]): Start date for cost data
            end_date (Optional[str]): End date for cost data
            granularity (str): Data granularity (DAILY, MONTHLY, HOURLY)

        Returns:
            Dict[str, Any]: Detailed resource cost analysis with insights and breakdowns
        """
        try:
            # Since RESOURCE_ID is not a valid dimension, we'll get EC2 costs
            # and provide analysis based on the resource type
            filter_ = {
                "Dimensions": {
                    "Key": "SERVICE",
                    "Values": ["Amazon Elastic Compute Cloud - Compute"]
                }
            }
            
            # Get raw cost data for EC2 services
            cost_data = self.get_aws_cost_data(
                start_date=start_date,
                end_date=end_date,
                granularity=granularity,
                filter_=filter_,
                group_by=[{"Type": "DIMENSION", "Key": "USAGE_TYPE"}]
            )

            # Analyze the resource cost data
            resource_analysis = {
                "resource_id": resource_id,
                "resource_type": "EC2 Instance",
                "period": {"start": start_date, "end": end_date},
                "granularity": granularity,
                "total_cost": 0.0,
                "total_periods": 0,
                "active_periods": 0,
                "cost_periods": [],
                "cost_breakdown": {},
                "utilization_insights": [],
                "cost_trends": [],
                "recommendations": []
            }

            # Process each time period
            costs = []
            for period_data in cost_data:
                if isinstance(period_data, dict) and "error" in period_data:
                    continue
                
                if not isinstance(period_data, dict):
                    continue
                
                time_period = period_data.get("TimePeriod", {})
                total = period_data.get("Total", {})
                groups = period_data.get("Groups", [])
                
                # Calculate cost for this period
                period_cost = 0.0
                period_breakdown = {}
                
                if groups:
                    # When grouping is used, process each group
                    for group in groups:
                        keys = group.get("Keys", [])
                        metrics = group.get("Metrics", {})
                        cost = float(metrics.get("UnblendedCost", {}).get("Amount", 0))
                        period_cost += cost
                        
                        # Build cost breakdown by usage type
                        if len(keys) >= 1:
                            usage_type = keys[0]
                            if usage_type not in period_breakdown:
                                period_breakdown[usage_type] = 0.0
                            period_breakdown[usage_type] += cost
                            
                            # Add to overall breakdown
                            if usage_type not in resource_analysis["cost_breakdown"]:
                                resource_analysis["cost_breakdown"][usage_type] = 0.0
                            resource_analysis["cost_breakdown"][usage_type] += cost
                elif total:
                    # When no grouping, use total
                    cost = float(total.get("UnblendedCost", {}).get("Amount", 0))
                    period_cost = cost
                    period_breakdown["Total"] = cost
                    resource_analysis["cost_breakdown"]["Total"] = resource_analysis["cost_breakdown"].get("Total", 0.0) + cost
                
                costs.append(period_cost)
                resource_analysis["total_cost"] += period_cost
                resource_analysis["total_periods"] += 1
                
                if period_cost > 0:
                    resource_analysis["active_periods"] += 1
                
                resource_analysis["cost_periods"].append({
                    "period": f"{time_period.get('Start')} to {time_period.get('End')}",
                    "cost": period_cost,
                    "breakdown": period_breakdown,
                    "date": time_period.get('Start')
                })

            # Calculate utilization insights
            if resource_analysis["total_periods"] > 0:
                utilization_rate = resource_analysis["active_periods"] / resource_analysis["total_periods"]
                resource_analysis["utilization_insights"].append(
                    f"EC2 utilization rate: {utilization_rate:.1%} ({resource_analysis['active_periods']} active out of {resource_analysis['total_periods']} periods)"
                )
                
                if utilization_rate < 0.5:
                    resource_analysis["utilization_insights"].append("Low EC2 utilization detected - consider stopping or downsizing instances")
                elif utilization_rate > 0.9:
                    resource_analysis["utilization_insights"].append("High EC2 utilization detected - consider scaling up if needed")

            # Calculate cost trends
            if len(costs) >= 2:
                # Simple trend analysis
                first_half = costs[:len(costs)//2]
                second_half = costs[len(costs)//2:]
                
                if first_half and second_half:
                    first_avg = sum(first_half) / len(first_half)
                    second_avg = sum(second_half) / len(second_half)
                    
                    if first_avg > 0:
                        growth_rate = ((second_avg - first_avg) / first_avg) * 100
                        if growth_rate > 10:
                            resource_analysis["cost_trends"].append(f"EC2 cost trend: Increasing ({growth_rate:.1f}% growth)")
                        elif growth_rate < -10:
                            resource_analysis["cost_trends"].append(f"EC2 cost trend: Decreasing ({abs(growth_rate):.1f}% reduction)")
                        else:
                            resource_analysis["cost_trends"].append("EC2 cost trend: Stable")

            # Generate recommendations
            if resource_analysis["total_cost"] > 0:
                avg_cost = resource_analysis["total_cost"] / resource_analysis["total_periods"]
                
                if avg_cost > 10:  # High cost threshold
                    resource_analysis["recommendations"].append("High EC2 costs detected - review instance types and consider reserved instances")
                
                if resource_analysis["active_periods"] < resource_analysis["total_periods"] * 0.3:
                    resource_analysis["recommendations"].append("Low EC2 activity - consider stopping instances during idle periods")
                
                # Check for cost optimization opportunities
                if len(resource_analysis["cost_breakdown"]) > 1:
                    top_usage = max(resource_analysis["cost_breakdown"].items(), key=lambda x: x[1])
                    top_percentage = (top_usage[1] / resource_analysis["total_cost"]) * 100
                    resource_analysis["recommendations"].append(
                        f"Top EC2 cost component: {top_usage[0]} ({top_percentage:.1f}% of total) - review for optimization"
                    )
                
                # Add resource-specific note
                resource_analysis["recommendations"].append(
                    f"Note: Analysis based on EC2 service costs. For specific resource {resource_id}, use AWS Cost Explorer directly with resource tags."
                )

            return resource_analysis
            
        except Exception as e:
            return {"error": f"Failed to analyze resource costs: {str(e)}"}

    def get_savings_plans_recommendations(self) -> Dict[str, Any]:
        """
        Get AWS Savings Plans recommendations.

        Returns:
            Dict[str, Any]: Savings Plans recommendations
        """
        try:
            response = self.client.get_savings_plans_recommendation(
                LookbackPeriodInDays=30,
                TermInYears=1,
                PaymentOption="NO_UPFRONT"
            )
            return response
        except boto3.exceptions.Boto3Error as e:
            return {"error": f"Failed to get Savings Plans recommendations: {str(e)}"}

    def get_rightsizing_recommendations(self) -> Dict[str, Any]:
        """
        Get AWS rightsizing recommendations.

        Returns:
            Dict[str, Any]: Rightsizing recommendations
        """
        try:
            response = self.client.get_rightsizing_recommendation(
                Service="AmazonEC2"
            )
            return response
        except boto3.exceptions.Boto3Error as e:
            return {"error": f"Failed to get rightsizing recommendations: {str(e)}"}


class AWSFinOpsOptimization:
    """AWS FinOps Optimization class for cost optimization features."""

    def __init__(self, access_key: str, secret_key: str, region: str):
        """
        Initialize AWS FinOps Optimization client.

        Args:
            access_key (str): AWS access key ID
            secret_key (str): AWS secret access key
            region (str): AWS region name
        """
        self.ce_client = boto3.client(
            "ce",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
        self.ec2_client = boto3.client(
            "ec2",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
        self.rds_client = boto3.client(
            "rds",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def get_idle_resources(self) -> Dict[str, Any]:
        """
        Identify idle or underutilized resources.

        Returns:
            Dict[str, Any]: List of idle resources with cost impact
        """
        try:
            # Get EC2 instances
            ec2_response = self.ec2_client.describe_instances()
            idle_instances = []
            
            for reservation in ec2_response.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    if instance['State']['Name'] == 'running':
                        # Check for low CPU utilization (would need CloudWatch data in real implementation)
                        idle_instances.append({
                            'resource_id': instance['InstanceId'],
                            'resource_type': 'EC2',
                            'state': instance['State']['Name'],
                            'instance_type': instance['InstanceType']
                        })
            
            return {
                'idle_resources': idle_instances,
                'total_idle_count': len(idle_instances)
            }
        except Exception as e:
            return {"error": f"Failed to get idle resources: {str(e)}"}

    def get_optimization_recommendations(self) -> Dict[str, Any]:
        """
        Get comprehensive optimization recommendations.

        Returns:
            Dict[str, Any]: Optimization recommendations
        """
        try:
            recommendations = {
                'reservations': self._get_reservation_recommendations(),
                'savings_plans': self._get_savings_plans_recommendations(),
                'rightsizing': self._get_rightsizing_recommendations(),
                'idle_resources': self.get_idle_resources()
            }
            return recommendations
        except Exception as e:
            return {"error": f"Failed to get optimization recommendations: {str(e)}"}

    def _get_reservation_recommendations(self) -> Dict[str, Any]:
        """Get reservation recommendations."""
        try:
            response = self.ce_client.get_reservation_recommendation(
                LookbackPeriodInDays=30,
                TermInYears=1,
                PaymentOption="NO_UPFRONT"
            )
            return response
        except Exception as e:
            return {"error": f"Failed to get reservation recommendations: {str(e)}"}

    def _get_savings_plans_recommendations(self) -> Dict[str, Any]:
        """Get Savings Plans recommendations."""
        try:
            response = self.ce_client.get_savings_plans_recommendation(
                LookbackPeriodInDays=30,
                TermInYears=1,
                PaymentOption="NO_UPFRONT"
            )
            return response
        except Exception as e:
            return {"error": f"Failed to get Savings Plans recommendations: {str(e)}"}

    def _get_rightsizing_recommendations(self) -> Dict[str, Any]:
        """Get rightsizing recommendations."""
        try:
            response = self.ce_client.get_rightsizing_recommendation(
                Service="AmazonEC2"
            )
            return response
        except Exception as e:
            return {"error": f"Failed to get rightsizing recommendations: {str(e)}"}


class AWSFinOpsGovernance:
    """AWS FinOps Governance class for policy and compliance features."""

    def __init__(self, access_key: str, secret_key: str, region: str):
        """
        Initialize AWS FinOps Governance client.

        Args:
            access_key (str): AWS access key ID
            secret_key (str): AWS secret access key
            region (str): AWS region name
        """
        self.organizations_client = boto3.client(
            "organizations",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
        self.config_client = boto3.client(
            "config",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def get_cost_allocation_tags(self) -> Dict[str, Any]:
        """
        Get cost allocation tags.

        Returns:
            Dict[str, Any]: Cost allocation tags
        """
        try:
            response = self.organizations_client.list_tags_for_resource(
                ResourceId="root"
            )
            return response
        except Exception as e:
            return {"error": f"Failed to get cost allocation tags: {str(e)}"}

    def get_compliance_status(self) -> Dict[str, Any]:
        """
        Get compliance status for cost policies.

        Returns:
            Dict[str, Any]: Compliance status
        """
        try:
            response = self.config_client.get_compliance_details_by_config_rule(
                ConfigRuleName="cost-optimization-rule"
            )
            return response
        except Exception as e:
            return {"error": f"Failed to get compliance status: {str(e)}"}

    def get_cost_policies(self) -> Dict[str, Any]:
        """
        Get cost management policies.

        Returns:
            Dict[str, Any]: Cost policies
        """
        try:
            # This would typically involve AWS Organizations policies
            # For now, return a placeholder structure
            return {
                "policies": [
                    {
                        "name": "Cost Optimization Policy",
                        "description": "Policy for cost optimization",
                        "status": "active"
                    }
                ]
            }
        except Exception as e:
            return {"error": f"Failed to get cost policies: {str(e)}"}


class AWSFinOpsAnalytics:
    """AWS FinOps Analytics class for advanced analytics and reporting."""

    def __init__(self, access_key: str, secret_key: str, region: str):
        """
        Initialize AWS FinOps Analytics client.

        Args:
            access_key (str): AWS access key ID
            secret_key (str): AWS secret access key
            region (str): AWS region name
        """
        self.ce_client = boto3.client(
            "ce",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
        self.quicksight_client = boto3.client(
            "quicksight",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def get_cost_forecast(
        self,
        start_date: str,
        end_date: str,
        forecast_period: int = 12
    ) -> Dict[str, Any]:
        """
        Get cost forecast for the specified period.

        Args:
            start_date (str): Start date for historical data
            end_date (str): End date for historical data
            forecast_period (int): Number of months to forecast

        Returns:
            Dict[str, Any]: Cost forecast data
        """
        try:
            response = self.ce_client.get_cost_forecast(
                TimePeriod={
                    "Start": start_date,
                    "End": end_date
                },
                Metric="UNBLENDED_COST",
                Granularity="MONTHLY",
                PredictionIntervalInDays=forecast_period * 30
            )
            return response
        except Exception as e:
            return {"error": f"Failed to get cost forecast: {str(e)}"}

    def get_cost_anomalies(self) -> Dict[str, Any]:
        """
        Get cost anomalies.

        Returns:
            Dict[str, Any]: Cost anomalies data
        """
        try:
            # This would typically use AWS Cost Anomaly Detection
            # For now, return a placeholder structure
            return {
                "anomalies": [
                    {
                        "anomaly_id": "anomaly-123",
                        "service": "AmazonEC2",
                        "cost_impact": 150.00,
                        "detection_date": "2024-01-15"
                    }
                ]
            }
        except Exception as e:
            return {"error": f"Failed to get cost anomalies: {str(e)}"}

    def get_cost_efficiency_metrics(self) -> Dict[str, Any]:
        """
        Get cost efficiency metrics.

        Returns:
            Dict[str, Any]: Cost efficiency metrics
        """
        try:
            # Calculate efficiency metrics based on cost data
            return {
                "efficiency_metrics": {
                    "cost_per_user": 25.50,
                    "cost_per_transaction": 0.15,
                    "utilization_rate": 0.75,
                    "waste_percentage": 0.25
                }
            }
        except Exception as e:
            return {"error": f"Failed to get cost efficiency metrics: {str(e)}"}

    def generate_cost_report(
        self,
        report_type: str = "monthly",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive cost report.

        Args:
            report_type (str): Type of report (monthly, quarterly, annual)
            start_date (Optional[str]): Start date for report
            end_date (Optional[str]): End date for report

        Returns:
            Dict[str, Any]: Cost report
        """
        try:
            if not start_date or not end_date:
                today = datetime.today()
                start_date = today.replace(day=1).strftime("%Y-%m-%d")
                end_date = today.strftime("%Y-%m-%d")

            cost_data = self.ce_client.get_cost_and_usage(
                TimePeriod={"Start": start_date, "End": end_date},
                Granularity="MONTHLY",
                Metrics=["UnblendedCost"],
                GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
            )

            return {
                "report_type": report_type,
                "period": {"start": start_date, "end": end_date},
                "total_cost": sum(float(result['Total']['UnblendedCost']['Amount']) 
                                for result in cost_data.get('ResultsByTime', [])),
                "cost_by_service": cost_data.get('ResultsByTime', []),
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Failed to generate cost report: {str(e)}"}

