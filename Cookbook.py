REPO_URL = "https://github.com/wavemm/kargo-demo"


def kubectl(cmd: str) -> str:
    return f"kubectl --context kind-kargo-quickstart {cmd}"


def kargo_create_project(recipe):
    return [
        f"export GITOPS_REPO_URL={REPO_URL}",
        "export GITHUB_USERNAME=abo-abo",
        "export GITHUB_PAT=$(gpg -q --for-your-eyes-only --no-tty -d ~/.password-store/com/github.com/kargo-research.gpg)",
        "export DOCKER_USERNAME=okrehel",
        "export DOCKER_PASSWORD=$(gpg -q --for-your-eyes-only --no-tty -d ~/.password-store/com/hub.docker.com/okrehel.gpg)",
        "cd ops",
        "kargo login https://localhost:31444 --admin --password admin --insecure-skip-tls-verify",
        "envsubst < project.yaml | kargo apply -f -"]


def setup(recipe):
    return [
        "# kind delete cluster -n kargo-quickstart",
        "cd ops",
        "./setup-kind-cluster.sh",
        kubectl("apply -f argocd-kargo-demo.yaml"),
        kubectl("-n kargo-demo-test create secret generic regcred  --from-file=.dockerconfigjson=$HOME/.docker/config.json --type=kubernetes.io/dockerconfigjson")
    ]


def curl_test(recipe):
    return "curl localhost:30081"


def curl_uat(recipe):
    return "curl localhost:30082"

def curl_prod(recipe):
    return "curl localhost:30083"
