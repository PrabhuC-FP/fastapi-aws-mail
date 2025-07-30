from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Load env vars
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
MAIL_FROM = os.getenv("MAIL_FROM")

# Boto3 client
ses_client = boto3.client(
    "ses",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# FastAPI app
app = FastAPI()

# Request body model
class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str
    from_email: EmailStr | None = None

@app.post("/send-email")
async def send_email(data: EmailRequest):
    from_address = data.from_email or MAIL_FROM

    try:
        response = ses_client.send_email(
            Source=from_address,
            Destination={"ToAddresses": [data.to]},
            Message={
                "Subject": {"Data": data.subject},
                "Body": {
                    "Html": {"Data": data.body}
                }
            }
        )
        return {"message": "Email sent successfully", "message_id": response["MessageId"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
