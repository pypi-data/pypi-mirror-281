import warnings

from rich import print_json
from traitlets import Dict, Unicode

from ...application_base import JupyterKernelsBaseApp, jupyter_kernels_aliases
from ..utils import display_kernels

create_alias = dict(jupyter_kernels_aliases)
create_alias["given-name"] = "KernelCreateApp.kernel_given_name"


class KernelCreateApp(JupyterKernelsBaseApp):
    """An application to create a kernel."""

    description = """
      An application to create the kernel.

      jupyter kernels create SPEC_ID [--given-name CUSTOM_NAME]
    """

    aliases = Dict(create_alias)

    kernel_given_name = Unicode(
        None, allow_none=True, config=True, help="Kernel custom name."
    )

    def start(self):
        """Start the app."""
        if len(self.extra_args) > 1:  # pragma: no cover
            warnings.warn("Too many arguments were provided for kernel create.")
            self.print_help()
            self.exit(1)
        environment_name = self.extra_args[0]
        body = {"kernel_type": "default"}
        if self.kernel_given_name:
            body["kernel_given_name"] = self.kernel_given_name

        response = self._fetch(
            "{}/api/jupyter/v1/environment/{}".format(
                self.cloud_base_url, environment_name
            ),
            method="POST",
            json=body,
        )
        raw = response.json()
        kernel = raw.get("kernel")
        if kernel:
            display_kernels([kernel])
        else:
            print_json(data=raw)
