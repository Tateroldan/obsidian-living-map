"""hook.py: qué rutas cuentan como «dentro de la bóveda» y qué se anota en events.jsonl."""
import unittest

from base import Aislada


class Hook(Aislada):
    def tocar(self, herramienta, entrada):
        p = self.correr("hook.py", entrada={"tool_name": herramienta, "tool_input": entrada, "session_id": "prueba123"})
        self.assertEqual(p.returncode, 0, p.err)

    def test_read_dentro_se_anota(self):
        self.tocar("Read", {"file_path": str(self.boveda / "Inicio.md")})
        ev = self.eventos()
        self.assertEqual(len(ev), 1)
        self.assertEqual(ev[0]["verb"], "read")
        self.assertTrue(ev[0]["path"].endswith("Mi Boveda/Inicio.md"))
        self.assertEqual(ev[0]["session"], "prueba123"[:8])

    def test_carpeta_hermana_con_mismo_prefijo_no_cuenta(self):
        self.tocar("Read", {"file_path": str(self.boveda) + "2/x.md"})
        self.assertEqual(self.eventos(), [])

    def test_fuera_de_la_boveda_no_se_anota(self):
        self.tocar("Read", {"file_path": str(self.tmp / "otra" / "x.md")})
        self.assertEqual(self.eventos(), [])

    def test_write_y_grep(self):
        self.tocar("Write", {"file_path": str(self.boveda / "Nueva.md")})
        self.tocar("Grep", {"path": str(self.boveda)})
        self.assertEqual([e["verb"] for e in self.eventos()], ["write", "search"])

    def test_bash_con_ruta_citada_sin_duplicar(self):
        ruta = (self.boveda / "Pendientes.md").as_posix()
        self.tocar("Bash", {"command": 'cat "%s"' % ruta})
        ev = self.eventos()
        self.assertEqual(len(ev), 1, ev)
        self.assertEqual(ev[0]["verb"], "read")

    def test_bash_que_escribe(self):
        ruta = (self.boveda / "Notas.md").as_posix()
        self.tocar("Bash", {"command": 'echo hola > "%s"' % ruta})
        self.assertEqual([e["verb"] for e in self.eventos()], ["write"])

    def test_entrada_rota_no_falla(self):
        p = self.correr("hook.py", entrada=b"esto no es json")
        self.assertEqual(p.returncode, 0)

    def test_log_rota_al_pasar_el_tope(self):
        self.log.write_bytes(b"x" * (5 * 1024 * 1024 + 1))
        self.tocar("Read", {"file_path": str(self.boveda / "Inicio.md")})
        self.assertTrue(self.log.with_name(self.log.name + ".1").exists())
        self.assertEqual(len(self.eventos()), 1)


if __name__ == "__main__":
    unittest.main()
