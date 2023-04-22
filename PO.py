import paho,time,struct,paho.mqtt.client as mqtt
class BarriDog:
    def __init__(self):
        self.client = mqtt.Client()
    def on_connect(self, obj, flags, rc):
        print("rc: " + str(rc))

    def on_message(self, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def on_publish(self, obj, mid):
        print("mid: " + str(mid))
        pass

    def on_subscribe(self, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, obj, level, string):
        print(string)

    def connect(self):
        mqtt.on_message = self.on_message
        mqtt.on_connect = self.on_connect
        mqtt.on_publish = self.on_publish
        mqtt.on_subscribe = self.on_subscribe
        mqtt.on_log = self.on_log
        self.client.connect("192.168.12.1", 1883, 120)
        self.client.loop_start()

    def checkMqtt(self):
        if isinstance(self.client, paho.mqtt.client.Client):
            return True
        else:
            return False

    def checkValue(self,value):
        if (type(value) == int or type(value) == float) and value < 0.3:
            return True
        else:
            return False

    def down(self):
        if self.checkMqtt():
            infot = self.client.publish("controller/action", "standDown", qos=2)
            infot.wait_for_publish()
            time.sleep(1)

    def up(self):
        if self.checkMqtt():
            infot = self.client.publish("controller/action", "standUp", qos=2)
            infot.wait_for_publish()
            time.sleep(1)

    def setWalk(self):
        if self.checkMqtt():
            infot = self.client.publish("controller/action", "walk", qos=2)
            infot.wait_for_publish()
            time.sleep(1)

    def setClimb(self):
        if self.checkMqtt():
            infot = self.client.publish("controller/action", "climb", qos=2)
            infot.wait_for_publish()
            time.sleep(1)

    def walk(self, f_speed, r_speed, yaw_speed, tilt, WalkRunClimb):
        if self.checkValue(f_speed) and self.checkValue(r_speed) and (type(yaw_speed) == int or type(yaw_speed) == float)  and (type(tilt) == int or type(tilt) == float) and self.checkMqtt():
            if (WalkRunClimb == "Walk"):
                self.setWalk()
                a = [r_speed, yaw_speed, tilt, f_speed]
                print(struct.pack('ffff', a[0], a[1], a[2], a[3]))
                infot = self.client.publish("controller/stick", struct.pack('ffff', a[0], a[1], a[2], a[3]), qos=2)
                infot.wait_for_publish()
                time.sleep(0.5)
            if (WalkRunClimb == "Climb"):
                self.setClimb()
                a = [r_speed, yaw_speed, tilt, f_speed]
                print(struct.pack('ffff', a[0], a[1], a[2], a[3]))
                infot = self.client.publish("controller/stick", struct.pack('ffff', a[0], a[1], a[2], a[3]), qos=2)
                infot.wait_for_publish()
                time.sleep(0.4)
        else:
            print("Вы ввели неправильное значение! Попробуйте еще раз")

    def dance(self, time):
        if (type(time) == int or type(time) == float) and self.checkMqtt():
            while (time > 0):
                self.walk(0, 0, 0, -1, "Walk")
                self.walk(0, 0, 0, 1, "Walk")
                self.walk(0, 0, 0, -1, "Walk")
                self.walk(0, 0, 0, 1, "Walk")
                self.walk(0, 0, 0, -1, "Walk")
                self.walk(0, 0, 0, 1, "Walk")
                self.walk(0, 0, 0, 0, "Walk")
                time = time - 1

    def goForward(self, value, WalkRunClimb):
        if self.checkValue(value) and self.checkMqtt():
            self.walk(value, 0, 0, 0, WalkRunClimb)
            time.sleep(3)
        else:
            self.walk(0.2, 0, 0, 0, WalkRunClimb)
            time.sleep(3)

    def goBack(self, value, WalkRunClimb):
        if self.checkValue(value) and self.checkMqtt():
            self.walk(-value, 0, 0, 0, WalkRunClimb)
            time.sleep(3)
        else:
            self.walk(-0.2, 0, 0, 0, WalkRunClimb)
            time.sleep(3)

    def goRight(self, value, WalkRunClimb):
        if self.checkValue(value) and self.checkMqtt():
            self.walk(0, value, 0, 0, WalkRunClimb)
            time.sleep(3)
        else:
            self.walk(0, 0.2, 0, 0, WalkRunClimb)
            time.sleep(3)

    def goLeft(self, value, WalkRunClimb):
        if self.checkValue(value) and self.checkMqtt():
            self.walk(0, -value, 0, 0, WalkRunClimb)
            time.sleep(3)
        else:
            self.walk(0, -0.2, 0, 0, WalkRunClimb)
            time.sleep(3)

    def yawMoveByTime(self, time):
        for i in range(time):
            self.walk(0, 0, 1, 0, "Walk")

    def yawMove(self, value):
        if self.checkMqtt():
            self.walk(0, 0, value, 0, "Walk")
