from . import resources

routes = [
    (f"/tickets", resources.TicketsResource),
    (f"/tickets/<id>", resources.TicketResource),
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
