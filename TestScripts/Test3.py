#encoding: utf-8

from flask import Flask, render_template, request
import eventlet
import json
import paho.mqtt.client as mqtt_client
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

eventlet.monkey_patch()

app = Flask(__name__)

app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'www.csustauto.xyz'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'Flask_MQTT'
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_LAST_WILL_TOPIC'] = 'life'
app.config['MQTT_LAST_WILL_MESSAGE'] = 'bye'
app.config['MQTT_LAST_WILL_QOS'] = 0


# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'


mqtt_ws = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

# 这里的初始化MQTT可以让纯Python代码运行起来
mqtt_client = mqtt_client.Client()
mqtt_client.connect("www.csustauto.xyz", 1883, 60)  # 连接服务器,端口为1883,维持心跳为60秒


@app.route('/')
def hello_world():
    return render_template('index.html')


# 每次访问这个路由将向chat主题，提交一次数据data
@app.route('/mqtts')
def mqtts():
    # mqtt_client = myMqtt()
    mqtt_client.publish('life', 'Htmlok')
    return 'Published ok!'


@app.route('/ws')
def wevsocket():
    return render_template('websocket_mqtt_demo.html')


@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt_ws.publish(data['topic'], data['message'])


@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt_ws.subscribe(data['topic'])


@mqtt_ws.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    socketio.emit('mqtt_message', data=data)


@mqtt_ws.on_log()
def handle_logging(client, userdata, level, buf):
    print(client, userdata, level, buf)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5001, use_reloader=True, debug=True)
