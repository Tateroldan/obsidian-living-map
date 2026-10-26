"""kit/instalar.py y kit/ajustes_hooks.py: instalación sin consola, idempotente y sin pisar nada."""
import json, sys, unittest
from pathlib import Path

from base import Aislada, RAIZ

sys.path.insert(0, str(RAIZ / "kit"))
import ajustes_hooks  # noqa: E402


class Instalar(Aislada):
    def setUp(self):
        super().setUp()
        self.claude = self.tmp / "claude"
        self.claude.mkdir()
        self.ajustes = self.claude / "settings.json"
        self.ajustes.write_text(json.dumps({"model": "x", "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo hi"}]}]}}),
                                encoding="utf-8")
        (self.claude / "CLAUDE.md").write_text("# mis reglas\n", encoding="utf-8")
        self.reglas = RAIZ / "reglas.json"
        self.reglas_existia = self.reglas.exists()  # el instalador la crea si falta: se borra al final

    def tearDown(self):
        if not self.reglas_existia and self.reglas.exists():
            self.reglas.unlink()
        super().tearDown()

    def instalar(self, *extra, lang="es"):
        p = self.correr("kit/instalar.py", "--lang", lang, "--boveda", str(self.boveda), "--claude-dir", str(self.claude), *extra)
        self.assertEqual(p.returncode, 0, p.out + p.err)
        return p

    def test_simulacro_no_escribe(self):
        self.instalar("--simulacro")
        self.assertEqual(list(self.boveda.iterdir()), [])
        self.assertEqual((self.claude / "CLAUDE.md").read_text(encoding="utf-8"), "# mis reglas\n")
        self.assertNotIn("PostToolUse", self.ajustes.read_text(encoding="utf-8"))
        self.assertFalse(self.prefs.exists())

    def test_sin_consola_y_sin_bandera_no_toca_claude_md(self):
        self.instalar("--si")
        self.assertNotIn("olm:inicio", (self.claude / "CLAUDE.md").read_text(encoding="utf-8"))

    def test_instalacion_completa(self):
        self.instalar("--si", "--claude-md", "--hooks")
        self.assertTrue((self.boveda / "Inicio.md").exists())
        md = (self.claude / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertTrue(md.startswith("# mis reglas"))
        self.assertIn("olm:inicio", md)
        self.assertNotIn("{{", md, "quedó una marca sin sustituir")
        self.assertIn(Path(sys.executable).as_posix(), md)
        self.assertTrue((self.claude / "CLAUDE.md.bak").exists())
        a = json.loads(self.ajustes.read_text(encoding="utf-8"))
        self.assertEqual(a["model"], "x")
        self.assertEqual(len(a["hooks"]["Stop"]), 1)
        self.assertEqual(len(a["hooks"]["PostToolUse"]), 2)
        self.assertEqual(len(a["hooks"]["SessionEnd"]), 1)
        self.assertEqual(json.loads(self.prefs.read_text(encoding="utf-8"))["boveda"], str(self.boveda))
        for agente in (self.claude / "agents").glob("*.md"):
            self.assertNotIn("{{", agente.read_text(encoding="utf-8"), agente.name)

    def test_segunda_vez_no_duplica(self):
        self.instalar("--si", "--claude-md", "--hooks")
        antes = self.ajustes.read_text(encoding="utf-8"), (self.claude / "CLAUDE.md").read_text(encoding="utf-8")
        self.instalar("--si", "--claude-md", "--hooks")
        despues = self.ajustes.read_text(encoding="utf-8"), (self.claude / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertEqual(antes, despues)

    def test_no_sobrescribe_notas_existentes(self):
        self.nota("Inicio.md", "mi inicio\n")
        self.instalar("--si")
        self.assertEqual((self.boveda / "Inicio.md").read_text(encoding="utf-8"), "mi inicio\n")

    def test_kit_en_ingles(self):
        self.instalar("--si", "--claude-md", lang="en")
        self.assertTrue((self.boveda / "Home.md").exists())
        self.assertNotIn("{{", (self.claude / "CLAUDE.md").read_text(encoding="utf-8"))


class AjustesHooks(Aislada):
    def test_settings_inexistente_se_crea(self):
        ruta = self.tmp / "nuevo" / "settings.json"
        self.assertEqual(len(ajustes_hooks.aplicar(ruta)), 3)
        self.assertEqual(ajustes_hooks.aplicar(ruta), [])

    def test_json_invalido_se_rechaza_sin_tocarlo(self):
        ruta = self.tmp / "settings.json"
        ruta.write_text("{ roto", encoding="utf-8")
        with self.assertRaises(SystemExit):
            ajustes_hooks.aplicar(ruta)
        self.assertEqual(ruta.read_text(encoding="utf-8"), "{ roto")

    def test_comando_con_comillas(self):
        c = ajustes_hooks.comando(Path("/a b/hook.py"))
        self.assertTrue(c.startswith('"') and c.endswith('/a b/hook.py"'), c)


if __name__ == "__main__":
    unittest.main()
