from ..functions.api_request import api_request

async def create_bill(client_yaya_account, customer_yaya_account, amount, start_at, due_at, customer_id, bill_id, fwd_institution, fwd_account_number, description, phone, email, details):
  payload = {
    "client_yaya_account": client_yaya_account,
    "amount": amount,
    "due_at": due_at,
    "customer_id": customer_id,
    "bill_id": bill_id,
  }

  if customer_yaya_account is not None:
    payload["customer_yaya_account"] = customer_yaya_account
  if start_at is not None:
    payload["start_at"] = start_at
  if fwd_institution is not None:
    payload["fwd_institution"] = fwd_institution
  if fwd_account_number is not None:
    payload["fwd_account_number"] = fwd_account_number
  if description is not None:
    payload["description"] = description
  if phone is not None:
    payload["phone"] = phone
  if email is not None:
    payload["email"] = email
  if details is not None:
    payload["details"] = details

  api_response = await api_request("POST", "/bill/create", "", payload)
  return api_response

async def create_bulk_bill(bulkBill):
  api_response = await api_request("POST", "/bulkimport/bills", "", bulkBill)
  return api_response

async def bulk_bill_status(client_yaya_account):
  api_response = await api_request("GET", "/bulkimport/", {"client_yaya_account": client_yaya_account})
  return api_response

async def update_bill(client_yaya_account, amount, customer_id, bill_id, customer_yaya_account, phone, email):
  payload = {
    "client_yaya_account": client_yaya_account,
    "amount": amount,
    "customer_id": customer_id,
    "bill_id": bill_id,
  }

  if customer_yaya_account is not None:
    payload["customer_yaya_account"] = customer_yaya_account
  if phone is not None:
    payload["phone"] = phone
  if email is not None:
    payload["email"] = email
  api_response = await api_request("POST", "/bill/update ", "", payload)
  return api_response