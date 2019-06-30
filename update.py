from kivy.clock import Clock
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest

from kivymd.snackbars import Snackbar
from kivymd.button import MDIconButton

from plyer import storagepath

try:
    import android
except ImportError:
    android = None

if android:
    from jnius import autoclass
    from plyer.platforms.android import activity


APK_FILE_PATH = storagepath.get_downloads_dir()+'/cryptculatorapp.apk'


class Update:
    def __init__(self, App, Window):
        self.status = 'None'
        self.App = App
        self.Window = Window

    def get_version(self):
        def callback(request, result):
            self.App.git_version = str(result)
            self.check_version()
            self.process()

        version_url = "https://raw.githubusercontent.com/bugsbringer/Cryptculator-actual-APK/master/version.txt"
        UrlRequest(version_url, verify=False, on_success=callback)

    def check_version(self):
        if self.App.git_version:
            if float(self.App.git_version[:3]) > float(self.App.version[:3]):
                self.App.update_available = True

            elif float(self.App.git_version[:3]) == float(self.App.version[:3]):
                if float(self.App.git_version[4]) > float(self.App.version[4]):
                    self.App.update_available = True

    def start(self):
        if android:
            # удаление старого апк файла
            File = autoclass('java.io.File')
            apkFile = File(APK_FILE_PATH)
            apkFile.delete()

        self.get_version()

    def process(self):
        if self.App.update_available:
            self.snackbar = UpdateSnackBar(button_callback=self.download_update)
            self.snackbar.show()
            self.dwnld_bnt_clock = Clock.schedule_once(self.add_download_button,
                                                       self.snackbar.duration + .5)

    def add_download_button(self, *args):
        def callback(*args):
            self.download_button.parent.remove_widget(self.download_button)
            self.process()

        if self.status == 'None':
            self.download_button = DownloadButton(on_press=callback)
            MainFrame_index = len(self.Window.children) - 1
            self.Window.children[MainFrame_index].calculator.ids.topbar.add_widget(
                self.download_button)

    def download_update(self, *args):
        self.status = 'downloading'
        self.dwnld_bnt_clock.cancel()
        self.snackbar.duration = 0

        self.downloading_snackbar = Snackbar(text='Загрузка', duration=20)
        self.downloading_snackbar.show()

        url = "https://raw.githubusercontent.com/bugsbringer/Cryptculator-actual-APK/master/cryptculatorapp.apk"
        self.request = UrlRequest(url, on_success=self.install_update,
                                  verify=False, file_path=APK_FILE_PATH)

    def install_update(self, *args):
        self.downloading_snackbar = 0
        if android:

            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')

            File = autoclass('java.io.File')
            apkFile = File(APK_FILE_PATH)

            intent = Intent()
            intent.setAction(Intent.ACTION_INSTALL_PACKAGE)
            intent.setData(Uri.fromFile(apkFile))

            activity.startActivity(intent)


Builder.load_string(open("kv/update.kv", encoding='utf-8').read())


class UpdateSnackBar(Snackbar):
    text = "Доступно обновление"
    button_text = "Установить"
    duration = 3


class DownloadButton(MDIconButton):
    pass
