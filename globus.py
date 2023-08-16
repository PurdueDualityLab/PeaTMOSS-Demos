import globus_sdk
from globus_sdk.scopes import TransferScopes
import os

#PeaTMOSS Access Token
CLIENT_ID = "2e3fa2a3-c37c-46f8-a3a6-c59d145503bd"

auth_client = globus_sdk.NativeAppAuthClient(CLIENT_ID)

# requested_scopes specifies a list of scopes to request
# instead of the defaults, only request access to the Transfer API
auth_client.oauth2_start_flow(requested_scopes=TransferScopes.all)
authorize_url = auth_client.oauth2_get_authorize_url()
print(f"Please go to this URL and login:\n\n{authorize_url}\n")

auth_code = input("Please enter the code here: ").strip()
tokens = auth_client.oauth2_exchange_code_for_tokens(auth_code)
transfer_tokens = tokens.by_resource_server["transfer.api.globus.org"]

# construct an AccessTokenAuthorizer and use it to construct the
# TransferClient
transfer_client = globus_sdk.TransferClient(
    authorizer=globus_sdk.AccessTokenAuthorizer(transfer_tokens["access_token"])
)

PeaTMOSS_endpoint_id = "c4ec6812-3315-11ee-b543-e72de9e39f95"
local_endpoint = globus_sdk.LocalGlobusConnectPersonal()
# local_endpoint_id = local_endpoint.endpoint_id 

### Instead of using local_endpoint.endpoint_id, I just copy pasted my collection's UUID, as local_endpoint.endpoint_id returned None
local_endpoint_id = "e3c2efc0-3bf5-11ee-920b-5b20905a64b1"
print(local_endpoint_id)

source_endpoint_id = PeaTMOSS_endpoint_id
dest_endpoint_id = local_endpoint_id

# create a Transfer task consisting of one or more items
task_data = globus_sdk.TransferData(
    source_endpoint=source_endpoint_id,
    destination_endpoint=dest_endpoint_id
)

curr_path = os.getcwd()
print(curr_path)
### Including ./ at the beginning of the filepath indicates it is in the root
print("./PeaTMOSS_DB/")
task_data.add_item(
    "/~/Database/PeaTMOSS.db",  # source
    f"./PeaTMOSS_DB/PeaTMOSS.db",  # dest
)

# submit, getting back the task ID
task_doc = transfer_client.submit_transfer(task_data)
task_id = task_doc["task_id"]
print(f"submitted transfer, task_id={task_id}")