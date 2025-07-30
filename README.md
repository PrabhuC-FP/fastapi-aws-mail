# 📧 AWS Mail API – FastAPI Implementation

Send emails using Amazon SES via a simple FastAPI-based REST API.

---

## 🚀 Features

- ✅ Send HTML emails via AWS SES
- 🔐 Uses credentials from `.env`
- 📬 Option to specify dynamic `from_email` (must be SES verified)
- 🛡 Validates inputs (to, subject, body) with Pydantic
- 🧪 Easy to test using Swagger or curl/Postman

---

## 📁 Project Structure
fastapi-aws-mail/
├── app.py # Main FastAPI app
├── .env # Environment variables
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

## ⚙️ Requirements

- Python 3.9+
- AWS SES account (with verified email/domain)
- AWS credentials with SES permissions

---

## 🔧 Setup Instructions

### 1. Clone this project

```bash
git clone https://github.com/yourname/fastapi-aws-mail.git
cd fastapi-aws-mail
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create a .env file
```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-west-2
MAIL_FROM=verified@example.com
```

### 4. Run the FastAPI server
```bash
uvicorn app:app --reload
```
- Visit the interactive docs: http://127.0.0.1:8000/docs

## 🔌 API Usage

# ▶️ POST /send-email
Sends an email via AWS SES.
- 📥 Request Body (JSON)
```
{
  "to": "recipient@example.com",
  "subject": "Welcome",
  "body": "<h1>Hello from FastAPI</h1>",
  "from_email": "optional@yourdomain.com"
}
```


- 📤 Sample cURL Request

```bash
curl -X POST http://localhost:8000/send-email \
  -H "Content-Type: application/json" \
  -d '{"to": "you@example.com", "subject": "Test Email", "body": "<b>Hello!</b>"}'
```

## ✅ Response (Success)
```json
{
  "message": "Email sent successfully",
  "message_id": "010f7e8f-xxxx"
}
```

## ❌ Response (Error)
```json
{
  "detail": "An error occurred (InvalidClientTokenId) when calling the SendEmail operation: The security token included in the request is invalid."
}
```

### 🧪 Testing the API
Visit Swagger Docs:
👉 http://localhost:8000/docs

Or use Postman/curl with the sample payload above

## 🌐 Deployment Suggestions
You can deploy the app to:

- Render.com (free-tier hosting)

- AWS EC2 / Lightsail

- Railway.app / Vercel / Fly.io

- Docker (optional Dockerfile can be added)

## 🛑 Important Notes
In SES Sandbox Mode:

- Both from and to emails must be verified.

- To send to unverified users, request production access from AWS.

- Ensure your .env is not committed to version control.

## 🙋‍♂️ Need Help?
Open an issue or reach out at yourname@example.com.

```yaml

Let me know if you also want:

- A `Dockerfile` or `Procfile`
- A GitHub repo structure
- Swagger schema auto-export

Ready to ship! ✅
```