# Prueba de anchos (12 tamaños) con iframes

Edge headless **no baja de ~500 px** de ventana, así que `--window-size=320` engaña (captura recortada). Se prueba con iframes del ancho deseado dentro de una ventana grande.

## 1. Medir desbordes (todos los anchos de una vez)
Crear una página temporal servida por el mismo servidor (p. ej. `public/_test-responsive.html` en Next/Vite; **borrarla al terminar**). Escribirla con la herramienta Write, no con `sed` ni heredocs largos (se rompe la sintaxis en silencio).

```html
<!doctype html><meta charset="utf-8"><body><pre id="out">running</pre><script>
var widths=[280,320,360,390,412,600,768,1024,1280,1440,1920,2560];
var out=document.getElementById('out');var res=[];var i=0;
function next(){
  if(i>=widths.length){out.textContent=res.join('\n')+'\nDONE';return;}
  var w=widths[i++];var f=document.createElement('iframe');var done=false;
  f.style.cssText='border:0;width:'+w+'px;height:900px;position:absolute;left:0;top:0;opacity:0';
  function go(){
    if(done)return;done=true;
    try{
      var d=f.contentDocument;var bad=[];
      d.querySelectorAll('main *').forEach(function(el){   // cambiar 'main' si la raíz es otra
        if(el.closest('video'))return;
        var r=el.getBoundingClientRect();
        if(r.width>0&&(r.right>w+1||r.left<-1))bad.push(el.tagName.toLowerCase()+'.'+String(el.className).split(' ').slice(0,3).join('.')+' L'+Math.round(r.left)+' R'+Math.round(r.right));
      });
      var sw=d.documentElement.scrollWidth;
      res.push(w+'px: scrollWidth='+sw+(sw>w?' [DESBORDE]':'')+' | fuera='+bad.length+(bad.length?' '+bad.slice(0,4).join(' ; '):''));
    }catch(e){res.push(w+'px: ERROR '+e.message);}
    f.remove();out.textContent=res.join('\n');next();
  }
  f.onload=function(){setTimeout(go,1500);};
  setTimeout(go,10000);
  f.src='/RUTA';   // la ruta de la página a probar
  document.body.appendChild(f);
}
next();
</script>
```
Correr (bash): `msedge --headless=new --disable-gpu --virtual-time-budget=400000 --dump-dom http://localhost:PUERTO/_test-responsive.html | tr '\n' '~' | grep -o '<pre id="out">[^<]*' | tr '~' '\n'`

- `scrollWidth` = ancho − ~15 es normal (barra de scroll). Solo importa `[DESBORDE]` o `fuera>0`.
- Si la raíz tiene `overflow-x-hidden`, `scrollWidth` no delata nada: hay que mirar `fuera`.
- Ignorar desbordes intencionales (marquee).
- Debe ser mismo origen (si no, `contentDocument` falla).

## 2. Ver cómo se ve (captura por ancho)
Página con `<iframe style="width:Wpx;height:Hpx" src="http://localhost:PUERTO/ruta#ancla">` y `--window-size=` ≥ 500 de ancho (o igual al ancho si es mayor). Con anclas directas sin iframe, Edge a veces captura en blanco.
Mirar como mínimo: 320, 390, 768, 1440 y 2560. Revisar texto que se corta, `object-cover` que recorta lo importante, tarjetas apretadas y menú móvil.
