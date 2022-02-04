# **Juju Charmed Kubernetes Calico**
### **Requirements**
1. [AWS CLI installed](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
```
sudo apt install unzip
```
```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```
2. [Configure AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config)
```
aws configure
```
3. Kubectl installed
```
sudo snap install kubectl --classic
```
4. [Boto3 installed](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)
```
pip3 install boto3
```
4. Juju installed
```
sudo snap install juju --classic
```
### **How To**
1. Bootstrap Controller
```
juju bootstrap aws aws-controller
```
2. Add k8s model
```
juju add-model k8s
```
3. Download or Create file aws-overlay.yaml
```
wget https://raw.githubusercontent.com/ludesdeveloper/juju-charmed-kubernetes/master/aws-overlay.yaml
```
```
description: Charmed Kubernetes overlay to add native AWS support.
applications:
  aws-integrator:
    annotations:
      gui-x: "600"
      gui-y: "300"
    charm: cs:~containers/aws-integrator
    num_units: 1
    trust: true
relations:
  - ['aws-integrator', 'kubernetes-master']
  - ['aws-integrator', 'kubernetes-worker']
```
4. Download or Create file calico-overlay.yaml
```
wget https://raw.githubusercontent.com/ludesdeveloper/juju-charmed-kubernetes/master/calico-overlay.yaml
```
```
description: Charmed Kubernetes overlay to add Calico CNI.
applications:
  calico:
    annotations:
      gui-x: '480'
      gui-y: '750'
    charm: cs:~containers/calico
  flannel:
relations:
- - calico:etcd
  - etcd:db
- - calico:cni
  - kubernetes-master:cni
- - calico:cni
  - kubernetes-worker:cni
```
5. Deploy Charmed Kubernetes with overlay
```
juju deploy charmed-kubernetes --overlay aws-overlay.yaml --trust --overlay calico-overlay.yaml
```
6. Disable source check destination on ec2(I use boto3 to do this)
```
python3 ec2_disable_source_check_destination.py 
```
7. Watch process
```
watch -c juju status --color
```
8. Copy kubeconfig
```
juju scp kubernetes-master/0:config ~/.kube/config
```
> Create ~/.kube folder if you don't have
### **Clean Up**
1. Destroy models
```
juju destroy-model k8s
```
2. Forced Destroy models
```
juju destroy-model k8s --timeout=0 --force
```
3. Destroy controller
```
juju destroy-controller aws-controller
```
