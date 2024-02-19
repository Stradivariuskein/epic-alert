from distutils.core import setup
import py2exe


from distutils.core import setup

setup(
      console=[{
        "script": "main.py",
        "icon_resources": [(1, "icon.png")]
      }]
      name='root',
      version='1.0',
      description='Root package',
      author='Alan Luque',
      author_email='luquealanbri@gmai.com',
      url='https://portafolio-boua.onrender.com/',
      packages=['auto_buy_game', 'file_manager', 'main_tray_icon', 'main_window', 'notification_windows', 'ui_app_dialog'],
      package_dir={
           "auto_buy_game": "auto_buy_game.py",
            "file_manager": "file_manager.py",
            "main_tray_icon": "main_tray_icon.py",
            "main_window": "main_window.py",
            "notification_windows": "notification_windows.py",
            "ui_app_dialog": "ui_app_dialog.py"
      },
)