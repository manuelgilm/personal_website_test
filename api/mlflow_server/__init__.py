import azure.functions as func
from typing import Optional
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

def generate_password(length:int=16) -> str:
    """
    Generate a random secure password
    
    :param length: Length of the password to generate
    :return: Randomly generated password string
    """
    characters = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(random.choice(characters) for _ in range(length))

def extract_username_from_email(email:str) -> str:
    """
    Extract username from email address (john@example.com -> john)
    
    :param email: Email address to extract the username from
    :return: Sanitized username string
    """
    username = email.split("@")[0].lower()
    # MLflow allows: lowercase alphanumeric and hyphens only
    username = username.replace(".", "-").replace("_", "-")
    # Remove any double hyphens
    while "--" in username:
        username = username.replace("--", "-")
    username = username.strip("-")
    return username

def send_email(user_email: str, username: str, password: str, workspace_name: str) -> tuple[bool, str]:
    """
    Send credentials email via Namecheap SMTP

    :param user_email: Recipient email address
    :param username: MLflow username to include in the email
    :param password: Generated password to include in the email
    :param workspace_name: MLflow workspace name to include in the email
    :return: Tuple of (success flag, status message)
    """
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

def create_mlflow_user(username: str, password: str) -> tuple[bool, str]:
    """
    Create a new MLflow user via the MLflow API

    :param username: Username for the new MLflow user
    :param password: Password for the new MLflow user
    :return: Tuple of (success flag, status message)
    """
    try:
        auth = HTTPBasicAuth(MLFLOW_ADMIN_USER, MLFLOW_ADMIN_PASSWORD)
        response = requests.post(
            f"{MLFLOW_SERVER_URL}/api/2.0/mlflow/users/create",
            auth=auth,
            json={"username": username, "password": password},
            timeout=10
        )
        
        # Accept both 200 and 201 as success (201 = Created)
        if response.status_code in [200, 201]:
            return True, "User created successfully"
        elif response.status_code == 400 and "already exists" in response.text:
            return False, "User already exists"
        else:
            return False, f"MLflow error: {response.text}"
    except Exception as e:
        return False, f"Create user error: {str(e)}"

def create_mlflow_workspace(workspace_name: str) -> tuple[bool, str]:
    """
    Create a new MLflow workspace via the MLflow API

    :param workspace_name: Name of the workspace to create
    :return: Tuple of (success flag, status message)
    """
    try:
        auth = HTTPBasicAuth(MLFLOW_ADMIN_USER, MLFLOW_ADMIN_PASSWORD)
        response = requests.post(
            f"{MLFLOW_SERVER_URL}/api/3.0/mlflow/workspaces",
            auth=auth,
            json={"name": workspace_name},
            timeout=10
        )
        
        # Accept both 200 and 201 as success (201 = Created)
        if response.status_code in [200, 201]:
            return True, "Workspace created successfully"
        elif response.status_code == 400:
            return False, f"Workspace creation failed: {response.text}"
        else:
            return False, f"MLflow error: {response.text}"
    except Exception as e:
        return False, f"Create workspace error: {str(e)}"

def grant_workspace_permissions(workspace_name: str, username: str) -> tuple[bool, str]:
    """
    Grant MANAGE permissions to a user on an MLflow workspace

    :param workspace_name: Name of the workspace to grant permissions on
    :param username: Username to grant MANAGE permissions to
    :return: Tuple of (success flag, status message)
    """
    try:
        auth = HTTPBasicAuth(MLFLOW_ADMIN_USER, MLFLOW_ADMIN_PASSWORD)
        response = requests.post(
            f"{MLFLOW_SERVER_URL}/api/3.0/mlflow/workspaces/{workspace_name}/permissions",
            auth=auth,
            json={"username": username, "permission": "MANAGE"},
            timeout=10
        )
        
        # Accept both 200 and 201 as success (201 = Created)
        if response.status_code in [200, 201]:
            return True, "Permissions granted successfully"
        else:
            return False, f"Permission error: {response.text}"
    except Exception as e:
        return False, f"Grant permission error: {str(e)}"

# ============================================
# HELPERS
# ============================================

def _error_response(message: str, status: int = 400) -> func.HttpResponse:
    """Create a JSON error response

    :param message: Error message
    :param status: HTTP status code (default 400)
    :return: HTTP response with JSON error body
    """
    return func.HttpResponse(
        json.dumps({"success": False, "message": message}),
        status_code=status,
        mimetype="application/json"
    )

def _validate_config() -> Optional[func.HttpResponse]:
    """Validate that all required environment variables are set

    :return: Error HTTP response if config is incomplete, None otherwise
    """
    if not all([MLFLOW_SERVER_URL, MLFLOW_ADMIN_USER, MLFLOW_ADMIN_PASSWORD,
                NAMECHEAP_EMAIL, NAMECHEAP_PASSWORD]):
        return _error_response(
            "Server configuration incomplete. Contact administrator.",
            status=500
        )
    return None

def _provision_mlflow(user_email: str) -> tuple[bool, str, dict | None]:
    """Execute the full MLflow provisioning workflow

    :param user_email: Email address of the user to provision
    :return: Tuple of (success flag, status message, optional data dict)
    """
    username = extract_username_from_email(user_email)
    password = generate_password()
    workspace_name = f"ws-{username}"

    provision_steps = [
        (create_mlflow_user, (username, password), False),
        (create_mlflow_workspace, (workspace_name,), False),
        (grant_workspace_permissions, (workspace_name, username), False),
        (send_email, (user_email, username, password, workspace_name), True),
    ]

    for step_func, step_args, soft_failure in provision_steps:
        success, message = step_func(*step_args)
        if not success:
            if soft_failure:
                return True, f"Account created but email delivery failed. {message}", {
                    "username": username, "workspace": workspace_name, "email": user_email
                }
            return False, message, None

    return True, "MLflow account created successfully. Credentials sent to email.", {
        "username": username, "workspace": workspace_name, "email": user_email
    }

# ============================================
# MAIN AZURE FUNCTION
# ============================================

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Handle MLflow user provisioning requests via Azure Functions

    :param req: HTTP request with JSON body containing "email" and "service" fields
    :return: HTTP response with JSON body containing success status and message
    :raises ValueError: If the request body is not valid JSON
    """
    config_error = _validate_config()
    if config_error:
        return config_error

    try:
        req_body = req.get_json()
        user_email = req_body.get("email")
        service = req_body.get("service", "mlflow")

        if not user_email:
            return _error_response("Email is required")
        if service != "mlflow":
            return _error_response(f"Service '{service}' not supported")

        success, message, data = _provision_mlflow(user_email)
        body = {"success": success, "message": message}
        if data:
            body["data"] = data
        return func.HttpResponse(
            json.dumps(body),
            status_code=200 if success else 400,
            mimetype="application/json"
        )
    except ValueError as e:
        return _error_response(f"Invalid request: {str(e)}")
    except Exception as e:
        return _error_response(f"Server error: {str(e)}", status=500)