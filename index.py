from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import pafy
from os import path
import sys, os, webbrowser,subprocess
import urllib.parse
import urllib.request as ur
import humanize
from urllib.parse import *
from os.path import splitext, basename
import win32clipboard
import threading

# import UI File to use it in the next class that runs the GUI in pycharm
# when you make change in Qt designer it change automatic here
FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))


# Initiate UI File
class MainApp(QMainWindow, FORM_CLASS):

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handel_ui()
        self.handel_buttons()
        self.lineEdit.installEventFilter(self)

    def handel_ui(self):
        # Main Window:
        self.setWindowTitle("Download Program v1.0")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setFixedSize(520,300)

        # download:
        self.lineEdit_4.setPlaceholderText("Enter url here")
        self.lineEdit_4.setStatusTip("Enter url here")
        self.lineEdit_3.setPlaceholderText("Choose Save Location")
        self.lineEdit_3.setStatusTip("Choose Save Location")
        self.textBrowser_5.setPlaceholderText("File Name ")
        self.textBrowser_2.setPlaceholderText("File Type ")
        self.textBrowser.setPlaceholderText("File Size ")
        self.textBrowser_4.setPlaceholderText("Downloaded ")
        self.textBrowser_3.setPlaceholderText("Speed ")
        # youtube:
        self.lineEdit.setPlaceholderText("Enter url here")
        self.lineEdit.setStatusTip("Enter url here")
        self.lineEdit_2.setPlaceholderText("Choose Save Location")
        self.lineEdit_2.setStatusTip("Choose Save Location")
        self.textBrowser_11.setPlaceholderText("Duration ")
        self.textBrowser_8.setPlaceholderText("Videos ")
        self.comboBox.setStatusTip("Quality")
        QApplication.processEvents()

        # check clipboard for url
        # def clipboardurl(self):
        #      try:
        #          win32clipboard.OpenClipboard()
        #          url = win32clipboard.GetClipboardData()
        #          if (url.startswith('http' or 'https')):
        #              self.lineEdit_4.setText(url)
        #              win32clipboard.CloseClipboard()
        #          else:
        #              pass
        #      except Exception :
        #          pass
        #      QApplication.processEvents()

    def handel_buttons(self):
        # all buttons of this program will be here because it is small project so we do it all in one class
        # with all func that is needed if it was big project there would be extra classes
        self.pushButton_7.clicked.connect(self.search)
        self.pushButton_4.clicked.connect(self.browse)
        self.pushButton_5.clicked.connect(self.download)
        # youtube:
        self.pushButton_8.clicked.connect(self.youtube_search)
        self.pushButton.clicked.connect(self.youtube_browse)
        self.pushButton_2.clicked.connect(self.youtube_download)
        # find me at:
        self.pushButton_16.clicked.connect(self.upwork)
        self.pushButton_17.clicked.connect(self.patreon)
        self.pushButton_15.clicked.connect(self.github)
        self.pushButton_13.clicked.connect(self.linkein)
        self.pushButton_14.clicked.connect(self.facebook)
        QApplication.processEvents()

    # check clipboard for url:
    def eventFilter(self, obj, event):
        win32clipboard.OpenClipboard()
        url = str(win32clipboard.GetClipboardData())
        if url.startswith("https://www.youtube.com/"):
            if obj == self.lineEdit and event.type() == QEvent.FocusIn:
                self.lineEdit.setText(url)
                win32clipboard.CloseClipboard()
            QApplication.processEvents()

        QApplication.processEvents()
        return super(MainApp, self).eventFilter(obj, event)

    def upwork(self):
        return webbrowser.open_new_tab("https://www.upwork.com/freelancers/~012320c27b0e56e249")

    def patreon(self):
        return webbrowser.open_new_tab("https://www.patreon.com/mostafa_abobakr")

    def github(self):
        return webbrowser.open_new_tab("https://github.com/mostafaabobakr7")

    def linkein(self):
        return webbrowser.open_new_tab("https://www.linkedin.com/in/mostafa-abobakr-3b2041145/")

    def facebook(self):
        return webbrowser.open_new_tab("https://www.facebook.com/mostafa7abobakr")

    # search handling(when search clicked):
    def search(self):
        try:
            # trying to get url info
            # first get pasted url from lineEdit_4
            mainurl = ur.urlopen(self.lineEdit_4.text())
            # use humanize lib to get size in MB from url.info()
            # note that (mainurl.info()['Content-Length']) because it is a dictionary
            file_size_mb = humanize.naturalsize(mainurl.info()['Content-Length'])
            self.textBrowser.setText(file_size_mb)
            # display file Name and type from a url
            disassembled = urlparse(self.lineEdit_4.text())
            filename, file_ext = splitext(basename(disassembled.path))
            name = urllib.parse.unquote(filename)
            self.textBrowser_5.setText(name + file_ext)
            self.textBrowser_2.setText(file_ext)
        except Exception:
            pass
        QApplication.processEvents()

    def youtube_search(self):
        url = self.lineEdit.text()
        # if it was a playlist:
        if url != "" and "&list=" in url:
            try:
                playlist = pafy.get_playlist(url)
                videos = playlist['items']
                length = str(len(playlist['items']))
                # Display playlist name:
                self.textBrowser_7.setText(playlist['title'])
                # Display playlist thumbnail:
                playlistthumb = pafy.new(url)
                imageurl = playlistthumb.thumb
                imageurlopen = ur.urlopen(imageurl).read()
                image = QtGui.QImage()
                image.loadFromData(imageurlopen)
                mypixmap = QtGui.QPixmap(image)
                self.label_10.setPixmap(mypixmap)
                # display number of videos:
                self.textBrowser_8.setText(length + " " + "Videos")
                # display author:
                author = str(playlist['author'])
                self.textBrowser_10.setText(author)
            except Exception:
                pass
            QApplication.processEvents()
        # if it was a video:
        elif url != "":
            try:
                v = pafy.new(url)
                # Display video name:
                self.textBrowser_6.setText(v.title)
                # Display video thumbnail:
                imageurl = v.thumb
                imageurlopen = ur.urlopen(imageurl).read()
                image = QtGui.QImage()
                image.loadFromData(imageurlopen)
                mypixmap = QtGui.QPixmap(image)
                self.label_10.setPixmap(mypixmap)
                # display author:
                self.textBrowser_10.setText(v.author)
                # display video duration:
                self.textBrowser_11.setText(v.duration)
                # Display video qualities and sizes:
                st = v.allstreams
                for s in st:
                    size = humanize.naturalsize(s.get_filesize())
                    data = '{} {} {} {}'.format(s.mediatype, s.extension, s.quality, size)
                    self.comboBox.addItem(data)
                    QApplication.processEvents()
            except Exception:
                pass
            QApplication.processEvents()
        QApplication.processEvents()

    # browse handling(when browse clicked):
    def browse(self):
        save_place = QFileDialog.getExistingDirectory(self, "Select Place To Save")
        self.lineEdit_3.setText(save_place)
        QApplication.processEvents()

    def youtube_browse(self):
        save_place = QFileDialog.getExistingDirectory(self, "Select Place To Save")
        self.lineEdit_2.setText(save_place)
        QApplication.processEvents()

    # All downloads handling (when download clicked):
    def download(self):
        url = self.lineEdit_4.text()
        save_loc = self.lineEdit_3.text() + "/" + self.textBrowser_5.toPlainText()
        # this error handling if user didn't place url or place path where to save
        try:
            ur.urlretrieve(url, save_loc, self.download_progress)
            # trying to get downloaded file size during download and displaying it in textBrowser_4

            # trying to measure download speed during download and displaying it in textBrowser_3

        except Exception:
            QMessageBox.warning(self, "Download Error", "Error Occurred ")
        # message when download complete
        QMessageBox.information(self, "Download Completed", "the Download finished")
        # reset progress bar and clear lineEdit after download finished
        self.progressBar_2.setValue(0)
        self.lineEdit_4.setText("")
        self.lineEdit_3.setText("")
        self.textBrowser.setText("")
        self.textBrowser_5.setText("")
        self.textBrowser_2.setText("")
        self.textBrowser_4.setText("")
        QApplication.processEvents()

    def youtube_download(self):
        url = self.lineEdit.text()
        # if url is playlist:
        if "&list=" in url:
            save_loc = self.lineEdit_2.text()
            playlist = pafy.get_playlist(url)
            videos = playlist['items']
            os.chdir(save_loc)
            QApplication.processEvents()
            # create folder to download in check if folder exist with playlist name:
            if os.path.exists(str(playlist['title'])):
                os.chdir(str(playlist['title']))
                QApplication.processEvents()
            else:
                os.mkdir(str(playlist['title']))
                os.chdir(str(playlist['title']))
                QApplication.processEvents()
            # Download playlist:
            for current, video in enumerate(videos, start=1):
                p = video['pafy']
                best = p.getbest(preftype='mp4')

                def mycb(total, recvd, ratio, rate, eta):
                    self.progressBar_7.setValue((recvd * 100) / total)
                    QApplication.processEvents()
                    self.label_4.setText(humanize.naturalsize(recvd))
                    self.label_3.setText(str(round(rate)) + " KB/S")
                    self.label_5.setText(humanize.naturalsize(total))
                    # display current video:
                    self.label_15.setText(str(current))
                    QApplication.processEvents()

                best.download(quiet=True, callback=mycb)
                QApplication.processEvents()
        # if it was video:
        else:
            save_loc = self.lineEdit_2.text()
            v = pafy.new(url)
            st = v.allstreams
            quailty = self.comboBox.currentIndex()

            # display speed and Downloaded:
            def mycb(total, recvd, ratio, rate, eta):
                self.progressBar.setValue((recvd * 100) / total)
                QApplication.processEvents()
                self.label_4.setText(humanize.naturalsize(recvd))
                self.label_3.setText(str(round(rate)) + " KB/S")
                self.label_5.setText(humanize.naturalsize(total))

            down = st[quailty].download(filepath=save_loc, quiet=True, callback=mycb)
            QMessageBox.information(self, "Download Completed", "the Download finished")
        QApplication.processEvents()

    # progress-bar handling:
    def download_progress(self, blocknum, blocksize, totalsize):
        # this is how progress bar act it needs these three arguments
        # which take it from urlretrieve (self.Handel_progress)
        read = blocknum * blocksize
        if totalsize > 0:
            percent = read * 100 / totalsize
            self.progressBar_2.setValue(percent)
        # display downloaded size:
        downloaded_mb = humanize.naturalsize(blocknum * blocksize)
        self.textBrowser_4.setText(downloaded_mb)
        QApplication.processEvents()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
