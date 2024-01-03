##  https://neilkuan.github.io/k8s-event-to-loki-grafana/
chart github pages

Release helm chart to `gh-pages``
```bash
git checkout gh-pages

## make some magic ~~~ 🥳 🥳 🥳

helm package ./k8s/

helm repo index --url https://neilkuan.github.io/k8s-event-to-loki-grafana .

git status

git add .

VERSION=$(cat k8s/Chart.yaml | grep "^version:" | awk '{print $2}')

git commit -m "gh page release ${VERSION}"

git push origin gh-pages
```