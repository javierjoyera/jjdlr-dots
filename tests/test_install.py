"""Public installer checks with isolated homes and fake package managers."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONFIG = b'format = "$character"\nadd_newline = false\n'
SUCCESS = "Starship configured. Open a new terminal.\n"


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix=".installer-test-", dir=ROOT)
        self.addCleanup(self.scratch.cleanup)
        self.home = Path(self.scratch.name) / "home with spaces"
        self.home.mkdir()
        self.bin = Path(self.scratch.name) / "bin"
        self.bin.mkdir()
        self.log = Path(self.scratch.name) / "install.log"
        self.env = dict(os.environ, HOME=str(self.home), PATH=f"{self.bin}:/usr/bin:/bin",
                        TEST_OS="Darwin", INSTALL_LOG=str(self.log), INSTALL_EXIT="0",
                        TMPDIR=self.scratch.name)
        self.env.pop("STARSHIP_CONFIG", None)
        self.stub("uname", 'printf "%s\\n" "$TEST_OS"\n')
        self.stub("starship", "exit 0\n")
        self.stub("brew", 'printf "brew:%s\\n" "$*" >> "$INSTALL_LOG"\nexit "$INSTALL_EXIT"\n')
        self.stub("curl", '''while [ "$#" -gt 0 ]; do
    if [ "$1" = "--output" ]; then shift; destination=$1; fi
    shift
done
printf '%s\n' 'printf "linux:%s\\n" "$*" >> "$INSTALL_LOG"' 'exit "$INSTALL_EXIT"' > "$destination"
''')

    def stub(self, name, content):
        path = self.bin / name
        path.write_text("#!/bin/sh\n" + content)
        path.chmod(0o755)

    def run_unix(self):
        return subprocess.run(["sh", str(ROOT / "install.sh")], cwd=self.home,
                              env=self.env, capture_output=True, text=True, timeout=10)

    def assert_result(self, result, code=0, out=SUCCESS, err=""):
        self.assertEqual((result.returncode, result.stdout, result.stderr), (code, out, err))

    def snapshot(self):
        return {str(p.relative_to(self.home)): p.read_bytes()
                for p in self.home.rglob("*") if p.is_file()}

    def test_minimal_prompt(self):
        self.assertEqual((ROOT / "config/starship.toml").read_bytes(), CONFIG)

    def test_unix_preserves_profile_and_is_repeatable(self):
        for system, profile_name, shell in [("Darwin", ".zshrc", "zsh"),
                                             ("Linux", ".bashrc", "bash")]:
            with self.subTest(system=system):
                self.env["TEST_OS"] = system
                profile = self.home / profile_name
                profile.write_text("# Keep my settings")
                self.assert_result(self.run_unix())
                self.assertTrue(profile.read_text().startswith("# Keep my settings\n"))
                self.assertEqual(profile.read_text().count(f'eval "$(starship init {shell})"'), 1)
                self.assertEqual((self.home / ".config/starship.toml").read_bytes(), CONFIG)
                before = self.snapshot()
                self.assert_result(self.run_unix())
                self.assertEqual(self.snapshot(), before)
                self.assertFalse(self.log.exists())

    def test_unix_installs_missing_binary(self):
        (self.bin / "starship").unlink()
        for system in ("Darwin", "Linux"):
            with self.subTest(system=system):
                self.env["TEST_OS"] = system
                self.assert_result(self.run_unix())
        self.assertEqual(self.log.read_text(),
                         f"brew:install starship\nlinux:--yes --bin-dir {self.home}/.local/bin\n")

    def test_unix_refuses_different_config_without_changes(self):
        target = self.home / ".config/starship.toml"
        target.parent.mkdir()
        target.write_text("# Personal prompt\n")
        (self.home / ".zshrc").write_text("# Personal shell\n")
        before = self.snapshot()
        self.assert_result(self.run_unix(), 1, "", "Existing Starship config differs; nothing changed.\n")
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.log.exists())

    def test_unix_failed_install_leaves_config_and_profile_untouched(self):
        (self.bin / "starship").unlink()
        self.env["INSTALL_EXIT"] = "7"
        for system in ("Darwin", "Linux"):
            with self.subTest(system=system):
                self.env["TEST_OS"] = system
                before = self.snapshot()
                self.assert_result(self.run_unix(), 1, "", "Starship installation failed.\n")
                self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.log.read_text(),
                         f"brew:install starship\nlinux:--yes --bin-dir {self.home}/.local/bin\n")

    def run_powershell(self, installed=True, install_exit=0):
        profile = self.home / "PowerShell/Microsoft.PowerShell_profile.ps1"
        quote = lambda p: "'" + str(p).replace("'", "''") + "'"
        command = (f"Set-Variable HOME {quote(self.home)} -Force; "
                   f"$PROFILE = {quote(profile)}; $env:PATH = ''; "
                   "function winget { Add-Content -LiteralPath $env:INSTALL_LOG "
                   f"-Value ($args -join ' '); $global:LASTEXITCODE = {install_exit} }}; ")
        if installed:
            command += "function starship {}; "
        command += f"& {quote(ROOT / 'install.ps1')}"
        return subprocess.run([shutil.which("pwsh"), "-NoProfile", "-Command", command],
                              env=self.env, capture_output=True, text=True, timeout=10)

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell is not installed")
    def test_powershell_preserves_profile_and_is_repeatable(self):
        profile = self.home / "PowerShell/Microsoft.PowerShell_profile.ps1"
        profile.parent.mkdir()
        profile.write_text("# Keep my settings")
        for attempt in range(2):
            self.assert_result(self.run_powershell())
            self.assertEqual((self.home / ".config/starship.toml").read_bytes(), CONFIG)
            self.assertEqual(profile.read_text(encoding="utf-8-sig").count(
                "Invoke-Expression (&starship init powershell)"), 1)
            self.assertTrue(profile.read_text(encoding="utf-8-sig").startswith("# Keep my settings\n"))
            if attempt == 0:
                before = self.snapshot()
            else:
                self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.log.exists())

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell is not installed")
    def test_powershell_installs_missing_binary(self):
        self.assert_result(self.run_powershell(installed=False))
        self.assertEqual(self.log.read_text(),
                         "install --id Starship.Starship --exact --source winget\n")
        self.assertEqual((self.home / ".config/starship.toml").read_bytes(), CONFIG)

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell is not installed")
    def test_powershell_refuses_different_config_without_changes(self):
        target = self.home / ".config/starship.toml"
        target.parent.mkdir()
        target.write_text("# Personal prompt\n")
        before = self.snapshot()
        self.assert_result(self.run_powershell(installed=False), 1, "",
                           "Existing Starship config differs; nothing changed.\n")
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.log.exists())

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell is not installed")
    def test_powershell_failed_install_leaves_config_and_profile_untouched(self):
        before = self.snapshot()
        self.assert_result(self.run_powershell(installed=False, install_exit=7), 1, "",
                           "Starship installation failed.\n")
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.log.read_text(),
                         "install --id Starship.Starship --exact --source winget\n")


if __name__ == "__main__":
    unittest.main()
