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
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

READERS_ROLE_NAME = "readers"
ROLE_RESOURCES = [
    'experiment',
    'gateway_endpoint',
    'gateway_model_definition',
    'gateway_secret',
    'prompt',
    'registered_model',
    'scorer',
]
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

def send_email(user_email: str, username: str, password: str) -> tuple[bool, str]:
    """
    Send credentials email via Namecheap SMTP

    :param user_email: Recipient email address
    :param username: MLflow username to include in the email
    :param password: Generated password to include in the email
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

def send_admin_notification(user_email: str, username: str, password: str) -> tuple[bool, str]:
    """
    Send admin notification email with new user credentials via Namecheap SMTP

    :param user_email: Email address of the newly created user
    :param username: MLflow username of the new user
    :param password: Generated password of the new user
    :return: Tuple of (success flag, status message)
    """
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "New MLflow User Created"
        msg["From"] = FROM_EMAIL
        msg["To"] = ADMIN_EMAIL

        text = f"""
A new MLflow user account has been created:

- Email: {user_email}
- Username: {username}
- Password: {password}
- Role: {READERS_ROLE_NAME}
- MLflow Server: {MLFLOW_SERVER_URL}

Best regards,
AI Room Team
        """

        html = f"""\
<html>
  <body style="font-family: Arial, sans-serif;">
    <h2>New MLflow User Created</h2>
    <p>A new MLflow user account has been created. Here are the details:</p>

    <table style="border: 1px solid #ddd; padding: 10px; margin: 20px 0;">
      <tr>
        <td style="font-weight: bold; width: 150px;">Email:</td>
        <td><code>{user_email}</code></td>
      </tr>
      <tr>
        <td style="font-weight: bold;">Username:</td>
        <td><code>{username}</code></td>
      </tr>
      <tr>
        <td style="font-weight: bold;">Password:</td>
        <td><code>{password}</code></td>
      </tr>
      <tr>
        <td style="font-weight: bold;">Role:</td>
        <td><code>{READERS_ROLE_NAME}</code></td>
      </tr>
      <tr>
        <td style="font-weight: bold;">Server:</td>
        <td><a href="{MLFLOW_SERVER_URL}">{MLFLOW_SERVER_URL}</a></td>
      </tr>
    </table>

    <p style="color: #666; font-size: 12px; margin-top: 30px;">
      Best regards,<br>
      AI Room Team
    </p>
  </body>
</html>
        """

        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(NAMECHEAP_SMTP_SERVER, NAMECHEAP_SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(NAMECHEAP_EMAIL, NAMECHEAP_PASSWORD)
            server.sendmail(FROM_EMAIL, ADMIN_EMAIL, msg.as_string())

        return True, "Admin notification sent successfully"
    except Exception as e:
        return False, f"Admin notification error: {str(e)}"

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

def get_mlflow_role(role_name: str) -> tuple[bool, int | None, str]:
    """
    Get an MLflow role by name via the MLflow API

    :param role_name: Name of the role to look up
    :return: Tuple of (success flag, role_id or None, status message)
    """
    try:
        auth = HTTPBasicAuth(MLFLOW_ADMIN_USER, MLFLOW_ADMIN_PASSWORD)
        response = requests.get(
            f"{MLFLOW_SERVER_URL}/api/3.0/mlflow/roles/list",
            auth=auth,
            timeout=10
        )
        if response.status_code == 200:
            for role in response.json().get("roles", []):
                if role.get("name") == role_name:
                    return True, int(role["id"]), "Role found"
            return False, None, f"Role '{role_name}' not found"
        return False, None, f"MLflow error: {response.text}"
    except Exception as e:
        return False, None, f"Get role error: {str(e)}"

def create_mlflow_role(role_name: str) -> tuple[bool, int, str]:
    """
    Create a new MLflow role via the MLflow API

    :param role_name: Name of the role to create
    :return: Tuple of (success flag, role_id, status message)
    """
    try:
        auth = HTTPBasicAuth(MLFLOW_ADMIN_USER, MLFLOW_ADMIN_PASSWORD)
        response = requests.post(
            f"{MLFLOW_SERVER_URL}/api/3.0/mlflow/roles/create",
            auth=auth,
            json={"workspace": "default", "name": role_name},
            timeout=10
        )
        if response.status_code in [200, 201]:
            role_id = int(response.json().get("role", {}).get("id"))
            return True, role_id, "Role created successfully"
        return False, 0, f"MLflow error: {response.text}"
    except Exception as e:
        return False, 0, f"Create role error: {str(e)}"

def add_role_permissions(role_id: int) -> tuple[bool, str]:
    """
    Grant READ permission to a role on all resource types via the MLflow API

    :param role_id: ID of the role to add permissions to
    :return: Tuple of (success flag, status message)
    """
    auth = HTTPBasicAuth(MLFLOW_ADMIN_USER, MLFLOW_ADMIN_PASSWORD)
    for resource_type in ROLE_RESOURCES:
        try:
            response = requests.post(
                f"{MLFLOW_SERVER_URL}/api/3.0/mlflow/roles/permissions/add",
                auth=auth,
                json={
                    "role_id": str(role_id),
                    "resource_type": resource_type,
                    "permission": "READ",
                    "resource_pattern": "*",
                },
                timeout=10
            )
            if response.status_code not in [200, 201]:
                return False, f"Permission error on '{resource_type}': {response.text}"
        except Exception as e:
            return False, f"Add permission error on '{resource_type}': {str(e)}"
    return True, "Role permissions granted successfully"

def assign_role_to_user(username: str, role_id: int) -> tuple[bool, str]:
    """
    Assign an MLflow role to a user via the MLflow API

    :param username: Username to assign the role to
    :param role_id: ID of the role to assign
    :return: Tuple of (success flag, status message)
    """
    try:
        auth = HTTPBasicAuth(MLFLOW_ADMIN_USER, MLFLOW_ADMIN_PASSWORD)
        response = requests.post(
            f"{MLFLOW_SERVER_URL}/api/3.0/mlflow/roles/assign",
            auth=auth,
            json={"username": username, "role_id": role_id},
            timeout=10
        )
        if response.status_code in [200, 201]:
            return True, "Role assigned successfully"
        return False, f"MLflow error: {response.text}"
    except Exception as e:
        return False, f"Assign role error: {str(e)}"

def ensure_readers_role() -> tuple[bool, int, str]:
    """
    Ensure the readers role exists, creating it with permissions if needed

    :return: Tuple of (success flag, role_id, status message)
    """
    success, role_id, message = get_mlflow_role(READERS_ROLE_NAME)
    if success:
        return True, role_id, "Readers role already exists"

    success, role_id, message = create_mlflow_role(READERS_ROLE_NAME)
    if not success:
        return False, 0, message

    success, message = add_role_permissions(role_id)
    if not success:
        return False, 0, message

    return True, role_id, "Readers role created with permissions"

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
                NAMECHEAP_EMAIL, NAMECHEAP_PASSWORD, ADMIN_EMAIL]):
        return _error_response(
            "Server configuration incomplete. Contact administrator.",
            status=500
        )
    return None

def _provision_mlflow(user_email: str) -> tuple[bool, str, Optional[dict]]:
    """Execute the full MLflow provisioning workflow

    :param user_email: Email address of the user to provision
    :return: Tuple of (success flag, status message, optional data dict)
    """
    username = extract_username_from_email(user_email)
    password = generate_password()

    success, message = create_mlflow_user(username, password)
    if not success:
        return False, message, None

    success, role_id, message = ensure_readers_role()
    if not success:
        return False, message, None

    provision_steps = [
        (assign_role_to_user, (username, role_id), False),
        (send_email, (user_email, username, password), True),
        (send_admin_notification, (user_email, username, password), True),
    ]

    for step_func, step_args, soft_failure in provision_steps:
        success, message = step_func(*step_args)
        if not success:
            if soft_failure:
                return True, f"Account created but email delivery failed. {message}", {
                    "username": username, "role": READERS_ROLE_NAME, "email": user_email
                }
            return False, message, None

    return True, "MLflow account created successfully. Credentials sent to email.", {
        "username": username, "role": READERS_ROLE_NAME, "email": user_email
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