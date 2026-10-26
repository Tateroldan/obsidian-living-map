"""validar.py (avisa sin bloquear) y config.py (de dónde sale la bóveda)."""
import json, unittest

from base import Aislada


class Validar(Aislada):
    def validar(self, ruta):
        return self.correr("validar.py", entrada={"tool_name": "Write", "tool_input": {"file_path": str(ruta)}})

    def test_nota_sin_propiedades_avisa(self):
        p = self.validar(self.nota("Suelta.md", "hola\n"))
        self.assertEqual(p.returncode, 2)
        self.assertIn("Suelta.md", p.err)

    def test_secreto_pegado_avisa(self):
        clave = "sk-" + "a" * 30
        p = self.validar(self.nota("Llave.md", "---\ntipo: nota\n---\nmi clave " + clave + "\n"))
        self.assertEqual(p.returncode, 2)

    def test_fuera_de_la_boveda_no_opina(self):
        fuera = self.tmp / "fuera.md"
        fuera.write_text("sin nada\n", encoding="utf-8")
        self.assertEqual(self.validar(fuera).returncode, 0)

    def test_entrada_rota_no_estorba(self):
        self.assertEqual(self.correr("validar.py", entrada=b"{").returncode, 0)


class AyudaServidor(Aislada):
    def test_help_no_arranca_el_servidor(self):
        p = self.correr("server.py", "--help")
        self.assertEqual(p.returncode, 0, p.err)
        self.assertIn("--abrir", p.out)
        self.assertIn(str(self.boveda), p.out)


class Config(Aislada):
    def boveda_vista(self, env):
        p = self.correr("tests/_ver_config.py", env=env)
        self.assertEqual(p.returncode, 0, p.err)
        return p.out.strip()

    def test_variable_de_entorno_manda(self):
        self.prefs.write_text(json.dumps({"boveda": str(self.tmp / "otra")}), encoding="utf-8")
        self.assertEqual(self.boveda_vista(self.env), str(self.boveda))

    def test_sin_variable_usa_preferencias(self):
        self.prefs.write_text(json.dumps({"boveda": str(self.tmp / "otra")}), encoding="utf-8")
        env = {k: v for k, v in self.env.items() if k != "MAPA_BOVEDA"}
        self.assertEqual(self.boveda_vista(env), str(self.tmp / "otra"))

    def test_preferencias_rotas_no_truenan(self):
        self.prefs.write_text("no es json", encoding="utf-8")
        env = {k: v for k, v in self.env.items() if k != "MAPA_BOVEDA"}
        self.assertTrue(self.boveda_vista(env).endswith("Boveda"))


if __name__ == "__main__":
    unittest.main()
