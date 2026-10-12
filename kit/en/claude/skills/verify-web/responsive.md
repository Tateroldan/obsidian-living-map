# Width test (12 sizes) with iframes

Headless Edge **doesn't go below ~500 px** of window, so `--window-size=320` lies (cropped capture). Test with iframes of the width you want inside a large window.

## 1. Measure overflows (all widths at once)
Create a temporary page served by the same server (e.g. `public/_test-responsive.html` in Next/Vite; **delete it when done**). Write it with the Write tool, not with `sed` or long heredocs (the syntax breaks silently).

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
      d.querySelectorAll('main *').forEach(function(el){   // change 'main' if the root is another element
        if(el.closest('video'))return;
        var r=el.getBoundingClientRect();
        if(r.width>0&&(r.right>w+1||r.left<-1))bad.push(el.tagName.toLowerCase()+'.'+String(el.className).split(' ').slice(0,3).join('.')+' L'+Math.round(r.left)+' R'+Math.round(r.right));
      });
      var sw=d.documentElement.scrollWidth;
      res.push(w+'px: scrollWidth='+sw+(sw>w?' [OVERFLOW]':'')+' | outside='+bad.length+(bad.length?' '+bad.slice(0,4).join(' ; '):''));
    }catch(e){res.push(w+'px: ERROR '+e.message);}
    f.remove();out.textContent=res.join('\n');next();
  }
  f.onload=function(){setTimeout(go,1500);};
  setTimeout(go,10000);
  f.src='/PATH';   // the route of the page under test
  document.body.appendChild(f);
}
next();
</script>
```
Run (bash): `msedge --headless=new --disable-gpu --virtual-time-budget=400000 --dump-dom http://localhost:PORT/_test-responsive.html | tr '\n' '~' | grep -o '<pre id="out">[^<]*' | tr '~' '\n'`

- `scrollWidth` = width − ~15 is normal (scrollbar). Only `[OVERFLOW]` or `outside>0` matter.
- If the root has `overflow-x-hidden`, `scrollWidth` reveals nothing: look at `outside`.
- Ignore intentional overflows (marquee).
- It must be same-origin (otherwise `contentDocument` fails).

## 2. See how it looks (capture per width)
A page with `<iframe style="width:Wpx;height:Hpx" src="http://localhost:PORT/route#anchor">` and `--window-size=` ≥ 500 wide (or equal to the width if larger). With direct anchors and no iframe, Edge sometimes captures a blank page.
Look at 320, 390, 768, 1440 and 2560 at least. Check cut-off text, `object-cover` cropping what matters, cramped cards and the mobile menu.
