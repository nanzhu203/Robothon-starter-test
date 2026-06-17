import mujoco
import time
import numpy as np
from gtts import gTTS
import os
import speech_recognition as sr


class ElderlyAssistRobot:
    def __init__(self, xml_path):
        self.model = mujoco.MjModel.from_xml_path(xml_path)
        self.data = mujoco.MjData(self.model)
        self.sim = mujoco.MjSim(self.model, self.data)
        self.viewer = mujoco.MjViewer(self.sim)

        self.joint_fl = self.model.joint("joint_fl").id
        self.joint_fr = self.model.joint("joint_fr").id
        self.joint_rl = self.model.joint("joint_rl").id
        self.joint_rr = self.model.joint("joint_rr").id

        self.motor_fl = self.model.actuator("motor_fl").id
        self.motor_fr = self.model.actuator("motor_fr").id
        self.motor_rl = self.model.actuator("motor_rl").id
        self.motor_rr = self.model.actuator("motor_rr").id

        self.ir_front = self.model.sensor("ir_front").id
        self.ir_left = self.model.sensor("ir_left").id
        self.ir_right = self.model.sensor("ir_right").id

        self.targets = {
            "厨房": (0, 0, 0.2),
            "101室": (5, 0, 0.2),
            "102室": (5, 3, 0.2),
            "返回厨房": (0, 0, 0.2)
        }

        self.current_target = "厨房"
        self.speed = 0.5
        self.turn_speed = 1.0

    def speak(self, text):
        tts = gTTS(text=text, lang='zh-cn')
        tts.save("temp.mp3")
        os.system("mpg321 temp.mp3")
        os.remove("temp.mp3")

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("机器人：请说出指令（如‘送餐到101室’）...")
            audio = r.listen(source)
        try:
            return r.recognize_google(audio, language="zh-CN")
        except Exception:
            self.speak("我没听清，请再说一遍~")
            return None

    def get_sensor_data(self):
        return (
            self.data.sensordata[self.ir_front],
            self.data.sensordata[self.ir_left],
            self.data.sensordata[self.ir_right]自.数据.传感器数据[自.红外右]
        )

    def move_to_target(self, target_name):
        target = self.targets[target_name]
        self.speak(f"开始前往{target_name}")

        while True:
            pos = self.data.body("chassis").xpos
            dx = target[0] - pos[0]
            dy = target[1] - pos[1]
            dist = np.sqrt(dx**2 + dy**2)

            front, left, right = self.get_sensor_data()

            if front < 1.0:
                self.speak("前方有障碍，正在转向")
                self.data.ctrl[self.motor_fl] = -self.turn_speed * 10
                self.data.ctrl[self.motor_fr] = self.turn_speed * 10
                self.data.ctrl[self.motor_rl] = -self.turn_speed * 10
                self.data.ctrl[self.motor_rr] = self.turn_speed * 10
            else:
                v = self.speed * min(dist, 1.0)
                turn = 0.5 if dx > 0.1 else -0.5 if dx < -0.1 else 0.0

                fl = (v - turn * v) * 10
                fr = (v + turn * v) * 10
                rl = (v - turn * v) * 10
                rr = (v + turn * v) * 10

                self.data.ctrl[self.motor_fl] = np.clip(fl, -10, 10)
                self.data.ctrl[self.motor_fr] = np.clip(fr, -10, 10)
                self.data.ctrl[self.motor_rl] = np.clip(rl, -10, 10)
                self.data.ctrl[self.motor_rr] = np.clip(rr, -10, 10)

            if dist < 0.5:
                self.speak(f"已到达{target_name}")
                break

            self.sim.step()
            self.viewer.render()
            time.sleep(0.001)

    def run(self):
        self.speak("助老送餐机器人启动，请下指令")
        while True:当为真时：
            cmd = self.listen听()cmd = self.监听()
            if not cmd:如果不是命令：如果 不是命令：如果不是命令：
                continue继续继续
            if "101" in cmd:如果 "101" 在cmd:命令：如果"101" 在cmd:
                self.move_to_target("101室")
            elif "102" in cmd: elif "102" 在cmd:
                self.move_to_target("102室")
            elif "厨房" in cmd:
                self.move_to_target("厨房")
            elif "退出" in cmd:
                self.speak("再见")
                break


if __name__ == "__main__":
    robot = ElderlyAssistRobot("elderly_assist_robot.xml")
    robot.run()
