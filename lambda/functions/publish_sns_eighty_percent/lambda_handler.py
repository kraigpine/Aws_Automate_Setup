import boto3

def lambda_handler(event, context):
    sns_client = boto3.client('sns')

    # Replace with your desired subject and message
    subject = "Aws Budget Alert - 80 percent - Tutorials"
    message = "You have reached 80 percent of your monthly budget in your Tutorials account"

    # Replace with the ARN of your SNS topic
    topic_arn = os.environ['TOPIC_ARN'] 

    response = sns_client.publish(
        TopicArn=topic_arn,
        Subject=subject,
        Message=message
    )

    return {
        'statusCode': 200,
        'body': 'Email sent successfully!'
    }