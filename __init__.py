from . import resources

from flask import Blueprint
from zou.app.utils.api import configure_api_from_blueprint


from flask import send_from_directory, abort, current_app
from flask_restful import Resource
from pathlib import Path
import os


class StaticResource(Resource):
    def get(self, filename):
        """
        Serve static files
        ---
        tags:
          - Static
        parameters:
          - in: path
            name: filename
            required: true
            schema:
              type: string
            description: Name of the file to serve
        responses:
          200:
            description: File served successfully
          404:
            description: File not found
        """
        print(filename)
        static_folder = Path(
            current_app.config.get("PLUGIN_FOLDER", "plugins")
        )
        file_path = (
            static_folder
            / manifest["id"]
            / "frontend"
            / "project"
            / "dist"
            / filename
        )

        try:
            file_path.resolve().relative_to(static_folder.resolve())
        except ValueError:
            abort(404)

        if not file_path.exists() or not file_path.is_file():
            abort(404)

        return send_from_directory(
            str(static_folder),
            filename,
            conditional=True,
            max_age=3600,  # Cache for 1 hour
        )


routes = [
    (f"/tickets", resources.Tickets),
    (f"/frontend/project/<path:filename>", StaticResource),
]


def pre_install(manifest):
    """
    Pre install the plugin.
    """


def post_install(manifest):
    """
    Post install the plugin.
    """


def pre_uninstall(manifest):
    """
    Pre uninstall the plugin.
    """


def post_uninstall(manifest):
    """
    Post uninstall the plugin.
    """
