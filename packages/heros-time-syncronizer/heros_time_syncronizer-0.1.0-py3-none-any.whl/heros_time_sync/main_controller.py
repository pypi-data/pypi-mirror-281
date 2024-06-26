import subprocess

from PyQt5.QtWidgets import QMessageBox


class MainController:
    def __init__(self, widget):
        self.server_address = None
        self.interval = None
        self.ui = widget.ui
        self.widget = widget
        self.ui.pushButton_apply.clicked.connect(self.configure_time_sync)

    def configure_time_sync(self):
        self.server_address = self.ui.time_server_lineEdit.text()
        self.interval = self.ui.interval.value()

        subprocess.run(["w32tm", "/config", "/syncfromflags:manual", f"/manualpeerlist:{self.server_address}", "/reliable:yes","/update"], capture_output=True)
        subprocess.run(["reg", "add", r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\W32Time\TimeProviders\NtpClient", "/v", "SpecialPollInterval", "/t", "REG_DWORD", "/d", str(self.interval), "/f"], capture_output=True)
        subprocess.run(["reg", "add", "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\W32Time\Config", "/v", "MaxPosPhaseCorrection", "/t", "REG_DWORD", "/d", "86400", "/f"], capture_output=True)
        subprocess.run(["reg", "add", "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\W32Time\Config", "/v", "MaxNegPhaseCorrection", "/t", "REG_DWORD", "/d", "86400", "/f"], capture_output=True)
        subprocess.run(["reg", "add", "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\W32Time\Parameters", "/v", "LargePhaseOffset", "/t", "REG_DWORD", "/d", "50000000", "/f"], capture_output=True)
        subprocess.run(["reg", "add", "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\W32Time\Parameters", "/v", "MaxAllowedPhaseOffset", "/t", "REG_DWORD", "/d", "50000000", "/f"], capture_output=True)
        subprocess.run(["net", "stop", "w32time"], capture_output=True)
        subprocess.run(["net", "start", "w32time"], capture_output=True)
        subprocess.run(["w32tm", "/resync", "/nowait"], capture_output=True)

        QMessageBox.about(self.widget, '  ', "설정 되었습니다.")
        self.widget.close()
