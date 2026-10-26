"""server.py: sirve el grafo y los eventos, solo en 127.0.0.1 y solo con un Host conocido."""
import http.client, json, socket, subprocess, sys, time, unittest

from base import Aislada, RAIZ


def puerto_libre():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Servidor(Aislada):
    def setUp(self):
        super().setUp()
        self.nota("Inicio.md", "---\ntipo: indice\n---\nVer [[Proyecto]]\n")
        self.nota("Proyecto.md", "---\ntipo: proyecto\n---\nVolver a [[Inicio]]\n")
        self.puerto = puerto_libre()
        self.env["MAPA_PUERTO"] = str(self.puerto)
        self.salida = open(self.tmp / "server.log", "w+b")
        self.proc = subprocess.Popen([sys.executable, str(RAIZ / "server.py")], env=self.env,
                                     stdout=self.salida, stderr=subprocess.STDOUT)
        for _ in range(100):  # hasta 10 s para que escuche
            if self.proc.poll() is not None:
                break
            try:
                socket.create_connection(("127.0.0.1", self.puerto), timeout=0.2).close()
                return
            except OSError:
                time.sleep(0.1)
        self.salida.seek(0)
        log = self.salida.read().decode("utf-8", "replace")
        self.tearDown()  # unittest no llama tearDown si setUp falla
        self.fail("el servidor no arrancó (código %s):\n%s" % (self.proc.returncode, log))

    def tearDown(self):
        if self.proc.poll() is None:
            self.proc.terminate()
            self.proc.wait(timeout=10)
        self.salida.close()
        super().tearDown()

    def pedir(self, ruta, host=None):
        c = http.client.HTTPConnection("127.0.0.1", self.puerto, timeout=10)
        c.request("GET", ruta, headers={"Host": host or "127.0.0.1:%d" % self.puerto})
        r = c.getresponse()
        cuerpo = r.read()
        c.close()
        return r.status, cuerpo

    def test_grafo_con_las_notas(self):
        status, cuerpo = self.pedir("/graph")
        self.assertEqual(status, 200)
        g = json.loads(cuerpo)
        self.assertGreaterEqual(len(g["nodes"]), 2)
        self.assertGreaterEqual(len(g["links"]), 1)

    def test_host_desconocido_se_rechaza(self):
        status, _ = self.pedir("/graph", host="evil.example:%d" % self.puerto)
        self.assertNotEqual(status, 200)

    def test_no_sirve_archivos_fuera_de_la_lista(self):
        for ruta in ("/config.py", "/../config.py", "/events.jsonl", "/preferencias.json"):
            status, _ = self.pedir(ruta)
            self.assertNotEqual(status, 200, ruta)

    def test_pagina_principal(self):
        status, cuerpo = self.pedir("/")
        self.assertEqual(status, 200)
        self.assertIn(b"<html", cuerpo.lower())

    def test_eventos_responde_json(self):
        status, cuerpo = self.pedir("/events?desde=0")
        self.assertEqual(status, 200)
        json.loads(cuerpo)


if __name__ == "__main__":
    unittest.main()
