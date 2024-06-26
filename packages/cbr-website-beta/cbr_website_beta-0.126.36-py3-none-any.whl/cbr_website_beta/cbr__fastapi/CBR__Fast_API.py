import cbr_static
from starlette.responses                                            import RedirectResponse, FileResponse
from starlette.staticfiles                                          import StaticFiles
from cbr_athena.athena__fastapi.FastAPI_Athena                      import FastAPI_Athena

from cbr_website_beta.cbr__fastapi.routes.CBR__Site_Info__Routes    import CBR__Site_Info__Routes
from cbr_website_beta.cbr__fastapi.routes.CBR__Site_Setup__Routes   import CBR__Site_Setup__Routes
from cbr_website_beta.config.CBR_Config                             import cbr_config
from cbr_website_beta.cbr__flask.Flask_Site                         import Flask_Site
from osbot_fast_api.api.Fast_API                                    import Fast_API
from osbot_utils.utils.Files                                        import path_combine


class CBR__Fast_API(Fast_API):

    def add_athena(self):
        cbr_athena_app = self.cbr_athena().app()
        self.app().mount("/api", cbr_athena_app)

    def add_static_routes(self):
        assets_path = path_combine(cbr_static.path, 'assets')
        self.app().mount("/assets", StaticFiles(directory=assets_path, html=True), name="assets")
        return self

    def add_flask__cbr_website(self):
        flask_site = self.cbr_apps__flask_site()
        flask_app  = flask_site.app()
        path       = '/'
        self.add_flask_app(path, flask_app)
        return self

    def cbr_athena(self):
        return FastAPI_Athena().setup()

    def cbr_apps__flask_site(self):
        return Flask_Site()

    def cbr_config(self):
        return cbr_config

    def setup(self):
        self.setup_server()
        super().setup()
        self.add_athena            ()
        self.add_static_routes     ()
        self.add_flask__cbr_website()
        return self

    def setup_routes(self):
        self.add_routes(CBR__Site_Info__Routes)
        self.add_routes(CBR__Site_Setup__Routes)

    def setup_add_root_route(self):
        app = self.app()

        @app.get("/")                                # todo: move this to a separate method
        def read_root():
            return RedirectResponse(url="/web/home")

        @app.get('/favicon.ico')                    # todo: convert the png below to .ico file (also see what are the side effects of returning a png instead of an ico)
        def favicon_ico():
            file_path = path_combine(cbr_static.path, "/assets/cbr/tcb-favicon.png")
            return FileResponse(file_path, media_type="image/png")

    def setup_server(self):
        print()
        print("####### Setting up AWS QA Server #######")
        print("#######")
        try:
            import boto3
            from osbot_utils.utils.Env import load_dotenv
            from osbot_utils.utils.Files import file_exists
            from osbot_utils.utils.Files import file_contents
            session = boto3.Session()
            s3_client = session.client('s3')
            s3_bucket = '654654216424--cbr-deploy--eu-west-1'
            s3_key = 'cbr-custom-websites/dotenv_files/cbr-site-live-qa.env'
            local_dotenv = '/tmp/cbr-site-live-qa.env'
            s3_client.download_file(s3_bucket, s3_key, local_dotenv)
            if file_exists(local_dotenv):
                load_dotenv(local_dotenv)
                print("####### OK: Dotenv file loaded from S3")
            else:
                print("####### Warning: Dotenv file NOT loaded from S3")
        except Exception as error:
            print(f"####### Warning: Dotenv file NOT loaded from S3: {error}")
        print("#######")
        print("####### Setting up AWS QA Server #######")
        print()