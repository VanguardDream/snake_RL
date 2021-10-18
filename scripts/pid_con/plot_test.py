import sys
import mujoco_py

from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget

import time
import csv

import description as des


class mainFrame(QWidget):
    model_xml = ""
    con_type = 0
    damping_value = 1

    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("pid simulator")

        # Component Declare
        label1 = QLabel("Controller type")
        self.tb_con = QLineEdit("0",self)

        label2 = QLabel("Damping value")
        self.tb_damp = QLineEdit("1",self)

        self.label_status = QLabel("Controller : , Damping : ")

        bt_conf = QPushButton("set",self)
        bt_run = QPushButton("run",self)

        self.canvas = FigureCanvas(Figure(figsize=(5,3)))

        # Layouts
        vlayout = QVBoxLayout()
        vlayout.addWidget(label1)
        vlayout.addWidget(self.tb_con)
        vlayout.addWidget(label2)
        vlayout.addWidget(self.tb_damp)
        vlayout.addWidget(self.label_status)
        vlayout.addWidget(bt_conf)
        vlayout.addWidget(bt_run)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.canvas)
        hlayout.addLayout(vlayout)

        self.setLayout(hlayout)

        # Slot and Connects
        bt_conf.clicked.connect(self.bt_con_clicked)
        bt_run.clicked.connect(self.bt_run_clicked)

        self.move(400,400)
        self.resize(800,400)
        self.show()

    def bt_con_clicked(self):
        type = self.tb_con.text()
        damp = self.tb_damp.text()

        self.con_type = int(type)
        self.damping_value = str(damp)

        info = "Controller : {type} , Damping : {damp}"

        info = info.format(type=int(type),damp=str(damp))

        self.model_xml = sim_config(int(type),damp)

        self.label_status.setText(info)

    def bt_run_clicked(self):
        model = mujoco_py.load_model_from_xml(sim_config(self.con_type,self.damping_value))
        sim = mujoco_py.MjSim(model)
        # simgui = mujoco_py.MjViewer(sim)

        log_qpos = []
        log_qvel = []

        for t in range(0,2500):
            if t == 500:
                sim.data.ctrl[0] = 1.0472
            if t == 1000:
                sim.data.ctrl[0] = -1.0472
            if t == 1500:
                sim.data.ctrl[0] = 1.0472
            if t == 2000:
                sim.data.ctrl[0] = -1.0472

            log_qpos.append(sim.data.get_joint_qpos('joint1'))
            log_qvel.append(sim.data.get_joint_qvel('joint1'))

            sim.step()
            # simgui.render()

        log_file = open('logs.csv','a')
        log_writer = csv.writer(log_file)

        log_writer.writerow([time.ctime(time.time())] + ["type : "] + [self.con_type] + [self.damping_value])

        for n_raws in range(0, len(log_qpos) -1):
            log_writer.writerow([log_qpos[n_raws]] + [log_qvel[n_raws]])

        log_file.close()

        ax = self.canvas.figure.subplots()
        ax.plot(list(range(0,2500)), log_qvel, log_qpos, '-')
        self.canvas.draw()


def main():
    
    # model = mujoco_py.load_model_from_xml(sim_config(0,1))
    # sim = mujoco_py.MjSim(model)
    # simgui = mujoco_py.MjViewer(sim)

    app = QApplication(sys.argv)
    frame = mainFrame()
    sys.exit(app.exec_())

def sim_config(type, damping):

    # 0 -> p controller, 1 -> pid controller

    if type == 0:
        model = des.model_xml.format(actuator = des.p_controller, damping = damping)
    else:
        model = des.model_xml.format(actuator = des.pid_controller, damping = damping)

    return model


if __name__ == "__main__":
    main()
