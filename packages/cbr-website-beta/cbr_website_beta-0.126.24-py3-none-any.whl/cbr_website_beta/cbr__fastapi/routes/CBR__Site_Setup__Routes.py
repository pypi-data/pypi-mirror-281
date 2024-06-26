from pydantic import BaseModel

from cbr_website_beta.config.CBR_Config import cbr_config
from cbr_website_beta.config.CBR__Site_Info import CBR__Site_Info
from cbr_website_beta.utils.performance.CBR__Health_Checks import CBR__Health_Checks
from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes


ROUTE_PATH__SITE_SETUP = 'site_setup'

class HCP_Secrets(BaseModel):
    access_token    : str
    organisation_id : str
    project_id      : str


class CBR__Site_Setup__Routes(Fast_API_Routes):
    tag : str =  ROUTE_PATH__SITE_SETUP

    def hcp_list_secrets_names(self, cbr_secrets_setup: HCP_Secrets):
        return {'will': 'go here'}

    def hcp_load_secrets(self, cbr_secrets_setup: HCP_Secrets):
        return {"it's": 42}


    def setup_routes(self):
        self.add_route_post(self.hcp_list_secrets_names)
        self.add_route_post(self.hcp_load_secrets)