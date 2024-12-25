from constructs import Construct
from aws_cdk import (
    Stack,
    aws_budgets as budgets,
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_iam as iam
)

class BudgetAlertStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # 1. Create SNS Topic for Budget Alerts
        budget_alert_topic = sns.Topic(self, "BudgetAlertTopic") 

        # 2. Create Budget with Notification
        budget = budgets.Budget(
            self, "Budget",
            budget_name="MyMonthlyBudget",
            budget_limit=budgets.BudgetLimit.of_amount("USD", .01), 
            budget_type=budgets.BudgetType.COST,
            notifications=[
                budgets.Notification(
                    notification_type=budgets.NotificationType.ACTUAL,
                    threshold=80,
                    comparison_operator=budgets.ComparisonOperator.GREATER_THAN,
                    subscriber=budgets.NotificationSubscriber.sns(budget_alert_topic)
                )
            ]
        )

        # Create the lambda role and 
        sns_lambda_role = iam.Role(
            self, "sns_lambda_role",
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess") 
            ]

        )

        self.sns_email = sns.Topic(self, "sns_email")

        publish_sns_eighty_percent = _lambda.Function(
            self, "publish_sns_eighty_percent",
            function_name="publish_sns_eighty_percent",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_handler", 
            code=_lambda.Code.from_asset("lambda/functions/publish_sns_eighty_percent"),
            role=sns_lambda_role,
            environment={
                "TOPIC_ARN": self.sns_email.topic_arn  # Pass the topic ARN as an environment variable
            }
        )

        sns_email.add_subscription(subscriptions.EmailSubscription("kraigpine@gmail.com"))