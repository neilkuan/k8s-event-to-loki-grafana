# Kubernetes Event Exporter with Loki and Grafana

![](./img/arch-0.png)

## 🚨 🚨 🚨 Before install helm chart, Please update the `$LOKI_URL` in `values.yaml` file. 🚨 🚨 🚨
> If you use docker compose to run loki and grafana, you can input your compute IP at LOKI_URL.

`values.yaml`
```yaml
config:
  logLevel: debug
  metricsNamePrefix: 'event_exporter_'
  logFormat: json
  receivers:
    # - name: dump
    #   file:
    #   layout: {}
    #   path: /dev/stdout
    - name: loki
      loki:
        streamLabels:
          app: kubernetes-event-exporter
          dataCenter: local-cluster
        url: http://$LOKI_URL:3100/loki/api/v1/push
        # layout:
```

### Install with helm chart
```bash
helm upgrade -i kubernetes-event-exporter \
oci://registry-1.docker.io/bitnamicharts/kubernetes-event-exporter \
--values values.yaml --debug
```


### (Optional): Install Loki and Grafana with docker compose
```bash
docker compose up -d 
```

open [http://localhost:3000](http://localhost:3000)
![](./img/grafana-0.png)

Select Dashboard
![](./img/grafana-1.png)

Import dashboard
![](./img/grafana-2.png)

Upload dashboard JSON file use dashboard.json in this project
![](./img/grafana-3.png)

Select Import
![](./img/grafana-4.png)

Make some event into your cluster
```bash
ex:

kubectl create deploy nginx-good --image=nginx

kubectl create deploy nginx-bad --image=nginx-bad

```

Demo Dashboard
![](./img/dashboard.png)



---
Clean up
```bash
helm uninstall kubernetes-event-exporter
```

Docker Compose down
```bash
docker compose down
```

---
Loki query example
1. label_format level=`info`
```sql
{app="kubernetes-event-exporter"} |= `` | json | line_format `[{{.metadata_namespace}}] [{{.involvedObject_kind}}] "{{.involvedObject_name}}" [{{.reason}}] {{.message}}` | type=~`Normal` | label_format  level=`info` | metadata_namespace =~ `$namespace`
```

2. label_format level=`warning`
```sql
{app="kubernetes-event-exporter"} |= `` | json | line_format `[{{.metadata_namespace}}] [{{.involvedObject_kind}}] "{{.involvedObject_name}}" [{{.reason}}] {{.message}}` | type=~`Warning` | label_format  level=`warning` | metadata_namespace =~ `$namespace`
```

3. label_format level=`error`
```sql
{app="kubernetes-event-exporter"} |= `` | json | line_format `[{{.metadata_namespace}}] [{{.involvedObject_kind}}] "{{.involvedObject_name}}" [{{.reason}}] {{.message}}` | reason=~`Failed`| label_format  level=`error` | metadata_namespace =~ `$namespace``
```
