from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# AWS credentials and region
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION", "us-west-2")
default_from_email = os.getenv("MAIL_FROM")

# Create AWS SES and SNS clients
ses_client = boto3.client(
    'ses',
    region_name=aws_region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

sns_client = boto3.client(
    'sns',
    region_name=aws_region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

# ----------------------------
# MODELS
# ----------------------------

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str
    from_email: EmailStr | None = None

class SMSRequest(BaseModel):
    phone_number: str
    message: str

class TopicPublishRequest(BaseModel):
    topic_arn: str
    message: str

# ----------------------------
# ROUTES
# ----------------------------

@app.post("/send-email")
def send_email(req: EmailRequest):
    try:
        response = ses_client.send_email(
            Source=req.from_email or default_from_email,
            Destination={'ToAddresses': [req.to]},
            Message={
                'Subject': {'Data': req.subject},
                'Body': {'Html': {'Data': req.body}}
            }
        )
        return {"message": "Email sent successfully", "message_id": response['MessageId']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send-sms")
def send_sms(req: SMSRequest):
    try:
        response = sns_client.publish(
            PhoneNumber=req.phone_number,
            Message=req.message
        )
        return {"message": "SMS sent", "message_id": response['MessageId']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send-topic")
def send_topic(req: TopicPublishRequest):
    try:
        response = sns_client.publish(
            TopicArn=req.topic_arn,
            Message=req.message
        )
        return {"message": "Message sent to topic", "message_id": response['MessageId']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
