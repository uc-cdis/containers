"""
Extend the jupyter API with a ready route
https://jupyter-notebook.readthedocs.io/en/stable/extending/handlers.html
"""

from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from os.path import exists


class HelloWorldHandler(IPythonHandler):
    def get(self):
        if exists("/tmp/ready"):
            self.set_status(200)
            self.finish("Stata sessions initialized")
        else:
            self.set_status(404)
            self.finish("Stata sessions not initialized")


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/ready')
    web_app.add_handlers(host_pattern, [(route_pattern, HelloWorldHandler)])
