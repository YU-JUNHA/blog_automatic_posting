from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QThread  # [수정]
import sys
import os
import blog_automatic_posting
from PyQt5.QtWidgets import QTextBrowser

if hasattr(sys, '_MEIPASS'):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UI_PATH = "bkig_automatic_posting.ui"

# [수정] 백그라운드 작업을 처리할 QThread 클래스 정의
class WorkerThread(QThread):
    def __init__(self, coupang_id, coupang_pw, blog_id, blog_pw, blog_write_page, search_word, post_num, api_key):
        super().__init__()
        self.coupang_id = coupang_id
        self.coupang_pw = coupang_pw
        self.blog_id = blog_id
        self.blog_pw = blog_pw
        self.blog_write_page = blog_write_page
        self.search_word = search_word
        self.post_num = post_num
        self.api_key = api_key

    def run(self):
        blog_automatic_posting.main(
            self.coupang_id, self.coupang_pw,
            self.blog_id, self.blog_pw,
            self.blog_write_page, self.search_word,
            self.post_num, self.api_key
        )


class MainDialog(QDialog):
    def __init__(self):
        super().__init__(None)
        uic.loadUi(os.path.join(BASE_DIR, UI_PATH), self)
        self.start.clicked.connect(self.run_main)

    def log(message):
        self.text_browser.append(message)
        QApplication.processEvents()

    def run_main(self):
        try:
            coupang_id = self.coupg_id.text()
            coupang_pw = self.coupang_pw.text()
            blog_id = self.blog_id.text()
            blog_pw = self.blog_pw.text()
            blog_write_page = self.write_page_url.text()
            search_word = self.search_word.text()
            post_num = self.post_num.text()
            api_key = self.api_key.text()

            if not post_num.isdigit() or int(post_num) == 0:
                raise ValueError("글 개수에는 0이 아닌 숫자만 들어갈 수 있습니다.")

            # [수정] QThread를 이용해 백그라운드에서 작업 실행
            self.worker = WorkerThread(
                coupang_id, coupang_pw, blog_id, blog_pw,
                blog_write_page, search_word, post_num, api_key
            )
            self.worker.start()

        except Exception as e:
            QMessageBox.critical(self, "에러", str(e))


if __name__ == "__main__":
    QApplication.setStyle("fusion")
    app = QApplication(sys.argv)

    main_dialog = MainDialog()
    main_dialog.show()
    sys.exit(app.exec_())