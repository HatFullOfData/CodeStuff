#!/usr/bin/env python
# coding: utf-8

# ## Notebook 2
# 
# New notebook

# # SharePoint Excel File
# 
# Goal of this notebook is to get data from an Excel file stored in SharePoint. The file, products.xlsx, is stored in the Documents library. The table of data is on the Products sheet and starts in A1.
# 
# A service principal has been set up with Sites Selected permission for the site. The secret for that service principal is stored in Azure Key Vault.
# 
# ## Steps
# 1. Get Secret from Azure Key Vault
# 1. Get Access token from Microsoft Graph
# 1. Get Site_ID and Drive_ID
# 1. Get download url for file and download
# 1. Extract data using pandas
# 
# 

# ### Prep - Import Libraries

# In[1]:


import requests
from pandas import read_excel
from pyspark.sql.functions import col
from io import BytesIO


# ### Prep - Variables / Parameters

# In[2]:


sharepoint_domain = "YOURDOMAIN.sharepoint.com"
site_name = "SITE"
library_name = "LIBRARY"
file_name = "FILE.xlsx"
sheet_name = "SHEET"


# ### Step 1 - Get Secret from Azure Key Vault

# In[ ]:


# Authentication details
tenant_id = "TENANT ID"
client_id = "CLIENT ID"
azure_key_vault_name = "VAULT NAME"
azure_key_vault_secret_name = "SECRET NAME"


# In[3]:


# Get secret from Key Vault
azure_key_vault_url = f"https://{azure_key_vault_name}.vault.azure.net/" 
client_secret = notebookutils.credentials.getSecret(azure_key_vault_url,azure_key_vault_secret_name)
print(client_secret)


# ### Step 2 - Get Access Token from Microsoft Graph

# In[4]:


token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "https://graph.microsoft.com/.default"
}
response = requests.post(token_url, data=token_data)
response.raise_for_status()  # Raise error if request fails
access_token = response.json().get("access_token")

# Print the result
print(" Access Token Received:", access_token[:50], "...")

headers = {"Authorization": f"Bearer {access_token}"}


# ### Step 3 - Get Site ID and Drive ID

# In[5]:


site_id_url = f"https://graph.microsoft.com/v1.0/sites/{sharepoint_domain}:/sites/{site_name}"
print("Site ID URL:",site_id_url)
response = requests.get(site_id_url, headers=headers)
response.raise_for_status()  # Raise error if request fails
display(response.json())

site_id=response.json()['id']
print("Site ID:",site_id[:50], "...")


# In[6]:


drive_id_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives?$select=name,id"
response = requests.get(drive_id_url, headers=headers)
response.raise_for_status()  # Raise error if request fails
# Convert response json into a dataframe
df_drives = spark.createDataFrame(response.json()['value'])
display(df_drives)
# Filter the dataframe to the specified library and get the id
drive_id = df_drives.filter(col("name")== library_name).collect()[0]["id"]
print("Drive ID:",drive_id[:25], "...")


# ### Step 4 - Get File content

# In[8]:


# Step 3: Retrieve the File Content from SharePoint using Graph API
file_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{file_name}:/content"
print("File URL:",file_url[:75], "...")
response = requests.get(file_url, headers=headers)
response.raise_for_status()  # Raise error if request fails
display(response)
#


# ### Step 5 - Extract table using Pandas

# In[9]:


# Convert response
xls = BytesIO(response.content)

# Get data from sheet
df = read_excel(xls, sheet_name=sheet_name) 
display(df)

