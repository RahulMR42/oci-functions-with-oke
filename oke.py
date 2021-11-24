import io
import json
import logging
import os,sys
import oci
from datetime import datetime
from fdk import response
from kubernetes import (
    client,

    config as kubeconfig
)


class oke:
    def __init__(self,cluster_id,cluster_ns):
        self.cluster_id = cluster_id

    def cluster_get_config(self):
        try:
            
            logging.getLogger().info("Inside oke handler")
         
            config = {
                "user": 'ocid1.user.oc1..xxxx',
                "key_file": "user.pem",
                "fingerprint": '6e:69:bb:b5:22:64:xx:xxxx',
                "tenancy": 'ocid1.tenancy.oc1..xx',
                "region": '<OCI Region>'
                }
            oke_oci_client = oci.container_engine.ContainerEngineClient(config)
            kube_config_object = oke_oci_client.create_kubeconfig(self.cluster_id)
            with open('/tmp/kubeconfig', 'w') as config_file:
                 config_file.write(kube_config_object.data.text)
            logging.getLogger().info('Got the kube config')
            kubeconfig.load_kube_config(config_file='/tmp/kubeconfig')
            v1 = client.CoreV1Api()
            print("Listing pods with their IPs:")
            ret = v1.list_pod_for_all_namespaces(watch=False)
            for i in ret.items:
                print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
                logging.getLogger().info(f"Printing pod info {i.status.pod_ip}, {i.metadata.namespace}, {i.metadata.name}")
            
            return {"status":"Ok"}
        except Exception as error:
            logging.getLogger().error('Exception' + str (error))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.getLogger().error(f'Exception details {exc_type},{fname},{exc_obj},{exc_tb.tb_lineno}')
            return {"status":f'Exception details {exc_type},{fname},{exc_tb.tb_lineno}'}


def handler(ctx, data: io.BytesIO = None):
    logging.getLogger().info("Start of invokation")
    try:
        body = json.loads(data.getvalue())
        logging.getLogger().info("Function inputs are  " + str(body))
        cluster_id = body.get('cluster_id')
        cluster_ns = body.get('cluster_ns')
        oke_object = oke(cluster_id,cluster_ns)
        return_value = oke_object.cluster_get_config()
       
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))
    except Exception as error:
            logging.getLogger().error('Exception' + str (error))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.getLogger().error(f'Exception details {exc_type},{fname},{exc_obj},{exc_tb.tb_lineno}')
            return {"status":f'Exception details {exc_type},{fname},{exc_tb.tb_lineno}'}
    logging.getLogger().info("Inside sdk handler")
    return response.Response(
        ctx, response_data=json.dumps(
            {"message": f"{return_value}"}),
        headers={"Content-Type": "application/json"}
    )


