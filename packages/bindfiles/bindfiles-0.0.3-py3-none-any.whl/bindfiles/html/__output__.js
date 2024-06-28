(function(){/*

 Copyright The Closure Library Authors.
 SPDX-License-Identifier: Apache-2.0
*/
var aa = this || self;
function ba(a, b, c, d) {
  if (b.i !== c.i) {
    a.status = t;
  } else if (b.id || c.id) {
    a.status = b.id === c.id ? u : t;
  }
  if (a.status !== t) {
    var e = c.j.reduce((h, n) => {
      ca(b, n.key) || h.push(n.key);
      return h;
    }, []);
    e.length && a.C.push({step:da, D:e.length, B:() => e.forEach(h => c.h.removeAttribute(h))});
    var f = b.j.reduce((h, n) => {
      var k;
      a: {
        for (k = 0; k < c.j.length; k++) {
          if (n.key === c.j[k].key) {
            k = c.j[k].value;
            break a;
          }
        }
        k = void 0;
      }
      k !== n.value && h.push(n);
      return h;
    }, []);
    f.length && a.C.push({step:ea, D:f.length, B:() => f.forEach(h => c.h.setAttribute(h.key, h.value))});
    var g = b.l.reduce((h, n) => {
      var k;
      a: {
        for (k = 0; k < c.l.length; k++) {
          if (n.key === c.l[k].key) {
            k = c.l[k].value;
            break a;
          }
        }
        k = void 0;
      }
      k !== n.value && h.push(n);
      return h;
    }, []);
    g.length && a.C.push({step:fa, D:g.length, B:() => g.forEach(h => {
      c.node instanceof HTMLInputElement && ("value" === h.key && (c.node.value = h.value), "checked" === h.key && (c.node.checked = h.value));
    })});
    b.o !== c.o && a.C.push({step:ha, D:1, B:() => {
      c.node.textContent = b.o;
    }});
    if (d) {
      let h = ia(d, b.node), n = ia(d, c.node), k = [], l = [];
      n.forEach((m, p) => {
        let q = !0;
        h.forEach(r => {
          m.event === r.event && m.hash === r.hash && (q = !1);
        });
        q && k.push(p);
      });
      h.forEach((m, p) => {
        let q = !0;
        n.forEach(r => {
          r.event === m.event && r.hash === m.hash && (q = !1);
        });
        q && l.push(p);
      });
      k.length && a.C.push({step:ja, D:k.length, B:() => {
        k.forEach(m => c.node.removeEventListener(n[m].event, n[m].B));
        k.sort((m, p) => m < p ? 1 : p < m ? -1 : 0).forEach(m => n.splice(m, 1));
        d.g.set(c.node, n);
      }});
      l.length && a.C.push({step:ka, D:l.length, B:() => {
        l.forEach(m => {
          c.node.addEventListener(h[m].event, h[m].B);
          n.push({event:h[m].event, B:h[m].B, hash:h[m].hash});
          d.g.set(c.node, n);
        });
      }});
    }
  }
}
function la(a, b, c, d) {
  let e = b.g.map(() => !1), f = c.g.map(() => !1), g = [], h = [];
  b.g.forEach((l, m) => {
    c.g.forEach((p, q) => {
      e[m] || f[q] || (p = new ma(l, p, d), p.status !== t && (p.status === u || 0 === p.g ? (e[m] = !0, f[q] = !0, g.push({H:m, S:q, N:q}), p.status === u ? a.j++ : a.i++, a.h.push(p)) : h.push({Z:m, X:q, T:p, Ma:p.g, selected:!1})));
    });
  });
  0 < h.length && (h = h.sort((l, m) => l.T.g < m.T.g ? -1 : l.T.g === m.T.g ? 0 : 1), h.forEach(l => {
    e[l.Z] || f[l.X] || (e[l.Z] = !0, f[l.X] = !0, l.selected = !0, g.push({H:l.Z, S:l.X, N:l.X}), a.h.push(l.T));
  }));
  let n = f.reduce((l, m, p) => m ? l : [...l, p], []);
  n.length && (a.C.push({step:na, D:n.length, B:() => n.forEach(l => {
    c.node.removeChild(c.g[l].node);
  })}), n.forEach(l => {
    g = g.map(m => l > m.S ? m : {H:m.H, S:m.S, N:m.N - 1});
  }));
  let k = e.reduce((l, m, p) => m ? l : [...l, p], []);
  k.length && (a.C.push({step:oa, D:k.length, B:() => k.forEach(l => {
    c.node.appendChild(b.g[l].node);
  })}), k.forEach(l => g.push({H:l, S:Number.NaN, N:g.length})));
  if (g.reduce((l, m) => l || m.N !== m.H, !1)) {
    let l = g.sort((m, p) => m.H < p.H ? -1 : m.H === p.H ? 0 : 1).map(m => m.N);
    a.C.push({step:pa, D:1, B:() => {
      for (let m = 0; m < l.length; m++) {
        if (m != l[m]) {
          let p = l[m];
          if (c.node instanceof HTMLElement || c.node instanceof SVGElement) {
            let q = c.node.childNodes[m], r = c.node.childNodes[p];
            l.splice(m, 1, m);
            l = l.map(v => v + (v >= m && v < p ? 1 : 0));
            c.node.insertBefore(r, q);
          }
        }
      }
    }});
  }
}
function qa(a) {
  if (a.status === t) {
    return 0;
  }
  let b = 0;
  a.C.forEach(c => b += w[c.step] * c.D);
  b += w[ra] * a.i;
  b += w[sa] * a.j;
  a.h.forEach(c => b += c.g);
  return b;
}
class ma {
  constructor(a, b, c, d) {
    this.C = [];
    this.status = ta;
    this.h = [];
    this.g = Number.NaN;
    this.j = this.i = 0;
    if (!0 !== d && (ba(this, a, b, c), this.status === t)) {
      return;
    }
    if (z.has(a.h)) {
      d = z.get(a.h);
      if (!z.has(b.h)) {
        var e = b.h.attachShadow({mode:d.mode});
        z.set(b.h, e);
      }
      e = z.get(b.h);
      ua(d, e, !0, c);
    } else {
      z.has(b.h) && (this.status = t, console.log("n\u00e3o tira sr"));
    }
    this.status !== t && (la(this, a, b, c), this.g = qa(this));
  }
  update() {
    this.h.forEach(a => {
      a.update();
    });
    this.C.forEach(a => {
      try {
        a.B();
      } catch (b) {
        console.error(a.step, b);
      }
    });
  }
}
function ua(a, b, c, d) {
  let e = "string" !== typeof a ? a : A("div", g => g.innerHTML = a);
  b instanceof ShadowRoot && e instanceof HTMLElement && e.attributes.length && (e = A("div", g => g.appendChild(e)));
  let f = va(e);
  b = va(b);
  (new ma(f, b, d, c)).update();
}
;function va(a) {
  function b(e) {
    d.currentNode.childNodes.length !== e.g.length ? (d.firstChild(), e = new wa(d.currentNode, e), b(e)) : d.nextSibling() ? (e = new wa(d.currentNode, e.A), b(e)) : (d.parentNode(), d.currentNode && e.A && b(e.A));
  }
  function c(e) {
    e.g = e.g.filter(f => {
      let g = f.node instanceof Text ? 0 < f.node.textContent.trim().length : !0;
      g || e.node.removeChild(f.node);
      return g;
    });
    e.g.forEach(f => c(f));
  }
  let d = document.createTreeWalker(a, NodeFilter.SHOW_ALL);
  a = new wa(a);
  b(a);
  c(a);
  return a;
}
function ca(a, b) {
  return b ? a.j.reduce((c, d) => c || d.key === b, !1) : a.node instanceof HTMLElement ? !0 : !1;
}
function xa(a) {
  let b = [];
  var c = [];
  if (a.node instanceof HTMLElement || a.node instanceof SVGElement) {
    c = a.node.attributes;
    for (let d = 0; d < c.length; d++) {
      b.push(c[d]);
    }
    c = b.reduce((d, e) => {
      "id" === e.localName && (a.id = e.value);
      d.push({key:e.localName, value:e.value});
      return d;
    }, []);
  }
  return c;
}
class wa {
  constructor(a, b) {
    b && (this.A = b);
    this.node = a;
    this.g = [];
    b && b.g.push(this);
    this.o = null;
    this.j = xa(this);
    this.l = [];
    this.id = "";
    a instanceof HTMLElement || a instanceof SVGElement ? (this.h = a, this.i = this.h.localName, a instanceof HTMLInputElement && (this.l.push({key:"value", value:a.value}), this.l.push({key:"checked", value:a.checked}))) : a instanceof Text ? (this.i = ya, this.o = a.textContent) : a instanceof ShadowRoot ? this.i = za : a instanceof Comment ? this.i = Aa : (this.i = a.constructor.name, console.log("TYPE", a, this.i));
  }
  toString(a = 0) {
    const b = "    ".repeat(a);
    let c = `${b}<${this.i}>\n`;
    this.g.forEach(d => {
      c += `${d.toString(a + 1)}`;
    });
    return c += `${b}</${this.i}>\n`;
  }
}
;var oa = 1, na = 2, pa = 3, ha = 4, ea = 5, da = 6, fa = 7, ka = 8, ja = 9, ra = 10, sa = 11, ya = "-Text", Aa = "!--", za = "div", t = 1, ta = 2, u = 3;
function ia(a, b) {
  return (a = a.g.get(b)) ? a : [];
}
class Ba {
  constructor() {
    this.g = new WeakMap();
    this.h = (a, b, c) => {
      let d = this.g.get(a);
      d || (d = [], this.g.set(a, d));
      if (!Ca.has(c)) {
        a = c.toString();
        let e = 0;
        for (let f = 0; f < a.length; f++) {
          e = (e << 5) - e + a.charCodeAt(f), e |= 0;
        }
        Ca.set(c, e);
      }
      a = Ca.get(c);
      d.push({event:b, B:c, hash:a});
    };
  }
}
var Ca = new WeakMap();
const w = {[da]:1, [ea]:1, [fa]:1, [oa]:10, [ha]:1, [pa]:1, [na]:10, [ka]:1, [ja]:1, [ra]:-100.11, [sa]:-100.33, [12]:0};
function Da() {
  let a = window.location.search.substring(1).split("&"), b = {};
  for (let c = 0; c < a.length; ++c) {
    let d = a[c].split("=", 2);
    b[d[0]] = 1 == d.length ? "" : decodeURIComponent(d[1].replace(/\+/g, " "));
  }
  return b;
}
const B = {J:{ga:function(a, b, c) {
  let d = 1;
  for (;;) {
    var e = 0;
    for (var f = 2; f <= d; f++) {
      e += Math.pow(b, f - 1);
    }
    e = a - e;
    f = [];
    for (let g = 1; g <= d; g++) {
      let h = e % b;
      f.splice(0, 0, c(h));
      e -= h;
      e /= b;
    }
    if (e) {
      d++;
    } else {
      return f.join("");
    }
  }
}, sa:function(a, b) {
  return B.J.ea(new Date(a), b);
}, ea:function(a, b) {
  const c = a.getDate().toString().padStart(2, "0"), d = (a.getMonth() + 1).toString().padStart(2, "0"), e = a.getFullYear(), f = a.getHours().toString().padStart(2, "0"), g = a.getMinutes().toString().padStart(2, "0");
  a = a.getSeconds().toString().padStart(2, "0");
  return b ? `${c}/${d}/${e} ${f}:${g}:${a}` : `${d}/${c}/${e} ${f}:${g}:${a}`;
}, La:function(a) {
  const [b, c, d] = a.split("-").map(e => parseInt(e, 10));
  return new Date(b, c - 1, d);
}, ua:function(a, b) {
  const [c, d, e] = a.split("-").map(f => parseInt(f, 10));
  return B.J.ea(new Date(c, d - 1, e), b);
}, va:function(a) {
  return B.J.ta(new Date(a));
}, ta:function(a) {
  return `${a.getFullYear()}-${(a.getMonth() + 1).toString().padStart(2, "0")}-${a.getDate().toString().padStart(2, "0")}`;
}, Oa:function(a) {
  return B.J.ga(a, 26, b => String.fromCharCode(65 + b));
}, Pa:function(a) {
  return B.J.ga(a, 64, b => 10 > b ? String.fromCharCode(48 + b - 0) : 36 > b ? String.fromCharCode(65 + b - 10) : 62 > b ? String.fromCharCode(97 + b - 36) : 62 === b ? "-" : "+");
}, Ba:async function(a) {
  return new Promise((b, c) => {
    const d = a instanceof Blob ? a : new Blob([a]), e = new FileReader();
    e.onloadend = function() {
      b(e.result.split(",")[1]);
    };
    e.onerror = c;
    e.readAsDataURL(d);
  });
}, Ka:function(a) {
  return a.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}}, debug:{Qa:function() {
  let a = new Date();
  return a.getHours().toString().padStart(2, "0") + ":" + a.getMinutes().toString().padStart(2, "0") + ":" + a.getSeconds().toString().padStart(2, "0");
}}, actions:{Aa:async function(a) {
  return new Promise(b => setTimeout(b, a));
}, Ta:function(a) {
  const b = (new Date()).getTime();
  for (; (new Date()).getTime() - b < a;) {
  }
}}, Sa:function(a) {
  return Math.floor((new Date(a) - a) / 6E4);
}, K:{Ha:function(a = 200, b = 440, c = 1, d = "sine") {
  const e = new (window.AudioContext || window.webkitAudioContext)(), f = e.createOscillator(), g = e.createGain();
  f.connect(g);
  g.connect(e.destination);
  g.gain.value = c;
  f.frequency.value = b;
  f.type = d;
  f.start(e.currentTime);
  f.stop(e.currentTime + 0.001 * a);
}, fa:function(a = 200, b = 400, c = 1, d = "square") {
  const e = new (window.AudioContext || window.webkitAudioContext)(), f = e.createOscillator(), g = e.createGain();
  f.connect(g);
  g.connect(e.destination);
  g.gain.value = c;
  f.frequency.value = b;
  f.type = d;
  f.start();
  f.stop(e.currentTime + a / 1000);
}, Ra:() => B.K.fa(100, 400, 0.2, "square"), wa:() => B.K.fa(200, 300, 0.3, "sawtooth"), R:function() {
  const a = new (window.AudioContext || window.webkitAudioContext)(), b = a.createOscillator();
  b.type = "sine";
  b.frequency.setValueAtTime(440, a.currentTime);
  const c = a.createGain();
  c.gain.setValueAtTime(0, a.currentTime);
  c.gain.linearRampToValueAtTime(0.3, a.currentTime + 0.01);
  c.gain.linearRampToValueAtTime(0, a.currentTime + 0.3);
  b.connect(c);
  c.connect(a.destination);
  b.start(a.currentTime);
  b.stop(a.currentTime + 0.3);
}}};
var C = ["arrayBuffer_pos", "_type_"];
async function Ea(a) {
  let b = {}, c = [];
  for (let [d, e] of a.entries()) {
    e instanceof Blob ? (a = c.length, c.push(await e.arrayBuffer()), b[d] = C[0] + a.toString() + C[1] + e.type) : b[d] = e;
  }
  return {form:b, buffer:c};
}
function Fa(a, b) {
  let c = new FormData();
  const d = new RegExp(`"${C[0]}(\\d+)${C[1]}(.*)`);
  for (let [e, f]in Object.entries(a)) {
    if (a = "string" === typeof f ? f.match(d) : null) {
      const [, g, h] = a;
      a = parseInt(g, 10);
      if (!isNaN(a) && b && b[a]) {
        c.append(e, new Blob([b[a]], {type:h}));
      } else {
        throw Error(`erro ao ler buffer ${e} ${f}`);
      }
    } else {
      c.append(e, f);
    }
  }
  return c;
}
;function Ga(a, b, c = null) {
  let d = IPython.notebook.kernel.comm_manager, e = {}, f = d.g(a), g = h => {
    h = h.content.data;
    e[h?._msgid ?? null] && (e[h._msgid].resolve(h), delete e[h._msgid]);
  };
  c ? c.push(g) : d.h(b, h => {
    h.g(g);
  });
  return async function(h) {
    console.log("py_calc", h);
    let n = f.send(h);
    return new Promise((k, l) => {
      e[n] = {resolve:k, reject:l};
    });
  };
}
;async function Ha(a) {
  if (a.form) {
    if (a.form instanceof FormData) {
      let b = await Ea(a.form);
      a.form = b.form;
      a.buffer = b.buffer;
    }
    a.headers || (a.headers = {});
    a.headers["Content-Type"] = "multipart/form-data";
  }
  a.json && (a.headers || (a.headers = {}), a.headers["Content-Type"] = "application/json", a.content = JSON.stringify(a.json));
}
function Ia(a) {
  let b = {};
  a.method && (b.method = a.method);
  a.headers && (b.headers = a.headers);
  if (1 < ["json", "form", "content"].reduce((c, d) => a[d] ? 1 : 0, 0) || a.buffer && (a.json || a.content)) {
    throw Error("par\u00e2metros em excesso", a);
  }
  if (a.json) {
    b.body = JSON.stringify(a.json), b.headers || (b.headers = {"Content-Type":"application/json"});
  } else if (a.form) {
    b.body = a.form instanceof FormData ? a.form : Fa(a.form, a.buffer);
  } else if (a.content && (b.body = a.content, b.headers = a.headers, !a.headers)) {
    throw Error("cabe\u00e7alho indefinido", a);
  }
  return {url:a?.url ?? "", za:b};
}
class Ja {
  async send(a) {
    a = Ia(a);
    return await this.g(a.url, a.za);
  }
  async g(a, b) {
    return await fetch(a, b);
  }
}
async function Ka(a, b) {
  a = {url:a};
  try {
    if (b) {
      let c, d;
      for (let [e, f] of Object.entries(b)) {
        if ("body" === e) {
          c = f;
        } else if ("headers" === e) {
          a.headers = d = f;
        } else if ("method" === e) {
          a.method = f;
        } else {
          throw Error("fetch_direct - RequestInit key - incluir " + typeof e);
        }
      }
      b = d?.["Content-Type"];
      c instanceof FormData ? (a.form = c, c = void 0) : "string" === typeof c ? "text/plain application/x-www-form-urlencoded text/xml application/xml text/html application/json".split(" ").includes(b) && (a.content = c, c = void 0) : c instanceof Blob ? (b || (b = c.type, a.headers || (a.headers = {}), b ||= "application/octet-stream", a.headers["Content-Type"] = b), a.buffer = [await c.arrayBuffer()], c = void 0) : c instanceof ArrayBuffer && (a.headers || (a.headers = {}), b ||= "application/octet-stream", 
      a.headers["Content-Type"] = b, a.buffer = [c], c = void 0);
      if (c) {
        throw Error("fetch_direct, body type=" + typeof c + ", incluir tipo = ", b);
      }
    }
  } catch (c) {
    console.log("erro=", c);
  }
  return a;
}
class La {
  constructor(a) {
    this.h = a;
  }
  async send(a) {
    await Ha(a);
    a = await this.h(a);
    let b = null, c = {};
    a.headers && (c.headers = a.headers);
    a.status && (c.status = a.status);
    let d = a?.headers?.["Content-Type"] ?? null;
    a.response && d ? b = new Response(new Blob([a.response], {type:d}), c) : (a?.buffer.length ?? !1) && d ? b = new Response(new Blob(a.buffer, {type:d}), c) : a.response || (b = new Response(null, c));
    if (b) {
      return b;
    }
    throw Error("Response sem mimetype");
  }
  async g(a, b) {
    a = await Ka(a, b);
    await Ha(a);
    return await this.send(a);
  }
}
;function D(a) {
  return new Promise((b, c) => {
    a.onsuccess = () => b(a.result);
    a.onerror = () => c(a.error);
  });
}
function Ma(a, b) {
  a = indexedDB.open(a);
  a.onupgradeneeded = d => {
    d = d.target.result;
    d.objectStoreNames.contains(b) || d.createObjectStore(b);
  };
  const c = D(a);
  return (d, e) => c.then(f => {
    f = f.transaction(b, d).objectStore(b);
    return e(f);
  });
}
let Na;
function E() {
  Na ||= Ma("keyval-store", "keyval");
  return Na;
}
function F(a, b) {
  return a("readonly", c => {
    c = c.openCursor();
    c.onsuccess = d => {
      if (d = d.target.result) {
        b(d), d.continue();
      }
    };
    return D(c);
  });
}
class Oa {
  constructor(a) {
    this.g = Ma(...a.split("."));
  }
  async get(a) {
    return G.get(a, this.g);
  }
  async set(a, b) {
    return G.set(a, b, this.g);
  }
  async L(a) {
    return G.L(a, this.g);
  }
  async clear() {
    return G.clear(this.g);
  }
  l() {
  }
}
class Pa {
  constructor(a) {
    a && (this.g = a);
  }
  async get(a) {
    return this.g.get(a);
  }
  async set(a, b) {
    return this.g.set(a, b);
  }
  async L(a) {
    return this.g.L(a);
  }
  async clear() {
    return this.g.clear();
  }
  l() {
    this.g.l();
  }
}
function Qa(a, b) {
  a.j.set(null, async(c, d) => {
    let e = Ra(a, d);
    return await a.h.g(e, {method:"POST", headers:{"Content-Type":"application/json"}, body:b(c, d)});
  });
}
function Ra(a, b) {
  let [c, d] = [encodeURIComponent(a.o), encodeURIComponent(b)];
  return `${a.A}?${c}=${d}`;
}
class Sa {
  constructor(a, b = null) {
    this.g = new Map();
    this.A = a;
    this.o = "key";
    this.h = b ? b : new Ja();
    this.i = new Map();
    this.j = new Map();
    this.i.set(null, async c => {
      try {
        return await c.json();
      } catch (d) {
        console.log(d);
      }
    });
    Qa(this, c => JSON.stringify(c));
  }
  l() {
    this.g.clear();
  }
  async get(a) {
    if (this.g.has(a)) {
      return this.g.get(a);
    }
    var b = await this.h.g(Ra(this, a));
    let c = this.i.has(a) ? this.i.get(a) : this.i.get(null);
    if (!c) {
      throw Error();
    }
    b = await c(b, a);
    this.g.set(a, b);
    return b;
  }
  async set(a, b) {
    let c = this.j.has(a) ? this.j.get(a) : this.j.get(null);
    if (!c) {
      throw Error();
    }
    await c(b, a);
    this.g.set(a, b);
  }
  async L(a) {
    this.g.delete(a);
    await this.h.g(Ra(this, a), {method:"DELETE"});
  }
  async clear() {
    this.g.clear();
    await this.h.g(this.A, {method:"DELETE"});
  }
}
async function Ta(a) {
  a.g = [];
  var b = await indexedDB.databases();
  for (let c of b) {
    c.name && (b = await Ua(c.name), a.g.push({name:c.name, version:c.version ?? -1, ja:b.ja, keys:b.keys}));
  }
}
async function Ua(a) {
  const b = indexedDB.open(a);
  return new Promise((c, d) => {
    b.onsuccess = async function() {
      const e = b.result, f = Array.from(e.objectStoreNames), g = [];
      for (let h of f) {
        const n = e.transaction(h, "readwrite").objectStore(h).getAllKeys();
        await (async() => {
          let k = await D(n);
          for (let l of k) {
            g.push({store:h, key:l});
          }
        })();
      }
      e.close();
      c({ja:f, keys:g});
    };
    b.onerror = () => d(b.error);
  });
}
class Va {
  constructor() {
    this.g = [];
    Ta(this);
  }
  async clear() {
    const a = await indexedDB.databases();
    for (let b of a) {
      b.name && indexedDB.deleteDatabase(b.name);
    }
  }
}
const G = {get:function(a, b = E()) {
  return b("readonly", c => D(c.get(a)));
}, set:function(a, b, c = E()) {
  return c("readwrite", d => {
    d = d.put(b, a);
    return D(d);
  });
}, update:function(a, b, c = E()) {
  return c("readwrite", d => new Promise((e, f) => {
    const g = d.get(a);
    g.onsuccess = () => {
      try {
        const h = b(g.result, a), n = d.put(h, a);
        e(D(n));
      } catch (h) {
        f(h);
      }
    };
    g.onerror = function() {
      f(g.error);
    };
  }));
}, L:function(a, b = E()) {
  return b("readwrite", c => D(c.delete(a)));
}, clear:function(a = E()) {
  return a("readwrite", b => D(b.clear()));
}, Na:function(a, b = E()) {
  return b("readonly", c => Promise.all(a.map(d => D(c.get(d)))));
}, Ja:F, keys:function(a = E()) {
  const b = [];
  return F(a, c => b.push(c.key)).then(() => b);
}, values:function(a = E()) {
  const b = [];
  return F(a, c => b.push(c.value)).then(() => b);
}, entries:function(a = E()) {
  const b = [];
  return F(a, c => b.push({key:c.key, value:c.value})).then(() => b);
}, Ia:Ma, Ga:Oa, ma:Va, oa:Sa, na:Pa};
var Wa = a => {
  a = a.folder && a.name ? `${a.folder}/${a.name}` : a.folder ? a.folder : a.name;
  a = a.split("/").reduce((b, c) => {
    c && b.push(c);
    return b;
  }, []);
  return a.join("/");
}, Xa = new Map();
function Ya(a, b) {
  const c = [];
  let d = 0;
  return {t:a.replace(/\/\*([\s\S]*?)\*\//g, (e, f) => {
    c.push(f.trim());
    e = b(d);
    d++;
    return e;
  }), a:c};
}
function Za(a) {
  var b = /__c\d{3}c__/;
  let c = [];
  a.split("}").filter(d => "" !== d.trim()).forEach(d => {
    const [e, f] = d.split("{");
    d = f.trim().split(";").filter(h => "" !== h.trim());
    let g = `s.add_chain('${e.trim()}', a => {`;
    d.forEach(h => {
      g = b.test(h) ? g + ` // ${h.replace(/\/\*|\*\//g, "").trim()}` : g + `\n   a('${h.trim()};');`;
    });
    g += "\n});\n";
    c.push(g);
  });
  return c.join("\n");
}
console.log("DEVTOOLS ATIVO");
window.DEV = {Da:function(a) {
  function b(d, e = !0) {
    d = `__c${String(d).padStart(3, "0")}c__`;
    e && (d += ";");
    return d;
  }
  a = Ya(a, b);
  let c = Za(a.t);
  a.a.forEach((d, e) => {
    c = c.replace(b(e, !1), d);
  });
  console.log(c);
}, Ca:function(a) {
  a = a.split("\n");
  const b = Math.min(...a.filter(Boolean).map(c => {
    c = c.search(/\S|$/);
    return 2 < c ? c : 5;
  }));
  console.log(b);
  a = a.map(c => " ".repeat(b) + "//" + c.substring(b));
  console.log(a.join("\n"));
}, Ea:G.ma, Fa:function() {
  const a = [];
  for (let [b, c] of Xa.entries()) {
    let d = 0;
    for (let [e, f] of c.entries()) {
      a.push({ext:b, M:e, n:d, D:f.length}), d++;
    }
  }
  console.log("\nORDEM EXTENS\u00c3O");
  a.sort((b, c) => b.ext < c.ext ? -1 : 1);
  a.forEach(b => console.log(`${b.ext} , ${b.M} , ${b.n},  ${b.D},`));
  console.log("\nORDEM MIMETYPE");
  a.sort((b, c) => b.M < c.M ? -1 : 1);
  a.forEach(b => console.log(`${b.M} , ${b.ext} , ${b.n},  ${b.D},`));
  console.log("\nEXP JSCODE");
  a.sort((b, c) => b.ext < c.ext ? -1 : b.ext === c.ext && b.D > c.D ? -1 : 1);
  a.map(b => console.log(`{'${b.ext}':'${b.M}'},`));
  console.log(a.reduce((b, c) => {
    b.push(`['${c.ext}','${c.M}'],`);
    return b;
  }, []).join("\n"));
}};
var $a = G, H = B;
var ab = new Ba(), bb = new WeakMap(), z = new WeakMap();
class cb {
  constructor(a) {
    this.g = a;
  }
  get j() {
    return this.g;
  }
  get h() {
    return this.g;
  }
  get button() {
    return this.g;
  }
  get style() {
    return this.g;
  }
  get l() {
    return this.g;
  }
  get i() {
    return this.g;
  }
  get a() {
    return this.g;
  }
  get label() {
    return this.g;
  }
}
function A(a, b) {
  a = document.createElement(a);
  b && b(a);
  return a;
}
async function db(a, b, c) {
  a = document.createElement(a);
  c && c.appendChild(a);
  c = new eb(a);
  b && await b(c);
  return c;
}
async function fb(a, b) {
  let c = await db(b && "tagName" in b ? b.tagName.toLocaleLowerCase() : "div");
  c.e.innerHTML = a;
  b.appendChild(c.h);
  return c;
}
function I(a, b, c) {
  let d = [];
  c(e => d.push(e));
  a.data.push({ia:b, rules:d.join("")});
}
function gb(a, b) {
  A("style", c => {
    b.e.appendChild(c);
    c.innerText = a.data.map(d => `${d.ia} { ${d.rules} }`).join(" ");
  });
}
class hb {
  constructor() {
    this.data = [];
  }
  add(a, b) {
    this.data.push({ia:a, rules:b});
  }
}
function ib(a) {
  return new Proxy(a, {get:(b, c) => "addEventListener" === c ? (d, e, f) => {
    ab.h(b, d, e);
    return b.addEventListener(d, e, f);
  } : "function" === typeof b[c] ? b[c].bind(b) : b[c], set:(b, c, d) => {
    "string" === typeof c && c.toLowerCase().startsWith("on") ? (c = c.substring(2), ab.h(b, c, d), b.addEventListener(c, d)) : b[c] = d;
    return !0;
  }});
}
async function J(a, b, c) {
  return db(b, c, a.g);
}
async function jb(a, b) {
  return fb(b, a.g);
}
function kb(a, b) {
  let c = new hb();
  b(c);
  gb(c, a);
}
async function lb(a) {
  var b = await J(a, "div");
  if ("attachShadow" in a.g) {
    return b = b.g.attachShadow({mode:"open"}), z.set(a.g, b), new eb(b);
  }
  throw Error("attachShadow");
}
class eb {
  constructor(a) {
    this.g = a;
    this.i = ib(a);
    this.t = new cb(a);
  }
  get e() {
    return this.i;
  }
  get h() {
    return this.g;
  }
}
async function mb(a, b, c) {
  b = 1000 / b;
  let d = Date.now();
  d - a[0] > b && (await c(), a[0] = d);
}
async function nb(a, b, c, d = null) {
  null === d && (d = 20);
  let e = await db("div");
  bb.has(a) || bb.set(a, [0]);
  let f = bb.get(a);
  await mb(f, d, async() => {
    await b(e);
    ua(e.h, a, c, ab);
  });
}
function ob(a, b) {
  let c = 0 === b, d = a;
  do {
    d.style.height = "100%";
    d.style.width = "100%";
    d.style.margin = 0;
    if (!c || "HTML" === d.tagName) {
      break;
    }
    d = d.parentNode;
  } while (d);
  if (b & 1 && (console.log("notebook"), a instanceof HTMLElement)) {
    let e = () => a.style.height = `${0.5 * a.offsetWidth}px`;
    window.addEventListener("resize", e);
    a.style.overflow = "auto";
    setTimeout(() => e(), 0);
  }
}
;var pb = {qa:function(a, b) {
  a = a.replace(/\/$/, "");
  b = b.replace(/\/$/, "");
  return b.startsWith(a) ? b === a ? !1 : "/" === b[a.length] : !1;
}};
async function qb(a, b = !1) {
  b || null === a.g ? (await a.o(), a.g && (a.files?.length ?? void 0) && await a.h.set(a.g, a.files)) : (b = await a.h.get(a.g), a.files = b ? b : []);
}
async function rb() {
  return null;
}
class sb {
  constructor(a) {
    this.files = [];
    this.g = null;
    this.h = a;
  }
  l() {
    return !0;
  }
  async o() {
  }
  async U() {
  }
  async G() {
  }
  async j() {
  }
  async A() {
  }
  async I() {
    this.g && await this.h.L(this.g);
  }
}
;async function K(a, b) {
  const c = new URLSearchParams();
  c.append("CMD", b);
  return a.inst + "/" + a.la + "?" + c.toString();
}
class tb extends sb {
  constructor(a, b, c, d) {
    super(a);
    this.g = "server" + b;
    this.la = b;
    this.inst = c;
    this.i = d;
  }
  l(a) {
    a && void 0 !== a.size && (a.size = parseInt(a.size, 10));
    return !0;
  }
  async o() {
    var a = await K(this, "LISTAR");
    a = await this.i.g(a, {method:"GET", headers:{source:"reolad_job"}});
    try {
      this.files = await a.clone().json();
    } catch (b) {
      console.log("__" + await a.text() + "__", b);
    }
  }
  async U(a, b, c) {
    if (b) {
      var d = new FormData();
      d.append("FILE", JSON.stringify(b));
      c && d.append("BLOB", c);
      d.append("MODIFIED", a.modifiedTime);
      a = await K(this, "UPDATE");
      a = await (await this.i.g(a, {method:"POST", body:d})).json();
      b.modifiedTime = a.modifiedTime;
      b.size = parseInt(a.size, 10);
    } else {
      d = new FormData(), d.append("FILE", JSON.stringify(a)), c && d.append("BLOB", c), a = await K(this, "CREATE"), a = await (await this.i.g(a, {method:"POST", body:d})).json(), this.files.push(a);
    }
    this.g && await this.h.set(this.g, this.files);
    return b;
  }
  async G(a) {
    a = {ID:a.id};
    let b = await K(this, "GET");
    return await (await this.i.g(b, {method:"POST", body:JSON.stringify(a), headers:{"Content-Type":"application/json"}})).blob();
  }
  async j(a) {
    let b = {FILE:a}, c = await K(this, "DELETE");
    await this.i.g(c, {method:"POST", body:JSON.stringify(b), headers:{"Content-Type":"application/json"}});
    this.files = this.files.filter(d => d !== a);
    this.g && await this.h.set(this.g, this.files);
    console.log("retorna delete item fserver");
  }
  async A(a) {
    let b = {FILE:a}, c = await K(this, "DELPATH");
    await this.i.g(c, {method:"POST", body:JSON.stringify(b), headers:{"Content-Type":"application/json"}});
    this.files = this.files.filter(d => !(pb.qa(a, Wa(d)) || Wa(d) === a));
    this.g && await this.h.set(this.g, this.files);
  }
  async I() {
    await this.h.clear();
  }
}
;function ub(a) {
  a.i = [];
  a.Y = [];
  a.o = [];
  a.j = -1;
  a.l = [];
  a.I = [0, 0];
  a.G = [0, 0];
  a.v.map(async b => ub(b));
}
function M(a, b = !1) {
  return (() => 1 === a.u ? [a] : b && 2 === a.u ? a.v.map(c => M(c, !0)).flat() : vb(a).some(c => 5 === a.i[c] || 1 === a.i[c]) ? a.v.map(c => M(c, !0)).flat(1) : [])();
}
function vb(a) {
  return a.O.reduce((b, c, d) => {
    b.includes(d) || b.push(d);
    return b;
  }, []);
}
function wb(a, b, c, d = null) {
  function e(h, n) {
    for (let k of f) {
      if ([h, n].includes(k)) {
        return k;
      }
    }
    return 0;
  }
  if (1 === a.u) {
    let h = [0, 0];
    if (a.s[b] || a.s[c]) {
      !a.s[b] && a.s[c] ? h[1] = 3 : a.s[b] && !a.s[c] ? h[0] = 3 : h = a.s[b].size === a.s[c].size ? [1, 1] : [2, 2];
    }
    d && (0 !== h[0] && d(a.s[b]) && (h[0] = 0), 0 !== h[1] && d(a.s[c]) && (h[1] = 0));
    return h;
  }
  let f = [2, 3, 1, 0], g = [0, 0];
  a.v.forEach(h => {
    h = wb(h, b, c, d);
    g[b] = e(g[b], h[b]);
    g[c] = e(g[c], h[c]);
  });
  return g;
}
function N(a, b) {
  return 1 === a.u ? a.s[b]?.size ?? 0 : a.v.reduce((c, d) => N(d, b) + c, 0);
}
function xb(a, b) {
  return 1 === a.u ? a.s[b] ? 1 : 0 : a.v.reduce((c, d) => xb(d, b) + c, 0);
}
function yb(a, b) {
  return 1 === a.u ? 0 : (0 < xb(a, b) ? 1 : 0) + a.v.reduce((c, d) => yb(d, b) + c, 0);
}
function O(a, b, c) {
  let d = c ? (new Date()).toISOString() : "1970-01-01T00:00:00.000Z";
  if (1 === a.u) {
    return a.s[b]?.modifiedTime ?? d;
  }
  let e = new Date(d);
  2 === a.u && a.v.forEach(f => {
    if (f = O(f, b, c)) {
      var g = new Date(f);
      if (c && g < e || g > e) {
        d = f, e = g;
      }
    }
  });
  return d;
}
function zb(a, b, c, d) {
  let e = `${b}/${c.replace("/", "\u2215")}`.split("/"), f = a;
  e.forEach((g, h) => {
    if (g) {
      let n = g.replace("\u2215", "/");
      h !== e.length - 1 || 2 === d ? (h = f.v.find(k => k.name === g && 2 === k.u), h || (h = new Ab(g, 2, f), h.name = n)) : (h = f.v.find(k => k.name === g && k.u === d), h || (h = new Ab(g, d, f), h.name = n));
      f = h;
    }
  });
  return f;
}
class Ab {
  constructor(a, b, c = null) {
    this.name = a;
    this.h = c && c.h ? `${c.h}/${a}` : a;
    this.u = b;
    this.g = c;
    this.v = [];
    this.A = this.h.split("/").reduce((d, e) => d + (e ? 1 : 0), 0);
    this.s = [];
    this.O = [];
    this.i = [];
    this.Y = [];
    this.o = [];
    this.j = -1;
    this.l = [];
    this.I = [];
    this.G = [];
    if (c) {
      if (2 !== c.u) {
        throw Error();
      }
      c.v.push(this);
    }
  }
}
;const P = {ca:"\ud83d\udcc1", aa:"\ud83d\udcc2", ba:"\ud83d\udd39"}, Bb = {ka:""};
function Q(a) {
  function b(k) {
    let l = 2 === k.u, m = e.includes(k.h);
    l && h.push(k);
    n.reduce((p, q) => {
      q = (q = k.s[q]) ? g(q) : !0;
      return p && q;
    }, !0) || h.push(k);
    l && m && l && m && k.v.map((p, q) => {
      b(p);
      p.j = q;
      n.forEach(r => {
        p.O[r] && (k.l[r] = q);
      });
      n.forEach(r => {
        let v = p.s[r];
        !v || g && g(v) || k.G[r]++;
      });
    });
  }
  function c(k, l, m) {
    k.i[l] = m;
    k.v.forEach(p => c(p, l, m));
  }
  function d(k, l) {
    let m = 2 === k.u, p = e.includes(k.h), [q, r] = n, v = wb(k, q, r, f.h);
    for (let x of n) {
      if (m ? k.i[x] = l ? p ? 2 : 1 : 5 : k.s[x] && (k.i[x] = 3), l) {
        var y = v[x];
        let Tb = 1 === y || 0 === y ? "gray" : 3 === y ? "purple" : 2 === y ? "red" : "purple";
        y = L => "function" === typeof L ? L(Tb) : L;
        let Ub = m ? p ? y(P.ca) : y(P.aa) : y(P.ba);
        k.Y[x] = function() {
          let L = `span class="${Bb.ka}"`;
          return k.O[x] ? `<${L}>${k.o[x]}</span>${Ub} ${k.name}` : `<${L}>${k.o[x]}</span>`;
        }();
      }
    }
    m && p ? k.v.map(x => d(x, l)) : m && !p && k.v.map(x => d(x, !1));
  }
  let e = a.i, f = a, g = a.h, h = [];
  a.j.forEach(k => Cb(k, a.l));
  ub(a.l);
  let n = a.A;
  a.l.v.forEach(k => b(k));
  n.forEach(k => h.forEach(l => {
    let m = [], p = l;
    for (; 1 < p.A;) {
      var q = l, r = p, v = k;
      if (1 === r.u) {
        let y = r.s[v];
        y && (g && g(y) || r.g.I[v]++);
      }
      q = r.O[v] ? 1 === r.u ? r.g.I[v] === r.g.G[v] ? "\u2514\u2500" : "\u251c\u2500" : r.j < r.g.l[v] ? "\u2502&nbsp" : r.j == r.g.l[v] ? q.A === r.A ? "\u2514\u2500" : "&nbsp&nbsp" : "ab" : r.j < r.g.l[v] ? "\u2502&nbsp" : "&nbsp&nbsp";
      void 0 === q && (q = "p");
      m.unshift(q);
      p = p.g;
    }
    l.o[k] = m.join("");
  }));
  a.l.v.forEach(k => {
    n.forEach(l => c(k, l, 0));
    d(k, !0);
  });
  a.o = h;
}
async function R(a, b, c = null) {
  null === c ? await Promise.all(a.source.map(async d => await qb(d, b))) : a.source[c] && await qb(a.source[c], b);
  Db(a);
  Q(a);
  a.G = !0;
}
async function Eb(a) {
  a.G ? Q(a) : await R(a, !1);
}
function Db(a) {
  let b = a.source.map(d => d.files), c = new Ab("", 2, null);
  for (let [d, e] of Array.from(b).entries()) {
    a.source[d].l(null), e.forEach(f => {
      if (a.source[d].l(f) && void 0 !== f.folder && void 0 !== f.name) {
        var g = zb(c, f.folder, f.name, f.isfile ? 1 : 2);
        for (f.isfile && (g.s[d] = f); g.O[d] = !0, g = g.g, g;) {
        }
      }
    });
  }
  a.l = c;
}
async function Fb(a, b, c = null) {
  let d = a.I[b] = !a.I[b];
  a.j = [...a.j.filter(e => e.P !== b), {P:b, da:d, V:c, xa:null}];
  a.j.forEach(e => Cb(e, a.l));
  await Eb(a);
}
async function Gb(a) {
  await Fb(a, 0);
}
async function Hb(a, b) {
  await Fb(a, 1, b);
}
async function Ib(a, b) {
  await Fb(a, 2, b);
}
async function Jb(a) {
  for (let d of a.A) {
    await rb();
  }
  let b = a.A.map(d => {
    let e = [], f = [], g = [];
    for (let h of a.g.F[d] ?? []) {
      d = a.o[h - 1];
      2 === d.u && f.push(d);
      for (let n of M(d, !0)) {
        e.push(n);
      }
      g.push(d);
    }
    return {files:e, ra:f, ya:g};
  }), c = [];
  a.U.forEach((d, e) => {
    let f = b[e].ra.reduce((h, n) => h + yb(n, e), 0), g = b[e].files.reduce((h, n) => h + xb(n, e), 0);
    f && c.push(`${f} pastas do lado ${d}`);
    g && c.push(`${g} arquivos do lado ${d}`);
  });
  if (confirm(`Confirma apagar: \n ${c.join("\n")}`)) {
    for (let d of a.A) {
      for (let e of b[d].ya) {
        2 === e.u ? await a.source[d].A(e.h) : await a.source[d].j(e.s[d]);
      }
    }
    a.g.F = [];
    Db(a);
    Q(a);
    console.log("retorna apagar");
  }
}
async function Kb(a, b, c) {
  var d = [...(new Set(a.g.F.reduce((f, g) => f.concat(g), [])))];
  d.length || H.K.wa();
  await rb();
  await rb();
  for (let f of d.map(g => a.o[g - 1])) {
    var e = M(f);
    d = !1;
    for (let g of e) {
      if (!a.h || !a.h(g.s[b])) {
        if (e = wb(g, b, c, a.h), 0 === e[0]) {
          if (0 !== e[1]) {
            if (e = d ? "y" : (prompt(`Apagar ${g.name} ? (Y)es / (N)o / (A)lways / (C)ancel`) ?? "").toLowerCase(), "a" === e) {
              d = !0;
            } else if ("y" === e || d) {
              await a.source[c].j(g.s[c]);
            } else if ("c" == e) {
              break;
            }
          }
        } else if (2 === e[0] || 3 === e[0]) {
          (e = await a.source[b].G(g.s[b])) ? await a.source[c].U(g.s[b], g.s[c], e) : console.log("sem blob");
        }
      }
    }
  }
  Db(a);
  Q(a);
}
class Lb {
  constructor() {
    this.source = [];
    this.o = [];
    this.A = [0, 1];
    this.U = ["esquerdo", "direito"];
    this.i = [];
    this.h = null;
    this.G = !1;
    this.I = [!0, !0, !0];
    this.j = [];
    this.j.push({P:0, da:!1, V:null, xa:null});
    this.g = new class {
      constructor() {
        this.F = [[]];
        this.$ = this.ha = this.W = null;
      }
    }();
    this.now = new Date();
  }
}
function Cb(a, b) {
  let c = a.V, d = a.da ? -1 : 1;
  b.v.sort((e, f) => e.u !== f.u ? (2 === e.u ? -1 : 1) * d : 0 === a.P ? e.name.toUpperCase().localeCompare(f.name.toUpperCase()) * d : 1 === a.P && null !== a.V ? (new Date(O(e, c, !1)) < new Date(O(f, c, !1)) ? -1 : 1) * d : 2 === a.P && null !== a.V ? (new Date(N(e, c)) < new Date(N(f, c)) ? -1 : 1) * d : 0);
  b.v.forEach(e => Cb(a, e));
}
var Mb = Lb, Nb = tb;
var S;
function Ob(a) {
  async function b(d) {
    "undefined" === typeof S && (S = 0);
    S++;
    let e = d._msgid = S.toString(), {buffer:f, ...g} = d;
    g._msgid = e;
    a.send(g, void 0, f);
    return new Promise((h, n) => {
      c[e] = {resolve:h, reject:n};
    });
  }
  let c = {};
  a.on("msg:custom", (d, e) => {
    c[d?._msgid ?? null] && (d.buffer = e, c[d._msgid].resolve(d), delete c[d._msgid]);
  });
  window.pc = b;
  window.m = a;
  return b;
}
;const T = new $a.na();
async function Pb(a) {
  a.g = new Mb();
  a.g.h = c => a.h ? new Date(c.modifiedTime) < new Date(a.h) : !1;
  if (!a.i) {
    if (0 == a.source.e) {
      a.i = new Ja();
      var b = Da();
      a.source.inst = b.INST;
    } else {
      if (a.source.py_name && a.source.js_name) {
        b = Ga(a.source.py_name, a.source.js_name, a.source.a_fmsg);
      } else if (a.source.model) {
        b = Ob(a.source.model);
      } else {
        throw Error("Falta par\u00e2metro para link pycall");
      }
      a.i = new La(b);
    }
    b = new $a.oa(a.source.inst + "/STW", a.i);
    b.o = "KS";
    T.g = b;
    if (0 == a.source.e) {
      await Qb(a);
    } else if (a.source.model) {
      a.source.model.on("msg:custom", c => {
        (c?._msgid ?? !1) || Rb(a, c);
      });
    }
  }
  Sb(a, "PPA");
  Sb(a, "PPB");
}
async function U(a, b) {
  await nb(a.source.el, a.j.C, a.j.pa, a.j.rate);
  b && (a.o ? a.o.send("WMSGRELOAD=" + a.l) : a.source.model ? a.source.model.send("WMSGRELOAD=" + a.l, void 0, []) : console.error("no websocket and no model ??"));
}
async function Vb(a, b) {
  b && (T.l(), a.h = "", await R(a.g));
  a.h = await T.get("FT DT-I") ?? a.h;
  a.g.i = await T.get("OF") ?? [];
  await Eb(a.g);
}
async function Rb(a, b) {
  if ("string" === typeof b) {
    let c = b.match(RegExp("WMSGRELOAD=(.+)"))?.[1] ?? void 0;
    if (c) {
      c != a.l && (await Vb(a, !0), await U(a, !1));
      return;
    }
  }
  console.log("msg:", b);
}
async function Qb(a) {
  var b = new URLSearchParams();
  b.append("GSPORT", "");
  b = await (await a.i.g(a.source.inst + "/PMC?" + b.toString())).text();
  if (!b.startsWith("ws:")) {
    throw console.log(b), Error("Erro url websocket:");
  }
  b = new WebSocket(b);
  a.o = b;
  window.ws = b;
  b.onmessage = function(c) {
    Rb(a, c.data);
  };
}
function Sb(a, b) {
  a.g.source.push(new Nb(T, b, a.source.inst, a.i));
}
class Wb {
  constructor(a) {
    this.title = this.h = "";
    this.o = null;
    this.j = {rate:null, pa:!0, C:void 0};
    this.source = a;
    this.l = (new Date()).toISOString();
    Pb(this);
  }
}
;function Xb(a) {
  I(a, "table", b => {
    b("width: 100%;");
    b("border-collapse: collapse;");
    b("font-family: 'Courier New', Courier, monospace;");
  });
  I(a, "table th, table td", b => {
    b("border-right: 1px solid #ddd;");
    b("text-align: left;");
    b("overflow: hidden;");
    b("white-space: nowrap;");
    b("text-overflow: ellipsis;");
    b("max-width: 400px;");
  });
  I(a, "table th:last-child, table td:last-child", b => {
    b("border-right: none;");
  });
  I(a, "table th, table td", b => {
    b("padding: 4px;");
    b("text-align: left;");
    b("border-right: 1px solid #ddd;");
  });
  I(a, "table th:last-child, table td:last-child", b => {
    b("border-right: none;");
  });
  I(a, "table tr:last-child td", b => {
    b("border-bottom: none;");
  });
  I(a, "table tr td,table tr th", b => {
    b("height: 30px;");
    b("white-space: nowrap;");
  });
  I(a, "table th", b => {
    b("background-color: #f2f2f2;");
    b("color: #333;");
    b("position: relative;");
  });
  I(a, "table td", b => {
    b("border-bottom: 1px dotted #ddd;");
  });
}
var Zb = a => {
  I(a, `.${Yb}`, b => {
    b("display: inline-block;");
    b("width: 5px;");
    b("height: 100%;");
    b("position: absolute;");
    b("right: 0;");
    b("top: 0;");
    b("cursor: col-resize;");
    b("user-select: none;");
  });
}, ac = a => {
  I(a, `.${$b} tr:hover`, b => {
    b("background-color: #ddd;");
  });
}, cc = a => {
  I(a, `.${bc}`, b => {
    b("background-color: rgba(135, 206, 235, 0.5);");
    b("border-top: 1px solid #87CEEB;");
    b("border-bottom: 1px solid #87CEEB;");
  });
};
function dc(a) {
  var b = ec;
  I(a, `.${b}`, c => {
    c("display: block;");
  });
  I(a, `.${b} a, .${b} button`, c => {
    c("float: left;");
    c("width: 30px;");
    c("height: 30px;");
    c("display: flex;");
    c("justify-content: center;");
    c("align-items: center;");
    c("background-color: #ddd;");
    c("border: 1px solid #ccc;");
    c("margin: 2px;");
    c("transition: background-color 0.3s;");
    c("outline:none;");
  });
  I(a, `.${b} button:focus`, () => {
  });
  I(a, `.${b} button`, c => {
    c("width: auto;");
    c("height: 31px;");
  });
  I(a, `.${b} a:hover,.${b} button:hover`, c => {
    c("filter: brightness(80%);");
  });
  I(a, `.${b} svg`, c => {
    c("width: 40px;");
    c("height: 40px;");
    c("fill: white;");
  });
}
function fc(a) {
  var b = gc;
  I(a, `.${b} div`, c => {
    c("display: flex;");
  });
  I(a, `.${b} table`, c => {
    c("margin-top: 30px;");
  });
}
function hc(a) {
  I(a, `.${ic} input`, b => {
    b("height: 30px;");
    b("float: right;");
  });
}
var kc = a => {
  I(a, `.${jc}`, b => {
    b("display: inline-block; transform: scaleY(2.0);");
  });
};
function lc(a, b, c, d, e) {
  var f = !1;
  a.F[e] || (a.F[e] = []);
  if (d) {
    f = a.F[e].indexOf(b), -1 < f ? a.F[e].splice(f, 1) : a.F[e].push(b), f = !0;
  } else if (c && null !== a.W) {
    c = Math.min(b, a.W);
    const g = Math.max(b, a.W);
    d || (a.F[e].length = 0);
    d = [e, a.ha].reduce((h, n) => {
      h.includes(n) || h.push(n);
      return h;
    }, []);
    for (let h of d) {
      for (d = c; d <= g; d++) {
        -1 === a.F[h].indexOf(d) && a.F[h].push(d);
      }
    }
  } else {
    a.F = [], a.F[e] = [b], f = !0;
  }
  f && (a.W = b, a.ha = e);
}
async function mc(a, b) {
  async function c(n) {
    n = h + n.clientX - g;
    a.style.width = n + "px";
    console.log(a, n);
    await T.set(f, n);
  }
  async function d() {
    document.removeEventListener("mousemove", c);
    document.removeEventListener("mouseup", d);
  }
  var e = Yb;
  const f = `width.${b}`;
  let [g, h] = [0, 0];
  b = document.createElement("div");
  b.classList.add(e);
  a.appendChild(b);
  b.addEventListener("mousedown", function(n) {
    g = n.clientX;
    h = a.offsetWidth;
    document.addEventListener("mousemove", c);
    document.addEventListener("mouseup", d);
  });
  return `${await T.get(f)}`;
}
async function nc(a, b, c) {
  a.addEventListener("mousedown", function(d) {
    d.preventDefault();
  });
  a.addEventListener("click", function(d) {
    d.preventDefault();
    var e = d.target.closest("tr");
    e && (e = Array.from(a.querySelectorAll("tr")).indexOf(e), lc(b, e, d.shiftKey, d.ctrlKey, c), b.$ && b.$());
  });
}
async function oc(a, b, c) {
  a.addEventListener("mousedown", function(d) {
    d.preventDefault();
  });
  a.addEventListener("dblclick", function(d) {
    var e = d.target.closest("tr");
    const f = d.target.closest("td,th");
    d.preventDefault();
    e && (d = Array.from(a.querySelectorAll("tr")).indexOf(e), e = Array.from(e.querySelectorAll("td,th")).indexOf(f), c(d, e, b));
  });
}
;function pc(a, b) {
  a.addEventListener("dblclick", c => {
    c.target === a && b.requestFullscreen();
  });
  window.addEventListener("fullscreenchange", () => {
  });
}
;async function qc(a, b) {
  b = await lb(b);
  (await J(b, "style")).e.textContent = "\n    :host {\n        all: initial;    \n    \n    }";
  b = await J(b, "div");
  b.e.id = "d_div";
  await J(b, "div", async d => {
    await jb(d, '\n        <svg style="display:none;">\n            <symbol id = "I001" viewBox = "0 -15 512 497"><svg viewBox="0 0 512 512" width="512" xmlns="http://www.w3.org/2000/svg"><g><g><path d="m483.79 135.915h-16.652v-19.381c0-15.555-12.655-28.21-28.21-28.21h-107.241l-15.23-38.423c-3.498-8.826-11.894-14.53-21.389-14.53h-32.412c-4.134 0-7.485 3.351-7.485 7.485s3.351 7.485 7.485 7.485h32.412c3.317 0 6.25 1.992 7.472 5.076l13.043 32.906h-103.09c-3.317 0-6.25-1.993-7.473-5.076l-13.043-32.907h35.848c4.134 0 7.485-3.351 7.485-7.485s-3.351-7.485-7.485-7.485h-167.137c-12.687 0-23.008 10.322-23.008 23.008v21.906c0 4.432-3.606 8.038-8.038 8.038h-1.432c-15.555.002-28.21 12.657-28.21 28.212v121.958c0 4.134 3.351 7.485 7.485 7.485s7.485-3.351 7.485-7.485v-121.958c0-7.301 5.939-13.24 13.24-13.24h1.432c12.687 0 23.008-10.322 23.008-23.008v-21.907c0-4.432 3.606-8.038 8.038-8.038h109.725c3.317 0 6.251 1.992 7.473 5.076l13.218 33.347c3.499 8.826 11.895 14.529 21.389 14.529h226.436c7.3 0 13.24 5.939 13.24 13.24v19.381h-354.539c-15.555 0-28.21 12.655-28.21 28.21v270.309c0 15.01-12.211 27.222-27.221 27.225h-.008c-15.01 0-27.221-12.212-27.221-27.222v-160.928c0-4.134-3.351-7.485-7.485-7.485s-7.485 3.351-7.485 7.485v160.929c0 23.265 18.927 42.192 42.191 42.192h.003 441.596c15.555 0 28.21-12.655 28.21-28.21v-284.294c0-15.556-12.655-28.21-28.21-28.21zm13.24 312.504c0 7.3-5.939 13.24-13.24 13.24h-409.382c6.225-7.354 9.982-16.858 9.982-27.225v-270.309c0-7.301 5.939-13.24 13.24-13.24h386.16c7.3 0 13.24 5.939 13.24 13.24z"/><path d="m125.707 380.061h67.803c4.134 0 7.485-3.351 7.485-7.485s-3.351-7.485-7.485-7.485h-67.803c-4.134 0-7.485 3.351-7.485 7.485s3.351 7.485 7.485 7.485z"/><path d="m233.569 397.689h-107.862c-4.134 0-7.485 3.351-7.485 7.485s3.351 7.485 7.485 7.485h107.862c4.134 0 7.485-3.351 7.485-7.485s-3.351-7.485-7.485-7.485z"/></g></g></svg></symbol>\n            <symbol id = "I004" viewBox = "0 -30 492 482"><svg viewBox="0 0 512 512" width="512" xmlns="http://www.w3.org/2000/svg"><g><g><path d="m485.643 145.982h-58.933v-16.979c0-14.533-11.823-26.357-26.356-26.357h-97.197l-13.701-34.564c-3.287-8.294-11.177-13.654-20.099-13.654h-167.83c-4.134 0-7.485 3.351-7.485 7.485s3.351 7.485 7.485 7.485h54.32c2.745 0 5.171 1.648 6.182 4.199l12.036 30.365c3.287 8.294 11.177 13.654 20.098 13.654h206.191c6.278 0 11.386 5.108 11.386 11.387v16.979h-277.731c-13.383 0-24.638 10.014-26.18 23.292l-44.064 248.131c-.642 3.596-1.542 6.714-2.747 9.533-4.575 10.685-11.54 15.662-21.924 15.663h-.005c-13.299 0-24.119-10.819-24.119-24.118v-289.48c0-6.279 5.108-11.387 11.387-11.387h1.304c11.921 0 21.62-9.698 21.62-21.62v-19.947c0-3.667 2.983-6.65 6.651-6.65h11.344c4.134 0 7.485-3.351 7.485-7.485s-3.351-7.485-7.485-7.485h-11.344c-11.921 0-21.621 9.699-21.621 21.62v19.948c0 3.667-2.983 6.65-6.65 6.65h-1.304c-14.533-.001-26.357 11.823-26.357 26.356v289.48c0 21.553 17.535 39.088 39.089 39.088h.002 402.113c14.302 0 25.98-11.451 26.348-25.666l11.732-68.346c.7-4.074-2.036-7.944-6.111-8.644-4.061-.7-7.943 2.036-8.643 6.111l-11.832 68.923c-.072.419-.108.842-.108 1.267 0 6.278-5.108 11.386-11.386 11.386h-42.633-329.287c2.096-2.863 3.933-6.124 5.496-9.773 1.659-3.878 2.876-8.062 3.721-12.791l44.199-249.037c.665-5.729 5.527-10.049 11.309-10.049h351.634c6.091 0 11.081 4.807 11.374 10.827l-26.608 154.984c-.7 4.074 2.036 7.944 6.11 8.644 4.072.701 7.944-2.036 8.644-6.111l26.73-155.691c.072-.418.108-.842.108-1.267-.001-14.532-11.825-26.356-26.358-26.356zm-291.48-43.336c-2.744 0-5.17-1.648-6.181-4.2l-11.515-29.048h92.889c2.745 0 5.171 1.648 6.182 4.199l11.514 29.048h-92.889z"/><path d="m201.827 369.639c4.134 0 7.485-3.351 7.485-7.485s-3.351-7.485-7.485-7.485h-61.74c-4.134 0-7.485 3.351-7.485 7.485s3.351 7.485 7.485 7.485z"/><path d="m120.627 391.836c0 4.134 3.351 7.485 7.485 7.485h98.217c4.134 0 7.485-3.351 7.485-7.485s-3.351-7.485-7.485-7.485h-98.217c-4.135 0-7.485 3.352-7.485 7.485z"/></g></g></svg></symbol> \n            <symbol id = "I016" viewBox = "0 0 512 512"><svg height="512" viewBox="0 0 512 512" width="512" xmlns="http://www.w3.org/2000/svg"><g><path d="m126.373 182.418h-18.254v41.444h18.254c11.461 0 20.784-9.296 20.784-20.722s-9.324-20.722-20.784-20.722z"/><path d="m423.006 437.605 4.096-3.902h-58.417v55.641z"/><path d="m238.709 182.686v87.167c21.901-2.426 38.989-21.046 38.989-43.584 0-22.537-17.088-41.157-38.989-43.583z"/><path d="m59.417 13.735v67.837h393.166v-67.837c0-7.585-6.15-13.735-13.736-13.735h-365.695c-7.586 0-13.735 6.15-13.735 13.735z"/><path d="m452.583 370.966h-393.166v127.298c0 7.586 6.15 13.735 13.735 13.735h261.555v-95.286c0-9.383 7.606-16.989 16.989-16.989h100.887z"/><path d="m472.979 115.551h-433.958c-7.586 0-13.735 6.15-13.735 13.735v193.966c0 7.586 6.15 13.735 13.735 13.735h433.958c7.586 0 13.735-6.15 13.735-13.735v-193.966c.001-7.585-6.149-13.735-13.735-13.735zm-346.606 142.29h-18.254v29.269c0 9.383-7.606 16.989-16.989 16.989s-16.99-7.606-16.99-16.989v-121.681c0-9.383 7.606-16.989 16.989-16.989h35.243c30.196 0 54.763 24.539 54.763 54.701s-24.566 54.7-54.762 54.7zm107.474 46.258h-12.127c-9.383 0-16.989-7.606-16.989-16.989v-121.681c0-9.383 7.606-16.989 16.989-16.989h12.127c42.915 0 77.829 34.914 77.829 77.829 0 42.916-34.914 77.83-77.829 77.83zm187.024-121.681h-41.165v33.6h22.511c9.383 0 16.989 7.606 16.989 16.989s-7.606 16.989-16.989 16.989h-22.511v37.113c0 9.383-7.606 16.989-16.989 16.989s-16.989-7.606-16.989-16.989v-121.68c0-9.383 7.606-16.989 16.989-16.989h58.154c9.383 0 16.989 7.606 16.989 16.989s-7.607 16.989-16.989 16.989z"/></g></svg></symbol> \n            <symbol id = "ITEM" viewBox = "0 -15 100 85"><svg  viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path d="M50 10 L90 50 L50 90 L10 50 Z" fill="currentColor" stroke = "var(--c_stroke, black)"/></svg></symbol> \n        </svg>\n        ');
  });
  let c = a.source;
  c.e & 1 && (c.el.style.background = "white", pc(b.t.j, c.el));
  b.e.style.border = "20px solid #F000";
  kb(b, d => {
    Xb(d);
    Zb(d);
    ac(d);
    cc(d);
    dc(d);
    fc(d);
    hc(d);
    I(d, `.${V}`, e => {
      e("display: none;");
      e("position: absolute;");
      e("background-color: #fff;");
      e("border: 1px solid #ccc;");
      e("padding: 5px 0;");
      e("box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);");
    });
    I(d, `.${V} div`, e => {
      e("padding: 5px 20px;");
      e("cursor: pointer;");
    });
    I(d, `.${V} div:hover`, e => {
      e("background-color: #f0f0f0;");
    });
    I(d, "table tr th, table tr td", () => {
    });
    I(d, `.${W}`, e => {
      e("width: 1.2em;");
      e("height: 1.2em;");
      e("vertical-align: -0.10em;");
    });
    kc(d);
  });
  await jb(b, `<h1>${a.title}</h1>`);
  await J(b, "div", async d => {
    d.e.classList.add(ec);
    await J(d, "button", async e => {
      async function f() {
        H.K.R();
        e.e.style.cursor = document.body.style.cursor = "wait";
        try {
          await R(a.g, !0, 0), await U(a, !1);
        } catch (g) {
        }
        e.e.style.cursor = document.body.style.cursor = "default";
        await U(a, !0);
      }
      e.e.innerText = "LER PASTA LOCAL";
      e.e.style.backgroundColor = "SandyBrown";
      e.e.onclick = f;
      e.e.onmousedown = async g => {
        2 === g.button && confirm("ESCOLHER OUTRA PASTA?") && (await a.g.source[0].I(), await f());
      };
    });
    await J(d, "button", async e => {
      e.e.innerText = "LER G-DRIVE";
      e.e.style.backgroundColor = "SandyBrown";
      e.e.onclick = async() => {
        H.K.R();
        e.e.style.cursor = document.body.style.cursor = "wait";
        try {
          await R(a.g, !0, 1), await U(a, !1);
        } catch (f) {
          f && console.log(f);
        }
        e.e.style.cursor = document.body.style.cursor = "default";
        await U(a, !0);
      };
    });
    await J(d, "button", async e => {
      e.e.innerText = "ABRIR DRIVE";
      e.e.style.marginLeft = "10px";
      e.e.onclick = async() => {
        await Vb(a, !0);
        await U(a, !1);
      };
    });
    await J(d, "button", async e => {
      e.e.innerText = "UPDLOAD >>";
      e.e.style.marginLeft = "20px";
      e.e.style.backgroundColor = "LightSkyBlue";
      e.e.onclick = async() => {
        H.K.R();
        e.e.style.cursor = document.body.style.cursor = "wait";
        await Kb(a.g, 0, 1);
        e.e.style.cursor = document.body.style.cursor = "default";
        await U(a, !0);
      };
    });
    await J(d, "button", async e => {
      e.e.innerText = "DOWNLOAD <<";
      e.e.style.marginLeft = "10px";
      e.e.style.backgroundColor = "LightSkyBlue";
      e.e.onclick = async() => {
        H.K.R();
        e.e.style.cursor = document.body.style.cursor = "wait";
        await Kb(a.g, 1, 0);
        e.e.style.cursor = document.body.style.cursor = "default";
        await U(a, !0);
      };
    });
    await J(d, "div", async e => {
      e.e.classList.add(ic);
      await J(e, "input", async f => {
        f.t.h.type = "date";
        f.t.h.value = H.J.va(a.h);
        f.e.style.marginLeft = "10px";
        f.t.h.title = "MOSTRAR ARQUIVOS MODIFICADOS A PARTIR DESTA DATA:";
        f.e.onchange = async() => {
          let g = H.J.ua(f.t.h.value, !1);
          await T.set("FT DT-I", g);
          a.h = g;
          await R(a.g, !1);
          U(a, !0);
        };
      });
    });
    await J(d, "div", async e => {
      e.e.classList.add(V);
      await J(e, "div", async f => {
        f.e.innerText = "APAGAR";
        f.e.onclick = async() => {
          H.K.R();
          document.body.style.cursor = "wait";
          await Jb(a.g);
          document.body.style.cursor = "default";
          await U(a, !0);
        };
      });
    });
  });
  await jb(b, "<br><br>");
  await J(b, "div", async d => {
    d.e.classList.add(gc);
    d = await J(d, "div");
    await rc(d, 0, a);
    await J(d, "div", async e => e.e.style.width = "50px");
    await rc(d, 1, a);
  });
}
async function rc(a, b, c) {
  await J(a, "table", async d => {
    nc(d.t.i, c.g.g, b);
    c.g.g.$ = () => U(c, !1);
    oc(d.t.i, b, async(e, f, g) => {
      0 === e ? (0 === f && await Gb(c.g), 1 === f && await Ib(c.g, g), 2 === f && await Hb(c.g, g)) : (e = c.g.o[e - 1].h, f = c.g.i.indexOf(e), -1 < f ? c.g.i.splice(f, 1) : c.g.i.push(e), await T.set("OF", c.g.i), await Eb(c.g), await H.actions.Aa(100));
      await U(c, !0);
    });
    d.e.oncontextmenu = async e => {
      e.preventDefault();
      let f = 0, g = e.target, h = null;
      for (; 100 > f && !(f++, g = g.parentElement, h = g.querySelector(`div.${V}`));) {
      }
      h.style.display = "block";
      h.style.top = e.pageY - c.source.el.getBoundingClientRect().top + "px";
      h.style.left = e.pageX - c.source.el.getBoundingClientRect().left + "px";
    };
    d.e.classList.add($b);
    await J(d, "tr", async e => {
      for (let [f, g] of Array.from(["Nome do Arauivo", "Tamanho", "\u00daltima Modifica\u00e7\u00e3o"]).entries()) {
        await J(e, "th", async h => {
          h.e.innerText = g;
          h.e.style.height = "1em";
          let n = await mc(h.t.l, `${f}`);
          h.e.style.width = `${n}px`;
        });
      }
    });
    for (let [e, f] of Array.from(c.g.o).entries()) {
      await J(d, "tr", async g => {
        (c.g.g.F[b]?.includes(e + 1) ?? !1) && g.e.classList.add(bc);
        let h = f.Y[b] ?? "", n = N(f, b).toLocaleString("pt-BR"), k = H.J.sa(O(f, b, !1), !0);
        f.O[b] || (k = n = "");
        try {
          await J(g, "td", async l => {
            l.e.innerHTML = h;
            l.e.style.fontSize = "0.95em";
            l.e.style.overflow = "hidden";
            l.e.style.textOverflow = "ellipses";
          }), await J(g, "td", async l => {
            l.e.innerText = `${n}`;
            l.e.style.textAlign = "right";
            l.e.style.fontSize = "0.8em";
          }), await J(g, "td", async l => {
            l.e.innerText = k;
            l.e.style.textAlign = "center";
            l.e.style.fontSize = "0.8em";
          });
        } catch (l) {
          console.log(e, f.name, l);
        }
      });
    }
  });
}
;var Yb = "rz", $b = "ho", bc = "ts", ec = "ib", W = "si", gc = "tc", ic = "dl", jc = "ftt", V = "mn";
P.aa = a => `<svg class="${W}" fill="${a}"><use href ="#I001"></use></svg>`;
P.ca = a => `<svg class="${W}" fill="${a}"><use href ="#I004"></use></svg>`;
P.ba = a => `<svg class="${W}" style="color:${a}" ><use href ="#ITEM"></use></svg>`;
Bb.ka = jc;
async function sc(a) {
  ob(a.el, a.e);
  let b = new Wb(a);
  b.j.C = async function(c) {
    c = await J(c, "div");
    c.e.style.display = "flex";
    c.e.style.justifyContent = "center";
    c = await J(c, "div");
    await qc(b, c);
  };
  await Vb(b, !1);
  await U(b, !1);
}
var X = ["run"], Y = aa;
X[0] in Y || "undefined" == typeof Y.execScript || Y.execScript("var " + X[0]);
for (var Z; X.length && (Z = X.shift());) {
  X.length || void 0 === sc ? Y[Z] && Y[Z] !== Object.prototype[Z] ? Y = Y[Z] : Y = Y[Z] = {} : Y[Z] = sc;
}
;}).call(this);
