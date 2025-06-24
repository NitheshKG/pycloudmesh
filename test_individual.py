from pycloudmesh.providers.aws import AWSCostManagement, AWSFinOpsOptimization

from pycloudmesh import aws_client

import os
import json

# Get credentials from environment variables
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.environ.get('AWS_REGION', 'ap-south-1')

def test_recommendations():
    if not all([AWS_ACCESS_KEY, AWS_SECRET_KEY]):
        raise ValueError("AWS credentials not found in environment variables")
        
    aws_cost = AWSCostManagement(
        access_key=AWS_ACCESS_KEY,
        secret_key=AWS_SECRET_KEY,
        region=AWS_REGION
    )

    aws_finops = AWSFinOpsOptimization(
        access_key=AWS_ACCESS_KEY,
        secret_key=AWS_SECRET_KEY,
        region=AWS_REGION
    )
    
    aws = aws_client(
        access_key=AWS_ACCESS_KEY,
        secret_key=AWS_SECRET_KEY,
        region=AWS_REGION
    )


    # # Test Savings Plans recommendations
    # print("\nTesting Savings Plans Recommendations...")
    # result = aws_cost.get_savings_plans_recommendations()
    # print("Result:", result)
    
    # # Test Reserved Instance recommendations
    # print("\nTesting Reserved Instance Recommendations...")
    # result = aws_cost.get_reservation_purchase_recommendations()
    # print("Result:", result)

    # # Test Idle recommendations
    # print("\nTesting Idle Recommendations")
    # result = aws_finops.get_idle_resources()
    # print("Result:", result)

    # result = aws.get_optimization_recommendations()
    # print(result)

    # result = aws.get_reservation_purchase_recommendations()
    # print(result)

    # result = aws.get_savings_plans_recommendations(
    #     SavingsPlansType="EC2_INSTANCE_SP",
    # TermInYears="THREE_YEARS",
    # PaymentOption="ALL_UPFRONT",
    # LookbackPeriodInDays="SIXTY_DAYS"
    # )
    # print(result)

    # result = aws.get_reservation_purchase_recommendations()
    # print(result)


    # result = aws.get_cost_forecast()
    # print(result)

    # result = aws.get_cost_anomalies(
    # )
    # print(result)

    # result = aws.get_cost_efficiency_metrics()
    # print(result)

    # result = aws.generate_cost_report(
    #     Metrics=['UnblendedCost', 'AmortizedCost', 'BlendedCost']
    # )

    result = aws.get_cost_trends()
    print(json.dumps(result, indent=3))
    # print(result)



if __name__ == "__main__":
    test_recommendations()
