import paho.mqtt.client as mqtt
import os
import json

from dotenv import load_dotenv
load_dotenv()

topico = os.getenv('TOPICO_NOTIFICACOES_MGC')
host = os.getenv('MQTT_HOST')
port = int(os.getenv('MQTT_PORT'))
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def connect_mqtt():
    """ Conecta o cliente ao broker """
    try:
        mqtt_client.connect(host,port,60)
        mqtt_client.loop_start()
        print(f"Conectado com sucesso ao Broker em {host}:{port}")
    except Exception as e:
        print(f"Falha ao conectar ao Broker: {e}")
    
def disconnect_mqtt():
    " Desconecta o cliente. "
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("Desconectado do Broker.")

def publish_policy_update(titular_id: int, dispositivo_id: int):
    """ Publica uma mensagem de atualização de política. """
    payload = {
        "evento":"ATUALIZACAO_POLITICA",
        "titular_id":titular_id,
        "dispositivo_id":dispositivo_id
    }

    msg = json.dumps(payload)
    result = mqtt_client.publish(topico, msg)

    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"Notificação de atualização publicada.")
    else:
        print(f"Falha ao publicar notificação. Código: {result.rc}")