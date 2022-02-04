kubectl rollout restart deployment/$(kubectl get deployment -n kube-system | awk 'NR==3 {print $1}') -n kube-system
kubectl rollout restart deployment/$(kubectl get deployment -n kube-system | awk 'NR==4 {print $1}') -n kube-system
kubectl rollout restart deployment/$(kubectl get deployment -n kube-system | awk 'NR==5 {print $1}') -n kube-system
