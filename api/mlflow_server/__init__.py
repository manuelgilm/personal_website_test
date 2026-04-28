import azure.functions as func
import requests
from requests.auth import HTTPBasicAuth
import os
import json
import smtplib
import string
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ============================================
# CONFIGURATION - Set these in Azure Function App Settings
# ============================================
MLFLOW_SERVER_URL = os.getenv("MLFLOW_SERVER_URL")
MLFLOW_ADMIN_USER = os.getenv("MLFLOW_ADMIN_USER")
MLFLOW_ADMIN_PASSWORD = os.getenv("MLFLOW_ADMIN_PASSWORD")

NAMECHEAP_SMTP_SERVER = os.getenv("NAMECHEAP_SMTP_SERVER", "smtp.namecheap.com")
NAMECHEAP_SMTP_PORT = int(os.getenv("NAMECHEAP_SMTP_PORT", "587"))
NAMECHEAP_EMAIL = os.getenv("NAMECHEAP_EMAIL")
NAMECHEAP_PASSWORD = os.getenv("NAMECHEAP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", NAMECHEAP_EMAIL)

# ============================================
# UTILITY FUNCTIONS
# ============================================

def generate_password(length=16):
    """Generate a random secure password"""
    characters = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(random.choice(characters) for _ in range(length))

def extract_username_from_email(email):
    """Extract username from email (john@example.com -> john)"""
    username = email.split("@")[0].lower()
    # Sanitize: replace invalid characters (., _, etc.) with hyphens
    # MLflow allows: lowercase alphanumeric and hyphens only
    username = username.replace(".", "-").replace("_", "-")
    # Remove any double hyphens
    while "--" in username:
        username = username.replace("--", "-")
    # Remove leading/trailing hyphens
    username = username.strip("-")
    return username

def send_email(user_email, username, password, workspace_name):
    """Send credentials email via Namecheap SMTP"""
    try:
        # Create email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Your MLflow Server Access Credentials"
        msg["From"] = FROM_EMAIL
        msg["To"] = user_email

        # Plain text version
        text = f"""
Hello {username},

Your MLflow server account has been created successfully!

Here are your credentials:
- Username: {username}
- Password: {password}
- Workspace: {workspace_name}
- MLflow Server: {MLFLOW_SERVER_URL}

You can now log in and start tracking your ML experiments.

Best regards,
AI Room Team
        """

        # HTML version
        html = f"""\
<html>
  <body style="font-family: Arial, sans-serif;">
    <h2>Welcome to MLflow Server!</h2>
    <p>Hello <strong>{username}</strong>,</p>
    <p>Your MLflow server account has been created successfully. Here are your credentials:</p>
    
    <table style="border: 1px solid #ddd; padding: 10px; margin: 20px 0;">
      <tr>
        <td style="font-weight: bold; width: 150px;">Username:</td>
        <td><code>{username}</code></td>
      </tr>
      <tr>
        <td style="font-weight: bold;">Password:</td>
        <td><code>{password}</code></td>
      </tr>
      <tr>
        <td style="font-weight: bold;">Workspace:</td>
        <td><code>{workspace_name}</code></td>
      </tr>
      <tr>
        <td style="font-weight: bold;">Server:</td>
        <td><a href="{MLFLOW_SERVER_URL}">{MLFLOW_SERVER_URL}</a></td>
      </tr>
    </table>
    
    <p>You can now log in and start tracking your ML experiments.</p>
    <p style="color: #666; font-size: 12px; margin-top: 30px;">
      Best regards,<br>
      AI Room Team
    </p>
  </body>
</html>
        """

        # Attach both versions
        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        # Send email
        with smtplib.SMTP(NAMECHEAP_SMTP_SERVER, NAMECHEAP_SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(NAMECHEAP_EMAIL, NAMECHEAP_PASSWORD)
            server.sendmail(FROM_EMAIL, user_email, msg.as_string())

        return True, "Email sent successfully"
    except Exception as e:
        return False, f"Email error: {str(e)}"

# ============================================
# MLFLOW API OPERATIONS
# ============================================

def create_mlflow_user(username, password):
    """Create a new MLflow user"""
    try:
        auth = HTTPBasicAuth(MLFLOW_ADMIN_USER, MLFLOW_ADMIN_PASSWORD)
        response = requests.post(
            f"{MLFLOW_SERVER_URL}/api/2.0/mlflow/users/create",
            auth=auth,
            json={"username": username, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            return True, "User created successfully"
        elif response.status_code == 400 and "already exists" in response.text:
            return False, "User already exists"
        else:
            return False, f"MLflow error: {response.text}"
    except Exception as e:
        return False, f"Create user error: {str(e)}"

def create_mlflow_workspace(workspace_name):
    """Create a new MLflow workspace"""
    try:
        auth = HTTPBasicAuth(MLFLOW_ADMIN_USER, MLFLOW_ADMIN_PASSWORD)
        response = requests.post(
            f"{MLFLOW_SERVER_URL}/api/3.0/mlflow/workspaces",
            auth=auth,
            json={"name": workspace_name},
            timeout=10
        )
        
        if response.status_code == 200:
            return True, "Workspace created successfully"
        elif response.status_code == 400:
            return False, f"Workspace creation failed: {response.text}"
        else:
            return False, f"MLflow error: {response.text}"
    except Exception as e:
        return False, f"Create workspace error: {str(e)}"

def grant_workspace_permissions(workspace_name, username):
    """Grant MANAGE permissions to user on workspace"""
    try:
        auth = HTTPBasicAuth(MLFLOW_ADMIN_USER, MLFLOW_ADMIN_PASSWORD)
        response = requests.post(
            f"{MLFLOW_SERVER_URL}/api/3.0/mlflow/workspaces/{workspace_name}/permissions",
            auth=auth,
            json={"username": username, "permission": "MANAGE"},
            timeout=10
        )
        
        if response.status_code == 200:
            return True, "Permissions granted successfully"
        else:
            return False, f"Permission error: {response.text}"
    except Exception as e:
        return False, f"Grant permission error: {str(e)}"

# ============================================
# MAIN AZURE FUNCTION
# ============================================

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Main Azure Function to handle MLflow user provisioning
    
    Expected POST body:
    {
        "email": "user@example.com",
        "service": "mlflow"
    }
    """
    
    # Validate configuration
    if not all([MLFLOW_SERVER_URL, MLFLOW_ADMIN_USER, MLFLOW_ADMIN_PASSWORD, 
                NAMECHEAP_EMAIL, NAMECHEAP_PASSWORD]):
        return func.HttpResponse(
            json.dumps({
                "success": False,
                "message": "Server configuration incomplete. Contact administrator."
            }),
            status_code=500,
            mimetype="application/json"
        )
    
    try:
        # Parse request
        req_body = req.get_json()
        user_email = req_body.get("email")
        service = req_body.get("service", "mlflow")
        
        # Validate input
        if not user_email:
            return func.HttpResponse(
                json.dumps({"success": False, "message": "Email is required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        if service != "mlflow":
            return func.HttpResponse(
                json.dumps({"success": False, "message": f"Service '{service}' not supported"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Generate credentials
        username = extract_username_from_email(user_email)
        password = generate_password()
        workspace_name = f"ws-{username}"  # Use hyphen, not underscore (MLflow requirement)
        
        # Step 1: Create user
        success, message = create_mlflow_user(username, password)
        if not success:
            return func.HttpResponse(
                json.dumps({"success": False, "message": message}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Step 2: Create workspace
        success, message = create_mlflow_workspace(workspace_name)
        if not success:
            return func.HttpResponse(
                json.dumps({"success": False, "message": message}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Step 3: Grant permissions
        success, message = grant_workspace_permissions(workspace_name, username)
        if not success:
            return func.HttpResponse(
                json.dumps({"success": False, "message": message}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Step 4: Send email
        success, message = send_email(user_email, username, password, workspace_name)
        if not success:
            return func.HttpResponse(
                json.dumps({
                    "success": True,
                    "message": f"Account created but email delivery failed. {message}"
                }),
                status_code=200,
                mimetype="application/json"
            )
        
        # Success
        return func.HttpResponse(
            json.dumps({
                "success": True,
                "message": "MLflow account created successfully. Credentials sent to email.",
                "data": {
                    "username": username,
                    "workspace": workspace_name,
                    "email": user_email
                }
            }),
            status_code=200,
            mimetype="application/json"
        )
        
    except ValueError as e:
        return func.HttpResponse(
            json.dumps({"success": False, "message": f"Invalid request: {str(e)}"}),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"success": False, "message": f"Server error: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )