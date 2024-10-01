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
        "envsubst < project.yaml | kargo apply -f -",

    ]

def create_regcred(recipe):
    return kubectl(
        "-n kargo-demo-migrate create secret generic regcred  --from-file=.dockerconfigjson=$HOME/.docker/config.json --type=kubernetes.io/dockerconfigjson"
    )


def setup(recipe):
    return [
        "kind delete cluster -n kargo-quickstart",
        "cd ops",
        "./setup-kind-cluster.sh",
        kubectl("apply -f argocd-kargo-demo.yaml"),
    ]


def curl_migrate(recipe):
    return "curl localhost:30081"


def curl_canary(recipe):
    return "curl localhost:30082"


def curl_prod(recipe):
    return "curl localhost:30083"


def get_freight(recipe):
    return "kargo get freight --project kargo-demo"


def get_promotions(recipe):
    return "kargo get promotions --project kargo-demo"


def get_stages(recipe):
    return "kargo get stages --project kargo-demo"


def get_analysisruns(recipe):
    return kubectl("get analysisruns --all-namespaces --sort-by=.metadata.creationTimestamp --no-headers | tac")


def get_last_analysisrun(recipe):
    return kubectl("get analysisrun --all-namespaces --sort-by=.metadata.creationTimestamp -o jsonpath=\"{.items[0]}\" | jq")


def get_last_migrate_logs(recipe, name="7273edf0-eef2-4b21-bb7c-6847e0a37444.test.1-7kq5k"):
    return kubectl(f"-n kargo-demo logs {name}")
