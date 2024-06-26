from e2clab.constants import NETWORK_CONF_FILE
from e2clab.errors import E2clabConfigError, E2clabFileError
from e2clab.network import Network
from e2clab.tests.unit import TestE2cLab


class TestUtils(TestE2cLab):

    def setUp(self) -> None:
        correct_conf = self.test_folder / NETWORK_CONF_FILE

        self.net = Network(config=correct_conf, roles=None, networks=None)

    def test_load_invalid_config(self):
        with self.assertRaises(E2clabConfigError):
            Network(
                config=self.test_folder / "invalid_network.yaml",
                roles=None,
                networks=None,
            )

        with self.assertRaises(E2clabFileError):
            Network(config="notafile", roles=None, networks=None)
