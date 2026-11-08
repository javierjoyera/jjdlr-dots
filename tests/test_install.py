"""Public installer checks with isolated homes and fake package managers."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ('format = "$directory$git_branch$git_commit$git_status$character"\n'
          'add_newline = false\n\n'
          '[directory]\nformat = "[$path]($style) "\nstyle = "bold #89b4fa"\n'
          'truncation_length = 3\ntruncate_to_repo = true\n\n'
          '[git_branch]\nformat = "on [$branch]($style) "\nstyle = "italic #cba6f7"\n'
          'truncation_length = 24\ntruncation_symbol = "…"\n\n'
          '[git_commit]\nformat = "at [$hash]($style) "\nstyle = "bold #94e2d5"\n\n'
          "[git_status]\nformat = '([\\[$all_status$ahead_behind\\]]($style) )'\n"
          'style = "bold #f9e2af"\n').encode()

COLORS = {"directory": "\x1b[1;38;2;137;180;250m",
          "branch": "\x1b[3;38;2;203;166;247m",
          "status": "\x1b[1;38;2;249;226;175m"}
COMMIT_COLOR = "\x1b[1;38;2;148;226;213m"
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
        self.env.pop("ZDOTDIR", None)
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

    def run_unix(self, extra=()):
        return subprocess.run(["sh", str(ROOT / "install.sh"), *extra], cwd=self.home,
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
        (self.bin / "starship").unlink()
        before = self.snapshot()
        self.assert_result(self.run_unix(), 1, "",
                           "Existing Starship config differs; nothing changed. "
                           "Re-run with --update to replace it and keep a backup.\n")
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.log.exists())

    def test_unix_update_backs_up_and_is_repeatable(self):
        for system, profile_name, shell in [("Darwin", ".zshrc", "zsh"),
                                             ("Linux", ".bashrc", "bash")]:
            with self.subTest(system=system):
                self.env["TEST_OS"] = system
                directory = ".config" if system == "Darwin" else "linux config"
                target = self.home / directory / "starship.toml"
                target.parent.mkdir()
                if system == "Linux":
                    self.env["STARSHIP_CONFIG"] = str(target)
                previous = f"# Previous {system} prompt\n".encode()
                target.write_bytes(previous)
                profile = self.home / profile_name
                profile.write_text("# Personal shell\n")
                self.assert_result(self.run_unix(["--update"]))
                self.assertEqual(target.read_bytes(), CONFIG)
                backups = set(target.parent.glob("starship.toml.bak-*"))
                self.assertEqual(len(backups), 1)
                backup = next(iter(backups))
                self.assertRegex(backup.name, r"^starship\.toml\.bak-\d{8}T\d{6}Z$")
                self.assertEqual(backup.read_bytes(), previous)
                expected = "# Personal shell\n"
                if shell == "bash":
                    expected += '\nexport PATH="$HOME/.local/bin:$PATH"\n'
                expected += f'\neval "$(starship init {shell})"\n'
                self.assertEqual(profile.read_text(), expected)
                before = self.snapshot()
                self.assert_result(self.run_unix(["--update"]))
                self.assertEqual(self.snapshot(), before)
                self.assertEqual(set(target.parent.glob("starship.toml.bak-*")), backups)
                self.assertFalse(self.log.exists())

    def test_unix_update_without_existing_config_makes_no_backup(self):
        self.assert_result(self.run_unix(["--update"]))
        target = self.home / ".config/starship.toml"
        self.assertEqual(target.read_bytes(), CONFIG)
        self.assertEqual(list(target.parent.glob("starship.toml.bak-*")), [])

    def test_unix_update_identical_config_does_not_write(self):
        self.assert_result(self.run_unix())
        target = self.home / ".config/starship.toml"
        before = self.snapshot()
        modified = target.stat().st_mtime_ns
        self.stub("cp", "exit 9\n")
        self.assert_result(self.run_unix(["--update"]))
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(target.stat().st_mtime_ns, modified)

    def test_unix_invalid_argument_leaves_everything_untouched(self):
        (self.bin / "starship").unlink()
        for extra in (["--invalid"], ["--update", "bad"], [""]):
            with self.subTest(extra=extra):
                before = self.snapshot()
                self.assert_result(self.run_unix(extra), 1, "",
                                   f"Unknown argument: {extra[-1]}. Usage: sh install.sh [--update]\n")
                self.assertEqual(self.snapshot(), before)
                self.assertFalse(self.log.exists())

    def test_unix_update_backup_failure_leaves_config_and_profile_untouched(self):
        target = self.home / ".config/starship.toml"
        target.parent.mkdir()
        target.write_text("# Personal prompt\n")
        (self.home / ".zshrc").write_text("# Personal shell\n")
        (self.bin / "starship").unlink()
        self.stub("cp", "exit 9\n")
        before = self.snapshot()
        self.assert_result(self.run_unix(["--update"]), 1, "",
                           "Could not back up the existing config; nothing changed.\n")
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

    def run_powershell(self, installed=True, install_exit=0, extra=()):
        profile = self.home / "PowerShell/Microsoft.PowerShell_profile.ps1"
        quote = lambda p: "'" + str(p).replace("'", "''") + "'"
        command = (f"Set-Variable HOME {quote(self.home)} -Force; "
                   f"$PROFILE = {quote(profile)}; $env:PATH = ''; "
                   "function winget { Add-Content -LiteralPath $env:INSTALL_LOG "
                   f"-Value ($args -join ' '); $global:LASTEXITCODE = {install_exit} }}; ")
        if installed:
            command += "function starship {}; "
        command += f"& {quote(ROOT / 'install.ps1')} " + " ".join(extra)
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
                           "Existing Starship config differs; nothing changed. "
                           "Re-run with -Update to replace it and keep a backup.\n")
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.log.exists())

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell is not installed")
    def test_powershell_update_backs_up_and_is_repeatable(self):
        target = self.home / ".config/starship.toml"
        target.parent.mkdir()
        previous = b"# Personal prompt\n"
        target.write_bytes(previous)
        profile = self.home / "PowerShell/Microsoft.PowerShell_profile.ps1"
        profile.parent.mkdir()
        profile.write_text("# Personal shell\n")
        self.assert_result(self.run_powershell(extra=["-Update"]))
        self.assertEqual(target.read_bytes(), CONFIG)
        backups = list(target.parent.glob("starship.toml.bak-*"))
        self.assertEqual(len(backups), 1)
        self.assertRegex(backups[0].name, r"^starship\.toml\.bak-\d{8}T\d{6}Z$")
        self.assertEqual(backups[0].read_bytes(), previous)
        self.assertEqual(profile.read_text(encoding="utf-8-sig"),
                         "# Personal shell\n\nInvoke-Expression (&starship init powershell)\n")
        before = self.snapshot()
        modified = target.stat().st_mtime_ns
        self.assert_result(self.run_powershell(extra=["-Update"]))
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(target.stat().st_mtime_ns, modified)
        self.assertFalse(self.log.exists())

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell is not installed")
    def test_powershell_failed_install_leaves_config_and_profile_untouched(self):
        before = self.snapshot()
        self.assert_result(self.run_powershell(installed=False, install_exit=7), 1, "",
                           "Starship installation failed.\n")
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.log.read_text(),
                         "install --id Starship.Starship --exact --source winget\n")


@unittest.skipUnless(shutil.which("starship") and shutil.which("git"),
                     "Starship or Git is not installed")
class PromptTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix=".prompt-test-", dir=ROOT)
        self.addCleanup(self.scratch.cleanup)
        self.home = Path(self.scratch.name) / "home"
        self.env = dict(os.environ, HOME=str(self.home),
                        STARSHIP_CONFIG=str(ROOT / "config/starship.toml"),
                        STARSHIP_CACHE=str(Path(self.scratch.name) / "cache"),
                        STARSHIP_SHELL="unknown", TERM="xterm-256color")
        self.env.pop("NO_COLOR", None)
        self.repo = self.make_repo()

    def make_repo(self, name="repo"):
        repo = self.home / "work" / name
        (repo / "src" / "components").mkdir(parents=True)
        self.git(repo, "init", "-q", "-b", "main")
        (repo / "file.txt").write_text("original\n")
        self.git(repo, "add", "file.txt")
        self.git(repo, "commit", "-qm", "init")
        return repo

    def git(self, repo, *args):
        return subprocess.run(["git", "-C", str(repo), "-c", "user.email=test@example.com",
                               "-c", "user.name=Test", *args], check=True, timeout=10,
                              env=self.env, capture_output=True, text=True).stdout

    def prompt(self, path, status=0):
        result = subprocess.run(
            [shutil.which("starship"), "prompt", "--path", str(path),
             "--logical-path", str(path), "--status", str(status)], cwd=path,
            env=self.env, capture_output=True, text=True, timeout=10)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        return result.stdout

    def plain(self, path, status=0):
        return re.sub(r"\x1b\[[0-9;]*m", "", self.prompt(path, status))

    def test_shows_path_from_repository_root(self):
        for path, shown in [(self.repo, "repo"),
                            (self.repo / "src", "repo/src"),
                            (self.repo / "src" / "components", "repo/src/components")]:
            with self.subTest(path=path.name):
                self.assertEqual(self.plain(path), f"{shown} on main \u276f ")

    def test_outside_repository_shortens_long_paths(self):
        self.env["GIT_DIR"] = str(self.home / "no-repository")
        drafts = self.home / "plain" / "notes" / "drafts"
        drafts.mkdir(parents=True)
        for path, shown in [(drafts, "plain/notes/drafts"), (self.home, "~")]:
            with self.subTest(path=path.name):
                self.assertEqual(self.plain(path), f"{shown} \u276f ")

    def test_indicator_keeps_success_and_failure_colors(self):
        for status, color in [(0, "32"), (1, "31")]:
            with self.subTest(status=status):
                self.assertIn(f"\x1b[1;{color}m\u276f", self.prompt(self.repo, status))

    def test_working_tree_status(self):
        cases = {
            "clean": (lambda repo: None, ""),
            "modified": (lambda repo: (repo / "file.txt").write_text("changed\n"), "[!]"),
            "deleted": (lambda repo: (repo / "file.txt").unlink(), "[\u2718]"),
            "staged": (lambda repo: ((repo / "file.txt").write_text("changed\n"),
                                     self.git(repo, "add", "file.txt")), "[+]"),
            "untracked": (lambda repo: (repo / "new.txt").write_text("new\n"), "[?]"),
        }
        for label, (change, marker) in cases.items():
            with self.subTest(state=label):
                repo = self.make_repo(name=f"status-{label}")
                change(repo)
                text = self.plain(repo)
                if marker:
                    self.assertIn(marker, text)
                else:
                    self.assertNotIn("[", text)

    def test_long_branch_name_is_truncated(self):
        self.git(self.repo, "checkout", "-q", "-b", "feature/a-very-long-branch-name")
        self.assertEqual(self.plain(self.repo), "repo on feature/a-very-long-bran\u2026 \u276f ")

    def test_detached_head_shows_short_commit(self):
        commit = self.git(self.repo, "rev-parse", "--short", "HEAD").strip()
        self.git(self.repo, "checkout", "-q", "--detach", "HEAD")
        self.assertEqual(self.plain(self.repo), f"repo on HEAD at {commit} \u276f ")
        self.assertIn(COMMIT_COLOR, self.prompt(self.repo))

    def test_catppuccin_colors(self):
        (self.repo / "file.txt").write_text("changed\n")
        output = self.prompt(self.repo)
        for element, escape in COLORS.items():
            with self.subTest(element=element):
                self.assertIn(escape, output)


if __name__ == "__main__":
    unittest.main()
