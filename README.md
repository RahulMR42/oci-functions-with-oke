A sample python function code to invoke OCI Kubernetes Engine (OKE)
=============

Usage
-----

- Edit oke.py and update the OCI config details.

```
       config = {
                "user": 'ocid1.user.oc1..xxxx',
                "key_file": "user.pem",
                "fingerprint": '6e:69:bb:b5:22:64:xx:xxxx',
                "tenancy": 'ocid1.tenancy.oc1..xx',
                "region": '<OCI Region>'
                }

```

- A pre-requisites you must need to have an OKE ,and an OCI function application provisioned.
- Deploy the function

```
 cd oci-functions-with-oke
 fn deploy -v --app <Your app name>

```

- Invoke the function 

```
echo -n '{"cluster_id":"<OKE Cluster OCI> ","cluster_ns":"<name space to use/Optional>"}'|fn invoke <You app name> function-with-oke
```

- Validate the output 

    - The output here is a list of pods with their  IP (If applicable).
    - You can alter the kubernetes commands according to the namespace and access rights.

- The code is enabled with extensive logging using python logger ,to view it enable logging via OCI function and refer the logging view via OCI console or other interfaces.


References
-----

- [OCI Functions](https://docs.oracle.com/en-us/iaas/Content/Functions/home.htm)
- [Oracle Kubernetes Engine/OKE]()
- [OCI python SDK](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/container_engine/client/oci.container_engine.ContainerEngineClient.html#oci.container_engine.ContainerEngineClient.create_kubeconfig)
- [Kubernetes Python client](https://k8s-python.readthedocs.io/en/latest/README.html#installation)
