import main
import a2wsgi
application = a2wsgi.ASGIMiddleware(main.app)