#!./venv/bin/python
import forecast,PyQt5.QtGui,PyQt5.QtWidgets,sys

rows=[PyQt5.QtWidgets.QAction() for i in range(5)]
application=PyQt5.QtWidgets.QApplication([])
icon=PyQt5.QtWidgets.QSystemTrayIcon()
menu=PyQt5.QtWidgets.QMenu()

def update():
  for r in rows[:-1]:
    r.setVisible(False)
  results=forecast.get()
  nresults=len(results)
  for i in range(nresults):
    r=rows[i]
    r.setText(results[i])
    r.setVisible(True)
  icon.setToolTip(results[1] if nresults>1 else results[0])

icon.setIcon(PyQt5.QtGui.QIcon(f"{'/'.join(sys.argv[0].split('/')[:-1])}/icon.webp"))
application.setQuitOnLastWindowClosed(False) 
icon.activated.connect(lambda:menu.popup(PyQt5.QtGui.QCursor.pos()))
q=rows[-1]
q.setText('Quit') 
q.triggered.connect(application.quit) 
for r in rows:
  menu.addAction(r)
icon.setContextMenu(menu) 
update()
icon.setVisible(True)
t=PyQt5.QtCore.QTimer()
t.timeout.connect(update)
t.setInterval(10*60*1000)
t.start()
application.exec() 
