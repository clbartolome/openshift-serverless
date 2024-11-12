# openshift-serverless

TODO: important with versions

https://docs.openshift.com/serverless/1.34/about/about-serverless.html

## Installation

OpenShift Serverless Operator 1.34.0
Installing Knative Serving - instance (default) in knative-serving namespace
Installing Knative Eventing - instance (default) in knative-eventing namespace
Knative CLI
OpenShift registry exposed (could be done with another registry) https://docs.openshift.com/container-platform/4.17/registry/securing-exposing-registry.html#registry-exposing-default-registry-manually_securing-exposing-registry
Docker or Podman 



## Demo

cd demo-app
oc new-build --name=demo-app --binary
oc start-build demo-app --from-dir=. --follow
IMG=image-registry.openshift-image-registry.svc:5000/demo/demo-app:latest

cd ..

oc new-app --name=app-b --image= $IMG --env ID=app-b

oc new-app --name=app-a --image= $IMG --env ID=app-a --env EVENT_URL=http://app-b:5000

oc expose svc app-a

kn service create kn-a --image $IMG --env ID=kn-a --env EVENT_URL=http://app-b:5000 --port 5000

kn service create kn-b --image $IMG --env ID=kn-b-v1 --port 5000 --revision-name v1
kn service update kn-b --image $IMG --env ID=kn-b-v2 --port 5000 --revision-name v2


kn service update kn-b --traffic kn-b-v1=50,kn-b-v2=50

kn service update kn-a --env EVENT_URL=http://kn-b.demo.svc.cluster.local


oc apply -f resources/broker.yaml

kn service update kn-a --env EVENT_URL=http://broker-ingress.knative-eventing.svc.cluster.local/demo/default

oc apply -f resources/trigger.yaml


oc apply -f resources/ping-source.yaml

oc apply -f resources/trigger-ping.yaml

oc delete -f resources/trigger-ping.yaml


kn func create fn -l node -t cloudevents

cd fn
tree

code .

kn func config
kn func build -v
kn func run
(kn funk invoke) in another tab
kn func deploy -v
kn func invoke --target https://fn-demo.apps.hetzner.calopezb.com



















