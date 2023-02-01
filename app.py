import os
from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS, cross_origin


from resources.user import UserResource, UserListResource,MeResource, UserRecipeListResource, UserActivateResource, UserAvatarUploadResource, config
from resources.token import TokenResource, RefreshResource, RevokeResource, black_list
from resources.recipe import RecipeListResource,RecipePublishResource, RecipeResource, RecipeCoverUploadResource

from config import Config
from extensions import db, jwt, image_set, cache, limiter
from flask_uploads import  configure_uploads


def create_app():
    # get the configurations dynamically
    env = os.environ.get('ENV', 'Development')
    if env == 'Production':
        config_str = 'config.ProductionConfig'
    elif env == 'Staging':
        config_str = 'config.StagingConfig'
    else:
        config_str = 'config.DevelopmentConfig'

    app = Flask(__name__)
    app.config.from_object(config_str)
    register_extensions(app)
    register_resources(app)
    return app

def show_swagger_ui(app):
    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.yaml"
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config= {
            'appname': "Smilecook API"
            }
        )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix = SWAGGER_URL)
    

def register_extensions(app):
    """ Method to register the instances of the used Flask extensions """
    jwt.init_app(app)    
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    # Upload set's configuration to be stored in the app
    configure_uploads(app, image_set)
    # Settings for the maximum file size for uploads as 10 MB
    # Note: by default there is no upload size limit
    # flask.MAX_CONTENT_LENGHT(app, 10 * 1024 * 1024)
    app.config['MAX_CONTENT_LENGHT'] = 10 * 1024 * 1024
    cache.init_app(app)
    limiter.init_app(app)


    
    @jwt.token_in_blocklist_loader
    def check_igf_token_in_blocklist(self,decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list
    
    @limiter.request_filter
    def ip_whitelist():
        """ A  IP whitelist which allows certain IP addresses to use the API without any rate limit"""
        return request.remote_addr == '127.0.0.1'

    # only for testing purposes (cache functionality)
    # @app.before_request
    # def before_request():
    #     print('\n==================== BEFORE REQUEST ==================== ')
    #     print(cache.cache._cache.keys())
    #     print('\n======================================== \n')
    
    # @app.after_request 
    # def after_request(response):
    #     print('\n====================  AFTER REQUEST ==================== \n')
    #     # shows the data in the cache so we can check the key-value stored inside it
    #     print(cache.cache._cache.keys())
    #     print('\n======================================== \n')
    #     return response



def register_resources(app):
    api = Api(app)
    # Adding resource routing
    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')
    api.add_resource(RecipeCoverUploadResource, '/recipes/<int:recipe_id>/cover')

    api.add_resource(UserListResource, '/users')
    api.add_resource(TokenResource, '/token')
    api.add_resource(MeResource, '/me')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')

    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(UserRecipeListResource, '/users/<string:username>/recipes')
    api.add_resource(UserActivateResource, '/users/activate/<string:token>')
    api.add_resource(UserAvatarUploadResource, '/users/avatar')



app = create_app()
cors = CORS(app)
show_swagger_ui(app)

if __name__ == "__main__":
    config()
    app.run()

