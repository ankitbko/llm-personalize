# Beyond One-Size-Fits-All: Digital Twins and LLM Agents Transform Digital Interactions

This repo is proof of concept of creating a digital twin that enables LLM to personalize the response based on user's profile. The repo is a part of the blog post [Beyond One-Size-Fits-All: Digital Twins and LLM Agents Transform Digital Interactions]().

## Setup

1. Create a [Microsoft Entra ID Application](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app?tabs=certificate) with permission to call MS Graph API.
2. Create Azure OpenAI resource and deploy GPT 4 model.
3. Rename `env_template` file to `.env` and update the values as follows.
   1. CLIENT_ID: Client ID of the Entra ID Application
   2. TENANT_ID: Tenant ID of Microsoft Entra
   3. OPENAI_MODEL: Deployment name of GPT 4 model in Azure OpenAI
   4. AZURE_OPENAI_API_KEY: AOAI Key
   5. AZURE_OPENAI_ENDPOINT: AOAI Endpoint
4. Run the following commands to install the dependencies.
```bash
make install
```
5. Start the server and the client app using the following commands.
```bash
make server
make run
```

