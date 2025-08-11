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

    def get_reservation_cost(self, **kwargs) -> Dict[str, Any]:
        """
        Get AWS reservation utilization and cost data.

        Args:
            start_date (Optional[str]): Start date in YYYY-MM-DD format. Defaults to one month before today.
            end_date (Optional[str]): End date in YYYY-MM-DD format. Defaults to today.
            granularity (str): Data granularity. Options: "DAILY", "MONTHLY", "HOURLY". Defaults to "MONTHLY".

        Returns:
            Dict[str, Any]: Reservation utilization data from AWS Cost Explorer.

        Raises:
            boto3.exceptions.Boto3Error: If AWS API call fails
        """

        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        granularity = kwargs.get('granularity', 'MONTHLY')

        if not start_date or not end_date:
            today = datetime.today()
            end_date = today.strftime("%Y-%m-%d")
            start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")

        try:
            response = self.client.get_reservation_utilization(
                TimePeriod={"Start": start_date, "End": end_date},
                Granularity=granularity
            )
            return response
        except boto3.exceptions.Boto3Error as e:
            return {"error": f"Failed to fetch reservation utilization: {str(e)}"}

    def get_reservation_recommendation(self, **kwargs) -> dict:
        """
        Get AWS reservation purchase recommendations (alias for get_reservation_purchase_recommendation).

        Args:
            **kwargs: Same parameters as get_reservation_purchase_recommendation

        Returns:
            dict: Reservation purchase recommendations from AWS Cost Explorer
        """
        return self.get_reservation_purchase_recommendation(**kwargs)

    def get_reservation_purchase_recommendation(self, **kwargs) -> dict:
        """
        Get AWS reservation purchase recommendations for various services using Cost Explorer.

        Parameters (all optional, with defaults shown):
            Service (str): e.g., 'AmazonEC2', 'AmazonRDS', etc. (default: 'AmazonEC2')
            LookbackPeriodInDays (str): 'SEVEN_DAYS', 'THIRTY_DAYS', 'SIXTY_DAYS' (default: 'SIXTY_DAYS')
            TermInYears (str): 'ONE_YEAR', 'THREE_YEARS' (default: 'ONE_YEAR')
            PaymentOption (str): 'NO_UPFRONT', 'PARTIAL_UPFRONT', 'ALL_UPFRONT' (default: 'NO_UPFRONT')
            AccountScope (str): 'PAYER' or 'LINKED' (default: 'PAYER')
            AccountId (str): AWS Account ID (optional)
            NextPageToken (str): for pagination (optional)
            PageSize (int): for pagination (optional)
            Filter (dict): Expression for filtering (optional)
            ServiceSpecification (dict): e.g., {"EC2Specification": {"OfferingClass": "STANDARD"}} (optional)

        Returns:
            dict: Full response from AWS get_reservation_purchase_recommendation
        """
        params = {
            'Service': kwargs.get('Service', 'AmazonEC2'),
            'LookbackPeriodInDays': kwargs.get('LookbackPeriodInDays', 'SIXTY_DAYS'),
            'TermInYears': kwargs.get('TermInYears', 'ONE_YEAR'),
            'PaymentOption': kwargs.get('PaymentOption', 'NO_UPFRONT'),
            'AccountScope': kwargs.get('AccountScope', 'PAYER'),
        }
        if 'AccountId' in kwargs:
            params['AccountId'] = kwargs['AccountId']
        if 'NextPageToken' in kwargs:
            params['NextPageToken'] = kwargs['NextPageToken']
        if 'PageSize' in kwargs:
            params['PageSize'] = kwargs['PageSize']
        if 'Filter' in kwargs:
            params['Filter'] = kwargs['Filter']
        if 'ServiceSpecification' in kwargs:
            params['ServiceSpecification'] = kwargs['ServiceSpecification']
        try:
            response = self.client.get_reservation_purchase_recommendation(**params)
            return response
        except Exception as e:
            return {"error": str(e)}

    def get_reservation_coverage(self, **kwargs) -> dict:
        """
        Get AWS reservation coverage data using Cost Explorer.

        Parameters (all optional, with defaults shown):
            start_date (str): Start date in YYYY-MM-DD format (default: 30 days ago)
            end_date (str): End date in YYYY-MM-DD format (default: today)
            granularity (str): 'DAILY' or 'MONTHLY' (default: 'MONTHLY')
            GroupBy (list): List of dicts for grouping (optional)
            Filter (dict): Expression for filtering (optional)
            NextPageToken (str): for pagination (optional)

        Returns:
            dict: Full response from AWS get_reservation_coverage
        """
        from datetime import datetime, timedelta
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        granularity = kwargs.get('granularity', 'MONTHLY')
        if not end_date:
            end_date = datetime.today().strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
        params = {
            'TimePeriod': {'Start': start_date, 'End': end_date},
            'Granularity': granularity
        }
        if 'GroupBy' in kwargs:
            params['GroupBy'] = kwargs['GroupBy']
        if 'Filter' in kwargs:
            params['Filter'] = kwargs['Filter']
        if 'NextPageToken' in kwargs:
            params['NextPageToken'] = kwargs['NextPageToken']
        try:
            response = self.client.get_reservation_coverage(**params)
            return response
        except Exception as e:
            return {"error": str(e)}


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
            dimensions = ["SERVICE", "REGION"]

        try:
            group_by = [{"Type": "DIMENSION", "Key": dim} for dim in dimensions]
            cost_data = self.get_aws_cost_data(
                start_date=start_date,
                end_date=end_date,
                group_by=group_by
            )

            analysis = {
                "period": {"start": start_date, "end": end_date},
                "dimensions": dimensions,
                "total_cost": 0.0,
                "cost_breakdown": {},
                "top_services": [],
                "cost_trends": [],
                "insights": []
            }

            for period_data in cost_data:
                if isinstance(period_data, dict) and "error" in period_data:
                    continue
                
                if not isinstance(period_data, dict):
                    continue
                
                time_period = period_data.get("TimePeriod", {})
                groups = period_data.get("Groups", [])
                total = period_data.get("Total", {})
                
                period_total = 0.0
                
                if groups:
                    for group in groups:
                        keys = group.get("Keys", [])
                        metrics = group.get("Metrics", {})
                        cost = float(metrics.get("UnblendedCost", {}).get("Amount", 0))
                        period_total += cost
                        
                        if len(keys) >= 1:
                            service = keys[0]
                            if service not in analysis["cost_breakdown"]:
                                analysis["cost_breakdown"][service] = 0.0
                            analysis["cost_breakdown"][service] += cost
                elif total:
                    cost = float(total.get("UnblendedCost", {}).get("Amount", 0))
                    period_total = cost
                    analysis["cost_breakdown"]["Total"] = analysis["cost_breakdown"].get("Total", 0.0) + cost
                
                analysis["total_cost"] += period_total
                analysis["cost_trends"].append({
                    "period": f"{time_period.get('Start')} to {time_period.get('End')}",
                    "cost": period_total
                })

            if analysis["cost_breakdown"]:
                sorted_services = sorted(
                    analysis["cost_breakdown"].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )
                analysis["top_services"] = [
                    {"service": service, "cost": cost} 
                    for service, cost in sorted_services[:5]
                ]
                
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

    def get_aws_cost_trends(self, **kwargs) -> Dict[str, Any]:
        """
        Get detailed cost trends analysis with insights and patterns.
        Accepts flexible parameters and uses sensible defaults if not provided.

        Args:
            **kwargs: start_date, end_date, granularity, and any other supported by get_aws_cost_data

        Returns:
            Dict[str, Any]: Cost trends analysis with patterns, growth rates, and insights
        """
        import datetime
        today = datetime.date.today()
        start_date = kwargs.get('start_date', today.replace(day=1).strftime("%Y-%m-%d"))
        end_date = kwargs.get('end_date', today.strftime("%Y-%m-%d"))
        granularity = kwargs.get('granularity', 'DAILY')
        try:
            cost_data = self.get_aws_cost_data(
                start_date=start_date,
                end_date=end_date,
                granularity=granularity,
                metrics=kwargs.get('metrics'),
                group_by=kwargs.get('group_by'),
                filter_=kwargs.get('filter_'),
                sort_by=kwargs.get('sort_by')
            )

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

            costs = []
            for period_data in cost_data:
                if isinstance(period_data, dict) and "error" in period_data:
                    continue
                if not isinstance(period_data, dict):
                    continue
                time_period = period_data.get("TimePeriod", {})
                total = period_data.get("Total", {})
                cost = float(total.get("UnblendedCost", {}).get("Amount", 0))
                costs.append(cost)
                trends_analysis["total_cost"] += cost
                trends_analysis["total_periods"] += 1
                trends_analysis["cost_periods"].append({
                    "period": f"{time_period.get('Start')} to {time_period.get('End')}",
                    "cost": cost,
                    "date": time_period.get('Start')
                })

            if trends_analysis["total_periods"] > 0:
                trends_analysis["average_daily_cost"] = trends_analysis["total_cost"] / trends_analysis["total_periods"]
                
                if costs:
                    max_cost = max(costs)
                    min_cost = min(costs)
                    
                    for period in trends_analysis["cost_periods"]:
                        if period["cost"] == max_cost and max_cost > 0:
                            trends_analysis["peak_periods"].append(period)
                        if period["cost"] == min_cost:
                            trends_analysis["low_periods"].append(period)

                if len(costs) >= 2:
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

                if costs:
                    non_zero_costs = [c for c in costs if c > 0]
                    if non_zero_costs:
                        cost_variance = max(non_zero_costs) - min(non_zero_costs)
                        if cost_variance > trends_analysis["average_daily_cost"]:
                            trends_analysis["patterns"].append("High cost variability")
                        else:
                            trends_analysis["patterns"].append("Consistent cost pattern")
                    
                    zero_cost_periods = len([c for c in costs if c == 0])
                    if zero_cost_periods > len(costs) * 0.5:
                        trends_analysis["patterns"].append("Many zero-cost periods")
                    
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
            filter_ = {
                "Dimensions": {
                    "Key": "SERVICE",
                    "Values": ["Amazon Elastic Compute Cloud - Compute"]
                }
            }
            
            cost_data = self.get_aws_cost_data(
                start_date=start_date,
                end_date=end_date,
                granularity=granularity,
                filter_=filter_,
                group_by=[{"Type": "DIMENSION", "Key": "USAGE_TYPE"}]
            )

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

            costs = []
            for period_data in cost_data:
                if isinstance(period_data, dict) and "error" in period_data:
                    continue
                
                if not isinstance(period_data, dict):
                    continue
                
                time_period = period_data.get("TimePeriod", {})
                total = period_data.get("Total", {})
                groups = period_data.get("Groups", [])
                
                period_cost = 0.0
                period_breakdown = {}
                
                if groups:
                    for group in groups:
                        keys = group.get("Keys", [])
                        metrics = group.get("Metrics", {})
                        cost = float(metrics.get("UnblendedCost", {}).get("Amount", 0))
                        period_cost += cost
                        
                        if len(keys) >= 1:
                            usage_type = keys[0]
                            if usage_type not in period_breakdown:
                                period_breakdown[usage_type] = 0.0
                            period_breakdown[usage_type] += cost
                            
                            if usage_type not in resource_analysis["cost_breakdown"]:
                                resource_analysis["cost_breakdown"][usage_type] = 0.0
                            resource_analysis["cost_breakdown"][usage_type] += cost
                elif total:
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

            if resource_analysis["total_periods"] > 0:
                utilization_rate = resource_analysis["active_periods"] / resource_analysis["total_periods"]
                resource_analysis["utilization_insights"].append(
                    f"EC2 utilization rate: {utilization_rate:.1%} ({resource_analysis['active_periods']} active out of {resource_analysis['total_periods']} periods)"
                )
                
                if utilization_rate < 0.5:
                    resource_analysis["utilization_insights"].append("Low EC2 utilization detected - consider stopping or downsizing instances")
                elif utilization_rate > 0.9:
                    resource_analysis["utilization_insights"].append("High EC2 utilization detected - consider scaling up if needed")

            if len(costs) >= 2:
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

            if resource_analysis["total_cost"] > 0:
                avg_cost = resource_analysis["total_cost"] / resource_analysis["total_periods"]
                
                if avg_cost > 10:
                    resource_analysis["recommendations"].append("High EC2 costs detected - review instance types and consider reserved instances")
                
                if resource_analysis["active_periods"] < resource_analysis["total_periods"] * 0.3:
                    resource_analysis["recommendations"].append("Low EC2 activity - consider stopping instances during idle periods")
                
                if len(resource_analysis["cost_breakdown"]) > 1:
                    top_usage = max(resource_analysis["cost_breakdown"].items(), key=lambda x: x[1])
                    top_percentage = (top_usage[1] / resource_analysis["total_cost"]) * 100
                    resource_analysis["recommendations"].append(
                        f"Top EC2 cost component: {top_usage[0]} ({top_percentage:.1f}% of total) - review for optimization"
                    )
                
                resource_analysis["recommendations"].append(
                    f"Note: Analysis based on EC2 service costs. For specific resource {resource_id}, use AWS Cost Explorer directly with resource tags."
                )

            return resource_analysis
            
        except Exception as e:
            return {"error": f"Failed to analyze resource costs: {str(e)}"}


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

    def get_idle_resources(self, **kwargs) -> Dict[str, Any]:
        """
        Identify idle or underutilized resources, allowing user to pass parameters to describe_instances.

        Returns:
            Dict[str, Any]: List of idle resources with cost impact
        """
        params = {}
        if 'InstanceIds' in kwargs:
            params['InstanceIds'] = kwargs['InstanceIds']
        if 'DryRun' in kwargs:
            params['DryRun'] = kwargs['DryRun']
        if 'Filters' in kwargs:
            params['Filters'] = kwargs['Filters']
        if 'NextToken' in kwargs:
            params['NextToken'] = kwargs['NextToken']
        if 'MaxResults' in kwargs:
            params['MaxResults'] = kwargs['MaxResults']
        try:
            ec2_response = self.ec2_client.describe_instances(**params)
            idle_instances = []
            for reservation in ec2_response.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    if instance['State']['Name'] == 'running':
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
            Dict[str, Any]: Optimization recommendations including savings plans,
                           reservations, rightsizing, and idle resources.
        """
        try:
            recommendations = {
                'savings_plans': self._get_savings_plans_recommendations(),
                'reservations': self._get_reservation_purchase_recommendations(),
                'rightsizing': self._get_rightsizing_recommendations(),
                'idle_resources': self.get_idle_resources()
            }
            return recommendations
        except Exception as e:
            return {"error": f"Failed to get optimization recommendations: {str(e)}"}

    def _get_savings_plans_recommendations(self, **kwargs) -> Dict[str, Any]:
        """
        Get AWS Savings Plans recommendations with user-provided parameters.

        Returns:
            Dict[str, Any]: Savings Plans recommendations
        """
        params = {
            'SavingsPlansType': kwargs.get('SavingsPlansType', 'COMPUTE_SP'),
            'AccountScope': kwargs.get('AccountScope', 'PAYER'),
            'LookbackPeriodInDays': kwargs.get('LookbackPeriodInDays', 'THIRTY_DAYS'),
            'TermInYears': kwargs.get('TermInYears', 'ONE_YEAR'),
            'PaymentOption': kwargs.get('PaymentOption', 'NO_UPFRONT'),
        }
        if 'NextPageToken' in kwargs:
            params['NextPageToken'] = kwargs['NextPageToken']
        if 'PageSize' in kwargs:
            params['PageSize'] = kwargs['PageSize']
        if 'Filter' in kwargs:
            params['Filter'] = kwargs['Filter']
        try:
            response = self.ce_client.get_savings_plans_purchase_recommendation(**params)
            return response
        except Exception as e:
            return {"error": f"Failed to get Savings Plans recommendations: {str(e)}"}

    def _get_reservation_purchase_recommendations(self, **kwargs) -> Dict[str, Any]:
        """
        Get AWS Reserved Instance recommendations with user-provided parameters.

        Returns:
            Dict[str, Any]: Reserved Instance recommendations
        """
        params = {
            'AccountScope': kwargs.get('AccountScope', 'PAYER'),
            'LookbackPeriodInDays': kwargs.get('LookbackPeriodInDays', 'THIRTY_DAYS'),
            'TermInYears': kwargs.get('TermInYears', 'ONE_YEAR'),
            'PaymentOption': kwargs.get('PaymentOption', 'NO_UPFRONT'),
            'Service': kwargs.get('Service', 'Amazon Elastic Compute Cloud - Compute'),
        }
        if 'AccountId' in kwargs:
            params['AccountId'] = kwargs['AccountId']
        if 'NextPageToken' in kwargs:
            params['NextPageToken'] = kwargs['NextPageToken']
        if 'PageSize' in kwargs:
            params['PageSize'] = kwargs['PageSize']
        if 'Filter' in kwargs:
            params['Filter'] = kwargs['Filter']
        if 'ServiceSpecification' in kwargs:
            params['ServiceSpecification'] = kwargs['ServiceSpecification']
        try:
            response = self.ce_client.get_reservation_purchase_recommendation(**params)
            return response
        except Exception as e:
            return {"error": f"Failed to get reservation recommendations: {str(e)}"}

    def _get_rightsizing_recommendations(self, **kwargs) -> Dict[str, Any]:
        """
        Get AWS rightsizing recommendations with user-provided parameters.

        Returns:
            Dict[str, Any]: Rightsizing recommendations
        """
        params = {
            'Service': kwargs.get('Service', 'AmazonEC2'),
        }
        if 'Filter' in kwargs:
            params['Filter'] = kwargs['Filter']
        if 'Configuration' in kwargs:
            params['Configuration'] = kwargs['Configuration']
        if 'PageSize' in kwargs:
            params['PageSize'] = kwargs['PageSize']
        if 'NextPageToken' in kwargs:
            params['NextPageToken'] = kwargs['NextPageToken']
        try:
            response = self.ce_client.get_rightsizing_recommendation(**params)
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

    def get_cost_allocation_tags(self, **kwargs) -> Dict[str, Any]:
        """
        Get cost allocation tags.

        Returns:
            Dict[str, Any]: Cost allocation tags
        """
        try:
            response = self.organizations_client.list_tags_for_resource(
                ResourceId=kwargs.get('ResourceId', '')
            )
            return response
        except Exception as e:
            return {"error": f"Failed to get cost allocation tags: {str(e)}"}

    def get_compliance_status(self, **kwargs) -> Dict[str, Any]:
        """
        Get compliance status for cost policies.

        Returns:
            Dict[str, Any]: Compliance status
        """
        try:
            response = self.config_client.get_compliance_details_by_config_rule(
                ConfigRuleName=kwargs.get('ConfigRuleName')
            )
            return response
        except Exception as e:
            return {"error": f"Failed to get compliance status: {str(e)}"}

    def get_cost_policies(self, **kwargs) -> Dict[str, Any]:
        """
        Get AWS cost-related management policies (e.g., SCPs mentioning cost).

        Returns:
            Dict[str, Any]: Cost policies
        """
        try:
            policies = []
            paginator = self.organizations_client.get_paginator('list_policies')
            for page in paginator.paginate(Filter='SERVICE_CONTROL_POLICY'):
                for policy in page.get('Policies', []):
                    policy_detail = self.organizations_client.describe_policy(
                        PolicyId=policy['Id']
                    )['Policy']
                    name = policy_detail['Name'].lower()
                    description = policy_detail['Description'].lower()
                    if 'cost' in name or 'cost' in description:
                        policies.append({
                            "id": policy_detail['Id'],
                            "name": policy_detail['Name'],
                            "description": policy_detail['Description'],
                            "type": policy_detail['Type'],
                            "aws_managed": policy_detail['AwsManaged'],
                            "content": policy_detail['Content'],
                            "arn": policy_detail['Arn'],
                            "tags": self.organizations_client.list_tags_for_resource(
                                ResourceId=policy_detail['Id']
                            ).get('Tags', [])
                        })
            return {"policies": policies}
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
        self.cost_client = AWSCostManagement(access_key, secret_key, region)

    def get_default_forecast_time_period(self, kwargs):
        import datetime
        def parse_date(date_str):
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        if 'TimePeriod' in kwargs:
            tp = kwargs['TimePeriod']
            start = parse_date(tp['Start'])
            if start < today:
                tp['Start'] = str(today)
            return tp
        if 'start_date' in kwargs and 'end_date' in kwargs:
            start = parse_date(kwargs['start_date'])
            end = parse_date(kwargs['end_date'])
            if start < today:
                start = today
            if end <= start:
                raise ValueError("end_date must be after start_date for forecast.")
            return {'Start': str(start), 'End': str(end)}
        if 'start_date' in kwargs:
            start = parse_date(kwargs['start_date'])
            if start < today:
                start = today
            end = start + datetime.timedelta(days=30)
            return {'Start': str(start), 'End': str(end)}
        if 'end_date' in kwargs:
            end = parse_date(kwargs['end_date'])
            start = today
            if end <= start:
                raise ValueError("end_date must be after today for forecast.")
            return {'Start': str(start), 'End': str(end)}
        return {'Start': str(today), 'End': str(today + datetime.timedelta(days=30))}

    def get_cost_forecast(self, **kwargs) -> Dict[str, Any]:
        """
        Get unified cost forecast with daily breakdowns and AI model integration.
        
        This method provides a unified response format that includes:
        - Daily cost forecasts with confidence intervals
        - Total cost summaries
        - AI model information and accuracy metrics
        - Historical data for comparison
        
        Args:
            **kwargs: Flexible parameters including:
                - start_date: Historical data start date
                - end_date: Historical data end date
                - forecast_period: Number of days to forecast (default: 30)
                - granularity: Data granularity (DAILY/MONTHLY)
                - use_ai_model: Whether to use AWS Forecast AI model (default: True)

        Returns:
            Dict[str, Any]: Unified forecast response with daily breakdowns
        """
        import datetime
        from datetime import timedelta
        
        today = datetime.date.today()
        start_date = kwargs.get('start_date', (today - timedelta(days=90)).strftime("%Y-%m-%d"))
        end_date = kwargs.get('end_date', today.strftime("%Y-%m-%d"))
        forecast_period = kwargs.get('forecast_period', 30)
        granularity = kwargs.get('granularity', 'DAILY')
        use_ai_model = kwargs.get('use_ai_model', True)
        
        try:
            historical_data = self.cost_client.get_aws_cost_data(
                start_date=start_date,
                end_date=end_date,
                granularity=granularity,
                metrics=['UnblendedCost']
            )
            
            daily_costs = []
            total_historical_cost = 0.0
            
            for period_data in historical_data:
                if isinstance(period_data, dict) and "error" not in period_data:
                    time_period = period_data.get("TimePeriod", {})
                    total = period_data.get("Total", {})
                    cost = float(total.get("UnblendedCost", {}).get("Amount", 0))
                    
                    start_date_str = time_period.get('Start', '')
                    if start_date_str:
                        daily_costs.append({
                            "date": start_date_str.split('T')[0],
                            "cost": cost
                        })
                        total_historical_cost += cost
            
            avg_daily_cost = total_historical_cost / len(daily_costs) if daily_costs else 0
            
            forecast_results = []
            total_forecast_cost = 0.0
            
            if use_ai_model:
                try:
                    forecast_results = self._generate_ai_enhanced_forecast(
                        daily_costs, forecast_period, avg_daily_cost
                    )
                except Exception as e:
                    forecast_results = self._generate_statistical_forecast(
                        daily_costs, forecast_period, avg_daily_cost
                    )
            else:
                forecast_results = self._generate_statistical_forecast(
                    daily_costs, forecast_period, avg_daily_cost
                )
            
            total_forecast_cost = sum(day["forecast_value"] for day in forecast_results)
            
            insights = []
            if daily_costs:
                recent_trend = self._calculate_trend(daily_costs[-7:]) if len(daily_costs) >= 7 else 0
                insights.append(f"Historical average daily cost: ${avg_daily_cost:.2f}")
                insights.append(f"Recent 7-day trend: {recent_trend:.1f}% change")
                insights.append(f"Forecasted total cost for {forecast_period} days: ${total_forecast_cost:.2f}")
            
            return {
                "forecast_period": forecast_period,
                "start_date": start_date,
                "end_date": end_date,
                "total_historical_cost": round(total_historical_cost, 2),
                "total_forecast_cost": round(total_forecast_cost, 2),
                "average_daily_cost": round(avg_daily_cost, 2),
                "forecast_results": forecast_results,
                "ai_model_used": use_ai_model,
                "model_accuracy": self._calculate_model_accuracy(daily_costs),
                "insights": insights,
                "granularity": granularity,
                "message": f"Unified cost forecast generated for {forecast_period} days using {'AI model' if use_ai_model else 'statistical analysis'}"
            }
            
        except Exception as e:
            return {"error": f"Failed to generate unified cost forecast: {str(e)}"}
    
    def _generate_ai_enhanced_forecast(self, daily_costs, forecast_period, avg_daily_cost):
        """Generate AI-enhanced forecast using trend analysis and seasonality."""
        import numpy as np
        from datetime import datetime, timedelta
        
        if not daily_costs:
            return []
        
        costs = [day["cost"] for day in daily_costs]
        dates = [datetime.strptime(day["date"], "%Y-%m-%d") for day in daily_costs]
        
        if len(costs) > 1:
            x = np.arange(len(costs))
            y = np.array(costs)
            trend_coef = np.polyfit(x, y, 1)[0]
        else:
            trend_coef = 0
        
        weekly_pattern = self._calculate_weekly_pattern(daily_costs)
        
        forecast_results = []
        last_date = dates[-1] if dates else datetime.today()
        
        for i in range(1, forecast_period + 1):
            forecast_date = last_date + timedelta(days=i)
            
            base_forecast = avg_daily_cost + (trend_coef * i)
            
            day_of_week = forecast_date.weekday()
            seasonal_factor = weekly_pattern.get(day_of_week, 1.0)
            adjusted_forecast = base_forecast * seasonal_factor
            
            confidence_range = avg_daily_cost * 0.2 
            lower_bound = max(0, adjusted_forecast - confidence_range)
            upper_bound = adjusted_forecast + confidence_range
            
            forecast_results.append({
                "date": forecast_date.strftime("%Y-%m-%d"),
                "forecast_value": round(adjusted_forecast, 2),
                "lower_bound": round(lower_bound, 2),
                "upper_bound": round(upper_bound, 2),
                "confidence_level": 0.8
            })
        
        return forecast_results
    
    def _generate_statistical_forecast(self, daily_costs, forecast_period, avg_daily_cost):
        """Generate statistical forecast using moving averages and variance."""
        from datetime import datetime, timedelta
        import numpy as np
        
        if not daily_costs:
            return []
        
        costs = [day["cost"] for day in daily_costs]
        moving_avg = sum(costs[-7:]) / 7 if len(costs) >= 7 else avg_daily_cost
        
        variance = np.var(costs) if len(costs) > 1 else (avg_daily_cost * 0.1) ** 2
        std_dev = np.sqrt(variance)
        
        forecast_results = []
        last_date = datetime.strptime(daily_costs[-1]["date"], "%Y-%m-%d")
        
        for i in range(1, forecast_period + 1):
            forecast_date = last_date + timedelta(days=i)
            
            forecast_value = moving_avg
            
            lower_bound = max(0, forecast_value - (1.96 * std_dev))
            upper_bound = forecast_value + (1.96 * std_dev)
            
            forecast_results.append({
                "date": forecast_date.strftime("%Y-%m-%d"),
                "forecast_value": round(forecast_value, 2),
                "lower_bound": round(lower_bound, 2),
                "upper_bound": round(upper_bound, 2),
                "confidence_level": 0.95
            })
        
        return forecast_results
    
    def _calculate_weekly_pattern(self, daily_costs):
        """Calculate weekly cost patterns for seasonality."""
        weekly_totals = {i: [] for i in range(7)}
        
        for day in daily_costs:
            date = datetime.strptime(day["date"], "%Y-%m-%d")
            day_of_week = date.weekday()
            weekly_totals[day_of_week].append(day["cost"])
        
        weekly_pattern = {}
        overall_avg = sum(day["cost"] for day in daily_costs) / len(daily_costs) if daily_costs else 1
        
        for day_of_week in range(7):
            if weekly_totals[day_of_week]:
                day_avg = sum(weekly_totals[day_of_week]) / len(weekly_totals[day_of_week])
                weekly_pattern[day_of_week] = day_avg / overall_avg if overall_avg > 0 else 1.0
            else:
                weekly_pattern[day_of_week] = 1.0
        
        return weekly_pattern
    
    def _calculate_trend(self, recent_costs):
        """Calculate trend percentage from recent cost data."""
        if len(recent_costs) < 2:
            return 0
        
        costs = [day["cost"] for day in recent_costs]
        first_avg = sum(costs[:len(costs)//2]) / (len(costs)//2)
        second_avg = sum(costs[len(costs)//2:]) / (len(costs)//2)
        
        if first_avg == 0:
            return 0
        
        return ((second_avg - first_avg) / first_avg) * 100
    
    def _calculate_model_accuracy(self, daily_costs):
        """Calculate model accuracy metrics."""
        import numpy as np
        
        if len(daily_costs) < 2:
            return {"mape": 0, "rmse": 0}
        
        costs = [day["cost"] for day in daily_costs]
        mean_cost = sum(costs) / len(costs)
        
        mape = sum(abs(cost - mean_cost) / mean_cost for cost in costs if mean_cost > 0) / len(costs) * 100
        
        rmse = np.sqrt(sum((cost - mean_cost) ** 2 for cost in costs) / len(costs))
        
        return {
            "mape": round(mape, 2),
            "rmse": round(rmse, 2),
            "mean_absolute_error": round(sum(abs(cost - mean_cost) for cost in costs) / len(costs), 2)
        }

    def get_default_date_interval(self, kwargs):
        import datetime
        today = datetime.date.today()
        if today.month == 1:
            start_date = today.replace(year=today.year - 1, month=12)
        else:
            start_date = today.replace(month=today.month - 1)
        return {
            'StartDate': str(start_date),
            'EndDate': str(today)
        }
    
    def get_cost_anomalies(self, **kwargs) -> Dict[str, Any]:
        """
        Get cost anomalies with user-provided parameters.
        Ensures required parameters (DateInterval) are present with defaults if not provided.

        Returns:
            Dict[str, Any]: Cost anomalies data
        """
        params = {}
        
        if 'DateInterval' in kwargs:
            params['DateInterval'] = kwargs['DateInterval']
        else:
            params['DateInterval'] = self.get_default_date_interval(kwargs)
        
        if 'MonitorArn' in kwargs:
            params['MonitorArn'] = kwargs['MonitorArn']
        if 'Feedback' in kwargs:
            params['Feedback'] = kwargs['Feedback']
        if 'TotalImpact' in kwargs:
            total_impact = kwargs['TotalImpact']
            if 'NumericOperator' not in total_impact or 'StartValue' not in total_impact:
                raise ValueError("TotalImpact must contain 'NumericOperator' and 'StartValue'")
            params['TotalImpact'] = total_impact
        if 'NextPageToken' in kwargs:
            params['NextPageToken'] = kwargs['NextPageToken']
        if 'MaxResults' in kwargs:
            params['MaxResults'] = kwargs['MaxResults']
        
        try:
            response = self.ce_client.get_anomalies(**params)
            return response
        except Exception as e:
            return {"error": f"Failed to get cost anomalies: {str(e)}"}

    def get_cost_efficiency_metrics(self, user_count=None, transaction_count=None, **kwargs) -> Dict[str, Any]:
        """
        Calculate real cost efficiency metrics from AWS Cost Explorer.
        Allows user to pass any supported parameters to get_cost_and_usage.
        Ensures required parameters (TimePeriod, Granularity) are present with sensible defaults if not provided.

        Args:
            user_count (int, optional): Number of users for cost per user
            transaction_count (int, optional): Number of transactions for cost per transaction
            **kwargs: Any supported parameters for get_cost_and_usage (e.g., TimePeriod, Granularity, Filter, Metrics, GroupBy, BillingViewArn, NextPageToken)

        Returns:
            Dict[str, Any]: Cost efficiency metrics
        """
        import datetime
        today = datetime.date.today()
        if 'TimePeriod' in kwargs:
            time_period = kwargs['TimePeriod']
            if 'Start' not in time_period or time_period['Start'] is None:
                time_period['Start'] = today.replace(day=1).strftime("%Y-%m-%d")
            if 'End' not in time_period or time_period['End'] is None:
                time_period['End'] = today.strftime("%Y-%m-%d")
        else:
            start_date = kwargs.get('start_date', today.replace(day=1).strftime("%Y-%m-%d"))
            end_date = kwargs.get('end_date', today.strftime("%Y-%m-%d"))
            time_period = {"Start": start_date, "End": end_date}
        granularity = kwargs.get('Granularity', 'MONTHLY')
        metrics = kwargs.get('Metrics', ['UnblendedCost'])
        group_by = kwargs.get('GroupBy', [{"Type": "DIMENSION", "Key": "SERVICE"}])
        params = {
            "TimePeriod": time_period,
            "Granularity": granularity,
            "Metrics": metrics,
            "GroupBy": group_by
        }
        if 'Filter' in kwargs:
            params['Filter'] = kwargs['Filter']
        if 'BillingViewArn' in kwargs:
            params['BillingViewArn'] = kwargs['BillingViewArn']
        if 'NextPageToken' in kwargs:
            params['NextPageToken'] = kwargs['NextPageToken']
        try:
            cost_data = self.ce_client.get_cost_and_usage(**params)
            total_cost = 0.0
            cost_by_service = {}
            for result in cost_data.get('ResultsByTime', []):
                for group in result.get('Groups', []):
                    key = group['Keys'][0]
                    amount = float(group['Metrics'][metrics[0]]['Amount'])
                    cost_by_service[key] = amount
                    total_cost += amount
            waste_cost = 0.0
            metrics_result = {
                "total_cost": total_cost,
                "cost_by_service": cost_by_service,
                "waste_estimate": waste_cost,
            }
            if user_count:
                metrics_result["cost_per_user"] = total_cost / user_count
            if transaction_count:
                metrics_result["cost_per_transaction"] = total_cost / transaction_count
            return {"efficiency_metrics": metrics_result}
        except Exception as e:
            return {"error": f"Failed to get cost efficiency metrics: {str(e)}"}

    def generate_cost_report(self, **kwargs) -> Dict[str, Any]:
        """
        Generate comprehensive cost report using AWS Cost Explorer get_cost_and_usage.
        Returns a unified format with processed data across all cloud providers.

        Args:
            report_type (str): Type of report (monthly, quarterly, annual)
            **kwargs: Any supported parameters for get_cost_and_usage

        Returns:
            Dict[str, Any]: Unified cost report format
        """
        import datetime
        from collections import defaultdict
        
        today = datetime.date.today()
        if 'TimePeriod' in kwargs:
            time_period = kwargs['TimePeriod']
            if 'Start' not in time_period or time_period['Start'] is None:
                time_period['Start'] = today.replace(day=1).strftime("%Y-%m-%d")
            if 'End' not in time_period or time_period['End'] is None:
                time_period['End'] = today.strftime("%Y-%m-%d")
        else:
            start_date = kwargs.get('start_date', today.replace(day=1).strftime("%Y-%m-%d"))
            end_date = kwargs.get('end_date', today.strftime("%Y-%m-%d"))
            time_period = {"Start": start_date, "End": end_date}

        report_type = kwargs.get('report_type', 'monthly')
        
        try:
            service_params = {
            "TimePeriod": time_period,
                "Granularity": "MONTHLY",
                "Metrics": ["UnblendedCost"],
                "GroupBy": [{"Type": "DIMENSION", "Key": "SERVICE"}]
            }
            service_data = self.ce_client.get_cost_and_usage(**service_params)
            
            region_params = {
                "TimePeriod": time_period,
                "Granularity": "MONTHLY", 
                "Metrics": ["UnblendedCost"],
                "GroupBy": [{"Type": "DIMENSION", "Key": "REGION"}]
            }
            region_data = self.ce_client.get_cost_and_usage(**region_params)
            
            daily_params = {
                "TimePeriod": time_period,
                "Granularity": "DAILY",
                "Metrics": ["UnblendedCost"]
            }
            daily_data = self.ce_client.get_cost_and_usage(**daily_params)
            
            service_breakdown = []
            total_cost = 0.0
            for result in service_data.get('ResultsByTime', []):
                for group in result.get('Groups', []):
                    service_name = group['Keys'][0]
                    amount = float(group['Metrics']['UnblendedCost']['Amount'])
                    total_cost += amount
                    service_breakdown.append({
                        "service": service_name,
                        "total_cost": amount,
                        "avg_daily_cost": amount
                    })
            
            region_breakdown = []
            for result in region_data.get('ResultsByTime', []):
                for group in result.get('Groups', []):
                    region_name = group['Keys'][0]
                    amount = float(group['Metrics']['UnblendedCost']['Amount'])
                    region_breakdown.append({
                        "region": region_name,
                        "total_cost": amount,
                        "avg_daily_cost": amount
                    })
            
            daily_trends = []
            for result in daily_data.get('ResultsByTime', []):
                date_str = result['TimePeriod']['Start']
                total = result.get('Total', {})
                daily_cost = float(total.get('UnblendedCost', {}).get('Amount', 0))
                daily_trends.append({
                    "date": date_str,
                    "daily_cost": daily_cost
                })
            
            total_days = len(daily_trends)
            avg_daily_cost = sum(d['daily_cost'] for d in daily_trends) / total_days if total_days > 0 else 0
            min_daily_cost = min(d['daily_cost'] for d in daily_trends) if daily_trends else 0
            max_daily_cost = max(d['daily_cost'] for d in daily_trends) if daily_trends else 0
            
            if daily_trends:
                costs = [d['daily_cost'] for d in daily_trends]
                cost_stddev = (sum((c - avg_daily_cost) ** 2 for c in costs) / len(costs)) ** 0.5 if len(costs) > 1 else 0
                cost_variance_ratio = cost_stddev / avg_daily_cost if avg_daily_cost > 0 else 0
                efficiency_score = max(0, 1 - cost_variance_ratio) if cost_variance_ratio > 0 else 1
            else:
                cost_stddev = 0
                cost_variance_ratio = 0
                efficiency_score = 1
            
            for service in service_breakdown:
                service["avg_daily_cost"] = service["total_cost"] / total_days if total_days > 0 else 0
            
            for region in region_breakdown:
                region["avg_daily_cost"] = region["total_cost"] / total_days if total_days > 0 else 0
            
            cost_drivers = []
            for service in service_breakdown[:10]:
                cost_drivers.append({
                    "sku": {
                        "id": service["service"],
                        "description": service["service"]
                    },
                    "service": {
                        "id": service["service"],
                        "description": service["service"]
                    },
                    "total_cost": service["total_cost"]
                })
            
            return {
                "report_type": report_type,
                "period": {"start": time_period['Start'], "end": time_period['End']},
                "generated_at": datetime.datetime.now().isoformat(),
                "summary": {
                "total_cost": total_cost,
                    "total_days": total_days,
                    "avg_daily_cost": avg_daily_cost,
                    "min_daily_cost": min_daily_cost,
                    "max_daily_cost": max_daily_cost,
                    "unique_services": len(service_breakdown),
                    "unique_regions": len(region_breakdown)
                },
                "breakdowns": {
                    "by_service": service_breakdown,
                    "by_region": region_breakdown
                },
                "trends": {
                    "daily_costs": daily_trends
                },
                "cost_drivers": cost_drivers,
                "efficiency_metrics": {
                    "cost_efficiency_score": efficiency_score,
                    "cost_variance_ratio": cost_variance_ratio,
                    "cost_stddev": cost_stddev
                },
                "message": "Comprehensive cost report generated for monthly period."
            }
        except Exception as e:
            return {"error": f"Failed to generate cost report: {str(e)}"}

