import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
  
class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit()  
  
#url = 'https://ke.qq.com/webcourse/index.html#course_id=148551&term_id=100168945&taid=709026086274119&vid=h1415xnd2aj'  
url = 'http://webscraping.com'
r = Render(url)
html = r.frame.toHtml()
print html