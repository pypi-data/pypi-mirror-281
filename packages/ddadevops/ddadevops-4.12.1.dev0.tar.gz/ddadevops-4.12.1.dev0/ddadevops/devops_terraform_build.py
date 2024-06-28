from .devops_build import DevopsBuild
from .application import TerraformService


class DevopsTerraformBuild(DevopsBuild):
    def __init__(self, project, config):
        inp = config.copy()
        inp["name"] = project.name
        inp["module"] = config.get("module")
        inp["stage"] = config.get("stage")
        inp["project_root_path"] = config.get("project_root_path")
        inp["build_types"] = config.get("build_types", [])
        inp["mixin_types"] = config.get("mixin_types", [])
        super().__init__(project, inp)
        project.build_depends_on("dda-python-terraform")
        self.terraform_service = TerraformService.prod()

    # TODO: we might want to make this private in the future, keeping this for compatibility
    def initialize_build_dir(self):
        super().initialize_build_dir()
        devops = self.devops_repo.get_devops(self.project)
        self.terraform_service.initialize_build_dir(devops)

    def pre_build(self):
        self.initialize_build_dir()
        devops = self.devops_repo.get_devops(self.project)
        if self.terraform_service.uses_backend_git(devops):
            self.terraform_service.start_tf_backend_git_daemon(devops)

    def post_build(self):
        devops = self.devops_repo.get_devops(self.project)
        self.terraform_service.post_build(devops)

    def read_output_json(self) -> map:
        devops = self.devops_repo.get_devops(self.project)
        return self.terraform_service.read_output(devops)

    def plan(self):
        devops = self.devops_repo.get_devops(self.project)
        self.terraform_service.plan(devops)
        self.post_build()

    def plan_fail_on_diff(self):
        devops = self.devops_repo.get_devops(self.project)
        self.terraform_service.plan(devops, fail_on_diff=True)
        self.post_build()

    def apply(self, auto_approve=False):
        devops = self.devops_repo.get_devops(self.project)
        self.terraform_service.apply(devops, auto_approve=auto_approve)
        self.post_build()

    def refresh(self):
        devops = self.devops_repo.get_devops(self.project)
        self.terraform_service.refresh(devops)
        self.post_build()

    def destroy(self, auto_approve=False):
        devops = self.devops_repo.get_devops(self.project)
        self.terraform_service.destroy(devops, auto_approve=auto_approve)
        self.post_build()

    def tf_import(
        self,
        tf_import_name,
        tf_import_resource,
    ):
        devops = self.devops_repo.get_devops(self.project)
        self.terraform_service.tf_import(devops, tf_import_name, tf_import_resource)
        self.post_build()
