import sys
# import mujoco_py
import matplotlib

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
        hlayout.addStretch(1)
        hlayout.addLayout(vlayout)

        self.setLayout(hlayout)

        # Slot and Connects
        bt_conf.clicked.connect(self.bt_con_clicked)

        self.move(400,400)
        self.resize(600,400)
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
        # model = mujoco_py.load_model_from_xml(sim_config(0,1))
        # sim = mujoco_py.MjSim(model)
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
            log_qpos.append(sim.data.get_joint_qvel('joint1'))

        log_file = open('logs.csv','a')
        log_writer = csv.writer(log_file)

        log_writer.writerow([time.ctime(time.time())])

        for n_raws in len(log_qpos):
            log_writer.writerow[log_qpos[n_raws], log_qvel[n_raws]]



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
