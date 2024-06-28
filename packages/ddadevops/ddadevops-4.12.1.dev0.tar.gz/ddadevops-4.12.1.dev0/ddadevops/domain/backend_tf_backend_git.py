from typing import List, Dict, Set, Any
from .common import Validateable, CredentialMappingDefault


class TerraformBackendGit(Validateable, CredentialMappingDefault):
    def __init__(
        self,
        inp: dict,
    ):
        self.stage = inp.get("stage")
        self.module = inp.get("module")
        self.git_backend_repo = inp.get("git_backend_repo")
        self.git_backend_ref = inp.get("git_backend_ref")
        self.git_backend_state = inp.get("git_backend_state")
        self.git_backend_username = inp.get("git_backend_username")
        self.git_backend_token = inp.get("git_backend_token")

    def validate(self) -> List[str]:
        result = []
        result += self.__validate_is_not_empty__("stage")
        result += self.__validate_is_not_empty__("module")
        result += self.__validate_is_not_empty__("git_backend_repo")
        result += self.__validate_is_not_empty__("git_backend_ref")
        result += self.__validate_is_not_empty__("git_backend_state")
        result += self.__validate_is_not_empty__("git_backend_username")
        result += self.__validate_is_not_empty__("git_backend_token")

        return result

    # See: https://developer.hashicorp.com/terraform/language/settings/backends/configuration#command-line-key-value-pairs
    # and https://github.com/plumber-cd/terraform-backend-git?tab=readme-ov-file#standalone-terraform-http-backend-mode
    def backend_config(self) -> Dict[str, Any]:
        return {
            "address": self.__make_http_backend_address__(),
            "lock_address": self.__make_http_backend_address__(),
            "unlock_address": self.__make_http_backend_address__(),
        }

    def resources_from_package(self) -> Set[str]:
        return {"tf_backend_git_backend.tf", "tf_backend_git_backend_vars.tf"}

    # TODO: This can not be used for backend, as the backend block can not reference vars.
    # This is another reason to introduce a 'backend' object
    def project_vars(self) -> Dict[str, Any]:
        return {
            "": ""
        }

    def is_local_state(self):
        return False

    def __make_http_backend_address__(self) -> str:
        # TODO Should we make this configurable?
        base_string = "http://localhost:6061/?type=git"
        state = f"{self.stage}/{self.module}/{self.git_backend_state}"
        return f"{base_string}&repository={self.git_backend_repo}&ref={self.git_backend_ref}&state={state}"

    # TODO: Implement ssh auth too
    @classmethod
    def get_mapping_default(cls) -> List[Dict[str, str]]:
        return [
            {
                "gopass_path": "server/meissa/repo/terraform-backend-git-test",
                "gopass_field": "user",
                "name": "git_backend_username",
            },
            {
                "gopass_path": "server/meissa/repo/terraform-backend-git-test",
                "gopass_field": "token",
                "name": "git_backend_token",
            },
        ]
