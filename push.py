from utils.KodiManagement import Kodi


kodi = Kodi(hostname="192.168.1.67", port="8080", username="kodi", password="Bright2021!")

kodi.GetOnScanFinished()
