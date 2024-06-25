import os

from .app import App
from .common import check_python_installation


def get_app_instance(
    exec_dir: str = os.path.abspath(__file__),
    open_path: str = None,
) -> App:
    """Get an instance of the application.

    Args:
        exec_dir (str, optional): The directory of the executable. Defaults to os.path.dirname(os.path.abspath(__file__)).
        open_path (str, optional): The path to open. Defaults to None.

    Returns:
        App: An instance of the application."""

    check_python_installation()
    return App(exec_dir, dir=open_path)
