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

        # Create the lambda role and assign policies
        # - The name of the AWSLambdaBasicExecutionRole is actually: service-role/AWSLambdaBasicExecutionRole
        sns_lambda_role = iam.Role(
            self, "sns_lambda_role",
            role_name="sns_lambda_role",
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )

        # Create the sns for the lambda to call (lambda > sns > email)
        sns_lambda_email = sns.Topic(
            self, "sns_budget_alert_email",
            topic_name="sns_budget_alert_email"
        )
        sns_lambda_email.add_subscription(subscriptions.EmailSubscription("you@email.com"))

        # Create the lambda function 
        publish_sns_eighty_percent = _lambda.Function(
            self, "z-publish_sns_eighty_percent",
            function_name="z-publish_sns_eighty_percent",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_handler.lambda_handler", 
            code=_lambda.Code.from_asset("lambda/functions/publish_sns_eighty_percent"),
            role=sns_lambda_role,
            environment={
                "TOPIC_ARN": sns_lambda_email.topic_arn  # Pass the topic ARN as an environment variable
            }
        )

        # Create SNS Topic for Budget Alert (BA > Sns > lambda)
        sns_budget_alert_relay = sns.Topic(
            self, "sns_budget_alert_relay", 
            topic_name="sns_budget_alert_relay"
        ) 
        sns_budget_alert_relay.add_subscription(subscriptions.LambdaSubscription(publish_sns_eighty_percent))
       
        # Create Budget with Notification
        # currently there is no L2 construct for a budget and its just quicker to make this in the console
        