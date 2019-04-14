import views


def setup_routes(app):
    app.router.add_get(r'/health', views.health_view)
    app.router.add_post(r'/speech', views.recognize_speech)
