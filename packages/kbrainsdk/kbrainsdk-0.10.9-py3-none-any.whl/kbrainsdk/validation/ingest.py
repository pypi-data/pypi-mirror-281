from kbrainsdk.validation.common import get_payload, validate_email
def validate_ingest_onedrive(req):
    body = get_payload(req)
    email = body.get('email')
    token = body.get('token')
    environment = body.get('environment')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')

    # Validate parameters
    if not all([email, token, environment, client_id, oauth_secret, tenant_id]):
        raise ValueError("Missing or empty parameter in request body. Requires: email, token, environment, client_id, oauth_secret, tenant_id")
    
    if not validate_email(email):
        raise ValueError("Invalid email address")
    
    return email, token, environment, client_id, oauth_secret, tenant_id

def validate_ingest_sharepoint(req):
    body = get_payload(req)
    host = body.get('host')
    site = body.get('site')
    token = body.get('token')
    environment = body.get('environment')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')

    # Validate parameters
    if not all([host, site, token, environment, client_id, oauth_secret, tenant_id]):
        raise ValueError("Missing or empty parameter in request body. Requires: host, site, token, environment, client_id, oauth_secret, tenant_id")
    
    return host, site, token, environment, client_id, oauth_secret, tenant_id

def validate_ingest_rfp_responses(req):
    body = get_payload(req)
    proposal_id = body.get('proposal_id')
    email = body.get('email')
    assertion_token = body.get('token')
    environment = body.get('environment')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')
    datasets = body.get('datasets', [])

    # Validate parameters
    if not all([proposal_id, email, assertion_token, environment, client_id, oauth_secret, tenant_id]):
        raise ValueError("Missing or empty parameter in request body. Requires: proposal_id, email, token, environment, client_id, oauth_secret, tenant_id")
    
    if not validate_email(email):
        raise ValueError("Invalid email address")
    
        
    return proposal_id, email, assertion_token, environment, client_id, oauth_secret, tenant_id, datasets

def validate_ingest_status(req):
    body = get_payload(req)
    datasource = body.get('datasource')

    # Validate parameters
    if not all([datasource]):
        raise ValueError("Missing or empty parameter \"datasource\" in request body")
    
    return datasource

def validate_ingest_pipeline_status(req):
    body = get_payload(req)
    run_id = body.get('run_id')

    # Validate parameters
    if not all([run_id]):
        raise ValueError("Missing or empty parameter \"run_id\" in request body")
    
    return run_id