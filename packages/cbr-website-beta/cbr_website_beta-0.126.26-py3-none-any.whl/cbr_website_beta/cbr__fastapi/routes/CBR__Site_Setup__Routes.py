from typing import Optional

from osbot_utils.utils.Env import get_env
from pydantic import BaseModel

from cbr_website_beta.config.CBR_Config import cbr_config
from cbr_website_beta.config.CBR__Site_Info import CBR__Site_Info
from cbr_website_beta.utils.performance.CBR__Health_Checks import CBR__Health_Checks
from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes
from osbot_utils.helpers.Hashicorp_Secrets import Hashicorp_Secrets

ROUTE_PATH__SITE_SETUP     = 'site_setup'
EXPECTED_SITE_SETUP_ROUTES = [ '/hcp-secrets-status', '/hcp-load-secrets']

class HCP_Config(BaseModel):
    access_token    : Optional[str] = None
    organisation_id : Optional[str] = None
    project_id      : Optional[str] = None

class CBR__Hashicorp_Secrets(Hashicorp_Secrets):
    hcp_config : HCP_Config

    def hcp__access_token(self):
        return self.hcp_config.access_token

    def hcp__organization_id(self):
        return self.hcp_config.organisation_id

    def hcp_project_id(self):
        return self.hcp_config.project_id



class CBR__Site_Setup__Routes(Fast_API_Routes):
    tag : str =  ROUTE_PATH__SITE_SETUP

    def hcp_secrets_status(self, hcp_config: HCP_Config):
        cbr_hcp_secrets = CBR__Hashicorp_Secrets(hcp_config=hcp_config)
        secrets_status = {}
        for secret_name in cbr_hcp_secrets.app_secrets_names():
            if get_env(secret_name):
                secret_status = 'OK'
            else:
                secret_status = 'Not set'

            secrets_status[secret_name] = secret_status

        return secrets_status

    def hcp_load_secrets(self, hcp_config: HCP_Config):
        return {"it's": 42}


    def setup_routes(self):
        self.add_route_post(self.hcp_secrets_status)
        self.add_route_post(self.hcp_load_secrets)