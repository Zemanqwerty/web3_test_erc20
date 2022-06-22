from importlib.resources import path
from unicodedata import name
from app.test_app import views

# URL paths
def setup_routes(app):
    # ----------STATIC FILES----------
    app.router.add_static('/js/', path='static/scripts', name='js')
    app.router.add_static('/css/', path='static/css', name='css')
    app.router.add_static('/img/', path='static/img', name='img')

    app.router.add_static('/admin/admin_js/', path='static/scripts/admin_scripts', name='admin_js')
    app.router.add_static('/admin/admin_css/', path='static/css/admin_css', name='admin_css')

    # ----------BACKEND FUNCTIONS----------
    app.router.add_post('/api/authorization', views.api_authorization)
    app.router.add_post('/api/registration', views.api_registration)
    app.router.add_get('/api/logout', views.api_logout)
    app.router.add_post('/api/create_new_project', views.api_create_new_project)
    app.router.add_post('/api/create_new_transaction', views.api_create_new_transaction)
    app.router.add_post('/admin/to_consider_project', views.to_consider)
    app.router.add_post('/admin/to_finish', views.to_finish)
    app.router.add_post('/admin/send_transaction_to_user', views.send_transaction_to_user)

    # ----------CLIENT USERS FUNCTIONS----------
    app.router.add_get('/create_new_account', views.registration_page)
    app.router.add_get('/autz', views.authorization_page, name='autz')
    app.router.add_get('/', views.main_page, name='main')
    app.router.add_get('/account', views.account_page)
    app.router.add_get('/create_new_project', views.create_new_project)
    app.router.add_get('/{project_name}', views.cur_project)
    
    # ----------CLIENT ADMINS FUNCTIONS----------
    app.router.add_get('/admin/main_page', views.main_admin_page, name='main_admin')
    app.router.add_get('/admin/acive_project_page', views.acive_project_page, name='active_admin')
    app.router.add_get('/admin/send_tocens', views.send_tocken_page)
    