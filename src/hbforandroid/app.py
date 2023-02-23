b"""
Package manager for Android.
"""
import toga
from toga.style import Pack
from toga.fonts import Font, SANS_SERIF
from toga.style.pack import CENTER, COLUMN, ROW
import requests
import os


class Homebrew(toga.App):
    self_ = None
    console_input = None
    main_window_ = None
    default_repo = 'http://repo.example.com'

    def startup(self):

        # passing down the self variable
        Homebrew.self_ = self
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        main_box = toga.Box(style=Pack(direction=COLUMN))
        main_box.style.update(alignment=CENTER)

        banner_box = toga.Box(style=Pack(direction=COLUMN))
        banner_box.style.update(alignment=CENTER)

        # thanks to: https://github.com/beeware/toga/blob/main/examples/imageview/imageview/app.py
        image_from_path = toga.Image("resources/banner.png")
        imageview_from_path = toga.ImageView(image_from_path)
        imageview_from_path.style.update(height=128)
        banner_box.add(imageview_from_path)

        # adding the top image thing
        main_box.add(imageview_from_path)

        console_box = toga.Box(style=Pack(direction=COLUMN))
        Homebrew.console_input = toga.TextInput(
            placeholder='Package to install')
        console_installbtn = toga.Button(
            'Install Package', on_press=Homebrew.installpkg)

        console_box.add(Homebrew.console_input)
        console_box.add(console_installbtn)

        # adding the console
        main_box.add(console_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        # passing down the main window variable
        Homebrew.main_window_ = self.main_window
        self.main_window.content = main_box
        self.main_window.show()

    installer = None

    def installpkg(self):

        # getting the values of console
        input = Homebrew.console_input
        pkg = input.value
        input.clear()

        # some checks before attempting to install the package
        if pkg == '':
            Homebrew.main_window_.info_dialog('No package name was entered', 'You need to input a package name')
            return

        if len(pkg) > 25:
            Homebrew.main_window_.info_dialog('Package name too long', 'The package name you\'ve entered is too long.')
            return

        if pkg.isalnum().replace(' ', '') != True:
            Homebrew.main_window_.info_dialog('Package name is invalid', 'You\'ve entered an invalid package name (Only letters and numbers are allowed)')
            return

        if pkg == self.formal_name:
            update_dia = Homebrew.main_window_.confirm_dialog('Update', 'Are you sure you want to update '+ self.formal_name + '?')
            if update_dia != True:
                return

        # main box for the window
        install_box = toga.Box(style=Pack(
            direction=COLUMN, background_color='#000000'))

        # box that holds update info
        info_box = toga.Box(style=Pack(
            direction=COLUMN, background_color='#000000'))
        info_box.style.update(alignment=CENTER)
        install_box.add(info_box)

        # creating a new window
        self.install_window = toga.Window(title="Installing " + pkg)
        Homebrew.installer = self.install_window
        Homebrew.self_.windows.add(self.install_window)
        self.install_window.content = install_box
        self.install_window.show()

        def addlabeltoconsole(t):
            text_box = toga.Box(style=Pack(
                direction=COLUMN, background_color='#FFFFFF'))
            text_box.add(toga.Label(t))
            info_box.add(text_box)
            # refreshes the window
            self.install_window.content = install_box

        # actually getting the apk
        addlabeltoconsole('Checking if server is up...')

        # checks if the server is up, and if its a valid repo
        try:
            checkreq = requests.get(Homebrew.default_repo+'/servinfo')
            if checkreq.text == "OK":
                addlabeltoconsole('Checking if server has the package...')

                # checks if the package exists on the server
                checkpkg = requests.get(Homebrew.default_repo+'/pkgcheck/'+pkg)
                if checkpkg.text == "200":
                    addlabeltoconsole(
                        'Downloading package, this may take a while...')

                    # downloading the package
                    # pkgrequest = requests.get(Homebrew.default_repo+'/pkg/'+pkg)
                else:
                    addlabeltoconsole('The specified package does not exist.')
            else:
                addlabeltoconsole('Server is not a valid repo.')
        except Exception as e:
            addlabeltoconsole('An error has occured. '+str(e))

        confirm_box = toga.Box(style=Pack(
            direction=COLUMN, background_color='#FFFFFF'))
        confirm_box.add(toga.Button('Close'))
        install_box.add(confirm_box)
        self.install_window.content = install_box

    def close_install(self):
        pass


def main():
    return Homebrew()
