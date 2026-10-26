"""Ayudas comunes de las pruebas: carpetas temporales y correr scripts del repo aislados.

Cada prueba usa su propia bóveda, log y preferencias (MAPA_BOVEDA, MAPA_LOG, MAPA_PREFS),
así nunca toca la configuración real de quien las corre.
"""
import json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


class Aislada(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="olm prueba "))  # con espacio a propósito
        self.boveda = self.tmp / "Mi Boveda"
        self.boveda.mkdir()
        self.log = self.tmp / "events.jsonl"
        self.prefs = self.tmp / "preferencias.json"
        self.env = dict(os.environ, MAPA_BOVEDA=str(self.boveda), MAPA_LOG=str(self.log),
                        MAPA_PREFS=str(self.prefs), PYTHONIOENCODING="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def correr(self, script, *args, entrada=None, env=None):
        """Corre un script del repo con el mismo Python; devuelve CompletedProcess (texto utf-8)."""
        datos = entrada if entrada is None or isinstance(entrada, bytes) else json.dumps(entrada).encode("utf-8")
        p = subprocess.run([sys.executable, str(RAIZ / script), *args], input=datos if datos is not None else b"",
                           capture_output=True, env=env or self.env, timeout=60)
        p.out = p.stdout.decode("utf-8", "replace")
        p.err = p.stderr.decode("utf-8", "replace")
        return p

    def nota(self, rel, texto):
        ruta = self.boveda / rel
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(texto, encoding="utf-8")
        return ruta

    def eventos(self):
        if not self.log.exists():
            return []
        return [json.loads(l) for l in self.log.read_text(encoding="utf-8").splitlines() if l.strip()]
