from cbr_website_beta.config.CBR_Config import cbr_config
from cbr_website_beta.config.CBR__Site_Info import CBR__Site_Info, cbr_site_info
from cbr_website_beta.utils.performance.CBR__Health_Checks import CBR__Health_Checks, cbr_health_checks
from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes

ROUTE_PATH__SITE_INFO     = 'site_info'
EXPECTED_SITE_INFO_ROUTES = ['/cbr-config', '/cbr-site-info', '/health-checks']

class CBR__Site_Info__Routes(Fast_API_Routes):

    tag : str = ROUTE_PATH__SITE_INFO

    def cbr_config(self):
        return cbr_config.config()

    def cbr_site_info(self):
        return cbr_site_info.data()

    def health_checks(self):
        return cbr_health_checks.execute_health_checks()


    def setup_routes(self):
        self.add_route_get(self.cbr_config)
        self.add_route_get(self.cbr_site_info)
        self.add_route_get(self.health_checks)