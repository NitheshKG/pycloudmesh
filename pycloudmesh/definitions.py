from enum import Enum

class AWSReservationService(str, Enum):
    """AWS services that support reservations."""
    AMAZONEC2 = "AmazonEC2"
    AMAZONRDS = "AmazonRDS"
    AMAZONREDSHIFT = "AmazonRedshift"
    AMAZONELASTICCACHE = "AmazonElastiCache"
    AMAZONOPENSEARCHSERVICE = "AmazonOpenSearchService"

class AWSCostMetrics(str, Enum):
    """AWS Cost Explorer metrics."""
    UNBLENDED_COST = "UnblendedCost"
    BLENDED_COST = "BlendedCost"
    AMORTIZED_COST = "AmortizedCost"
    NET_AMORTIZED_COST = "NetAmortizedCost"
    USAGE_QUANTITY = "UsageQuantity"
    NORMALIZED_USAGE_AMOUNT = "NormalizedUsageAmount"
    NET_UNBLENDED_COST = "NetUnblendedCost"
    NET_BLENDED_COST = "NetBlendedCost"

