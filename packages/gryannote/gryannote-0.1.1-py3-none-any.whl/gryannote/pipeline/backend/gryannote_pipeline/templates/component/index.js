function Ie() {
}
function ql(e) {
  return e();
}
function Xl(e) {
  e.forEach(ql);
}
function zl(e) {
  return typeof e == "function";
}
function Zl(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function Wl(e, ...t) {
  if (e == null) {
    for (const i of t)
      i(void 0);
    return Ie;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function Un(e) {
  const t = typeof e == "string" && e.match(/^\s*(-?[\d.]+)([^\s]*)\s*$/);
  return t ? [parseFloat(t[1]), t[2] || "px"] : [
    /** @type {number} */
    e,
    "px"
  ];
}
const Ji = typeof window < "u";
let Gn = Ji ? () => window.performance.now() : () => Date.now(), Yi = Ji ? (e) => requestAnimationFrame(e) : Ie;
const ze = /* @__PURE__ */ new Set();
function Ki(e) {
  ze.forEach((t) => {
    t.c(e) || (ze.delete(t), t.f());
  }), ze.size !== 0 && Yi(Ki);
}
function Ql(e) {
  let t;
  return ze.size === 0 && Yi(Ki), {
    promise: new Promise((n) => {
      ze.add(t = { c: e, f: n });
    }),
    abort() {
      ze.delete(t);
    }
  };
}
function Jl(e) {
  const t = e - 1;
  return t * t * t + 1;
}
function Fn(e, { delay: t = 0, duration: n = 400, easing: i = Jl, x: l = 0, y: r = 0, opacity: a = 0 } = {}) {
  const s = getComputedStyle(e), o = +s.opacity, u = s.transform === "none" ? "" : s.transform, f = o * (1 - a), [h, d] = Un(l), [b, y] = Un(r);
  return {
    delay: t,
    duration: n,
    easing: i,
    css: (w, p) => `
			transform: ${u} translate(${(1 - w) * h}${d}, ${(1 - w) * b}${y});
			opacity: ${o - f * p}`
  };
}
const Me = [];
function Yl(e, t) {
  return {
    subscribe: pt(e, t).subscribe
  };
}
function pt(e, t = Ie) {
  let n;
  const i = /* @__PURE__ */ new Set();
  function l(s) {
    if (Zl(e, s) && (e = s, n)) {
      const o = !Me.length;
      for (const u of i)
        u[1](), Me.push(u, e);
      if (o) {
        for (let u = 0; u < Me.length; u += 2)
          Me[u][0](Me[u + 1]);
        Me.length = 0;
      }
    }
  }
  function r(s) {
    l(s(e));
  }
  function a(s, o = Ie) {
    const u = [s, o];
    return i.add(u), i.size === 1 && (n = t(l, r) || Ie), s(e), () => {
      i.delete(u), i.size === 0 && n && (n(), n = null);
    };
  }
  return { set: l, update: r, subscribe: a };
}
function tt(e, t, n) {
  const i = !Array.isArray(e), l = i ? [e] : e;
  if (!l.every(Boolean))
    throw new Error("derived() expects stores as input, got a falsy value");
  const r = t.length < 2;
  return Yl(n, (a, s) => {
    let o = !1;
    const u = [];
    let f = 0, h = Ie;
    const d = () => {
      if (f)
        return;
      h();
      const y = t(i ? u[0] : u, a, s);
      r ? a(y) : h = zl(y) ? y : Ie;
    }, b = l.map(
      (y, w) => Wl(
        y,
        (p) => {
          u[w] = p, f &= ~(1 << w), o && d();
        },
        () => {
          f |= 1 << w;
        }
      )
    );
    return o = !0, d(), function() {
      Xl(b), h(), o = !1;
    };
  });
}
function jn(e) {
  return Object.prototype.toString.call(e) === "[object Date]";
}
function un(e, t, n, i) {
  if (typeof n == "number" || jn(n)) {
    const l = i - n, r = (n - t) / (e.dt || 1 / 60), a = e.opts.stiffness * l, s = e.opts.damping * r, o = (a - s) * e.inv_mass, u = (r + o) * e.dt;
    return Math.abs(u) < e.opts.precision && Math.abs(l) < e.opts.precision ? i : (e.settled = !1, jn(n) ? new Date(n.getTime() + u) : n + u);
  } else {
    if (Array.isArray(n))
      return n.map(
        (l, r) => un(e, t[r], n[r], i[r])
      );
    if (typeof n == "object") {
      const l = {};
      for (const r in n)
        l[r] = un(e, t[r], n[r], i[r]);
      return l;
    } else
      throw new Error(`Cannot spring ${typeof n} values`);
  }
}
function xn(e, t = {}) {
  const n = pt(e), { stiffness: i = 0.15, damping: l = 0.8, precision: r = 0.01 } = t;
  let a, s, o, u = e, f = e, h = 1, d = 0, b = !1;
  function y(p, m = {}) {
    f = p;
    const v = o = {};
    return e == null || m.hard || w.stiffness >= 1 && w.damping >= 1 ? (b = !0, a = Gn(), u = p, n.set(e = f), Promise.resolve()) : (m.soft && (d = 1 / ((m.soft === !0 ? 0.5 : +m.soft) * 60), h = 0), s || (a = Gn(), b = !1, s = Ql((c) => {
      if (b)
        return b = !1, s = null, !1;
      h = Math.min(h + d, 1);
      const _ = {
        inv_mass: h,
        opts: w,
        settled: !0,
        dt: (c - a) * 60 / 1e3
      }, E = un(_, u, e, f);
      return a = c, u = e, n.set(e = E), _.settled && (s = null), !_.settled;
    })), new Promise((c) => {
      s.promise.then(() => {
        v === o && c();
      });
    }));
  }
  const w = {
    set: y,
    update: (p, m) => y(p(f, e), m),
    subscribe: n.subscribe,
    stiffness: i,
    damping: l,
    precision: r
  };
  return w;
}
const {
  SvelteComponent: Kl,
  add_render_callback: $i,
  append: Et,
  attr: ie,
  binding_callbacks: Vn,
  check_outros: $l,
  create_bidirectional_transition: qn,
  destroy_each: er,
  detach: ft,
  element: Ot,
  empty: tr,
  ensure_array_like: Xn,
  group_outros: nr,
  init: ir,
  insert: ct,
  listen: fn,
  prevent_default: lr,
  run_all: rr,
  safe_not_equal: sr,
  set_data: or,
  set_style: Te,
  space: cn,
  text: ar,
  toggle_class: fe,
  transition_in: Jt,
  transition_out: zn
} = window.__gradio__svelte__internal, { createEventDispatcher: ur } = window.__gradio__svelte__internal;
function Zn(e, t, n) {
  const i = e.slice();
  return i[24] = t[n], i;
}
function Wn(e) {
  let t, n, i, l, r, a = Xn(
    /*filtered_indices*/
    e[1]
  ), s = [];
  for (let o = 0; o < a.length; o += 1)
    s[o] = Qn(Zn(e, a, o));
  return {
    c() {
      t = Ot("ul");
      for (let o = 0; o < s.length; o += 1)
        s[o].c();
      ie(t, "class", "options svelte-yuohum"), ie(t, "role", "listbox"), Te(
        t,
        "top",
        /*top*/
        e[9]
      ), Te(
        t,
        "bottom",
        /*bottom*/
        e[10]
      ), Te(t, "max-height", `calc(${/*max_height*/
      e[11]}px - var(--window-padding))`), Te(
        t,
        "width",
        /*input_width*/
        e[8] + "px"
      );
    },
    m(o, u) {
      ct(o, t, u);
      for (let f = 0; f < s.length; f += 1)
        s[f] && s[f].m(t, null);
      e[21](t), i = !0, l || (r = fn(t, "mousedown", lr(
        /*mousedown_handler*/
        e[20]
      )), l = !0);
    },
    p(o, u) {
      if (u & /*filtered_indices, choices, selected_indices, active_index*/
      51) {
        a = Xn(
          /*filtered_indices*/
          o[1]
        );
        let f;
        for (f = 0; f < a.length; f += 1) {
          const h = Zn(o, a, f);
          s[f] ? s[f].p(h, u) : (s[f] = Qn(h), s[f].c(), s[f].m(t, null));
        }
        for (; f < s.length; f += 1)
          s[f].d(1);
        s.length = a.length;
      }
      u & /*top*/
      512 && Te(
        t,
        "top",
        /*top*/
        o[9]
      ), u & /*bottom*/
      1024 && Te(
        t,
        "bottom",
        /*bottom*/
        o[10]
      ), u & /*max_height*/
      2048 && Te(t, "max-height", `calc(${/*max_height*/
      o[11]}px - var(--window-padding))`), u & /*input_width*/
      256 && Te(
        t,
        "width",
        /*input_width*/
        o[8] + "px"
      );
    },
    i(o) {
      i || (o && $i(() => {
        i && (n || (n = qn(t, Fn, { duration: 200, y: 5 }, !0)), n.run(1));
      }), i = !0);
    },
    o(o) {
      o && (n || (n = qn(t, Fn, { duration: 200, y: 5 }, !1)), n.run(0)), i = !1;
    },
    d(o) {
      o && ft(t), er(s, o), e[21](null), o && n && n.end(), l = !1, r();
    }
  };
}
function Qn(e) {
  let t, n, i, l = (
    /*choices*/
    e[0][
      /*index*/
      e[24]
    ][0] + ""
  ), r, a, s, o, u;
  return {
    c() {
      t = Ot("li"), n = Ot("span"), n.textContent = "✓", i = cn(), r = ar(l), a = cn(), ie(n, "class", "inner-item svelte-yuohum"), fe(n, "hide", !/*selected_indices*/
      e[4].includes(
        /*index*/
        e[24]
      )), ie(t, "class", "item svelte-yuohum"), ie(t, "data-index", s = /*index*/
      e[24]), ie(t, "aria-label", o = /*choices*/
      e[0][
        /*index*/
        e[24]
      ][0]), ie(t, "data-testid", "dropdown-option"), ie(t, "role", "option"), ie(t, "aria-selected", u = /*selected_indices*/
      e[4].includes(
        /*index*/
        e[24]
      )), fe(
        t,
        "selected",
        /*selected_indices*/
        e[4].includes(
          /*index*/
          e[24]
        )
      ), fe(
        t,
        "active",
        /*index*/
        e[24] === /*active_index*/
        e[5]
      ), fe(
        t,
        "bg-gray-100",
        /*index*/
        e[24] === /*active_index*/
        e[5]
      ), fe(
        t,
        "dark:bg-gray-600",
        /*index*/
        e[24] === /*active_index*/
        e[5]
      );
    },
    m(f, h) {
      ct(f, t, h), Et(t, n), Et(t, i), Et(t, r), Et(t, a);
    },
    p(f, h) {
      h & /*selected_indices, filtered_indices*/
      18 && fe(n, "hide", !/*selected_indices*/
      f[4].includes(
        /*index*/
        f[24]
      )), h & /*choices, filtered_indices*/
      3 && l !== (l = /*choices*/
      f[0][
        /*index*/
        f[24]
      ][0] + "") && or(r, l), h & /*filtered_indices*/
      2 && s !== (s = /*index*/
      f[24]) && ie(t, "data-index", s), h & /*choices, filtered_indices*/
      3 && o !== (o = /*choices*/
      f[0][
        /*index*/
        f[24]
      ][0]) && ie(t, "aria-label", o), h & /*selected_indices, filtered_indices*/
      18 && u !== (u = /*selected_indices*/
      f[4].includes(
        /*index*/
        f[24]
      )) && ie(t, "aria-selected", u), h & /*selected_indices, filtered_indices*/
      18 && fe(
        t,
        "selected",
        /*selected_indices*/
        f[4].includes(
          /*index*/
          f[24]
        )
      ), h & /*filtered_indices, active_index*/
      34 && fe(
        t,
        "active",
        /*index*/
        f[24] === /*active_index*/
        f[5]
      ), h & /*filtered_indices, active_index*/
      34 && fe(
        t,
        "bg-gray-100",
        /*index*/
        f[24] === /*active_index*/
        f[5]
      ), h & /*filtered_indices, active_index*/
      34 && fe(
        t,
        "dark:bg-gray-600",
        /*index*/
        f[24] === /*active_index*/
        f[5]
      );
    },
    d(f) {
      f && ft(t);
    }
  };
}
function fr(e) {
  let t, n, i, l, r;
  $i(
    /*onwindowresize*/
    e[18]
  );
  let a = (
    /*show_options*/
    e[2] && !/*disabled*/
    e[3] && Wn(e)
  );
  return {
    c() {
      t = Ot("div"), n = cn(), a && a.c(), i = tr(), ie(t, "class", "reference");
    },
    m(s, o) {
      ct(s, t, o), e[19](t), ct(s, n, o), a && a.m(s, o), ct(s, i, o), l || (r = [
        fn(
          window,
          "scroll",
          /*scroll_listener*/
          e[13]
        ),
        fn(
          window,
          "resize",
          /*onwindowresize*/
          e[18]
        )
      ], l = !0);
    },
    p(s, [o]) {
      /*show_options*/
      s[2] && !/*disabled*/
      s[3] ? a ? (a.p(s, o), o & /*show_options, disabled*/
      12 && Jt(a, 1)) : (a = Wn(s), a.c(), Jt(a, 1), a.m(i.parentNode, i)) : a && (nr(), zn(a, 1, 1, () => {
        a = null;
      }), $l());
    },
    i(s) {
      Jt(a);
    },
    o(s) {
      zn(a);
    },
    d(s) {
      s && (ft(t), ft(n), ft(i)), e[19](null), a && a.d(s), l = !1, rr(r);
    }
  };
}
function St(e) {
  let t, n = e[0], i = 1;
  for (; i < e.length; ) {
    const l = e[i], r = e[i + 1];
    if (i += 2, (l === "optionalAccess" || l === "optionalCall") && n == null)
      return;
    l === "access" || l === "optionalAccess" ? (t = n, n = r(n)) : (l === "call" || l === "optionalCall") && (n = r((...a) => n.call(t, ...a)), t = void 0);
  }
  return n;
}
function cr(e, t, n) {
  let { choices: i } = t, { filtered_indices: l } = t, { show_options: r = !1 } = t, { disabled: a = !1 } = t, { selected_indices: s = [] } = t, { active_index: o = null } = t, u, f, h, d, b, y, w, p, m, v;
  function c() {
    const { top: C, bottom: G } = b.getBoundingClientRect();
    n(15, u = C), n(16, f = v - G);
  }
  let _ = null;
  function E() {
    r && (_ !== null && clearTimeout(_), _ = setTimeout(
      () => {
        c(), _ = null;
      },
      10
    ));
  }
  const g = ur();
  function P() {
    n(12, v = window.innerHeight);
  }
  function A(C) {
    Vn[C ? "unshift" : "push"](() => {
      b = C, n(6, b);
    });
  }
  const k = (C) => g("change", C);
  function q(C) {
    Vn[C ? "unshift" : "push"](() => {
      y = C, n(7, y);
    });
  }
  return e.$$set = (C) => {
    "choices" in C && n(0, i = C.choices), "filtered_indices" in C && n(1, l = C.filtered_indices), "show_options" in C && n(2, r = C.show_options), "disabled" in C && n(3, a = C.disabled), "selected_indices" in C && n(4, s = C.selected_indices), "active_index" in C && n(5, o = C.active_index);
  }, e.$$.update = () => {
    if (e.$$.dirty & /*show_options, refElement, listElement, selected_indices, distance_from_bottom, distance_from_top, input_height*/
    229588) {
      if (r && b) {
        if (y && s.length > 0) {
          let G = y.querySelectorAll("li");
          for (const z of Array.from(G))
            if (z.getAttribute("data-index") === s[0].toString()) {
              St([
                y,
                "optionalAccess",
                (W) => W.scrollTo,
                "optionalCall",
                (W) => W(0, z.offsetTop)
              ]);
              break;
            }
        }
        c();
        const C = St([
          b,
          "access",
          (G) => G.parentElement,
          "optionalAccess",
          (G) => G.getBoundingClientRect,
          "call",
          (G) => G()
        ]);
        n(17, h = St([C, "optionalAccess", (G) => G.height]) || 0), n(8, d = St([C, "optionalAccess", (G) => G.width]) || 0);
      }
      f > u ? (n(9, w = `${u}px`), n(11, m = f), n(10, p = null)) : (n(10, p = `${f + h}px`), n(11, m = u - h), n(9, w = null));
    }
  }, [
    i,
    l,
    r,
    a,
    s,
    o,
    b,
    y,
    d,
    w,
    p,
    m,
    v,
    E,
    g,
    u,
    f,
    h,
    P,
    A,
    k,
    q
  ];
}
class el extends Kl {
  constructor(t) {
    super(), ir(this, t, cr, fr, sr, {
      choices: 0,
      filtered_indices: 1,
      show_options: 2,
      disabled: 3,
      selected_indices: 4,
      active_index: 5
    });
  }
}
const {
  SvelteComponent: hr,
  assign: _r,
  create_slot: mr,
  detach: dr,
  element: br,
  get_all_dirty_from_scope: pr,
  get_slot_changes: gr,
  get_spread_update: vr,
  init: yr,
  insert: wr,
  safe_not_equal: Er,
  set_dynamic_element_data: Jn,
  set_style: te,
  toggle_class: Ae,
  transition_in: tl,
  transition_out: nl,
  update_slot_base: Sr
} = window.__gradio__svelte__internal;
function Tr(e) {
  let t, n, i;
  const l = (
    /*#slots*/
    e[18].default
  ), r = mr(
    l,
    e,
    /*$$scope*/
    e[17],
    null
  );
  let a = [
    { "data-testid": (
      /*test_id*/
      e[7]
    ) },
    { id: (
      /*elem_id*/
      e[2]
    ) },
    {
      class: n = "block " + /*elem_classes*/
      e[3].join(" ") + " svelte-1t38q2d"
    }
  ], s = {};
  for (let o = 0; o < a.length; o += 1)
    s = _r(s, a[o]);
  return {
    c() {
      t = br(
        /*tag*/
        e[14]
      ), r && r.c(), Jn(
        /*tag*/
        e[14]
      )(t, s), Ae(
        t,
        "hidden",
        /*visible*/
        e[10] === !1
      ), Ae(
        t,
        "padded",
        /*padding*/
        e[6]
      ), Ae(
        t,
        "border_focus",
        /*border_mode*/
        e[5] === "focus"
      ), Ae(t, "hide-container", !/*explicit_call*/
      e[8] && !/*container*/
      e[9]), te(
        t,
        "height",
        /*get_dimension*/
        e[15](
          /*height*/
          e[0]
        )
      ), te(t, "width", typeof /*width*/
      e[1] == "number" ? `calc(min(${/*width*/
      e[1]}px, 100%))` : (
        /*get_dimension*/
        e[15](
          /*width*/
          e[1]
        )
      )), te(
        t,
        "border-style",
        /*variant*/
        e[4]
      ), te(
        t,
        "overflow",
        /*allow_overflow*/
        e[11] ? "visible" : "hidden"
      ), te(
        t,
        "flex-grow",
        /*scale*/
        e[12]
      ), te(t, "min-width", `calc(min(${/*min_width*/
      e[13]}px, 100%))`), te(t, "border-width", "var(--block-border-width)");
    },
    m(o, u) {
      wr(o, t, u), r && r.m(t, null), i = !0;
    },
    p(o, u) {
      r && r.p && (!i || u & /*$$scope*/
      131072) && Sr(
        r,
        l,
        o,
        /*$$scope*/
        o[17],
        i ? gr(
          l,
          /*$$scope*/
          o[17],
          u,
          null
        ) : pr(
          /*$$scope*/
          o[17]
        ),
        null
      ), Jn(
        /*tag*/
        o[14]
      )(t, s = vr(a, [
        (!i || u & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          o[7]
        ) },
        (!i || u & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          o[2]
        ) },
        (!i || u & /*elem_classes*/
        8 && n !== (n = "block " + /*elem_classes*/
        o[3].join(" ") + " svelte-1t38q2d")) && { class: n }
      ])), Ae(
        t,
        "hidden",
        /*visible*/
        o[10] === !1
      ), Ae(
        t,
        "padded",
        /*padding*/
        o[6]
      ), Ae(
        t,
        "border_focus",
        /*border_mode*/
        o[5] === "focus"
      ), Ae(t, "hide-container", !/*explicit_call*/
      o[8] && !/*container*/
      o[9]), u & /*height*/
      1 && te(
        t,
        "height",
        /*get_dimension*/
        o[15](
          /*height*/
          o[0]
        )
      ), u & /*width*/
      2 && te(t, "width", typeof /*width*/
      o[1] == "number" ? `calc(min(${/*width*/
      o[1]}px, 100%))` : (
        /*get_dimension*/
        o[15](
          /*width*/
          o[1]
        )
      )), u & /*variant*/
      16 && te(
        t,
        "border-style",
        /*variant*/
        o[4]
      ), u & /*allow_overflow*/
      2048 && te(
        t,
        "overflow",
        /*allow_overflow*/
        o[11] ? "visible" : "hidden"
      ), u & /*scale*/
      4096 && te(
        t,
        "flex-grow",
        /*scale*/
        o[12]
      ), u & /*min_width*/
      8192 && te(t, "min-width", `calc(min(${/*min_width*/
      o[13]}px, 100%))`);
    },
    i(o) {
      i || (tl(r, o), i = !0);
    },
    o(o) {
      nl(r, o), i = !1;
    },
    d(o) {
      o && dr(t), r && r.d(o);
    }
  };
}
function Ar(e) {
  let t, n = (
    /*tag*/
    e[14] && Tr(e)
  );
  return {
    c() {
      n && n.c();
    },
    m(i, l) {
      n && n.m(i, l), t = !0;
    },
    p(i, [l]) {
      /*tag*/
      i[14] && n.p(i, l);
    },
    i(i) {
      t || (tl(n, i), t = !0);
    },
    o(i) {
      nl(n, i), t = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function Hr(e, t, n) {
  let { $$slots: i = {}, $$scope: l } = t, { height: r = void 0 } = t, { width: a = void 0 } = t, { elem_id: s = "" } = t, { elem_classes: o = [] } = t, { variant: u = "solid" } = t, { border_mode: f = "base" } = t, { padding: h = !0 } = t, { type: d = "normal" } = t, { test_id: b = void 0 } = t, { explicit_call: y = !1 } = t, { container: w = !0 } = t, { visible: p = !0 } = t, { allow_overflow: m = !0 } = t, { scale: v = null } = t, { min_width: c = 0 } = t, _ = d === "fieldset" ? "fieldset" : "div";
  const E = (g) => {
    if (g !== void 0) {
      if (typeof g == "number")
        return g + "px";
      if (typeof g == "string")
        return g;
    }
  };
  return e.$$set = (g) => {
    "height" in g && n(0, r = g.height), "width" in g && n(1, a = g.width), "elem_id" in g && n(2, s = g.elem_id), "elem_classes" in g && n(3, o = g.elem_classes), "variant" in g && n(4, u = g.variant), "border_mode" in g && n(5, f = g.border_mode), "padding" in g && n(6, h = g.padding), "type" in g && n(16, d = g.type), "test_id" in g && n(7, b = g.test_id), "explicit_call" in g && n(8, y = g.explicit_call), "container" in g && n(9, w = g.container), "visible" in g && n(10, p = g.visible), "allow_overflow" in g && n(11, m = g.allow_overflow), "scale" in g && n(12, v = g.scale), "min_width" in g && n(13, c = g.min_width), "$$scope" in g && n(17, l = g.$$scope);
  }, [
    r,
    a,
    s,
    o,
    u,
    f,
    h,
    b,
    y,
    w,
    p,
    m,
    v,
    c,
    _,
    E,
    d,
    l,
    i
  ];
}
class Br extends hr {
  constructor(t) {
    super(), yr(this, t, Hr, Ar, Er, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: kr,
  attr: Cr,
  create_slot: Pr,
  detach: Nr,
  element: Or,
  get_all_dirty_from_scope: Ir,
  get_slot_changes: Lr,
  init: Mr,
  insert: Rr,
  safe_not_equal: Dr,
  transition_in: Ur,
  transition_out: Gr,
  update_slot_base: Fr
} = window.__gradio__svelte__internal;
function jr(e) {
  let t, n;
  const i = (
    /*#slots*/
    e[1].default
  ), l = Pr(
    i,
    e,
    /*$$scope*/
    e[0],
    null
  );
  return {
    c() {
      t = Or("div"), l && l.c(), Cr(t, "class", "svelte-1hnfib2");
    },
    m(r, a) {
      Rr(r, t, a), l && l.m(t, null), n = !0;
    },
    p(r, [a]) {
      l && l.p && (!n || a & /*$$scope*/
      1) && Fr(
        l,
        i,
        r,
        /*$$scope*/
        r[0],
        n ? Lr(
          i,
          /*$$scope*/
          r[0],
          a,
          null
        ) : Ir(
          /*$$scope*/
          r[0]
        ),
        null
      );
    },
    i(r) {
      n || (Ur(l, r), n = !0);
    },
    o(r) {
      Gr(l, r), n = !1;
    },
    d(r) {
      r && Nr(t), l && l.d(r);
    }
  };
}
function xr(e, t, n) {
  let { $$slots: i = {}, $$scope: l } = t;
  return e.$$set = (r) => {
    "$$scope" in r && n(0, l = r.$$scope);
  }, [l, i];
}
class Vr extends kr {
  constructor(t) {
    super(), Mr(this, t, xr, jr, Dr, {});
  }
}
const {
  SvelteComponent: qr,
  attr: Yn,
  check_outros: Xr,
  create_component: zr,
  create_slot: Zr,
  destroy_component: Wr,
  detach: Bt,
  element: Qr,
  empty: Jr,
  get_all_dirty_from_scope: Yr,
  get_slot_changes: Kr,
  group_outros: $r,
  init: es,
  insert: kt,
  mount_component: ts,
  safe_not_equal: ns,
  set_data: is,
  space: ls,
  text: rs,
  toggle_class: Re,
  transition_in: at,
  transition_out: Ct,
  update_slot_base: ss
} = window.__gradio__svelte__internal;
function Kn(e) {
  let t, n;
  return t = new Vr({
    props: {
      $$slots: { default: [os] },
      $$scope: { ctx: e }
    }
  }), {
    c() {
      zr(t.$$.fragment);
    },
    m(i, l) {
      ts(t, i, l), n = !0;
    },
    p(i, l) {
      const r = {};
      l & /*$$scope, info*/
      10 && (r.$$scope = { dirty: l, ctx: i }), t.$set(r);
    },
    i(i) {
      n || (at(t.$$.fragment, i), n = !0);
    },
    o(i) {
      Ct(t.$$.fragment, i), n = !1;
    },
    d(i) {
      Wr(t, i);
    }
  };
}
function os(e) {
  let t;
  return {
    c() {
      t = rs(
        /*info*/
        e[1]
      );
    },
    m(n, i) {
      kt(n, t, i);
    },
    p(n, i) {
      i & /*info*/
      2 && is(
        t,
        /*info*/
        n[1]
      );
    },
    d(n) {
      n && Bt(t);
    }
  };
}
function as(e) {
  let t, n, i, l;
  const r = (
    /*#slots*/
    e[2].default
  ), a = Zr(
    r,
    e,
    /*$$scope*/
    e[3],
    null
  );
  let s = (
    /*info*/
    e[1] && Kn(e)
  );
  return {
    c() {
      t = Qr("span"), a && a.c(), n = ls(), s && s.c(), i = Jr(), Yn(t, "data-testid", "block-info"), Yn(t, "class", "svelte-22c38v"), Re(t, "sr-only", !/*show_label*/
      e[0]), Re(t, "hide", !/*show_label*/
      e[0]), Re(
        t,
        "has-info",
        /*info*/
        e[1] != null
      );
    },
    m(o, u) {
      kt(o, t, u), a && a.m(t, null), kt(o, n, u), s && s.m(o, u), kt(o, i, u), l = !0;
    },
    p(o, [u]) {
      a && a.p && (!l || u & /*$$scope*/
      8) && ss(
        a,
        r,
        o,
        /*$$scope*/
        o[3],
        l ? Kr(
          r,
          /*$$scope*/
          o[3],
          u,
          null
        ) : Yr(
          /*$$scope*/
          o[3]
        ),
        null
      ), (!l || u & /*show_label*/
      1) && Re(t, "sr-only", !/*show_label*/
      o[0]), (!l || u & /*show_label*/
      1) && Re(t, "hide", !/*show_label*/
      o[0]), (!l || u & /*info*/
      2) && Re(
        t,
        "has-info",
        /*info*/
        o[1] != null
      ), /*info*/
      o[1] ? s ? (s.p(o, u), u & /*info*/
      2 && at(s, 1)) : (s = Kn(o), s.c(), at(s, 1), s.m(i.parentNode, i)) : s && ($r(), Ct(s, 1, 1, () => {
        s = null;
      }), Xr());
    },
    i(o) {
      l || (at(a, o), at(s), l = !0);
    },
    o(o) {
      Ct(a, o), Ct(s), l = !1;
    },
    d(o) {
      o && (Bt(t), Bt(n), Bt(i)), a && a.d(o), s && s.d(o);
    }
  };
}
function us(e, t, n) {
  let { $$slots: i = {}, $$scope: l } = t, { show_label: r = !0 } = t, { info: a = void 0 } = t;
  return e.$$set = (s) => {
    "show_label" in s && n(0, r = s.show_label), "info" in s && n(1, a = s.info), "$$scope" in s && n(3, l = s.$$scope);
  }, [r, a, i, l];
}
class il extends qr {
  constructor(t) {
    super(), es(this, t, us, as, ns, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: fs,
  append: cs,
  attr: De,
  detach: hs,
  init: _s,
  insert: ms,
  noop: Yt,
  safe_not_equal: ds,
  svg_element: $n
} = window.__gradio__svelte__internal;
function bs(e) {
  let t, n;
  return {
    c() {
      t = $n("svg"), n = $n("path"), De(n, "d", "M5 8l4 4 4-4z"), De(t, "class", "dropdown-arrow svelte-145leq6"), De(t, "xmlns", "http://www.w3.org/2000/svg"), De(t, "width", "100%"), De(t, "height", "100%"), De(t, "viewBox", "0 0 18 18");
    },
    m(i, l) {
      ms(i, t, l), cs(t, n);
    },
    p: Yt,
    i: Yt,
    o: Yt,
    d(i) {
      i && hs(t);
    }
  };
}
class ll extends fs {
  constructor(t) {
    super(), _s(this, t, null, bs, ds, {});
  }
}
const {
  SvelteComponent: ps,
  append: gs,
  attr: Kt,
  detach: vs,
  init: ys,
  insert: ws,
  noop: $t,
  safe_not_equal: Es,
  svg_element: ei
} = window.__gradio__svelte__internal;
function Ss(e) {
  let t, n;
  return {
    c() {
      t = ei("svg"), n = ei("path"), Kt(n, "d", "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"), Kt(t, "xmlns", "http://www.w3.org/2000/svg"), Kt(t, "viewBox", "0 0 24 24");
    },
    m(i, l) {
      ws(i, t, l), gs(t, n);
    },
    p: $t,
    i: $t,
    o: $t,
    d(i) {
      i && vs(t);
    }
  };
}
class rl extends ps {
  constructor(t) {
    super(), ys(this, t, null, Ss, Es, {});
  }
}
const Ts = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], ti = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Ts.reduce(
  (e, { color: t, primary: n, secondary: i }) => ({
    ...e,
    [t]: {
      primary: ti[t][n],
      secondary: ti[t][i]
    }
  }),
  {}
);
function As(e, t) {
  return (e % t + t) % t;
}
function hn(e, t) {
  return e.reduce((n, i, l) => ((!t || i[0].toLowerCase().includes(t.toLowerCase())) && n.push(l), n), []);
}
function sl(e, t, n) {
  e("change", t), n || e("input");
}
function ol(e, t, n) {
  if (e.key === "Escape")
    return [!1, t];
  if ((e.key === "ArrowDown" || e.key === "ArrowUp") && n.length >= 0)
    if (t === null)
      t = e.key === "ArrowDown" ? n[0] : n[n.length - 1];
    else {
      const i = n.indexOf(t), l = e.key === "ArrowUp" ? -1 : 1;
      t = n[As(i + l, n.length)];
    }
  return [!0, t];
}
const {
  SvelteComponent: Hs,
  append: Ne,
  attr: ne,
  binding_callbacks: Bs,
  check_outros: ks,
  create_component: _n,
  destroy_component: mn,
  detach: Cn,
  element: je,
  group_outros: Cs,
  init: Ps,
  insert: Pn,
  listen: rt,
  mount_component: dn,
  run_all: Ns,
  safe_not_equal: Os,
  set_data: Is,
  set_input_value: ni,
  space: en,
  text: Ls,
  toggle_class: Ue,
  transition_in: xe,
  transition_out: ut
} = window.__gradio__svelte__internal, { createEventDispatcher: Ms, afterUpdate: Rs } = window.__gradio__svelte__internal;
function Ds(e) {
  let t;
  return {
    c() {
      t = Ls(
        /*label*/
        e[0]
      );
    },
    m(n, i) {
      Pn(n, t, i);
    },
    p(n, i) {
      i[0] & /*label*/
      1 && Is(
        t,
        /*label*/
        n[0]
      );
    },
    d(n) {
      n && Cn(t);
    }
  };
}
function ii(e) {
  let t, n, i;
  return n = new ll({}), {
    c() {
      t = je("div"), _n(n.$$.fragment), ne(t, "class", "icon-wrap svelte-1m1zvyj");
    },
    m(l, r) {
      Pn(l, t, r), dn(n, t, null), i = !0;
    },
    i(l) {
      i || (xe(n.$$.fragment, l), i = !0);
    },
    o(l) {
      ut(n.$$.fragment, l), i = !1;
    },
    d(l) {
      l && Cn(t), mn(n);
    }
  };
}
function Us(e) {
  let t, n, i, l, r, a, s, o, u, f, h, d, b, y;
  n = new il({
    props: {
      show_label: (
        /*show_label*/
        e[4]
      ),
      info: (
        /*info*/
        e[1]
      ),
      $$slots: { default: [Ds] },
      $$scope: { ctx: e }
    }
  });
  let w = !/*disabled*/
  e[3] && ii();
  return h = new el({
    props: {
      show_options: (
        /*show_options*/
        e[12]
      ),
      choices: (
        /*choices*/
        e[2]
      ),
      filtered_indices: (
        /*filtered_indices*/
        e[10]
      ),
      disabled: (
        /*disabled*/
        e[3]
      ),
      selected_indices: (
        /*selected_index*/
        e[11] === null ? [] : [
          /*selected_index*/
          e[11]
        ]
      ),
      active_index: (
        /*active_index*/
        e[14]
      )
    }
  }), h.$on(
    "change",
    /*handle_option_selected*/
    e[16]
  ), {
    c() {
      t = je("div"), _n(n.$$.fragment), i = en(), l = je("div"), r = je("div"), a = je("div"), s = je("input"), u = en(), w && w.c(), f = en(), _n(h.$$.fragment), ne(s, "role", "listbox"), ne(s, "aria-controls", "dropdown-options"), ne(
        s,
        "aria-expanded",
        /*show_options*/
        e[12]
      ), ne(
        s,
        "aria-label",
        /*label*/
        e[0]
      ), ne(s, "class", "border-none svelte-1m1zvyj"), s.disabled = /*disabled*/
      e[3], ne(s, "autocomplete", "off"), s.readOnly = o = !/*filterable*/
      e[7], Ue(s, "subdued", !/*choices_names*/
      e[13].includes(
        /*input_text*/
        e[9]
      ) && !/*allow_custom_value*/
      e[6]), ne(a, "class", "secondary-wrap svelte-1m1zvyj"), ne(r, "class", "wrap-inner svelte-1m1zvyj"), Ue(
        r,
        "show_options",
        /*show_options*/
        e[12]
      ), ne(l, "class", "wrap svelte-1m1zvyj"), ne(t, "class", "svelte-1m1zvyj"), Ue(
        t,
        "container",
        /*container*/
        e[5]
      );
    },
    m(p, m) {
      Pn(p, t, m), dn(n, t, null), Ne(t, i), Ne(t, l), Ne(l, r), Ne(r, a), Ne(a, s), ni(
        s,
        /*input_text*/
        e[9]
      ), e[29](s), Ne(a, u), w && w.m(a, null), Ne(l, f), dn(h, l, null), d = !0, b || (y = [
        rt(
          s,
          "input",
          /*input_input_handler*/
          e[28]
        ),
        rt(
          s,
          "keydown",
          /*handle_key_down*/
          e[19]
        ),
        rt(
          s,
          "keyup",
          /*keyup_handler*/
          e[30]
        ),
        rt(
          s,
          "blur",
          /*handle_blur*/
          e[18]
        ),
        rt(
          s,
          "focus",
          /*handle_focus*/
          e[17]
        )
      ], b = !0);
    },
    p(p, m) {
      const v = {};
      m[0] & /*show_label*/
      16 && (v.show_label = /*show_label*/
      p[4]), m[0] & /*info*/
      2 && (v.info = /*info*/
      p[1]), m[0] & /*label*/
      1 | m[1] & /*$$scope*/
      4 && (v.$$scope = { dirty: m, ctx: p }), n.$set(v), (!d || m[0] & /*show_options*/
      4096) && ne(
        s,
        "aria-expanded",
        /*show_options*/
        p[12]
      ), (!d || m[0] & /*label*/
      1) && ne(
        s,
        "aria-label",
        /*label*/
        p[0]
      ), (!d || m[0] & /*disabled*/
      8) && (s.disabled = /*disabled*/
      p[3]), (!d || m[0] & /*filterable*/
      128 && o !== (o = !/*filterable*/
      p[7])) && (s.readOnly = o), m[0] & /*input_text*/
      512 && s.value !== /*input_text*/
      p[9] && ni(
        s,
        /*input_text*/
        p[9]
      ), (!d || m[0] & /*choices_names, input_text, allow_custom_value*/
      8768) && Ue(s, "subdued", !/*choices_names*/
      p[13].includes(
        /*input_text*/
        p[9]
      ) && !/*allow_custom_value*/
      p[6]), /*disabled*/
      p[3] ? w && (Cs(), ut(w, 1, 1, () => {
        w = null;
      }), ks()) : w ? m[0] & /*disabled*/
      8 && xe(w, 1) : (w = ii(), w.c(), xe(w, 1), w.m(a, null)), (!d || m[0] & /*show_options*/
      4096) && Ue(
        r,
        "show_options",
        /*show_options*/
        p[12]
      );
      const c = {};
      m[0] & /*show_options*/
      4096 && (c.show_options = /*show_options*/
      p[12]), m[0] & /*choices*/
      4 && (c.choices = /*choices*/
      p[2]), m[0] & /*filtered_indices*/
      1024 && (c.filtered_indices = /*filtered_indices*/
      p[10]), m[0] & /*disabled*/
      8 && (c.disabled = /*disabled*/
      p[3]), m[0] & /*selected_index*/
      2048 && (c.selected_indices = /*selected_index*/
      p[11] === null ? [] : [
        /*selected_index*/
        p[11]
      ]), m[0] & /*active_index*/
      16384 && (c.active_index = /*active_index*/
      p[14]), h.$set(c), (!d || m[0] & /*container*/
      32) && Ue(
        t,
        "container",
        /*container*/
        p[5]
      );
    },
    i(p) {
      d || (xe(n.$$.fragment, p), xe(w), xe(h.$$.fragment, p), d = !0);
    },
    o(p) {
      ut(n.$$.fragment, p), ut(w), ut(h.$$.fragment, p), d = !1;
    },
    d(p) {
      p && Cn(t), mn(n), e[29](null), w && w.d(), mn(h), b = !1, Ns(y);
    }
  };
}
function Gs(e, t, n) {
  let { label: i } = t, { info: l = void 0 } = t, { value: r = [] } = t, a = [], { value_is_output: s = !1 } = t, { choices: o } = t, u, { disabled: f = !1 } = t, { show_label: h } = t, { container: d = !0 } = t, { allow_custom_value: b = !1 } = t, { filterable: y = !0 } = t, w, p = !1, m, v, c = "", _ = "", E = !1, g = [], P = null, A = null, k;
  const q = Ms();
  r ? (k = o.map((B) => B[1]).indexOf(r), A = k, A === -1 ? (a = r, A = null) : ([c, a] = o[A], _ = c), G()) : o.length > 0 && (k = 0, A = 0, [c, r] = o[A], a = r, _ = c);
  function C() {
    n(13, m = o.map((B) => B[0])), n(24, v = o.map((B) => B[1]));
  }
  function G() {
    C(), r === void 0 ? (n(9, c = ""), n(11, A = null)) : v.includes(r) ? (n(9, c = m[v.indexOf(r)]), n(11, A = v.indexOf(r))) : b ? (n(9, c = r), n(11, A = null)) : (n(9, c = ""), n(11, A = null)), n(27, k = A);
  }
  function z(B) {
    if (n(11, A = parseInt(B.detail.target.dataset.index)), isNaN(A)) {
      n(11, A = null);
      return;
    }
    n(12, p = !1), n(14, P = null), w.blur();
  }
  function W(B) {
    n(10, g = o.map((K, U) => U)), n(12, p = !0), q("focus");
  }
  function Y() {
    b ? n(20, r = c) : n(9, c = m[v.indexOf(r)]), n(12, p = !1), n(14, P = null), q("blur");
  }
  function pe(B) {
    n(12, [p, P] = ol(B, P, g), p, (n(14, P), n(2, o), n(23, u), n(6, b), n(9, c), n(10, g), n(8, w), n(25, _), n(11, A), n(27, k), n(26, E), n(24, v))), B.key === "Enter" && (P !== null ? (n(11, A = P), n(12, p = !1), w.blur(), n(14, P = null)) : m.includes(c) ? (n(11, A = m.indexOf(c)), n(12, p = !1), n(14, P = null), w.blur()) : b && (n(20, r = c), n(11, A = null), n(12, p = !1), n(14, P = null), w.blur()));
  }
  Rs(() => {
    n(21, s = !1), n(26, E = !0);
  });
  function Ee() {
    c = this.value, n(9, c), n(11, A), n(27, k), n(26, E), n(2, o), n(24, v);
  }
  function Se(B) {
    Bs[B ? "unshift" : "push"](() => {
      w = B, n(8, w);
    });
  }
  const T = (B) => q("key_up", { key: B.key, input_value: c });
  return e.$$set = (B) => {
    "label" in B && n(0, i = B.label), "info" in B && n(1, l = B.info), "value" in B && n(20, r = B.value), "value_is_output" in B && n(21, s = B.value_is_output), "choices" in B && n(2, o = B.choices), "disabled" in B && n(3, f = B.disabled), "show_label" in B && n(4, h = B.show_label), "container" in B && n(5, d = B.container), "allow_custom_value" in B && n(6, b = B.allow_custom_value), "filterable" in B && n(7, y = B.filterable);
  }, e.$$.update = () => {
    e.$$.dirty[0] & /*selected_index, old_selected_index, initialized, choices, choices_values*/
    218105860 && A !== k && A !== null && E && (n(9, [c, r] = o[A], c, (n(20, r), n(11, A), n(27, k), n(26, E), n(2, o), n(24, v))), n(27, k = A), q("select", {
      index: A,
      value: v[A],
      selected: !0
    })), e.$$.dirty[0] & /*value, old_value, value_is_output*/
    7340032 && r != a && (G(), sl(q, r, s), n(22, a = r)), e.$$.dirty[0] & /*choices*/
    4 && C(), e.$$.dirty[0] & /*choices, old_choices, allow_custom_value, input_text, filtered_indices, filter_input*/
    8390468 && o !== u && (b || G(), n(23, u = o), n(10, g = hn(o, c)), !b && g.length > 0 && n(14, P = g[0]), w == document.activeElement && n(12, p = !0)), e.$$.dirty[0] & /*input_text, old_input_text, choices, allow_custom_value, filtered_indices*/
    33556036 && c !== _ && (n(10, g = hn(o, c)), n(25, _ = c), !b && g.length > 0 && n(14, P = g[0]));
  }, [
    i,
    l,
    o,
    f,
    h,
    d,
    b,
    y,
    w,
    c,
    g,
    A,
    p,
    m,
    P,
    q,
    z,
    W,
    Y,
    pe,
    r,
    s,
    a,
    u,
    v,
    _,
    E,
    k,
    Ee,
    Se,
    T
  ];
}
class Fs extends Hs {
  constructor(t) {
    super(), Ps(
      this,
      t,
      Gs,
      Us,
      Os,
      {
        label: 0,
        info: 1,
        value: 20,
        value_is_output: 21,
        choices: 2,
        disabled: 3,
        show_label: 4,
        container: 5,
        allow_custom_value: 6,
        filterable: 7
      },
      null,
      [-1, -1]
    );
  }
}
function Ve(e) {
  let t = ["", "k", "M", "G", "T", "P", "E", "Z"], n = 0;
  for (; e > 1e3 && n < t.length - 1; )
    e /= 1e3, n++;
  let i = t[n];
  return (Number.isInteger(e) ? e : e.toFixed(1)) + i;
}
const {
  SvelteComponent: js,
  append: ae,
  attr: M,
  component_subscribe: li,
  detach: xs,
  element: Vs,
  init: qs,
  insert: Xs,
  noop: ri,
  safe_not_equal: zs,
  set_style: Tt,
  svg_element: ue,
  toggle_class: si
} = window.__gradio__svelte__internal, { onMount: Zs } = window.__gradio__svelte__internal;
function Ws(e) {
  let t, n, i, l, r, a, s, o, u, f, h, d;
  return {
    c() {
      t = Vs("div"), n = ue("svg"), i = ue("g"), l = ue("path"), r = ue("path"), a = ue("path"), s = ue("path"), o = ue("g"), u = ue("path"), f = ue("path"), h = ue("path"), d = ue("path"), M(l, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), M(l, "fill", "#FF7C00"), M(l, "fill-opacity", "0.4"), M(l, "class", "svelte-43sxxs"), M(r, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), M(r, "fill", "#FF7C00"), M(r, "class", "svelte-43sxxs"), M(a, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), M(a, "fill", "#FF7C00"), M(a, "fill-opacity", "0.4"), M(a, "class", "svelte-43sxxs"), M(s, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), M(s, "fill", "#FF7C00"), M(s, "class", "svelte-43sxxs"), Tt(i, "transform", "translate(" + /*$top*/
      e[1][0] + "px, " + /*$top*/
      e[1][1] + "px)"), M(u, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), M(u, "fill", "#FF7C00"), M(u, "fill-opacity", "0.4"), M(u, "class", "svelte-43sxxs"), M(f, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), M(f, "fill", "#FF7C00"), M(f, "class", "svelte-43sxxs"), M(h, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), M(h, "fill", "#FF7C00"), M(h, "fill-opacity", "0.4"), M(h, "class", "svelte-43sxxs"), M(d, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), M(d, "fill", "#FF7C00"), M(d, "class", "svelte-43sxxs"), Tt(o, "transform", "translate(" + /*$bottom*/
      e[2][0] + "px, " + /*$bottom*/
      e[2][1] + "px)"), M(n, "viewBox", "-1200 -1200 3000 3000"), M(n, "fill", "none"), M(n, "xmlns", "http://www.w3.org/2000/svg"), M(n, "class", "svelte-43sxxs"), M(t, "class", "svelte-43sxxs"), si(
        t,
        "margin",
        /*margin*/
        e[0]
      );
    },
    m(b, y) {
      Xs(b, t, y), ae(t, n), ae(n, i), ae(i, l), ae(i, r), ae(i, a), ae(i, s), ae(n, o), ae(o, u), ae(o, f), ae(o, h), ae(o, d);
    },
    p(b, [y]) {
      y & /*$top*/
      2 && Tt(i, "transform", "translate(" + /*$top*/
      b[1][0] + "px, " + /*$top*/
      b[1][1] + "px)"), y & /*$bottom*/
      4 && Tt(o, "transform", "translate(" + /*$bottom*/
      b[2][0] + "px, " + /*$bottom*/
      b[2][1] + "px)"), y & /*margin*/
      1 && si(
        t,
        "margin",
        /*margin*/
        b[0]
      );
    },
    i: ri,
    o: ri,
    d(b) {
      b && xs(t);
    }
  };
}
function Qs(e, t, n) {
  let i, l, { margin: r = !0 } = t;
  const a = xn([0, 0]);
  li(e, a, (d) => n(1, i = d));
  const s = xn([0, 0]);
  li(e, s, (d) => n(2, l = d));
  let o;
  async function u() {
    await Promise.all([a.set([125, 140]), s.set([-125, -140])]), await Promise.all([a.set([-125, 140]), s.set([125, -140])]), await Promise.all([a.set([-125, 0]), s.set([125, -0])]), await Promise.all([a.set([125, 0]), s.set([-125, 0])]);
  }
  async function f() {
    await u(), o || f();
  }
  async function h() {
    await Promise.all([a.set([125, 0]), s.set([-125, 0])]), f();
  }
  return Zs(() => (h(), () => o = !0)), e.$$set = (d) => {
    "margin" in d && n(0, r = d.margin);
  }, [r, i, l, a, s];
}
class Js extends js {
  constructor(t) {
    super(), qs(this, t, Qs, Ws, zs, { margin: 0 });
  }
}
const {
  SvelteComponent: Ys,
  append: Oe,
  attr: me,
  binding_callbacks: oi,
  check_outros: al,
  create_component: Ks,
  create_slot: $s,
  destroy_component: eo,
  destroy_each: ul,
  detach: N,
  element: ve,
  empty: nt,
  ensure_array_like: It,
  get_all_dirty_from_scope: to,
  get_slot_changes: no,
  group_outros: fl,
  init: io,
  insert: O,
  mount_component: lo,
  noop: bn,
  safe_not_equal: ro,
  set_data: oe,
  set_style: ke,
  space: de,
  text: V,
  toggle_class: se,
  transition_in: Ze,
  transition_out: We,
  update_slot_base: so
} = window.__gradio__svelte__internal, { tick: oo } = window.__gradio__svelte__internal, { onDestroy: ao } = window.__gradio__svelte__internal, uo = (e) => ({}), ai = (e) => ({});
function ui(e, t, n) {
  const i = e.slice();
  return i[38] = t[n], i[40] = n, i;
}
function fi(e, t, n) {
  const i = e.slice();
  return i[38] = t[n], i;
}
function fo(e) {
  let t, n = (
    /*i18n*/
    e[1]("common.error") + ""
  ), i, l, r;
  const a = (
    /*#slots*/
    e[29].error
  ), s = $s(
    a,
    e,
    /*$$scope*/
    e[28],
    ai
  );
  return {
    c() {
      t = ve("span"), i = V(n), l = de(), s && s.c(), me(t, "class", "error svelte-1yserjw");
    },
    m(o, u) {
      O(o, t, u), Oe(t, i), O(o, l, u), s && s.m(o, u), r = !0;
    },
    p(o, u) {
      (!r || u[0] & /*i18n*/
      2) && n !== (n = /*i18n*/
      o[1]("common.error") + "") && oe(i, n), s && s.p && (!r || u[0] & /*$$scope*/
      268435456) && so(
        s,
        a,
        o,
        /*$$scope*/
        o[28],
        r ? no(
          a,
          /*$$scope*/
          o[28],
          u,
          uo
        ) : to(
          /*$$scope*/
          o[28]
        ),
        ai
      );
    },
    i(o) {
      r || (Ze(s, o), r = !0);
    },
    o(o) {
      We(s, o), r = !1;
    },
    d(o) {
      o && (N(t), N(l)), s && s.d(o);
    }
  };
}
function co(e) {
  let t, n, i, l, r, a, s, o, u, f = (
    /*variant*/
    e[8] === "default" && /*show_eta_bar*/
    e[18] && /*show_progress*/
    e[6] === "full" && ci(e)
  );
  function h(c, _) {
    if (
      /*progress*/
      c[7]
    )
      return mo;
    if (
      /*queue_position*/
      c[2] !== null && /*queue_size*/
      c[3] !== void 0 && /*queue_position*/
      c[2] >= 0
    )
      return _o;
    if (
      /*queue_position*/
      c[2] === 0
    )
      return ho;
  }
  let d = h(e), b = d && d(e), y = (
    /*timer*/
    e[5] && mi(e)
  );
  const w = [vo, go], p = [];
  function m(c, _) {
    return (
      /*last_progress_level*/
      c[15] != null ? 0 : (
        /*show_progress*/
        c[6] === "full" ? 1 : -1
      )
    );
  }
  ~(r = m(e)) && (a = p[r] = w[r](e));
  let v = !/*timer*/
  e[5] && wi(e);
  return {
    c() {
      f && f.c(), t = de(), n = ve("div"), b && b.c(), i = de(), y && y.c(), l = de(), a && a.c(), s = de(), v && v.c(), o = nt(), me(n, "class", "progress-text svelte-1yserjw"), se(
        n,
        "meta-text-center",
        /*variant*/
        e[8] === "center"
      ), se(
        n,
        "meta-text",
        /*variant*/
        e[8] === "default"
      );
    },
    m(c, _) {
      f && f.m(c, _), O(c, t, _), O(c, n, _), b && b.m(n, null), Oe(n, i), y && y.m(n, null), O(c, l, _), ~r && p[r].m(c, _), O(c, s, _), v && v.m(c, _), O(c, o, _), u = !0;
    },
    p(c, _) {
      /*variant*/
      c[8] === "default" && /*show_eta_bar*/
      c[18] && /*show_progress*/
      c[6] === "full" ? f ? f.p(c, _) : (f = ci(c), f.c(), f.m(t.parentNode, t)) : f && (f.d(1), f = null), d === (d = h(c)) && b ? b.p(c, _) : (b && b.d(1), b = d && d(c), b && (b.c(), b.m(n, i))), /*timer*/
      c[5] ? y ? y.p(c, _) : (y = mi(c), y.c(), y.m(n, null)) : y && (y.d(1), y = null), (!u || _[0] & /*variant*/
      256) && se(
        n,
        "meta-text-center",
        /*variant*/
        c[8] === "center"
      ), (!u || _[0] & /*variant*/
      256) && se(
        n,
        "meta-text",
        /*variant*/
        c[8] === "default"
      );
      let E = r;
      r = m(c), r === E ? ~r && p[r].p(c, _) : (a && (fl(), We(p[E], 1, 1, () => {
        p[E] = null;
      }), al()), ~r ? (a = p[r], a ? a.p(c, _) : (a = p[r] = w[r](c), a.c()), Ze(a, 1), a.m(s.parentNode, s)) : a = null), /*timer*/
      c[5] ? v && (v.d(1), v = null) : v ? v.p(c, _) : (v = wi(c), v.c(), v.m(o.parentNode, o));
    },
    i(c) {
      u || (Ze(a), u = !0);
    },
    o(c) {
      We(a), u = !1;
    },
    d(c) {
      c && (N(t), N(n), N(l), N(s), N(o)), f && f.d(c), b && b.d(), y && y.d(), ~r && p[r].d(c), v && v.d(c);
    }
  };
}
function ci(e) {
  let t, n = `translateX(${/*eta_level*/
  (e[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      t = ve("div"), me(t, "class", "eta-bar svelte-1yserjw"), ke(t, "transform", n);
    },
    m(i, l) {
      O(i, t, l);
    },
    p(i, l) {
      l[0] & /*eta_level*/
      131072 && n !== (n = `translateX(${/*eta_level*/
      (i[17] || 0) * 100 - 100}%)`) && ke(t, "transform", n);
    },
    d(i) {
      i && N(t);
    }
  };
}
function ho(e) {
  let t;
  return {
    c() {
      t = V("processing |");
    },
    m(n, i) {
      O(n, t, i);
    },
    p: bn,
    d(n) {
      n && N(t);
    }
  };
}
function _o(e) {
  let t, n = (
    /*queue_position*/
    e[2] + 1 + ""
  ), i, l, r, a;
  return {
    c() {
      t = V("queue: "), i = V(n), l = V("/"), r = V(
        /*queue_size*/
        e[3]
      ), a = V(" |");
    },
    m(s, o) {
      O(s, t, o), O(s, i, o), O(s, l, o), O(s, r, o), O(s, a, o);
    },
    p(s, o) {
      o[0] & /*queue_position*/
      4 && n !== (n = /*queue_position*/
      s[2] + 1 + "") && oe(i, n), o[0] & /*queue_size*/
      8 && oe(
        r,
        /*queue_size*/
        s[3]
      );
    },
    d(s) {
      s && (N(t), N(i), N(l), N(r), N(a));
    }
  };
}
function mo(e) {
  let t, n = It(
    /*progress*/
    e[7]
  ), i = [];
  for (let l = 0; l < n.length; l += 1)
    i[l] = _i(fi(e, n, l));
  return {
    c() {
      for (let l = 0; l < i.length; l += 1)
        i[l].c();
      t = nt();
    },
    m(l, r) {
      for (let a = 0; a < i.length; a += 1)
        i[a] && i[a].m(l, r);
      O(l, t, r);
    },
    p(l, r) {
      if (r[0] & /*progress*/
      128) {
        n = It(
          /*progress*/
          l[7]
        );
        let a;
        for (a = 0; a < n.length; a += 1) {
          const s = fi(l, n, a);
          i[a] ? i[a].p(s, r) : (i[a] = _i(s), i[a].c(), i[a].m(t.parentNode, t));
        }
        for (; a < i.length; a += 1)
          i[a].d(1);
        i.length = n.length;
      }
    },
    d(l) {
      l && N(t), ul(i, l);
    }
  };
}
function hi(e) {
  let t, n = (
    /*p*/
    e[38].unit + ""
  ), i, l, r = " ", a;
  function s(f, h) {
    return (
      /*p*/
      f[38].length != null ? po : bo
    );
  }
  let o = s(e), u = o(e);
  return {
    c() {
      u.c(), t = de(), i = V(n), l = V(" | "), a = V(r);
    },
    m(f, h) {
      u.m(f, h), O(f, t, h), O(f, i, h), O(f, l, h), O(f, a, h);
    },
    p(f, h) {
      o === (o = s(f)) && u ? u.p(f, h) : (u.d(1), u = o(f), u && (u.c(), u.m(t.parentNode, t))), h[0] & /*progress*/
      128 && n !== (n = /*p*/
      f[38].unit + "") && oe(i, n);
    },
    d(f) {
      f && (N(t), N(i), N(l), N(a)), u.d(f);
    }
  };
}
function bo(e) {
  let t = Ve(
    /*p*/
    e[38].index || 0
  ) + "", n;
  return {
    c() {
      n = V(t);
    },
    m(i, l) {
      O(i, n, l);
    },
    p(i, l) {
      l[0] & /*progress*/
      128 && t !== (t = Ve(
        /*p*/
        i[38].index || 0
      ) + "") && oe(n, t);
    },
    d(i) {
      i && N(n);
    }
  };
}
function po(e) {
  let t = Ve(
    /*p*/
    e[38].index || 0
  ) + "", n, i, l = Ve(
    /*p*/
    e[38].length
  ) + "", r;
  return {
    c() {
      n = V(t), i = V("/"), r = V(l);
    },
    m(a, s) {
      O(a, n, s), O(a, i, s), O(a, r, s);
    },
    p(a, s) {
      s[0] & /*progress*/
      128 && t !== (t = Ve(
        /*p*/
        a[38].index || 0
      ) + "") && oe(n, t), s[0] & /*progress*/
      128 && l !== (l = Ve(
        /*p*/
        a[38].length
      ) + "") && oe(r, l);
    },
    d(a) {
      a && (N(n), N(i), N(r));
    }
  };
}
function _i(e) {
  let t, n = (
    /*p*/
    e[38].index != null && hi(e)
  );
  return {
    c() {
      n && n.c(), t = nt();
    },
    m(i, l) {
      n && n.m(i, l), O(i, t, l);
    },
    p(i, l) {
      /*p*/
      i[38].index != null ? n ? n.p(i, l) : (n = hi(i), n.c(), n.m(t.parentNode, t)) : n && (n.d(1), n = null);
    },
    d(i) {
      i && N(t), n && n.d(i);
    }
  };
}
function mi(e) {
  let t, n = (
    /*eta*/
    e[0] ? `/${/*formatted_eta*/
    e[19]}` : ""
  ), i, l;
  return {
    c() {
      t = V(
        /*formatted_timer*/
        e[20]
      ), i = V(n), l = V("s");
    },
    m(r, a) {
      O(r, t, a), O(r, i, a), O(r, l, a);
    },
    p(r, a) {
      a[0] & /*formatted_timer*/
      1048576 && oe(
        t,
        /*formatted_timer*/
        r[20]
      ), a[0] & /*eta, formatted_eta*/
      524289 && n !== (n = /*eta*/
      r[0] ? `/${/*formatted_eta*/
      r[19]}` : "") && oe(i, n);
    },
    d(r) {
      r && (N(t), N(i), N(l));
    }
  };
}
function go(e) {
  let t, n;
  return t = new Js({
    props: { margin: (
      /*variant*/
      e[8] === "default"
    ) }
  }), {
    c() {
      Ks(t.$$.fragment);
    },
    m(i, l) {
      lo(t, i, l), n = !0;
    },
    p(i, l) {
      const r = {};
      l[0] & /*variant*/
      256 && (r.margin = /*variant*/
      i[8] === "default"), t.$set(r);
    },
    i(i) {
      n || (Ze(t.$$.fragment, i), n = !0);
    },
    o(i) {
      We(t.$$.fragment, i), n = !1;
    },
    d(i) {
      eo(t, i);
    }
  };
}
function vo(e) {
  let t, n, i, l, r, a = `${/*last_progress_level*/
  e[15] * 100}%`, s = (
    /*progress*/
    e[7] != null && di(e)
  );
  return {
    c() {
      t = ve("div"), n = ve("div"), s && s.c(), i = de(), l = ve("div"), r = ve("div"), me(n, "class", "progress-level-inner svelte-1yserjw"), me(r, "class", "progress-bar svelte-1yserjw"), ke(r, "width", a), me(l, "class", "progress-bar-wrap svelte-1yserjw"), me(t, "class", "progress-level svelte-1yserjw");
    },
    m(o, u) {
      O(o, t, u), Oe(t, n), s && s.m(n, null), Oe(t, i), Oe(t, l), Oe(l, r), e[30](r);
    },
    p(o, u) {
      /*progress*/
      o[7] != null ? s ? s.p(o, u) : (s = di(o), s.c(), s.m(n, null)) : s && (s.d(1), s = null), u[0] & /*last_progress_level*/
      32768 && a !== (a = `${/*last_progress_level*/
      o[15] * 100}%`) && ke(r, "width", a);
    },
    i: bn,
    o: bn,
    d(o) {
      o && N(t), s && s.d(), e[30](null);
    }
  };
}
function di(e) {
  let t, n = It(
    /*progress*/
    e[7]
  ), i = [];
  for (let l = 0; l < n.length; l += 1)
    i[l] = yi(ui(e, n, l));
  return {
    c() {
      for (let l = 0; l < i.length; l += 1)
        i[l].c();
      t = nt();
    },
    m(l, r) {
      for (let a = 0; a < i.length; a += 1)
        i[a] && i[a].m(l, r);
      O(l, t, r);
    },
    p(l, r) {
      if (r[0] & /*progress_level, progress*/
      16512) {
        n = It(
          /*progress*/
          l[7]
        );
        let a;
        for (a = 0; a < n.length; a += 1) {
          const s = ui(l, n, a);
          i[a] ? i[a].p(s, r) : (i[a] = yi(s), i[a].c(), i[a].m(t.parentNode, t));
        }
        for (; a < i.length; a += 1)
          i[a].d(1);
        i.length = n.length;
      }
    },
    d(l) {
      l && N(t), ul(i, l);
    }
  };
}
function bi(e) {
  let t, n, i, l, r = (
    /*i*/
    e[40] !== 0 && yo()
  ), a = (
    /*p*/
    e[38].desc != null && pi(e)
  ), s = (
    /*p*/
    e[38].desc != null && /*progress_level*/
    e[14] && /*progress_level*/
    e[14][
      /*i*/
      e[40]
    ] != null && gi()
  ), o = (
    /*progress_level*/
    e[14] != null && vi(e)
  );
  return {
    c() {
      r && r.c(), t = de(), a && a.c(), n = de(), s && s.c(), i = de(), o && o.c(), l = nt();
    },
    m(u, f) {
      r && r.m(u, f), O(u, t, f), a && a.m(u, f), O(u, n, f), s && s.m(u, f), O(u, i, f), o && o.m(u, f), O(u, l, f);
    },
    p(u, f) {
      /*p*/
      u[38].desc != null ? a ? a.p(u, f) : (a = pi(u), a.c(), a.m(n.parentNode, n)) : a && (a.d(1), a = null), /*p*/
      u[38].desc != null && /*progress_level*/
      u[14] && /*progress_level*/
      u[14][
        /*i*/
        u[40]
      ] != null ? s || (s = gi(), s.c(), s.m(i.parentNode, i)) : s && (s.d(1), s = null), /*progress_level*/
      u[14] != null ? o ? o.p(u, f) : (o = vi(u), o.c(), o.m(l.parentNode, l)) : o && (o.d(1), o = null);
    },
    d(u) {
      u && (N(t), N(n), N(i), N(l)), r && r.d(u), a && a.d(u), s && s.d(u), o && o.d(u);
    }
  };
}
function yo(e) {
  let t;
  return {
    c() {
      t = V(" /");
    },
    m(n, i) {
      O(n, t, i);
    },
    d(n) {
      n && N(t);
    }
  };
}
function pi(e) {
  let t = (
    /*p*/
    e[38].desc + ""
  ), n;
  return {
    c() {
      n = V(t);
    },
    m(i, l) {
      O(i, n, l);
    },
    p(i, l) {
      l[0] & /*progress*/
      128 && t !== (t = /*p*/
      i[38].desc + "") && oe(n, t);
    },
    d(i) {
      i && N(n);
    }
  };
}
function gi(e) {
  let t;
  return {
    c() {
      t = V("-");
    },
    m(n, i) {
      O(n, t, i);
    },
    d(n) {
      n && N(t);
    }
  };
}
function vi(e) {
  let t = (100 * /*progress_level*/
  (e[14][
    /*i*/
    e[40]
  ] || 0)).toFixed(1) + "", n, i;
  return {
    c() {
      n = V(t), i = V("%");
    },
    m(l, r) {
      O(l, n, r), O(l, i, r);
    },
    p(l, r) {
      r[0] & /*progress_level*/
      16384 && t !== (t = (100 * /*progress_level*/
      (l[14][
        /*i*/
        l[40]
      ] || 0)).toFixed(1) + "") && oe(n, t);
    },
    d(l) {
      l && (N(n), N(i));
    }
  };
}
function yi(e) {
  let t, n = (
    /*p*/
    (e[38].desc != null || /*progress_level*/
    e[14] && /*progress_level*/
    e[14][
      /*i*/
      e[40]
    ] != null) && bi(e)
  );
  return {
    c() {
      n && n.c(), t = nt();
    },
    m(i, l) {
      n && n.m(i, l), O(i, t, l);
    },
    p(i, l) {
      /*p*/
      i[38].desc != null || /*progress_level*/
      i[14] && /*progress_level*/
      i[14][
        /*i*/
        i[40]
      ] != null ? n ? n.p(i, l) : (n = bi(i), n.c(), n.m(t.parentNode, t)) : n && (n.d(1), n = null);
    },
    d(i) {
      i && N(t), n && n.d(i);
    }
  };
}
function wi(e) {
  let t, n;
  return {
    c() {
      t = ve("p"), n = V(
        /*loading_text*/
        e[9]
      ), me(t, "class", "loading svelte-1yserjw");
    },
    m(i, l) {
      O(i, t, l), Oe(t, n);
    },
    p(i, l) {
      l[0] & /*loading_text*/
      512 && oe(
        n,
        /*loading_text*/
        i[9]
      );
    },
    d(i) {
      i && N(t);
    }
  };
}
function wo(e) {
  let t, n, i, l, r;
  const a = [co, fo], s = [];
  function o(u, f) {
    return (
      /*status*/
      u[4] === "pending" ? 0 : (
        /*status*/
        u[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(n = o(e)) && (i = s[n] = a[n](e)), {
    c() {
      t = ve("div"), i && i.c(), me(t, "class", l = "wrap " + /*variant*/
      e[8] + " " + /*show_progress*/
      e[6] + " svelte-1yserjw"), se(t, "hide", !/*status*/
      e[4] || /*status*/
      e[4] === "complete" || /*show_progress*/
      e[6] === "hidden"), se(
        t,
        "translucent",
        /*variant*/
        e[8] === "center" && /*status*/
        (e[4] === "pending" || /*status*/
        e[4] === "error") || /*translucent*/
        e[11] || /*show_progress*/
        e[6] === "minimal"
      ), se(
        t,
        "generating",
        /*status*/
        e[4] === "generating"
      ), se(
        t,
        "border",
        /*border*/
        e[12]
      ), ke(
        t,
        "position",
        /*absolute*/
        e[10] ? "absolute" : "static"
      ), ke(
        t,
        "padding",
        /*absolute*/
        e[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(u, f) {
      O(u, t, f), ~n && s[n].m(t, null), e[31](t), r = !0;
    },
    p(u, f) {
      let h = n;
      n = o(u), n === h ? ~n && s[n].p(u, f) : (i && (fl(), We(s[h], 1, 1, () => {
        s[h] = null;
      }), al()), ~n ? (i = s[n], i ? i.p(u, f) : (i = s[n] = a[n](u), i.c()), Ze(i, 1), i.m(t, null)) : i = null), (!r || f[0] & /*variant, show_progress*/
      320 && l !== (l = "wrap " + /*variant*/
      u[8] + " " + /*show_progress*/
      u[6] + " svelte-1yserjw")) && me(t, "class", l), (!r || f[0] & /*variant, show_progress, status, show_progress*/
      336) && se(t, "hide", !/*status*/
      u[4] || /*status*/
      u[4] === "complete" || /*show_progress*/
      u[6] === "hidden"), (!r || f[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && se(
        t,
        "translucent",
        /*variant*/
        u[8] === "center" && /*status*/
        (u[4] === "pending" || /*status*/
        u[4] === "error") || /*translucent*/
        u[11] || /*show_progress*/
        u[6] === "minimal"
      ), (!r || f[0] & /*variant, show_progress, status*/
      336) && se(
        t,
        "generating",
        /*status*/
        u[4] === "generating"
      ), (!r || f[0] & /*variant, show_progress, border*/
      4416) && se(
        t,
        "border",
        /*border*/
        u[12]
      ), f[0] & /*absolute*/
      1024 && ke(
        t,
        "position",
        /*absolute*/
        u[10] ? "absolute" : "static"
      ), f[0] & /*absolute*/
      1024 && ke(
        t,
        "padding",
        /*absolute*/
        u[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(u) {
      r || (Ze(i), r = !0);
    },
    o(u) {
      We(i), r = !1;
    },
    d(u) {
      u && N(t), ~n && s[n].d(), e[31](null);
    }
  };
}
let At = [], tn = !1;
async function Eo(e, t = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
    if (At.push(e), !tn)
      tn = !0;
    else
      return;
    await oo(), requestAnimationFrame(() => {
      let n = [0, 0];
      for (let i = 0; i < At.length; i++) {
        const r = At[i].getBoundingClientRect();
        (i === 0 || r.top + window.scrollY <= n[0]) && (n[0] = r.top + window.scrollY, n[1] = i);
      }
      window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), tn = !1, At = [];
    });
  }
}
function So(e, t, n) {
  let i, { $$slots: l = {}, $$scope: r } = t, { i18n: a } = t, { eta: s = null } = t, { queue_position: o } = t, { queue_size: u } = t, { status: f } = t, { scroll_to_output: h = !1 } = t, { timer: d = !0 } = t, { show_progress: b = "full" } = t, { message: y = null } = t, { progress: w = null } = t, { variant: p = "default" } = t, { loading_text: m = "Loading..." } = t, { absolute: v = !0 } = t, { translucent: c = !1 } = t, { border: _ = !1 } = t, { autoscroll: E } = t, g, P = !1, A = 0, k = 0, q = null, C = null, G = 0, z = null, W, Y = null, pe = !0;
  const Ee = () => {
    n(0, s = n(26, q = n(19, B = null))), n(24, A = performance.now()), n(25, k = 0), P = !0, Se();
  };
  function Se() {
    requestAnimationFrame(() => {
      n(25, k = (performance.now() - A) / 1e3), P && Se();
    });
  }
  function T() {
    n(25, k = 0), n(0, s = n(26, q = n(19, B = null))), P && (P = !1);
  }
  ao(() => {
    P && T();
  });
  let B = null;
  function K(H) {
    oi[H ? "unshift" : "push"](() => {
      Y = H, n(16, Y), n(7, w), n(14, z), n(15, W);
    });
  }
  function U(H) {
    oi[H ? "unshift" : "push"](() => {
      g = H, n(13, g);
    });
  }
  return e.$$set = (H) => {
    "i18n" in H && n(1, a = H.i18n), "eta" in H && n(0, s = H.eta), "queue_position" in H && n(2, o = H.queue_position), "queue_size" in H && n(3, u = H.queue_size), "status" in H && n(4, f = H.status), "scroll_to_output" in H && n(21, h = H.scroll_to_output), "timer" in H && n(5, d = H.timer), "show_progress" in H && n(6, b = H.show_progress), "message" in H && n(22, y = H.message), "progress" in H && n(7, w = H.progress), "variant" in H && n(8, p = H.variant), "loading_text" in H && n(9, m = H.loading_text), "absolute" in H && n(10, v = H.absolute), "translucent" in H && n(11, c = H.translucent), "border" in H && n(12, _ = H.border), "autoscroll" in H && n(23, E = H.autoscroll), "$$scope" in H && n(28, r = H.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    218103809 && (s === null && n(0, s = q), s != null && q !== s && (n(27, C = (performance.now() - A) / 1e3 + s), n(19, B = C.toFixed(1)), n(26, q = s))), e.$$.dirty[0] & /*eta_from_start, timer_diff*/
    167772160 && n(17, G = C === null || C <= 0 || !k ? null : Math.min(k / C, 1)), e.$$.dirty[0] & /*progress*/
    128 && w != null && n(18, pe = !1), e.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (w != null ? n(14, z = w.map((H) => {
      if (H.index != null && H.length != null)
        return H.index / H.length;
      if (H.progress != null)
        return H.progress;
    })) : n(14, z = null), z ? (n(15, W = z[z.length - 1]), Y && (W === 0 ? n(16, Y.style.transition = "0", Y) : n(16, Y.style.transition = "150ms", Y))) : n(15, W = void 0)), e.$$.dirty[0] & /*status*/
    16 && (f === "pending" ? Ee() : T()), e.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    10493968 && g && h && (f === "pending" || f === "complete") && Eo(g, E), e.$$.dirty[0] & /*status, message*/
    4194320, e.$$.dirty[0] & /*timer_diff*/
    33554432 && n(20, i = k.toFixed(1));
  }, [
    s,
    a,
    o,
    u,
    f,
    d,
    b,
    w,
    p,
    m,
    v,
    c,
    _,
    g,
    z,
    W,
    Y,
    G,
    pe,
    B,
    i,
    h,
    y,
    E,
    A,
    k,
    q,
    C,
    r,
    l,
    K,
    U
  ];
}
class To extends Ys {
  constructor(t) {
    super(), io(
      this,
      t,
      So,
      wo,
      ro,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 21,
        timer: 5,
        show_progress: 6,
        message: 22,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 23
      },
      null,
      [-1, -1]
    );
  }
}
class Ao {
  constructor({
    name: t,
    token: n,
    param_specs: i
  }) {
    this.name = t, this.token = n, this.param_specs = i || new Object();
  }
}
var cl = (e, t, n) => {
  if (!t.has(e))
    throw TypeError("Cannot " + n);
}, st = (e, t, n) => (cl(e, t, "read from private field"), n ? n.call(e) : t.get(e)), Ho = (e, t, n) => {
  if (t.has(e))
    throw TypeError("Cannot add the same private member more than once");
  t instanceof WeakSet ? t.add(e) : t.set(e, n);
}, Bo = (e, t, n, i) => (cl(e, t, "write to private field"), i ? i.call(e, n) : t.set(e, n), n), He;
new Intl.Collator(0, { numeric: 1 }).compare;
typeof process < "u" && process.versions && process.versions.node;
class hf extends TransformStream {
  /** Constructs a new instance. */
  constructor(t = { allowCR: !1 }) {
    super({
      transform: (n, i) => {
        for (n = st(this, He) + n; ; ) {
          const l = n.indexOf(`
`), r = t.allowCR ? n.indexOf("\r") : -1;
          if (r !== -1 && r !== n.length - 1 && (l === -1 || l - 1 > r)) {
            i.enqueue(n.slice(0, r)), n = n.slice(r + 1);
            continue;
          }
          if (l === -1)
            break;
          const a = n[l - 1] === "\r" ? l - 1 : l;
          i.enqueue(n.slice(0, a)), n = n.slice(l + 1);
        }
        Bo(this, He, n);
      },
      flush: (n) => {
        if (st(this, He) === "")
          return;
        const i = t.allowCR && st(this, He).endsWith("\r") ? st(this, He).slice(0, -1) : st(this, He);
        n.enqueue(i);
      }
    }), Ho(this, He, "");
  }
}
He = /* @__PURE__ */ new WeakMap();
const {
  SvelteComponent: ko,
  append: hl,
  attr: x,
  bubble: Co,
  check_outros: Po,
  create_slot: _l,
  detach: gt,
  element: jt,
  empty: No,
  get_all_dirty_from_scope: ml,
  get_slot_changes: dl,
  group_outros: Oo,
  init: Io,
  insert: vt,
  listen: Lo,
  safe_not_equal: Mo,
  set_style: $,
  space: bl,
  src_url_equal: Lt,
  toggle_class: qe,
  transition_in: Mt,
  transition_out: Rt,
  update_slot_base: pl
} = window.__gradio__svelte__internal;
function Ro(e) {
  let t, n, i, l, r, a, s = (
    /*icon*/
    e[7] && Ei(e)
  );
  const o = (
    /*#slots*/
    e[12].default
  ), u = _l(
    o,
    e,
    /*$$scope*/
    e[11],
    null
  );
  return {
    c() {
      t = jt("button"), s && s.c(), n = bl(), u && u.c(), x(t, "class", i = /*size*/
      e[4] + " " + /*variant*/
      e[3] + " " + /*elem_classes*/
      e[1].join(" ") + " svelte-8huxfn"), x(
        t,
        "id",
        /*elem_id*/
        e[0]
      ), t.disabled = /*disabled*/
      e[8], qe(t, "hidden", !/*visible*/
      e[2]), $(
        t,
        "flex-grow",
        /*scale*/
        e[9]
      ), $(
        t,
        "width",
        /*scale*/
        e[9] === 0 ? "fit-content" : null
      ), $(t, "min-width", typeof /*min_width*/
      e[10] == "number" ? `calc(min(${/*min_width*/
      e[10]}px, 100%))` : null);
    },
    m(f, h) {
      vt(f, t, h), s && s.m(t, null), hl(t, n), u && u.m(t, null), l = !0, r || (a = Lo(
        t,
        "click",
        /*click_handler*/
        e[13]
      ), r = !0);
    },
    p(f, h) {
      /*icon*/
      f[7] ? s ? s.p(f, h) : (s = Ei(f), s.c(), s.m(t, n)) : s && (s.d(1), s = null), u && u.p && (!l || h & /*$$scope*/
      2048) && pl(
        u,
        o,
        f,
        /*$$scope*/
        f[11],
        l ? dl(
          o,
          /*$$scope*/
          f[11],
          h,
          null
        ) : ml(
          /*$$scope*/
          f[11]
        ),
        null
      ), (!l || h & /*size, variant, elem_classes*/
      26 && i !== (i = /*size*/
      f[4] + " " + /*variant*/
      f[3] + " " + /*elem_classes*/
      f[1].join(" ") + " svelte-8huxfn")) && x(t, "class", i), (!l || h & /*elem_id*/
      1) && x(
        t,
        "id",
        /*elem_id*/
        f[0]
      ), (!l || h & /*disabled*/
      256) && (t.disabled = /*disabled*/
      f[8]), (!l || h & /*size, variant, elem_classes, visible*/
      30) && qe(t, "hidden", !/*visible*/
      f[2]), h & /*scale*/
      512 && $(
        t,
        "flex-grow",
        /*scale*/
        f[9]
      ), h & /*scale*/
      512 && $(
        t,
        "width",
        /*scale*/
        f[9] === 0 ? "fit-content" : null
      ), h & /*min_width*/
      1024 && $(t, "min-width", typeof /*min_width*/
      f[10] == "number" ? `calc(min(${/*min_width*/
      f[10]}px, 100%))` : null);
    },
    i(f) {
      l || (Mt(u, f), l = !0);
    },
    o(f) {
      Rt(u, f), l = !1;
    },
    d(f) {
      f && gt(t), s && s.d(), u && u.d(f), r = !1, a();
    }
  };
}
function Do(e) {
  let t, n, i, l, r = (
    /*icon*/
    e[7] && Si(e)
  );
  const a = (
    /*#slots*/
    e[12].default
  ), s = _l(
    a,
    e,
    /*$$scope*/
    e[11],
    null
  );
  return {
    c() {
      t = jt("a"), r && r.c(), n = bl(), s && s.c(), x(
        t,
        "href",
        /*link*/
        e[6]
      ), x(t, "rel", "noopener noreferrer"), x(
        t,
        "aria-disabled",
        /*disabled*/
        e[8]
      ), x(t, "class", i = /*size*/
      e[4] + " " + /*variant*/
      e[3] + " " + /*elem_classes*/
      e[1].join(" ") + " svelte-8huxfn"), x(
        t,
        "id",
        /*elem_id*/
        e[0]
      ), qe(t, "hidden", !/*visible*/
      e[2]), qe(
        t,
        "disabled",
        /*disabled*/
        e[8]
      ), $(
        t,
        "flex-grow",
        /*scale*/
        e[9]
      ), $(
        t,
        "pointer-events",
        /*disabled*/
        e[8] ? "none" : null
      ), $(
        t,
        "width",
        /*scale*/
        e[9] === 0 ? "fit-content" : null
      ), $(t, "min-width", typeof /*min_width*/
      e[10] == "number" ? `calc(min(${/*min_width*/
      e[10]}px, 100%))` : null);
    },
    m(o, u) {
      vt(o, t, u), r && r.m(t, null), hl(t, n), s && s.m(t, null), l = !0;
    },
    p(o, u) {
      /*icon*/
      o[7] ? r ? r.p(o, u) : (r = Si(o), r.c(), r.m(t, n)) : r && (r.d(1), r = null), s && s.p && (!l || u & /*$$scope*/
      2048) && pl(
        s,
        a,
        o,
        /*$$scope*/
        o[11],
        l ? dl(
          a,
          /*$$scope*/
          o[11],
          u,
          null
        ) : ml(
          /*$$scope*/
          o[11]
        ),
        null
      ), (!l || u & /*link*/
      64) && x(
        t,
        "href",
        /*link*/
        o[6]
      ), (!l || u & /*disabled*/
      256) && x(
        t,
        "aria-disabled",
        /*disabled*/
        o[8]
      ), (!l || u & /*size, variant, elem_classes*/
      26 && i !== (i = /*size*/
      o[4] + " " + /*variant*/
      o[3] + " " + /*elem_classes*/
      o[1].join(" ") + " svelte-8huxfn")) && x(t, "class", i), (!l || u & /*elem_id*/
      1) && x(
        t,
        "id",
        /*elem_id*/
        o[0]
      ), (!l || u & /*size, variant, elem_classes, visible*/
      30) && qe(t, "hidden", !/*visible*/
      o[2]), (!l || u & /*size, variant, elem_classes, disabled*/
      282) && qe(
        t,
        "disabled",
        /*disabled*/
        o[8]
      ), u & /*scale*/
      512 && $(
        t,
        "flex-grow",
        /*scale*/
        o[9]
      ), u & /*disabled*/
      256 && $(
        t,
        "pointer-events",
        /*disabled*/
        o[8] ? "none" : null
      ), u & /*scale*/
      512 && $(
        t,
        "width",
        /*scale*/
        o[9] === 0 ? "fit-content" : null
      ), u & /*min_width*/
      1024 && $(t, "min-width", typeof /*min_width*/
      o[10] == "number" ? `calc(min(${/*min_width*/
      o[10]}px, 100%))` : null);
    },
    i(o) {
      l || (Mt(s, o), l = !0);
    },
    o(o) {
      Rt(s, o), l = !1;
    },
    d(o) {
      o && gt(t), r && r.d(), s && s.d(o);
    }
  };
}
function Ei(e) {
  let t, n, i;
  return {
    c() {
      t = jt("img"), x(t, "class", "button-icon svelte-8huxfn"), Lt(t.src, n = /*icon*/
      e[7].url) || x(t, "src", n), x(t, "alt", i = `${/*value*/
      e[5]} icon`);
    },
    m(l, r) {
      vt(l, t, r);
    },
    p(l, r) {
      r & /*icon*/
      128 && !Lt(t.src, n = /*icon*/
      l[7].url) && x(t, "src", n), r & /*value*/
      32 && i !== (i = `${/*value*/
      l[5]} icon`) && x(t, "alt", i);
    },
    d(l) {
      l && gt(t);
    }
  };
}
function Si(e) {
  let t, n, i;
  return {
    c() {
      t = jt("img"), x(t, "class", "button-icon svelte-8huxfn"), Lt(t.src, n = /*icon*/
      e[7].url) || x(t, "src", n), x(t, "alt", i = `${/*value*/
      e[5]} icon`);
    },
    m(l, r) {
      vt(l, t, r);
    },
    p(l, r) {
      r & /*icon*/
      128 && !Lt(t.src, n = /*icon*/
      l[7].url) && x(t, "src", n), r & /*value*/
      32 && i !== (i = `${/*value*/
      l[5]} icon`) && x(t, "alt", i);
    },
    d(l) {
      l && gt(t);
    }
  };
}
function Uo(e) {
  let t, n, i, l;
  const r = [Do, Ro], a = [];
  function s(o, u) {
    return (
      /*link*/
      o[6] && /*link*/
      o[6].length > 0 ? 0 : 1
    );
  }
  return t = s(e), n = a[t] = r[t](e), {
    c() {
      n.c(), i = No();
    },
    m(o, u) {
      a[t].m(o, u), vt(o, i, u), l = !0;
    },
    p(o, [u]) {
      let f = t;
      t = s(o), t === f ? a[t].p(o, u) : (Oo(), Rt(a[f], 1, 1, () => {
        a[f] = null;
      }), Po(), n = a[t], n ? n.p(o, u) : (n = a[t] = r[t](o), n.c()), Mt(n, 1), n.m(i.parentNode, i));
    },
    i(o) {
      l || (Mt(n), l = !0);
    },
    o(o) {
      Rt(n), l = !1;
    },
    d(o) {
      o && gt(i), a[t].d(o);
    }
  };
}
function Go(e, t, n) {
  let { $$slots: i = {}, $$scope: l } = t, { elem_id: r = "" } = t, { elem_classes: a = [] } = t, { visible: s = !0 } = t, { variant: o = "secondary" } = t, { size: u = "lg" } = t, { value: f = null } = t, { link: h = null } = t, { icon: d = null } = t, { disabled: b = !1 } = t, { scale: y = null } = t, { min_width: w = void 0 } = t;
  function p(m) {
    Co.call(this, e, m);
  }
  return e.$$set = (m) => {
    "elem_id" in m && n(0, r = m.elem_id), "elem_classes" in m && n(1, a = m.elem_classes), "visible" in m && n(2, s = m.visible), "variant" in m && n(3, o = m.variant), "size" in m && n(4, u = m.size), "value" in m && n(5, f = m.value), "link" in m && n(6, h = m.link), "icon" in m && n(7, d = m.icon), "disabled" in m && n(8, b = m.disabled), "scale" in m && n(9, y = m.scale), "min_width" in m && n(10, w = m.min_width), "$$scope" in m && n(11, l = m.$$scope);
  }, [
    r,
    a,
    s,
    o,
    u,
    f,
    h,
    d,
    b,
    y,
    w,
    l,
    i,
    p
  ];
}
class Fo extends ko {
  constructor(t) {
    super(), Io(this, t, Go, Uo, Mo, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      variant: 3,
      size: 4,
      value: 5,
      link: 6,
      icon: 7,
      disabled: 8,
      scale: 9,
      min_width: 10
    });
  }
}
const {
  SvelteComponent: jo,
  attr: xo,
  detach: Vo,
  element: qo,
  init: Xo,
  insert: zo,
  noop: Ti,
  safe_not_equal: Zo,
  toggle_class: Ge
} = window.__gradio__svelte__internal;
function Wo(e) {
  let t;
  return {
    c() {
      t = qo("div"), t.textContent = `${/*names_string*/
      e[2]}`, xo(t, "class", "svelte-1gecy8w"), Ge(
        t,
        "table",
        /*type*/
        e[0] === "table"
      ), Ge(
        t,
        "gallery",
        /*type*/
        e[0] === "gallery"
      ), Ge(
        t,
        "selected",
        /*selected*/
        e[1]
      );
    },
    m(n, i) {
      zo(n, t, i);
    },
    p(n, [i]) {
      i & /*type*/
      1 && Ge(
        t,
        "table",
        /*type*/
        n[0] === "table"
      ), i & /*type*/
      1 && Ge(
        t,
        "gallery",
        /*type*/
        n[0] === "gallery"
      ), i & /*selected*/
      2 && Ge(
        t,
        "selected",
        /*selected*/
        n[1]
      );
    },
    i: Ti,
    o: Ti,
    d(n) {
      n && Vo(t);
    }
  };
}
function Qo(e) {
  let t, n = e[0], i = 1;
  for (; i < e.length; ) {
    const l = e[i], r = e[i + 1];
    if (i += 2, (l === "optionalAccess" || l === "optionalCall") && n == null)
      return;
    l === "access" || l === "optionalAccess" ? (t = n, n = r(n)) : (l === "call" || l === "optionalCall") && (n = r((...a) => n.call(t, ...a)), t = void 0);
  }
  return n;
}
function Jo(e, t, n) {
  let { value: i } = t, { type: l } = t, { selected: r = !1 } = t, { choices: a } = t, u = (i ? Array.isArray(i) ? i : [i] : []).map((f) => Qo([a.find((h) => h[1] === f), "optionalAccess", (h) => h[0]])).filter((f) => f !== void 0).join(", ");
  return e.$$set = (f) => {
    "value" in f && n(3, i = f.value), "type" in f && n(0, l = f.type), "selected" in f && n(1, r = f.selected), "choices" in f && n(4, a = f.choices);
  }, [l, r, u, i, a];
}
class _f extends jo {
  constructor(t) {
    super(), Xo(this, t, Jo, Wo, Zo, {
      value: 3,
      type: 0,
      selected: 1,
      choices: 4
    });
  }
}
function Yo(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var Ko = function(t) {
  return $o(t) && !ea(t);
};
function $o(e) {
  return !!e && typeof e == "object";
}
function ea(e) {
  var t = Object.prototype.toString.call(e);
  return t === "[object RegExp]" || t === "[object Date]" || ia(e);
}
var ta = typeof Symbol == "function" && Symbol.for, na = ta ? Symbol.for("react.element") : 60103;
function ia(e) {
  return e.$$typeof === na;
}
function la(e) {
  return Array.isArray(e) ? [] : {};
}
function ht(e, t) {
  return t.clone !== !1 && t.isMergeableObject(e) ? Qe(la(e), e, t) : e;
}
function ra(e, t, n) {
  return e.concat(t).map(function(i) {
    return ht(i, n);
  });
}
function sa(e, t) {
  if (!t.customMerge)
    return Qe;
  var n = t.customMerge(e);
  return typeof n == "function" ? n : Qe;
}
function oa(e) {
  return Object.getOwnPropertySymbols ? Object.getOwnPropertySymbols(e).filter(function(t) {
    return Object.propertyIsEnumerable.call(e, t);
  }) : [];
}
function Ai(e) {
  return Object.keys(e).concat(oa(e));
}
function gl(e, t) {
  try {
    return t in e;
  } catch {
    return !1;
  }
}
function aa(e, t) {
  return gl(e, t) && !(Object.hasOwnProperty.call(e, t) && Object.propertyIsEnumerable.call(e, t));
}
function ua(e, t, n) {
  var i = {};
  return n.isMergeableObject(e) && Ai(e).forEach(function(l) {
    i[l] = ht(e[l], n);
  }), Ai(t).forEach(function(l) {
    aa(e, l) || (gl(e, l) && n.isMergeableObject(t[l]) ? i[l] = sa(l, n)(e[l], t[l], n) : i[l] = ht(t[l], n));
  }), i;
}
function Qe(e, t, n) {
  n = n || {}, n.arrayMerge = n.arrayMerge || ra, n.isMergeableObject = n.isMergeableObject || Ko, n.cloneUnlessOtherwiseSpecified = ht;
  var i = Array.isArray(t), l = Array.isArray(e), r = i === l;
  return r ? i ? n.arrayMerge(e, t, n) : ua(e, t, n) : ht(t, n);
}
Qe.all = function(t, n) {
  if (!Array.isArray(t))
    throw new Error("first argument should be an array");
  return t.reduce(function(i, l) {
    return Qe(i, l, n);
  }, {});
};
var fa = Qe, ca = fa;
const ha = /* @__PURE__ */ Yo(ca);
var pn = function(e, t) {
  return pn = Object.setPrototypeOf || { __proto__: [] } instanceof Array && function(n, i) {
    n.__proto__ = i;
  } || function(n, i) {
    for (var l in i)
      Object.prototype.hasOwnProperty.call(i, l) && (n[l] = i[l]);
  }, pn(e, t);
};
function xt(e, t) {
  if (typeof t != "function" && t !== null)
    throw new TypeError("Class extends value " + String(t) + " is not a constructor or null");
  pn(e, t);
  function n() {
    this.constructor = e;
  }
  e.prototype = t === null ? Object.create(t) : (n.prototype = t.prototype, new n());
}
var R = function() {
  return R = Object.assign || function(t) {
    for (var n, i = 1, l = arguments.length; i < l; i++) {
      n = arguments[i];
      for (var r in n)
        Object.prototype.hasOwnProperty.call(n, r) && (t[r] = n[r]);
    }
    return t;
  }, R.apply(this, arguments);
};
function nn(e, t, n) {
  if (n || arguments.length === 2)
    for (var i = 0, l = t.length, r; i < l; i++)
      (r || !(i in t)) && (r || (r = Array.prototype.slice.call(t, 0, i)), r[i] = t[i]);
  return e.concat(r || Array.prototype.slice.call(t));
}
var I;
(function(e) {
  e[e.EXPECT_ARGUMENT_CLOSING_BRACE = 1] = "EXPECT_ARGUMENT_CLOSING_BRACE", e[e.EMPTY_ARGUMENT = 2] = "EMPTY_ARGUMENT", e[e.MALFORMED_ARGUMENT = 3] = "MALFORMED_ARGUMENT", e[e.EXPECT_ARGUMENT_TYPE = 4] = "EXPECT_ARGUMENT_TYPE", e[e.INVALID_ARGUMENT_TYPE = 5] = "INVALID_ARGUMENT_TYPE", e[e.EXPECT_ARGUMENT_STYLE = 6] = "EXPECT_ARGUMENT_STYLE", e[e.INVALID_NUMBER_SKELETON = 7] = "INVALID_NUMBER_SKELETON", e[e.INVALID_DATE_TIME_SKELETON = 8] = "INVALID_DATE_TIME_SKELETON", e[e.EXPECT_NUMBER_SKELETON = 9] = "EXPECT_NUMBER_SKELETON", e[e.EXPECT_DATE_TIME_SKELETON = 10] = "EXPECT_DATE_TIME_SKELETON", e[e.UNCLOSED_QUOTE_IN_ARGUMENT_STYLE = 11] = "UNCLOSED_QUOTE_IN_ARGUMENT_STYLE", e[e.EXPECT_SELECT_ARGUMENT_OPTIONS = 12] = "EXPECT_SELECT_ARGUMENT_OPTIONS", e[e.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE = 13] = "EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE", e[e.INVALID_PLURAL_ARGUMENT_OFFSET_VALUE = 14] = "INVALID_PLURAL_ARGUMENT_OFFSET_VALUE", e[e.EXPECT_SELECT_ARGUMENT_SELECTOR = 15] = "EXPECT_SELECT_ARGUMENT_SELECTOR", e[e.EXPECT_PLURAL_ARGUMENT_SELECTOR = 16] = "EXPECT_PLURAL_ARGUMENT_SELECTOR", e[e.EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT = 17] = "EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT", e[e.EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT = 18] = "EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT", e[e.INVALID_PLURAL_ARGUMENT_SELECTOR = 19] = "INVALID_PLURAL_ARGUMENT_SELECTOR", e[e.DUPLICATE_PLURAL_ARGUMENT_SELECTOR = 20] = "DUPLICATE_PLURAL_ARGUMENT_SELECTOR", e[e.DUPLICATE_SELECT_ARGUMENT_SELECTOR = 21] = "DUPLICATE_SELECT_ARGUMENT_SELECTOR", e[e.MISSING_OTHER_CLAUSE = 22] = "MISSING_OTHER_CLAUSE", e[e.INVALID_TAG = 23] = "INVALID_TAG", e[e.INVALID_TAG_NAME = 25] = "INVALID_TAG_NAME", e[e.UNMATCHED_CLOSING_TAG = 26] = "UNMATCHED_CLOSING_TAG", e[e.UNCLOSED_TAG = 27] = "UNCLOSED_TAG";
})(I || (I = {}));
var j;
(function(e) {
  e[e.literal = 0] = "literal", e[e.argument = 1] = "argument", e[e.number = 2] = "number", e[e.date = 3] = "date", e[e.time = 4] = "time", e[e.select = 5] = "select", e[e.plural = 6] = "plural", e[e.pound = 7] = "pound", e[e.tag = 8] = "tag";
})(j || (j = {}));
var Je;
(function(e) {
  e[e.number = 0] = "number", e[e.dateTime = 1] = "dateTime";
})(Je || (Je = {}));
function Hi(e) {
  return e.type === j.literal;
}
function _a(e) {
  return e.type === j.argument;
}
function vl(e) {
  return e.type === j.number;
}
function yl(e) {
  return e.type === j.date;
}
function wl(e) {
  return e.type === j.time;
}
function El(e) {
  return e.type === j.select;
}
function Sl(e) {
  return e.type === j.plural;
}
function ma(e) {
  return e.type === j.pound;
}
function Tl(e) {
  return e.type === j.tag;
}
function Al(e) {
  return !!(e && typeof e == "object" && e.type === Je.number);
}
function gn(e) {
  return !!(e && typeof e == "object" && e.type === Je.dateTime);
}
var Hl = /[ \xA0\u1680\u2000-\u200A\u202F\u205F\u3000]/, da = /(?:[Eec]{1,6}|G{1,5}|[Qq]{1,5}|(?:[yYur]+|U{1,5})|[ML]{1,5}|d{1,2}|D{1,3}|F{1}|[abB]{1,5}|[hkHK]{1,2}|w{1,2}|W{1}|m{1,2}|s{1,2}|[zZOvVxX]{1,4})(?=([^']*'[^']*')*[^']*$)/g;
function ba(e) {
  var t = {};
  return e.replace(da, function(n) {
    var i = n.length;
    switch (n[0]) {
      case "G":
        t.era = i === 4 ? "long" : i === 5 ? "narrow" : "short";
        break;
      case "y":
        t.year = i === 2 ? "2-digit" : "numeric";
        break;
      case "Y":
      case "u":
      case "U":
      case "r":
        throw new RangeError("`Y/u/U/r` (year) patterns are not supported, use `y` instead");
      case "q":
      case "Q":
        throw new RangeError("`q/Q` (quarter) patterns are not supported");
      case "M":
      case "L":
        t.month = ["numeric", "2-digit", "short", "long", "narrow"][i - 1];
        break;
      case "w":
      case "W":
        throw new RangeError("`w/W` (week) patterns are not supported");
      case "d":
        t.day = ["numeric", "2-digit"][i - 1];
        break;
      case "D":
      case "F":
      case "g":
        throw new RangeError("`D/F/g` (day) patterns are not supported, use `d` instead");
      case "E":
        t.weekday = i === 4 ? "short" : i === 5 ? "narrow" : "short";
        break;
      case "e":
        if (i < 4)
          throw new RangeError("`e..eee` (weekday) patterns are not supported");
        t.weekday = ["short", "long", "narrow", "short"][i - 4];
        break;
      case "c":
        if (i < 4)
          throw new RangeError("`c..ccc` (weekday) patterns are not supported");
        t.weekday = ["short", "long", "narrow", "short"][i - 4];
        break;
      case "a":
        t.hour12 = !0;
        break;
      case "b":
      case "B":
        throw new RangeError("`b/B` (period) patterns are not supported, use `a` instead");
      case "h":
        t.hourCycle = "h12", t.hour = ["numeric", "2-digit"][i - 1];
        break;
      case "H":
        t.hourCycle = "h23", t.hour = ["numeric", "2-digit"][i - 1];
        break;
      case "K":
        t.hourCycle = "h11", t.hour = ["numeric", "2-digit"][i - 1];
        break;
      case "k":
        t.hourCycle = "h24", t.hour = ["numeric", "2-digit"][i - 1];
        break;
      case "j":
      case "J":
      case "C":
        throw new RangeError("`j/J/C` (hour) patterns are not supported, use `h/H/K/k` instead");
      case "m":
        t.minute = ["numeric", "2-digit"][i - 1];
        break;
      case "s":
        t.second = ["numeric", "2-digit"][i - 1];
        break;
      case "S":
      case "A":
        throw new RangeError("`S/A` (second) patterns are not supported, use `s` instead");
      case "z":
        t.timeZoneName = i < 4 ? "short" : "long";
        break;
      case "Z":
      case "O":
      case "v":
      case "V":
      case "X":
      case "x":
        throw new RangeError("`Z/O/v/V/X/x` (timeZone) patterns are not supported, use `z` instead");
    }
    return "";
  }), t;
}
var pa = /[\t-\r \x85\u200E\u200F\u2028\u2029]/i;
function ga(e) {
  if (e.length === 0)
    throw new Error("Number skeleton cannot be empty");
  for (var t = e.split(pa).filter(function(d) {
    return d.length > 0;
  }), n = [], i = 0, l = t; i < l.length; i++) {
    var r = l[i], a = r.split("/");
    if (a.length === 0)
      throw new Error("Invalid number skeleton");
    for (var s = a[0], o = a.slice(1), u = 0, f = o; u < f.length; u++) {
      var h = f[u];
      if (h.length === 0)
        throw new Error("Invalid number skeleton");
    }
    n.push({ stem: s, options: o });
  }
  return n;
}
function va(e) {
  return e.replace(/^(.*?)-/, "");
}
var Bi = /^\.(?:(0+)(\*)?|(#+)|(0+)(#+))$/g, Bl = /^(@+)?(\+|#+)?[rs]?$/g, ya = /(\*)(0+)|(#+)(0+)|(0+)/g, kl = /^(0+)$/;
function ki(e) {
  var t = {};
  return e[e.length - 1] === "r" ? t.roundingPriority = "morePrecision" : e[e.length - 1] === "s" && (t.roundingPriority = "lessPrecision"), e.replace(Bl, function(n, i, l) {
    return typeof l != "string" ? (t.minimumSignificantDigits = i.length, t.maximumSignificantDigits = i.length) : l === "+" ? t.minimumSignificantDigits = i.length : i[0] === "#" ? t.maximumSignificantDigits = i.length : (t.minimumSignificantDigits = i.length, t.maximumSignificantDigits = i.length + (typeof l == "string" ? l.length : 0)), "";
  }), t;
}
function Cl(e) {
  switch (e) {
    case "sign-auto":
      return {
        signDisplay: "auto"
      };
    case "sign-accounting":
    case "()":
      return {
        currencySign: "accounting"
      };
    case "sign-always":
    case "+!":
      return {
        signDisplay: "always"
      };
    case "sign-accounting-always":
    case "()!":
      return {
        signDisplay: "always",
        currencySign: "accounting"
      };
    case "sign-except-zero":
    case "+?":
      return {
        signDisplay: "exceptZero"
      };
    case "sign-accounting-except-zero":
    case "()?":
      return {
        signDisplay: "exceptZero",
        currencySign: "accounting"
      };
    case "sign-never":
    case "+_":
      return {
        signDisplay: "never"
      };
  }
}
function wa(e) {
  var t;
  if (e[0] === "E" && e[1] === "E" ? (t = {
    notation: "engineering"
  }, e = e.slice(2)) : e[0] === "E" && (t = {
    notation: "scientific"
  }, e = e.slice(1)), t) {
    var n = e.slice(0, 2);
    if (n === "+!" ? (t.signDisplay = "always", e = e.slice(2)) : n === "+?" && (t.signDisplay = "exceptZero", e = e.slice(2)), !kl.test(e))
      throw new Error("Malformed concise eng/scientific notation");
    t.minimumIntegerDigits = e.length;
  }
  return t;
}
function Ci(e) {
  var t = {}, n = Cl(e);
  return n || t;
}
function Ea(e) {
  for (var t = {}, n = 0, i = e; n < i.length; n++) {
    var l = i[n];
    switch (l.stem) {
      case "percent":
      case "%":
        t.style = "percent";
        continue;
      case "%x100":
        t.style = "percent", t.scale = 100;
        continue;
      case "currency":
        t.style = "currency", t.currency = l.options[0];
        continue;
      case "group-off":
      case ",_":
        t.useGrouping = !1;
        continue;
      case "precision-integer":
      case ".":
        t.maximumFractionDigits = 0;
        continue;
      case "measure-unit":
      case "unit":
        t.style = "unit", t.unit = va(l.options[0]);
        continue;
      case "compact-short":
      case "K":
        t.notation = "compact", t.compactDisplay = "short";
        continue;
      case "compact-long":
      case "KK":
        t.notation = "compact", t.compactDisplay = "long";
        continue;
      case "scientific":
        t = R(R(R({}, t), { notation: "scientific" }), l.options.reduce(function(o, u) {
          return R(R({}, o), Ci(u));
        }, {}));
        continue;
      case "engineering":
        t = R(R(R({}, t), { notation: "engineering" }), l.options.reduce(function(o, u) {
          return R(R({}, o), Ci(u));
        }, {}));
        continue;
      case "notation-simple":
        t.notation = "standard";
        continue;
      case "unit-width-narrow":
        t.currencyDisplay = "narrowSymbol", t.unitDisplay = "narrow";
        continue;
      case "unit-width-short":
        t.currencyDisplay = "code", t.unitDisplay = "short";
        continue;
      case "unit-width-full-name":
        t.currencyDisplay = "name", t.unitDisplay = "long";
        continue;
      case "unit-width-iso-code":
        t.currencyDisplay = "symbol";
        continue;
      case "scale":
        t.scale = parseFloat(l.options[0]);
        continue;
      case "integer-width":
        if (l.options.length > 1)
          throw new RangeError("integer-width stems only accept a single optional option");
        l.options[0].replace(ya, function(o, u, f, h, d, b) {
          if (u)
            t.minimumIntegerDigits = f.length;
          else {
            if (h && d)
              throw new Error("We currently do not support maximum integer digits");
            if (b)
              throw new Error("We currently do not support exact integer digits");
          }
          return "";
        });
        continue;
    }
    if (kl.test(l.stem)) {
      t.minimumIntegerDigits = l.stem.length;
      continue;
    }
    if (Bi.test(l.stem)) {
      if (l.options.length > 1)
        throw new RangeError("Fraction-precision stems only accept a single optional option");
      l.stem.replace(Bi, function(o, u, f, h, d, b) {
        return f === "*" ? t.minimumFractionDigits = u.length : h && h[0] === "#" ? t.maximumFractionDigits = h.length : d && b ? (t.minimumFractionDigits = d.length, t.maximumFractionDigits = d.length + b.length) : (t.minimumFractionDigits = u.length, t.maximumFractionDigits = u.length), "";
      });
      var r = l.options[0];
      r === "w" ? t = R(R({}, t), { trailingZeroDisplay: "stripIfInteger" }) : r && (t = R(R({}, t), ki(r)));
      continue;
    }
    if (Bl.test(l.stem)) {
      t = R(R({}, t), ki(l.stem));
      continue;
    }
    var a = Cl(l.stem);
    a && (t = R(R({}, t), a));
    var s = wa(l.stem);
    s && (t = R(R({}, t), s));
  }
  return t;
}
var Ht = {
  AX: [
    "H"
  ],
  BQ: [
    "H"
  ],
  CP: [
    "H"
  ],
  CZ: [
    "H"
  ],
  DK: [
    "H"
  ],
  FI: [
    "H"
  ],
  ID: [
    "H"
  ],
  IS: [
    "H"
  ],
  ML: [
    "H"
  ],
  NE: [
    "H"
  ],
  RU: [
    "H"
  ],
  SE: [
    "H"
  ],
  SJ: [
    "H"
  ],
  SK: [
    "H"
  ],
  AS: [
    "h",
    "H"
  ],
  BT: [
    "h",
    "H"
  ],
  DJ: [
    "h",
    "H"
  ],
  ER: [
    "h",
    "H"
  ],
  GH: [
    "h",
    "H"
  ],
  IN: [
    "h",
    "H"
  ],
  LS: [
    "h",
    "H"
  ],
  PG: [
    "h",
    "H"
  ],
  PW: [
    "h",
    "H"
  ],
  SO: [
    "h",
    "H"
  ],
  TO: [
    "h",
    "H"
  ],
  VU: [
    "h",
    "H"
  ],
  WS: [
    "h",
    "H"
  ],
  "001": [
    "H",
    "h"
  ],
  AL: [
    "h",
    "H",
    "hB"
  ],
  TD: [
    "h",
    "H",
    "hB"
  ],
  "ca-ES": [
    "H",
    "h",
    "hB"
  ],
  CF: [
    "H",
    "h",
    "hB"
  ],
  CM: [
    "H",
    "h",
    "hB"
  ],
  "fr-CA": [
    "H",
    "h",
    "hB"
  ],
  "gl-ES": [
    "H",
    "h",
    "hB"
  ],
  "it-CH": [
    "H",
    "h",
    "hB"
  ],
  "it-IT": [
    "H",
    "h",
    "hB"
  ],
  LU: [
    "H",
    "h",
    "hB"
  ],
  NP: [
    "H",
    "h",
    "hB"
  ],
  PF: [
    "H",
    "h",
    "hB"
  ],
  SC: [
    "H",
    "h",
    "hB"
  ],
  SM: [
    "H",
    "h",
    "hB"
  ],
  SN: [
    "H",
    "h",
    "hB"
  ],
  TF: [
    "H",
    "h",
    "hB"
  ],
  VA: [
    "H",
    "h",
    "hB"
  ],
  CY: [
    "h",
    "H",
    "hb",
    "hB"
  ],
  GR: [
    "h",
    "H",
    "hb",
    "hB"
  ],
  CO: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  DO: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  KP: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  KR: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  NA: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  PA: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  PR: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  VE: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  AC: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  AI: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  BW: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  BZ: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  CC: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  CK: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  CX: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  DG: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  FK: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  GB: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  GG: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  GI: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  IE: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  IM: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  IO: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  JE: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  LT: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  MK: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  MN: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  MS: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  NF: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  NG: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  NR: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  NU: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  PN: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  SH: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  SX: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  TA: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  ZA: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  "af-ZA": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  AR: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  CL: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  CR: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  CU: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  EA: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-BO": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-BR": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-EC": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-ES": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-GQ": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-PE": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  GT: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  HN: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  IC: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  KG: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  KM: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  LK: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  MA: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  MX: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  NI: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  PY: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  SV: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  UY: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  JP: [
    "H",
    "h",
    "K"
  ],
  AD: [
    "H",
    "hB"
  ],
  AM: [
    "H",
    "hB"
  ],
  AO: [
    "H",
    "hB"
  ],
  AT: [
    "H",
    "hB"
  ],
  AW: [
    "H",
    "hB"
  ],
  BE: [
    "H",
    "hB"
  ],
  BF: [
    "H",
    "hB"
  ],
  BJ: [
    "H",
    "hB"
  ],
  BL: [
    "H",
    "hB"
  ],
  BR: [
    "H",
    "hB"
  ],
  CG: [
    "H",
    "hB"
  ],
  CI: [
    "H",
    "hB"
  ],
  CV: [
    "H",
    "hB"
  ],
  DE: [
    "H",
    "hB"
  ],
  EE: [
    "H",
    "hB"
  ],
  FR: [
    "H",
    "hB"
  ],
  GA: [
    "H",
    "hB"
  ],
  GF: [
    "H",
    "hB"
  ],
  GN: [
    "H",
    "hB"
  ],
  GP: [
    "H",
    "hB"
  ],
  GW: [
    "H",
    "hB"
  ],
  HR: [
    "H",
    "hB"
  ],
  IL: [
    "H",
    "hB"
  ],
  IT: [
    "H",
    "hB"
  ],
  KZ: [
    "H",
    "hB"
  ],
  MC: [
    "H",
    "hB"
  ],
  MD: [
    "H",
    "hB"
  ],
  MF: [
    "H",
    "hB"
  ],
  MQ: [
    "H",
    "hB"
  ],
  MZ: [
    "H",
    "hB"
  ],
  NC: [
    "H",
    "hB"
  ],
  NL: [
    "H",
    "hB"
  ],
  PM: [
    "H",
    "hB"
  ],
  PT: [
    "H",
    "hB"
  ],
  RE: [
    "H",
    "hB"
  ],
  RO: [
    "H",
    "hB"
  ],
  SI: [
    "H",
    "hB"
  ],
  SR: [
    "H",
    "hB"
  ],
  ST: [
    "H",
    "hB"
  ],
  TG: [
    "H",
    "hB"
  ],
  TR: [
    "H",
    "hB"
  ],
  WF: [
    "H",
    "hB"
  ],
  YT: [
    "H",
    "hB"
  ],
  BD: [
    "h",
    "hB",
    "H"
  ],
  PK: [
    "h",
    "hB",
    "H"
  ],
  AZ: [
    "H",
    "hB",
    "h"
  ],
  BA: [
    "H",
    "hB",
    "h"
  ],
  BG: [
    "H",
    "hB",
    "h"
  ],
  CH: [
    "H",
    "hB",
    "h"
  ],
  GE: [
    "H",
    "hB",
    "h"
  ],
  LI: [
    "H",
    "hB",
    "h"
  ],
  ME: [
    "H",
    "hB",
    "h"
  ],
  RS: [
    "H",
    "hB",
    "h"
  ],
  UA: [
    "H",
    "hB",
    "h"
  ],
  UZ: [
    "H",
    "hB",
    "h"
  ],
  XK: [
    "H",
    "hB",
    "h"
  ],
  AG: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  AU: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  BB: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  BM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  BS: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  CA: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  DM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  "en-001": [
    "h",
    "hb",
    "H",
    "hB"
  ],
  FJ: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  FM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  GD: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  GM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  GU: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  GY: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  JM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  KI: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  KN: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  KY: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  LC: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  LR: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  MH: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  MP: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  MW: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  NZ: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  SB: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  SG: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  SL: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  SS: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  SZ: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  TC: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  TT: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  UM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  US: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  VC: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  VG: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  VI: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  ZM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  BO: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  EC: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  ES: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  GQ: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  PE: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  AE: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  "ar-001": [
    "h",
    "hB",
    "hb",
    "H"
  ],
  BH: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  DZ: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  EG: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  EH: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  HK: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  IQ: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  JO: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  KW: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  LB: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  LY: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  MO: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  MR: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  OM: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  PH: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  PS: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  QA: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  SA: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  SD: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  SY: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  TN: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  YE: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  AF: [
    "H",
    "hb",
    "hB",
    "h"
  ],
  LA: [
    "H",
    "hb",
    "hB",
    "h"
  ],
  CN: [
    "H",
    "hB",
    "hb",
    "h"
  ],
  LV: [
    "H",
    "hB",
    "hb",
    "h"
  ],
  TL: [
    "H",
    "hB",
    "hb",
    "h"
  ],
  "zu-ZA": [
    "H",
    "hB",
    "hb",
    "h"
  ],
  CD: [
    "hB",
    "H"
  ],
  IR: [
    "hB",
    "H"
  ],
  "hi-IN": [
    "hB",
    "h",
    "H"
  ],
  "kn-IN": [
    "hB",
    "h",
    "H"
  ],
  "ml-IN": [
    "hB",
    "h",
    "H"
  ],
  "te-IN": [
    "hB",
    "h",
    "H"
  ],
  KH: [
    "hB",
    "h",
    "H",
    "hb"
  ],
  "ta-IN": [
    "hB",
    "h",
    "hb",
    "H"
  ],
  BN: [
    "hb",
    "hB",
    "h",
    "H"
  ],
  MY: [
    "hb",
    "hB",
    "h",
    "H"
  ],
  ET: [
    "hB",
    "hb",
    "h",
    "H"
  ],
  "gu-IN": [
    "hB",
    "hb",
    "h",
    "H"
  ],
  "mr-IN": [
    "hB",
    "hb",
    "h",
    "H"
  ],
  "pa-IN": [
    "hB",
    "hb",
    "h",
    "H"
  ],
  TW: [
    "hB",
    "hb",
    "h",
    "H"
  ],
  KE: [
    "hB",
    "hb",
    "H",
    "h"
  ],
  MM: [
    "hB",
    "hb",
    "H",
    "h"
  ],
  TZ: [
    "hB",
    "hb",
    "H",
    "h"
  ],
  UG: [
    "hB",
    "hb",
    "H",
    "h"
  ]
};
function Sa(e, t) {
  for (var n = "", i = 0; i < e.length; i++) {
    var l = e.charAt(i);
    if (l === "j") {
      for (var r = 0; i + 1 < e.length && e.charAt(i + 1) === l; )
        r++, i++;
      var a = 1 + (r & 1), s = r < 2 ? 1 : 3 + (r >> 1), o = "a", u = Ta(t);
      for ((u == "H" || u == "k") && (s = 0); s-- > 0; )
        n += o;
      for (; a-- > 0; )
        n = u + n;
    } else
      l === "J" ? n += "H" : n += l;
  }
  return n;
}
function Ta(e) {
  var t = e.hourCycle;
  if (t === void 0 && // @ts-ignore hourCycle(s) is not identified yet
  e.hourCycles && // @ts-ignore
  e.hourCycles.length && (t = e.hourCycles[0]), t)
    switch (t) {
      case "h24":
        return "k";
      case "h23":
        return "H";
      case "h12":
        return "h";
      case "h11":
        return "K";
      default:
        throw new Error("Invalid hourCycle");
    }
  var n = e.language, i;
  n !== "root" && (i = e.maximize().region);
  var l = Ht[i || ""] || Ht[n || ""] || Ht["".concat(n, "-001")] || Ht["001"];
  return l[0];
}
var ln, Aa = new RegExp("^".concat(Hl.source, "*")), Ha = new RegExp("".concat(Hl.source, "*$"));
function L(e, t) {
  return { start: e, end: t };
}
var Ba = !!String.prototype.startsWith, ka = !!String.fromCodePoint, Ca = !!Object.fromEntries, Pa = !!String.prototype.codePointAt, Na = !!String.prototype.trimStart, Oa = !!String.prototype.trimEnd, Ia = !!Number.isSafeInteger, La = Ia ? Number.isSafeInteger : function(e) {
  return typeof e == "number" && isFinite(e) && Math.floor(e) === e && Math.abs(e) <= 9007199254740991;
}, vn = !0;
try {
  var Ma = Nl("([^\\p{White_Space}\\p{Pattern_Syntax}]*)", "yu");
  vn = ((ln = Ma.exec("a")) === null || ln === void 0 ? void 0 : ln[0]) === "a";
} catch {
  vn = !1;
}
var Pi = Ba ? (
  // Native
  function(t, n, i) {
    return t.startsWith(n, i);
  }
) : (
  // For IE11
  function(t, n, i) {
    return t.slice(i, i + n.length) === n;
  }
), yn = ka ? String.fromCodePoint : (
  // IE11
  function() {
    for (var t = [], n = 0; n < arguments.length; n++)
      t[n] = arguments[n];
    for (var i = "", l = t.length, r = 0, a; l > r; ) {
      if (a = t[r++], a > 1114111)
        throw RangeError(a + " is not a valid code point");
      i += a < 65536 ? String.fromCharCode(a) : String.fromCharCode(((a -= 65536) >> 10) + 55296, a % 1024 + 56320);
    }
    return i;
  }
), Ni = (
  // native
  Ca ? Object.fromEntries : (
    // Ponyfill
    function(t) {
      for (var n = {}, i = 0, l = t; i < l.length; i++) {
        var r = l[i], a = r[0], s = r[1];
        n[a] = s;
      }
      return n;
    }
  )
), Pl = Pa ? (
  // Native
  function(t, n) {
    return t.codePointAt(n);
  }
) : (
  // IE 11
  function(t, n) {
    var i = t.length;
    if (!(n < 0 || n >= i)) {
      var l = t.charCodeAt(n), r;
      return l < 55296 || l > 56319 || n + 1 === i || (r = t.charCodeAt(n + 1)) < 56320 || r > 57343 ? l : (l - 55296 << 10) + (r - 56320) + 65536;
    }
  }
), Ra = Na ? (
  // Native
  function(t) {
    return t.trimStart();
  }
) : (
  // Ponyfill
  function(t) {
    return t.replace(Aa, "");
  }
), Da = Oa ? (
  // Native
  function(t) {
    return t.trimEnd();
  }
) : (
  // Ponyfill
  function(t) {
    return t.replace(Ha, "");
  }
);
function Nl(e, t) {
  return new RegExp(e, t);
}
var wn;
if (vn) {
  var Oi = Nl("([^\\p{White_Space}\\p{Pattern_Syntax}]*)", "yu");
  wn = function(t, n) {
    var i;
    Oi.lastIndex = n;
    var l = Oi.exec(t);
    return (i = l[1]) !== null && i !== void 0 ? i : "";
  };
} else
  wn = function(t, n) {
    for (var i = []; ; ) {
      var l = Pl(t, n);
      if (l === void 0 || Ol(l) || ja(l))
        break;
      i.push(l), n += l >= 65536 ? 2 : 1;
    }
    return yn.apply(void 0, i);
  };
var Ua = (
  /** @class */
  function() {
    function e(t, n) {
      n === void 0 && (n = {}), this.message = t, this.position = { offset: 0, line: 1, column: 1 }, this.ignoreTag = !!n.ignoreTag, this.locale = n.locale, this.requiresOtherClause = !!n.requiresOtherClause, this.shouldParseSkeletons = !!n.shouldParseSkeletons;
    }
    return e.prototype.parse = function() {
      if (this.offset() !== 0)
        throw Error("parser can only be used once");
      return this.parseMessage(0, "", !1);
    }, e.prototype.parseMessage = function(t, n, i) {
      for (var l = []; !this.isEOF(); ) {
        var r = this.char();
        if (r === 123) {
          var a = this.parseArgument(t, i);
          if (a.err)
            return a;
          l.push(a.val);
        } else {
          if (r === 125 && t > 0)
            break;
          if (r === 35 && (n === "plural" || n === "selectordinal")) {
            var s = this.clonePosition();
            this.bump(), l.push({
              type: j.pound,
              location: L(s, this.clonePosition())
            });
          } else if (r === 60 && !this.ignoreTag && this.peek() === 47) {
            if (i)
              break;
            return this.error(I.UNMATCHED_CLOSING_TAG, L(this.clonePosition(), this.clonePosition()));
          } else if (r === 60 && !this.ignoreTag && En(this.peek() || 0)) {
            var a = this.parseTag(t, n);
            if (a.err)
              return a;
            l.push(a.val);
          } else {
            var a = this.parseLiteral(t, n);
            if (a.err)
              return a;
            l.push(a.val);
          }
        }
      }
      return { val: l, err: null };
    }, e.prototype.parseTag = function(t, n) {
      var i = this.clonePosition();
      this.bump();
      var l = this.parseTagName();
      if (this.bumpSpace(), this.bumpIf("/>"))
        return {
          val: {
            type: j.literal,
            value: "<".concat(l, "/>"),
            location: L(i, this.clonePosition())
          },
          err: null
        };
      if (this.bumpIf(">")) {
        var r = this.parseMessage(t + 1, n, !0);
        if (r.err)
          return r;
        var a = r.val, s = this.clonePosition();
        if (this.bumpIf("</")) {
          if (this.isEOF() || !En(this.char()))
            return this.error(I.INVALID_TAG, L(s, this.clonePosition()));
          var o = this.clonePosition(), u = this.parseTagName();
          return l !== u ? this.error(I.UNMATCHED_CLOSING_TAG, L(o, this.clonePosition())) : (this.bumpSpace(), this.bumpIf(">") ? {
            val: {
              type: j.tag,
              value: l,
              children: a,
              location: L(i, this.clonePosition())
            },
            err: null
          } : this.error(I.INVALID_TAG, L(s, this.clonePosition())));
        } else
          return this.error(I.UNCLOSED_TAG, L(i, this.clonePosition()));
      } else
        return this.error(I.INVALID_TAG, L(i, this.clonePosition()));
    }, e.prototype.parseTagName = function() {
      var t = this.offset();
      for (this.bump(); !this.isEOF() && Fa(this.char()); )
        this.bump();
      return this.message.slice(t, this.offset());
    }, e.prototype.parseLiteral = function(t, n) {
      for (var i = this.clonePosition(), l = ""; ; ) {
        var r = this.tryParseQuote(n);
        if (r) {
          l += r;
          continue;
        }
        var a = this.tryParseUnquoted(t, n);
        if (a) {
          l += a;
          continue;
        }
        var s = this.tryParseLeftAngleBracket();
        if (s) {
          l += s;
          continue;
        }
        break;
      }
      var o = L(i, this.clonePosition());
      return {
        val: { type: j.literal, value: l, location: o },
        err: null
      };
    }, e.prototype.tryParseLeftAngleBracket = function() {
      return !this.isEOF() && this.char() === 60 && (this.ignoreTag || // If at the opening tag or closing tag position, bail.
      !Ga(this.peek() || 0)) ? (this.bump(), "<") : null;
    }, e.prototype.tryParseQuote = function(t) {
      if (this.isEOF() || this.char() !== 39)
        return null;
      switch (this.peek()) {
        case 39:
          return this.bump(), this.bump(), "'";
        case 123:
        case 60:
        case 62:
        case 125:
          break;
        case 35:
          if (t === "plural" || t === "selectordinal")
            break;
          return null;
        default:
          return null;
      }
      this.bump();
      var n = [this.char()];
      for (this.bump(); !this.isEOF(); ) {
        var i = this.char();
        if (i === 39)
          if (this.peek() === 39)
            n.push(39), this.bump();
          else {
            this.bump();
            break;
          }
        else
          n.push(i);
        this.bump();
      }
      return yn.apply(void 0, n);
    }, e.prototype.tryParseUnquoted = function(t, n) {
      if (this.isEOF())
        return null;
      var i = this.char();
      return i === 60 || i === 123 || i === 35 && (n === "plural" || n === "selectordinal") || i === 125 && t > 0 ? null : (this.bump(), yn(i));
    }, e.prototype.parseArgument = function(t, n) {
      var i = this.clonePosition();
      if (this.bump(), this.bumpSpace(), this.isEOF())
        return this.error(I.EXPECT_ARGUMENT_CLOSING_BRACE, L(i, this.clonePosition()));
      if (this.char() === 125)
        return this.bump(), this.error(I.EMPTY_ARGUMENT, L(i, this.clonePosition()));
      var l = this.parseIdentifierIfPossible().value;
      if (!l)
        return this.error(I.MALFORMED_ARGUMENT, L(i, this.clonePosition()));
      if (this.bumpSpace(), this.isEOF())
        return this.error(I.EXPECT_ARGUMENT_CLOSING_BRACE, L(i, this.clonePosition()));
      switch (this.char()) {
        case 125:
          return this.bump(), {
            val: {
              type: j.argument,
              // value does not include the opening and closing braces.
              value: l,
              location: L(i, this.clonePosition())
            },
            err: null
          };
        case 44:
          return this.bump(), this.bumpSpace(), this.isEOF() ? this.error(I.EXPECT_ARGUMENT_CLOSING_BRACE, L(i, this.clonePosition())) : this.parseArgumentOptions(t, n, l, i);
        default:
          return this.error(I.MALFORMED_ARGUMENT, L(i, this.clonePosition()));
      }
    }, e.prototype.parseIdentifierIfPossible = function() {
      var t = this.clonePosition(), n = this.offset(), i = wn(this.message, n), l = n + i.length;
      this.bumpTo(l);
      var r = this.clonePosition(), a = L(t, r);
      return { value: i, location: a };
    }, e.prototype.parseArgumentOptions = function(t, n, i, l) {
      var r, a = this.clonePosition(), s = this.parseIdentifierIfPossible().value, o = this.clonePosition();
      switch (s) {
        case "":
          return this.error(I.EXPECT_ARGUMENT_TYPE, L(a, o));
        case "number":
        case "date":
        case "time": {
          this.bumpSpace();
          var u = null;
          if (this.bumpIf(",")) {
            this.bumpSpace();
            var f = this.clonePosition(), h = this.parseSimpleArgStyleIfPossible();
            if (h.err)
              return h;
            var d = Da(h.val);
            if (d.length === 0)
              return this.error(I.EXPECT_ARGUMENT_STYLE, L(this.clonePosition(), this.clonePosition()));
            var b = L(f, this.clonePosition());
            u = { style: d, styleLocation: b };
          }
          var y = this.tryParseArgumentClose(l);
          if (y.err)
            return y;
          var w = L(l, this.clonePosition());
          if (u && Pi(u == null ? void 0 : u.style, "::", 0)) {
            var p = Ra(u.style.slice(2));
            if (s === "number") {
              var h = this.parseNumberSkeletonFromString(p, u.styleLocation);
              return h.err ? h : {
                val: { type: j.number, value: i, location: w, style: h.val },
                err: null
              };
            } else {
              if (p.length === 0)
                return this.error(I.EXPECT_DATE_TIME_SKELETON, w);
              var m = p;
              this.locale && (m = Sa(p, this.locale));
              var d = {
                type: Je.dateTime,
                pattern: m,
                location: u.styleLocation,
                parsedOptions: this.shouldParseSkeletons ? ba(m) : {}
              }, v = s === "date" ? j.date : j.time;
              return {
                val: { type: v, value: i, location: w, style: d },
                err: null
              };
            }
          }
          return {
            val: {
              type: s === "number" ? j.number : s === "date" ? j.date : j.time,
              value: i,
              location: w,
              style: (r = u == null ? void 0 : u.style) !== null && r !== void 0 ? r : null
            },
            err: null
          };
        }
        case "plural":
        case "selectordinal":
        case "select": {
          var c = this.clonePosition();
          if (this.bumpSpace(), !this.bumpIf(","))
            return this.error(I.EXPECT_SELECT_ARGUMENT_OPTIONS, L(c, R({}, c)));
          this.bumpSpace();
          var _ = this.parseIdentifierIfPossible(), E = 0;
          if (s !== "select" && _.value === "offset") {
            if (!this.bumpIf(":"))
              return this.error(I.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE, L(this.clonePosition(), this.clonePosition()));
            this.bumpSpace();
            var h = this.tryParseDecimalInteger(I.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE, I.INVALID_PLURAL_ARGUMENT_OFFSET_VALUE);
            if (h.err)
              return h;
            this.bumpSpace(), _ = this.parseIdentifierIfPossible(), E = h.val;
          }
          var g = this.tryParsePluralOrSelectOptions(t, s, n, _);
          if (g.err)
            return g;
          var y = this.tryParseArgumentClose(l);
          if (y.err)
            return y;
          var P = L(l, this.clonePosition());
          return s === "select" ? {
            val: {
              type: j.select,
              value: i,
              options: Ni(g.val),
              location: P
            },
            err: null
          } : {
            val: {
              type: j.plural,
              value: i,
              options: Ni(g.val),
              offset: E,
              pluralType: s === "plural" ? "cardinal" : "ordinal",
              location: P
            },
            err: null
          };
        }
        default:
          return this.error(I.INVALID_ARGUMENT_TYPE, L(a, o));
      }
    }, e.prototype.tryParseArgumentClose = function(t) {
      return this.isEOF() || this.char() !== 125 ? this.error(I.EXPECT_ARGUMENT_CLOSING_BRACE, L(t, this.clonePosition())) : (this.bump(), { val: !0, err: null });
    }, e.prototype.parseSimpleArgStyleIfPossible = function() {
      for (var t = 0, n = this.clonePosition(); !this.isEOF(); ) {
        var i = this.char();
        switch (i) {
          case 39: {
            this.bump();
            var l = this.clonePosition();
            if (!this.bumpUntil("'"))
              return this.error(I.UNCLOSED_QUOTE_IN_ARGUMENT_STYLE, L(l, this.clonePosition()));
            this.bump();
            break;
          }
          case 123: {
            t += 1, this.bump();
            break;
          }
          case 125: {
            if (t > 0)
              t -= 1;
            else
              return {
                val: this.message.slice(n.offset, this.offset()),
                err: null
              };
            break;
          }
          default:
            this.bump();
            break;
        }
      }
      return {
        val: this.message.slice(n.offset, this.offset()),
        err: null
      };
    }, e.prototype.parseNumberSkeletonFromString = function(t, n) {
      var i = [];
      try {
        i = ga(t);
      } catch {
        return this.error(I.INVALID_NUMBER_SKELETON, n);
      }
      return {
        val: {
          type: Je.number,
          tokens: i,
          location: n,
          parsedOptions: this.shouldParseSkeletons ? Ea(i) : {}
        },
        err: null
      };
    }, e.prototype.tryParsePluralOrSelectOptions = function(t, n, i, l) {
      for (var r, a = !1, s = [], o = /* @__PURE__ */ new Set(), u = l.value, f = l.location; ; ) {
        if (u.length === 0) {
          var h = this.clonePosition();
          if (n !== "select" && this.bumpIf("=")) {
            var d = this.tryParseDecimalInteger(I.EXPECT_PLURAL_ARGUMENT_SELECTOR, I.INVALID_PLURAL_ARGUMENT_SELECTOR);
            if (d.err)
              return d;
            f = L(h, this.clonePosition()), u = this.message.slice(h.offset, this.offset());
          } else
            break;
        }
        if (o.has(u))
          return this.error(n === "select" ? I.DUPLICATE_SELECT_ARGUMENT_SELECTOR : I.DUPLICATE_PLURAL_ARGUMENT_SELECTOR, f);
        u === "other" && (a = !0), this.bumpSpace();
        var b = this.clonePosition();
        if (!this.bumpIf("{"))
          return this.error(n === "select" ? I.EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT : I.EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT, L(this.clonePosition(), this.clonePosition()));
        var y = this.parseMessage(t + 1, n, i);
        if (y.err)
          return y;
        var w = this.tryParseArgumentClose(b);
        if (w.err)
          return w;
        s.push([
          u,
          {
            value: y.val,
            location: L(b, this.clonePosition())
          }
        ]), o.add(u), this.bumpSpace(), r = this.parseIdentifierIfPossible(), u = r.value, f = r.location;
      }
      return s.length === 0 ? this.error(n === "select" ? I.EXPECT_SELECT_ARGUMENT_SELECTOR : I.EXPECT_PLURAL_ARGUMENT_SELECTOR, L(this.clonePosition(), this.clonePosition())) : this.requiresOtherClause && !a ? this.error(I.MISSING_OTHER_CLAUSE, L(this.clonePosition(), this.clonePosition())) : { val: s, err: null };
    }, e.prototype.tryParseDecimalInteger = function(t, n) {
      var i = 1, l = this.clonePosition();
      this.bumpIf("+") || this.bumpIf("-") && (i = -1);
      for (var r = !1, a = 0; !this.isEOF(); ) {
        var s = this.char();
        if (s >= 48 && s <= 57)
          r = !0, a = a * 10 + (s - 48), this.bump();
        else
          break;
      }
      var o = L(l, this.clonePosition());
      return r ? (a *= i, La(a) ? { val: a, err: null } : this.error(n, o)) : this.error(t, o);
    }, e.prototype.offset = function() {
      return this.position.offset;
    }, e.prototype.isEOF = function() {
      return this.offset() === this.message.length;
    }, e.prototype.clonePosition = function() {
      return {
        offset: this.position.offset,
        line: this.position.line,
        column: this.position.column
      };
    }, e.prototype.char = function() {
      var t = this.position.offset;
      if (t >= this.message.length)
        throw Error("out of bound");
      var n = Pl(this.message, t);
      if (n === void 0)
        throw Error("Offset ".concat(t, " is at invalid UTF-16 code unit boundary"));
      return n;
    }, e.prototype.error = function(t, n) {
      return {
        val: null,
        err: {
          kind: t,
          message: this.message,
          location: n
        }
      };
    }, e.prototype.bump = function() {
      if (!this.isEOF()) {
        var t = this.char();
        t === 10 ? (this.position.line += 1, this.position.column = 1, this.position.offset += 1) : (this.position.column += 1, this.position.offset += t < 65536 ? 1 : 2);
      }
    }, e.prototype.bumpIf = function(t) {
      if (Pi(this.message, t, this.offset())) {
        for (var n = 0; n < t.length; n++)
          this.bump();
        return !0;
      }
      return !1;
    }, e.prototype.bumpUntil = function(t) {
      var n = this.offset(), i = this.message.indexOf(t, n);
      return i >= 0 ? (this.bumpTo(i), !0) : (this.bumpTo(this.message.length), !1);
    }, e.prototype.bumpTo = function(t) {
      if (this.offset() > t)
        throw Error("targetOffset ".concat(t, " must be greater than or equal to the current offset ").concat(this.offset()));
      for (t = Math.min(t, this.message.length); ; ) {
        var n = this.offset();
        if (n === t)
          break;
        if (n > t)
          throw Error("targetOffset ".concat(t, " is at invalid UTF-16 code unit boundary"));
        if (this.bump(), this.isEOF())
          break;
      }
    }, e.prototype.bumpSpace = function() {
      for (; !this.isEOF() && Ol(this.char()); )
        this.bump();
    }, e.prototype.peek = function() {
      if (this.isEOF())
        return null;
      var t = this.char(), n = this.offset(), i = this.message.charCodeAt(n + (t >= 65536 ? 2 : 1));
      return i ?? null;
    }, e;
  }()
);
function En(e) {
  return e >= 97 && e <= 122 || e >= 65 && e <= 90;
}
function Ga(e) {
  return En(e) || e === 47;
}
function Fa(e) {
  return e === 45 || e === 46 || e >= 48 && e <= 57 || e === 95 || e >= 97 && e <= 122 || e >= 65 && e <= 90 || e == 183 || e >= 192 && e <= 214 || e >= 216 && e <= 246 || e >= 248 && e <= 893 || e >= 895 && e <= 8191 || e >= 8204 && e <= 8205 || e >= 8255 && e <= 8256 || e >= 8304 && e <= 8591 || e >= 11264 && e <= 12271 || e >= 12289 && e <= 55295 || e >= 63744 && e <= 64975 || e >= 65008 && e <= 65533 || e >= 65536 && e <= 983039;
}
function Ol(e) {
  return e >= 9 && e <= 13 || e === 32 || e === 133 || e >= 8206 && e <= 8207 || e === 8232 || e === 8233;
}
function ja(e) {
  return e >= 33 && e <= 35 || e === 36 || e >= 37 && e <= 39 || e === 40 || e === 41 || e === 42 || e === 43 || e === 44 || e === 45 || e >= 46 && e <= 47 || e >= 58 && e <= 59 || e >= 60 && e <= 62 || e >= 63 && e <= 64 || e === 91 || e === 92 || e === 93 || e === 94 || e === 96 || e === 123 || e === 124 || e === 125 || e === 126 || e === 161 || e >= 162 && e <= 165 || e === 166 || e === 167 || e === 169 || e === 171 || e === 172 || e === 174 || e === 176 || e === 177 || e === 182 || e === 187 || e === 191 || e === 215 || e === 247 || e >= 8208 && e <= 8213 || e >= 8214 && e <= 8215 || e === 8216 || e === 8217 || e === 8218 || e >= 8219 && e <= 8220 || e === 8221 || e === 8222 || e === 8223 || e >= 8224 && e <= 8231 || e >= 8240 && e <= 8248 || e === 8249 || e === 8250 || e >= 8251 && e <= 8254 || e >= 8257 && e <= 8259 || e === 8260 || e === 8261 || e === 8262 || e >= 8263 && e <= 8273 || e === 8274 || e === 8275 || e >= 8277 && e <= 8286 || e >= 8592 && e <= 8596 || e >= 8597 && e <= 8601 || e >= 8602 && e <= 8603 || e >= 8604 && e <= 8607 || e === 8608 || e >= 8609 && e <= 8610 || e === 8611 || e >= 8612 && e <= 8613 || e === 8614 || e >= 8615 && e <= 8621 || e === 8622 || e >= 8623 && e <= 8653 || e >= 8654 && e <= 8655 || e >= 8656 && e <= 8657 || e === 8658 || e === 8659 || e === 8660 || e >= 8661 && e <= 8691 || e >= 8692 && e <= 8959 || e >= 8960 && e <= 8967 || e === 8968 || e === 8969 || e === 8970 || e === 8971 || e >= 8972 && e <= 8991 || e >= 8992 && e <= 8993 || e >= 8994 && e <= 9e3 || e === 9001 || e === 9002 || e >= 9003 && e <= 9083 || e === 9084 || e >= 9085 && e <= 9114 || e >= 9115 && e <= 9139 || e >= 9140 && e <= 9179 || e >= 9180 && e <= 9185 || e >= 9186 && e <= 9254 || e >= 9255 && e <= 9279 || e >= 9280 && e <= 9290 || e >= 9291 && e <= 9311 || e >= 9472 && e <= 9654 || e === 9655 || e >= 9656 && e <= 9664 || e === 9665 || e >= 9666 && e <= 9719 || e >= 9720 && e <= 9727 || e >= 9728 && e <= 9838 || e === 9839 || e >= 9840 && e <= 10087 || e === 10088 || e === 10089 || e === 10090 || e === 10091 || e === 10092 || e === 10093 || e === 10094 || e === 10095 || e === 10096 || e === 10097 || e === 10098 || e === 10099 || e === 10100 || e === 10101 || e >= 10132 && e <= 10175 || e >= 10176 && e <= 10180 || e === 10181 || e === 10182 || e >= 10183 && e <= 10213 || e === 10214 || e === 10215 || e === 10216 || e === 10217 || e === 10218 || e === 10219 || e === 10220 || e === 10221 || e === 10222 || e === 10223 || e >= 10224 && e <= 10239 || e >= 10240 && e <= 10495 || e >= 10496 && e <= 10626 || e === 10627 || e === 10628 || e === 10629 || e === 10630 || e === 10631 || e === 10632 || e === 10633 || e === 10634 || e === 10635 || e === 10636 || e === 10637 || e === 10638 || e === 10639 || e === 10640 || e === 10641 || e === 10642 || e === 10643 || e === 10644 || e === 10645 || e === 10646 || e === 10647 || e === 10648 || e >= 10649 && e <= 10711 || e === 10712 || e === 10713 || e === 10714 || e === 10715 || e >= 10716 && e <= 10747 || e === 10748 || e === 10749 || e >= 10750 && e <= 11007 || e >= 11008 && e <= 11055 || e >= 11056 && e <= 11076 || e >= 11077 && e <= 11078 || e >= 11079 && e <= 11084 || e >= 11085 && e <= 11123 || e >= 11124 && e <= 11125 || e >= 11126 && e <= 11157 || e === 11158 || e >= 11159 && e <= 11263 || e >= 11776 && e <= 11777 || e === 11778 || e === 11779 || e === 11780 || e === 11781 || e >= 11782 && e <= 11784 || e === 11785 || e === 11786 || e === 11787 || e === 11788 || e === 11789 || e >= 11790 && e <= 11798 || e === 11799 || e >= 11800 && e <= 11801 || e === 11802 || e === 11803 || e === 11804 || e === 11805 || e >= 11806 && e <= 11807 || e === 11808 || e === 11809 || e === 11810 || e === 11811 || e === 11812 || e === 11813 || e === 11814 || e === 11815 || e === 11816 || e === 11817 || e >= 11818 && e <= 11822 || e === 11823 || e >= 11824 && e <= 11833 || e >= 11834 && e <= 11835 || e >= 11836 && e <= 11839 || e === 11840 || e === 11841 || e === 11842 || e >= 11843 && e <= 11855 || e >= 11856 && e <= 11857 || e === 11858 || e >= 11859 && e <= 11903 || e >= 12289 && e <= 12291 || e === 12296 || e === 12297 || e === 12298 || e === 12299 || e === 12300 || e === 12301 || e === 12302 || e === 12303 || e === 12304 || e === 12305 || e >= 12306 && e <= 12307 || e === 12308 || e === 12309 || e === 12310 || e === 12311 || e === 12312 || e === 12313 || e === 12314 || e === 12315 || e === 12316 || e === 12317 || e >= 12318 && e <= 12319 || e === 12320 || e === 12336 || e === 64830 || e === 64831 || e >= 65093 && e <= 65094;
}
function Sn(e) {
  e.forEach(function(t) {
    if (delete t.location, El(t) || Sl(t))
      for (var n in t.options)
        delete t.options[n].location, Sn(t.options[n].value);
    else
      vl(t) && Al(t.style) || (yl(t) || wl(t)) && gn(t.style) ? delete t.style.location : Tl(t) && Sn(t.children);
  });
}
function xa(e, t) {
  t === void 0 && (t = {}), t = R({ shouldParseSkeletons: !0, requiresOtherClause: !0 }, t);
  var n = new Ua(e, t).parse();
  if (n.err) {
    var i = SyntaxError(I[n.err.kind]);
    throw i.location = n.err.location, i.originalMessage = n.err.message, i;
  }
  return t != null && t.captureLocation || Sn(n.val), n.val;
}
function rn(e, t) {
  var n = t && t.cache ? t.cache : Wa, i = t && t.serializer ? t.serializer : Za, l = t && t.strategy ? t.strategy : qa;
  return l(e, {
    cache: n,
    serializer: i
  });
}
function Va(e) {
  return e == null || typeof e == "number" || typeof e == "boolean";
}
function Il(e, t, n, i) {
  var l = Va(i) ? i : n(i), r = t.get(l);
  return typeof r > "u" && (r = e.call(this, i), t.set(l, r)), r;
}
function Ll(e, t, n) {
  var i = Array.prototype.slice.call(arguments, 3), l = n(i), r = t.get(l);
  return typeof r > "u" && (r = e.apply(this, i), t.set(l, r)), r;
}
function Nn(e, t, n, i, l) {
  return n.bind(t, e, i, l);
}
function qa(e, t) {
  var n = e.length === 1 ? Il : Ll;
  return Nn(e, this, n, t.cache.create(), t.serializer);
}
function Xa(e, t) {
  return Nn(e, this, Ll, t.cache.create(), t.serializer);
}
function za(e, t) {
  return Nn(e, this, Il, t.cache.create(), t.serializer);
}
var Za = function() {
  return JSON.stringify(arguments);
};
function On() {
  this.cache = /* @__PURE__ */ Object.create(null);
}
On.prototype.get = function(e) {
  return this.cache[e];
};
On.prototype.set = function(e, t) {
  this.cache[e] = t;
};
var Wa = {
  create: function() {
    return new On();
  }
}, sn = {
  variadic: Xa,
  monadic: za
}, Ye;
(function(e) {
  e.MISSING_VALUE = "MISSING_VALUE", e.INVALID_VALUE = "INVALID_VALUE", e.MISSING_INTL_API = "MISSING_INTL_API";
})(Ye || (Ye = {}));
var Vt = (
  /** @class */
  function(e) {
    xt(t, e);
    function t(n, i, l) {
      var r = e.call(this, n) || this;
      return r.code = i, r.originalMessage = l, r;
    }
    return t.prototype.toString = function() {
      return "[formatjs Error: ".concat(this.code, "] ").concat(this.message);
    }, t;
  }(Error)
), Ii = (
  /** @class */
  function(e) {
    xt(t, e);
    function t(n, i, l, r) {
      return e.call(this, 'Invalid values for "'.concat(n, '": "').concat(i, '". Options are "').concat(Object.keys(l).join('", "'), '"'), Ye.INVALID_VALUE, r) || this;
    }
    return t;
  }(Vt)
), Qa = (
  /** @class */
  function(e) {
    xt(t, e);
    function t(n, i, l) {
      return e.call(this, 'Value for "'.concat(n, '" must be of type ').concat(i), Ye.INVALID_VALUE, l) || this;
    }
    return t;
  }(Vt)
), Ja = (
  /** @class */
  function(e) {
    xt(t, e);
    function t(n, i) {
      return e.call(this, 'The intl string context variable "'.concat(n, '" was not provided to the string "').concat(i, '"'), Ye.MISSING_VALUE, i) || this;
    }
    return t;
  }(Vt)
), J;
(function(e) {
  e[e.literal = 0] = "literal", e[e.object = 1] = "object";
})(J || (J = {}));
function Ya(e) {
  return e.length < 2 ? e : e.reduce(function(t, n) {
    var i = t[t.length - 1];
    return !i || i.type !== J.literal || n.type !== J.literal ? t.push(n) : i.value += n.value, t;
  }, []);
}
function Ka(e) {
  return typeof e == "function";
}
function Pt(e, t, n, i, l, r, a) {
  if (e.length === 1 && Hi(e[0]))
    return [
      {
        type: J.literal,
        value: e[0].value
      }
    ];
  for (var s = [], o = 0, u = e; o < u.length; o++) {
    var f = u[o];
    if (Hi(f)) {
      s.push({
        type: J.literal,
        value: f.value
      });
      continue;
    }
    if (ma(f)) {
      typeof r == "number" && s.push({
        type: J.literal,
        value: n.getNumberFormat(t).format(r)
      });
      continue;
    }
    var h = f.value;
    if (!(l && h in l))
      throw new Ja(h, a);
    var d = l[h];
    if (_a(f)) {
      (!d || typeof d == "string" || typeof d == "number") && (d = typeof d == "string" || typeof d == "number" ? String(d) : ""), s.push({
        type: typeof d == "string" ? J.literal : J.object,
        value: d
      });
      continue;
    }
    if (yl(f)) {
      var b = typeof f.style == "string" ? i.date[f.style] : gn(f.style) ? f.style.parsedOptions : void 0;
      s.push({
        type: J.literal,
        value: n.getDateTimeFormat(t, b).format(d)
      });
      continue;
    }
    if (wl(f)) {
      var b = typeof f.style == "string" ? i.time[f.style] : gn(f.style) ? f.style.parsedOptions : i.time.medium;
      s.push({
        type: J.literal,
        value: n.getDateTimeFormat(t, b).format(d)
      });
      continue;
    }
    if (vl(f)) {
      var b = typeof f.style == "string" ? i.number[f.style] : Al(f.style) ? f.style.parsedOptions : void 0;
      b && b.scale && (d = d * (b.scale || 1)), s.push({
        type: J.literal,
        value: n.getNumberFormat(t, b).format(d)
      });
      continue;
    }
    if (Tl(f)) {
      var y = f.children, w = f.value, p = l[w];
      if (!Ka(p))
        throw new Qa(w, "function", a);
      var m = Pt(y, t, n, i, l, r), v = p(m.map(function(E) {
        return E.value;
      }));
      Array.isArray(v) || (v = [v]), s.push.apply(s, v.map(function(E) {
        return {
          type: typeof E == "string" ? J.literal : J.object,
          value: E
        };
      }));
    }
    if (El(f)) {
      var c = f.options[d] || f.options.other;
      if (!c)
        throw new Ii(f.value, d, Object.keys(f.options), a);
      s.push.apply(s, Pt(c.value, t, n, i, l));
      continue;
    }
    if (Sl(f)) {
      var c = f.options["=".concat(d)];
      if (!c) {
        if (!Intl.PluralRules)
          throw new Vt(`Intl.PluralRules is not available in this environment.
Try polyfilling it using "@formatjs/intl-pluralrules"
`, Ye.MISSING_INTL_API, a);
        var _ = n.getPluralRules(t, { type: f.pluralType }).select(d - (f.offset || 0));
        c = f.options[_] || f.options.other;
      }
      if (!c)
        throw new Ii(f.value, d, Object.keys(f.options), a);
      s.push.apply(s, Pt(c.value, t, n, i, l, d - (f.offset || 0)));
      continue;
    }
  }
  return Ya(s);
}
function $a(e, t) {
  return t ? R(R(R({}, e || {}), t || {}), Object.keys(e).reduce(function(n, i) {
    return n[i] = R(R({}, e[i]), t[i] || {}), n;
  }, {})) : e;
}
function eu(e, t) {
  return t ? Object.keys(e).reduce(function(n, i) {
    return n[i] = $a(e[i], t[i]), n;
  }, R({}, e)) : e;
}
function on(e) {
  return {
    create: function() {
      return {
        get: function(t) {
          return e[t];
        },
        set: function(t, n) {
          e[t] = n;
        }
      };
    }
  };
}
function tu(e) {
  return e === void 0 && (e = {
    number: {},
    dateTime: {},
    pluralRules: {}
  }), {
    getNumberFormat: rn(function() {
      for (var t, n = [], i = 0; i < arguments.length; i++)
        n[i] = arguments[i];
      return new ((t = Intl.NumberFormat).bind.apply(t, nn([void 0], n, !1)))();
    }, {
      cache: on(e.number),
      strategy: sn.variadic
    }),
    getDateTimeFormat: rn(function() {
      for (var t, n = [], i = 0; i < arguments.length; i++)
        n[i] = arguments[i];
      return new ((t = Intl.DateTimeFormat).bind.apply(t, nn([void 0], n, !1)))();
    }, {
      cache: on(e.dateTime),
      strategy: sn.variadic
    }),
    getPluralRules: rn(function() {
      for (var t, n = [], i = 0; i < arguments.length; i++)
        n[i] = arguments[i];
      return new ((t = Intl.PluralRules).bind.apply(t, nn([void 0], n, !1)))();
    }, {
      cache: on(e.pluralRules),
      strategy: sn.variadic
    })
  };
}
var nu = (
  /** @class */
  function() {
    function e(t, n, i, l) {
      var r = this;
      if (n === void 0 && (n = e.defaultLocale), this.formatterCache = {
        number: {},
        dateTime: {},
        pluralRules: {}
      }, this.format = function(a) {
        var s = r.formatToParts(a);
        if (s.length === 1)
          return s[0].value;
        var o = s.reduce(function(u, f) {
          return !u.length || f.type !== J.literal || typeof u[u.length - 1] != "string" ? u.push(f.value) : u[u.length - 1] += f.value, u;
        }, []);
        return o.length <= 1 ? o[0] || "" : o;
      }, this.formatToParts = function(a) {
        return Pt(r.ast, r.locales, r.formatters, r.formats, a, void 0, r.message);
      }, this.resolvedOptions = function() {
        return {
          locale: r.resolvedLocale.toString()
        };
      }, this.getAst = function() {
        return r.ast;
      }, this.locales = n, this.resolvedLocale = e.resolveLocale(n), typeof t == "string") {
        if (this.message = t, !e.__parse)
          throw new TypeError("IntlMessageFormat.__parse must be set to process `message` of type `string`");
        this.ast = e.__parse(t, {
          ignoreTag: l == null ? void 0 : l.ignoreTag,
          locale: this.resolvedLocale
        });
      } else
        this.ast = t;
      if (!Array.isArray(this.ast))
        throw new TypeError("A message must be provided as a String or AST.");
      this.formats = eu(e.formats, i), this.formatters = l && l.formatters || tu(this.formatterCache);
    }
    return Object.defineProperty(e, "defaultLocale", {
      get: function() {
        return e.memoizedDefaultLocale || (e.memoizedDefaultLocale = new Intl.NumberFormat().resolvedOptions().locale), e.memoizedDefaultLocale;
      },
      enumerable: !1,
      configurable: !0
    }), e.memoizedDefaultLocale = null, e.resolveLocale = function(t) {
      var n = Intl.NumberFormat.supportedLocalesOf(t);
      return n.length > 0 ? new Intl.Locale(n[0]) : new Intl.Locale(typeof t == "string" ? t : t[0]);
    }, e.__parse = xa, e.formats = {
      number: {
        integer: {
          maximumFractionDigits: 0
        },
        currency: {
          style: "currency"
        },
        percent: {
          style: "percent"
        }
      },
      date: {
        short: {
          month: "numeric",
          day: "numeric",
          year: "2-digit"
        },
        medium: {
          month: "short",
          day: "numeric",
          year: "numeric"
        },
        long: {
          month: "long",
          day: "numeric",
          year: "numeric"
        },
        full: {
          weekday: "long",
          month: "long",
          day: "numeric",
          year: "numeric"
        }
      },
      time: {
        short: {
          hour: "numeric",
          minute: "numeric"
        },
        medium: {
          hour: "numeric",
          minute: "numeric",
          second: "numeric"
        },
        long: {
          hour: "numeric",
          minute: "numeric",
          second: "numeric",
          timeZoneName: "short"
        },
        full: {
          hour: "numeric",
          minute: "numeric",
          second: "numeric",
          timeZoneName: "short"
        }
      }
    }, e;
  }()
);
function iu(e, t) {
  if (t == null)
    return;
  if (t in e)
    return e[t];
  const n = t.split(".");
  let i = e;
  for (let l = 0; l < n.length; l++)
    if (typeof i == "object") {
      if (l > 0) {
        const r = n.slice(l, n.length).join(".");
        if (r in i) {
          i = i[r];
          break;
        }
      }
      i = i[n[l]];
    } else
      i = void 0;
  return i;
}
const Ce = {}, lu = (e, t, n) => n && (t in Ce || (Ce[t] = {}), e in Ce[t] || (Ce[t][e] = n), n), Ml = (e, t) => {
  if (t == null)
    return;
  if (t in Ce && e in Ce[t])
    return Ce[t][e];
  const n = qt(t);
  for (let i = 0; i < n.length; i++) {
    const l = n[i], r = su(l, e);
    if (r)
      return lu(e, t, r);
  }
};
let In;
const yt = pt({});
function ru(e) {
  return In[e] || null;
}
function Rl(e) {
  return e in In;
}
function su(e, t) {
  if (!Rl(e))
    return null;
  const n = ru(e);
  return iu(n, t);
}
function ou(e) {
  if (e == null)
    return;
  const t = qt(e);
  for (let n = 0; n < t.length; n++) {
    const i = t[n];
    if (Rl(i))
      return i;
  }
}
function au(e, ...t) {
  delete Ce[e], yt.update((n) => (n[e] = ha.all([n[e] || {}, ...t]), n));
}
tt(
  [yt],
  ([e]) => Object.keys(e)
);
yt.subscribe((e) => In = e);
const Nt = {};
function uu(e, t) {
  Nt[e].delete(t), Nt[e].size === 0 && delete Nt[e];
}
function Dl(e) {
  return Nt[e];
}
function fu(e) {
  return qt(e).map((t) => {
    const n = Dl(t);
    return [t, n ? [...n] : []];
  }).filter(([, t]) => t.length > 0);
}
function Tn(e) {
  return e == null ? !1 : qt(e).some(
    (t) => {
      var n;
      return (n = Dl(t)) == null ? void 0 : n.size;
    }
  );
}
function cu(e, t) {
  return Promise.all(
    t.map((i) => (uu(e, i), i().then((l) => l.default || l)))
  ).then((i) => au(e, ...i));
}
const ot = {};
function Ul(e) {
  if (!Tn(e))
    return e in ot ? ot[e] : Promise.resolve();
  const t = fu(e);
  return ot[e] = Promise.all(
    t.map(
      ([n, i]) => cu(n, i)
    )
  ).then(() => {
    if (Tn(e))
      return Ul(e);
    delete ot[e];
  }), ot[e];
}
const hu = {
  number: {
    scientific: { notation: "scientific" },
    engineering: { notation: "engineering" },
    compactLong: { notation: "compact", compactDisplay: "long" },
    compactShort: { notation: "compact", compactDisplay: "short" }
  },
  date: {
    short: { month: "numeric", day: "numeric", year: "2-digit" },
    medium: { month: "short", day: "numeric", year: "numeric" },
    long: { month: "long", day: "numeric", year: "numeric" },
    full: { weekday: "long", month: "long", day: "numeric", year: "numeric" }
  },
  time: {
    short: { hour: "numeric", minute: "numeric" },
    medium: { hour: "numeric", minute: "numeric", second: "numeric" },
    long: {
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
      timeZoneName: "short"
    },
    full: {
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
      timeZoneName: "short"
    }
  }
}, _u = {
  fallbackLocale: null,
  loadingDelay: 200,
  formats: hu,
  warnOnMissingMessages: !0,
  handleMissingMessage: void 0,
  ignoreTag: !0
}, mu = _u;
function Ke() {
  return mu;
}
const an = pt(!1);
var du = Object.defineProperty, bu = Object.defineProperties, pu = Object.getOwnPropertyDescriptors, Li = Object.getOwnPropertySymbols, gu = Object.prototype.hasOwnProperty, vu = Object.prototype.propertyIsEnumerable, Mi = (e, t, n) => t in e ? du(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n, yu = (e, t) => {
  for (var n in t || (t = {}))
    gu.call(t, n) && Mi(e, n, t[n]);
  if (Li)
    for (var n of Li(t))
      vu.call(t, n) && Mi(e, n, t[n]);
  return e;
}, wu = (e, t) => bu(e, pu(t));
let An;
const Dt = pt(null);
function Ri(e) {
  return e.split("-").map((t, n, i) => i.slice(0, n + 1).join("-")).reverse();
}
function qt(e, t = Ke().fallbackLocale) {
  const n = Ri(e);
  return t ? [.../* @__PURE__ */ new Set([...n, ...Ri(t)])] : n;
}
function Le() {
  return An ?? void 0;
}
Dt.subscribe((e) => {
  An = e ?? void 0, typeof window < "u" && e != null && document.documentElement.setAttribute("lang", e);
});
const Eu = (e) => {
  if (e && ou(e) && Tn(e)) {
    const { loadingDelay: t } = Ke();
    let n;
    return typeof window < "u" && Le() != null && t ? n = window.setTimeout(
      () => an.set(!0),
      t
    ) : an.set(!0), Ul(e).then(() => {
      Dt.set(e);
    }).finally(() => {
      clearTimeout(n), an.set(!1);
    });
  }
  return Dt.set(e);
}, wt = wu(yu({}, Dt), {
  set: Eu
}), Xt = (e) => {
  const t = /* @__PURE__ */ Object.create(null);
  return (i) => {
    const l = JSON.stringify(i);
    return l in t ? t[l] : t[l] = e(i);
  };
};
var Su = Object.defineProperty, Ut = Object.getOwnPropertySymbols, Gl = Object.prototype.hasOwnProperty, Fl = Object.prototype.propertyIsEnumerable, Di = (e, t, n) => t in e ? Su(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n, Ln = (e, t) => {
  for (var n in t || (t = {}))
    Gl.call(t, n) && Di(e, n, t[n]);
  if (Ut)
    for (var n of Ut(t))
      Fl.call(t, n) && Di(e, n, t[n]);
  return e;
}, it = (e, t) => {
  var n = {};
  for (var i in e)
    Gl.call(e, i) && t.indexOf(i) < 0 && (n[i] = e[i]);
  if (e != null && Ut)
    for (var i of Ut(e))
      t.indexOf(i) < 0 && Fl.call(e, i) && (n[i] = e[i]);
  return n;
};
const _t = (e, t) => {
  const { formats: n } = Ke();
  if (e in n && t in n[e])
    return n[e][t];
  throw new Error(`[svelte-i18n] Unknown "${t}" ${e} format.`);
}, Tu = Xt(
  (e) => {
    var t = e, { locale: n, format: i } = t, l = it(t, ["locale", "format"]);
    if (n == null)
      throw new Error('[svelte-i18n] A "locale" must be set to format numbers');
    return i && (l = _t("number", i)), new Intl.NumberFormat(n, l);
  }
), Au = Xt(
  (e) => {
    var t = e, { locale: n, format: i } = t, l = it(t, ["locale", "format"]);
    if (n == null)
      throw new Error('[svelte-i18n] A "locale" must be set to format dates');
    return i ? l = _t("date", i) : Object.keys(l).length === 0 && (l = _t("date", "short")), new Intl.DateTimeFormat(n, l);
  }
), Hu = Xt(
  (e) => {
    var t = e, { locale: n, format: i } = t, l = it(t, ["locale", "format"]);
    if (n == null)
      throw new Error(
        '[svelte-i18n] A "locale" must be set to format time values'
      );
    return i ? l = _t("time", i) : Object.keys(l).length === 0 && (l = _t("time", "short")), new Intl.DateTimeFormat(n, l);
  }
), Bu = (e = {}) => {
  var t = e, {
    locale: n = Le()
  } = t, i = it(t, [
    "locale"
  ]);
  return Tu(Ln({ locale: n }, i));
}, ku = (e = {}) => {
  var t = e, {
    locale: n = Le()
  } = t, i = it(t, [
    "locale"
  ]);
  return Au(Ln({ locale: n }, i));
}, Cu = (e = {}) => {
  var t = e, {
    locale: n = Le()
  } = t, i = it(t, [
    "locale"
  ]);
  return Hu(Ln({ locale: n }, i));
}, Pu = Xt(
  // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
  (e, t = Le()) => new nu(e, t, Ke().formats, {
    ignoreTag: Ke().ignoreTag
  })
), Nu = (e, t = {}) => {
  var n, i, l, r;
  let a = t;
  typeof e == "object" && (a = e, e = a.id);
  const {
    values: s,
    locale: o = Le(),
    default: u
  } = a;
  if (o == null)
    throw new Error(
      "[svelte-i18n] Cannot format a message without first setting the initial locale."
    );
  let f = Ml(e, o);
  if (!f)
    f = (r = (l = (i = (n = Ke()).handleMissingMessage) == null ? void 0 : i.call(n, { locale: o, id: e, defaultValue: u })) != null ? l : u) != null ? r : e;
  else if (typeof f != "string")
    return console.warn(
      `[svelte-i18n] Message with id "${e}" must be of type "string", found: "${typeof f}". Gettin its value through the "$format" method is deprecated; use the "json" method instead.`
    ), f;
  if (!s)
    return f;
  let h = f;
  try {
    h = Pu(f, o).format(s);
  } catch (d) {
    d instanceof Error && console.warn(
      `[svelte-i18n] Message "${e}" has syntax error:`,
      d.message
    );
  }
  return h;
}, Ou = (e, t) => Cu(t).format(e), Iu = (e, t) => ku(t).format(e), Lu = (e, t) => Bu(t).format(e), Mu = (e, t = Le()) => Ml(e, t);
tt([wt, yt], () => Nu);
tt([wt], () => Ou);
tt([wt], () => Iu);
tt([wt], () => Lu);
tt([wt, yt], () => Mu);
const {
  SvelteComponent: Ru,
  append: ce,
  attr: Z,
  binding_callbacks: Du,
  check_outros: Gt,
  create_component: mt,
  destroy_component: dt,
  destroy_each: Uu,
  detach: ye,
  element: he,
  ensure_array_like: Ui,
  group_outros: Ft,
  init: Gu,
  insert: we,
  listen: ge,
  mount_component: bt,
  prevent_default: Gi,
  run_all: Mn,
  safe_not_equal: Fu,
  set_data: Rn,
  set_input_value: Fi,
  space: Xe,
  text: Dn,
  toggle_class: Fe,
  transition_in: Q,
  transition_out: le
} = window.__gradio__svelte__internal, { afterUpdate: ju, createEventDispatcher: xu } = window.__gradio__svelte__internal;
function ji(e, t, n) {
  const i = e.slice();
  return i[40] = t[n], i;
}
function Vu(e) {
  let t;
  return {
    c() {
      t = Dn(
        /*label*/
        e[0]
      );
    },
    m(n, i) {
      we(n, t, i);
    },
    p(n, i) {
      i[0] & /*label*/
      1 && Rn(
        t,
        /*label*/
        n[0]
      );
    },
    d(n) {
      n && ye(t);
    }
  };
}
function qu(e) {
  let t = (
    /*s*/
    e[40] + ""
  ), n;
  return {
    c() {
      n = Dn(t);
    },
    m(i, l) {
      we(i, n, l);
    },
    p(i, l) {
      l[0] & /*selected_indices*/
      4096 && t !== (t = /*s*/
      i[40] + "") && Rn(n, t);
    },
    d(i) {
      i && ye(n);
    }
  };
}
function Xu(e) {
  let t = (
    /*choices_names*/
    e[15][
      /*s*/
      e[40]
    ] + ""
  ), n;
  return {
    c() {
      n = Dn(t);
    },
    m(i, l) {
      we(i, n, l);
    },
    p(i, l) {
      l[0] & /*choices_names, selected_indices*/
      36864 && t !== (t = /*choices_names*/
      i[15][
        /*s*/
        i[40]
      ] + "") && Rn(n, t);
    },
    d(i) {
      i && ye(n);
    }
  };
}
function xi(e) {
  let t, n, i, l, r, a;
  n = new rl({});
  function s() {
    return (
      /*click_handler*/
      e[31](
        /*s*/
        e[40]
      )
    );
  }
  function o(...u) {
    return (
      /*keydown_handler*/
      e[32](
        /*s*/
        e[40],
        ...u
      )
    );
  }
  return {
    c() {
      t = he("div"), mt(n.$$.fragment), Z(t, "class", "token-remove svelte-xtjjyg"), Z(t, "role", "button"), Z(t, "tabindex", "0"), Z(t, "title", i = /*i18n*/
      e[9]("common.remove") + " " + /*s*/
      e[40]);
    },
    m(u, f) {
      we(u, t, f), bt(n, t, null), l = !0, r || (a = [
        ge(t, "click", Gi(s)),
        ge(t, "keydown", Gi(o))
      ], r = !0);
    },
    p(u, f) {
      e = u, (!l || f[0] & /*i18n, selected_indices*/
      4608 && i !== (i = /*i18n*/
      e[9]("common.remove") + " " + /*s*/
      e[40])) && Z(t, "title", i);
    },
    i(u) {
      l || (Q(n.$$.fragment, u), l = !0);
    },
    o(u) {
      le(n.$$.fragment, u), l = !1;
    },
    d(u) {
      u && ye(t), dt(n), r = !1, Mn(a);
    }
  };
}
function Vi(e) {
  let t, n, i, l;
  function r(u, f) {
    return typeof /*s*/
    u[40] == "number" ? Xu : qu;
  }
  let a = r(e), s = a(e), o = !/*disabled*/
  e[4] && xi(e);
  return {
    c() {
      t = he("div"), n = he("span"), s.c(), i = Xe(), o && o.c(), Z(n, "class", "svelte-xtjjyg"), Z(t, "class", "token svelte-xtjjyg");
    },
    m(u, f) {
      we(u, t, f), ce(t, n), s.m(n, null), ce(t, i), o && o.m(t, null), l = !0;
    },
    p(u, f) {
      a === (a = r(u)) && s ? s.p(u, f) : (s.d(1), s = a(u), s && (s.c(), s.m(n, null))), /*disabled*/
      u[4] ? o && (Ft(), le(o, 1, 1, () => {
        o = null;
      }), Gt()) : o ? (o.p(u, f), f[0] & /*disabled*/
      16 && Q(o, 1)) : (o = xi(u), o.c(), Q(o, 1), o.m(t, null));
    },
    i(u) {
      l || (Q(o), l = !0);
    },
    o(u) {
      le(o), l = !1;
    },
    d(u) {
      u && ye(t), s.d(), o && o.d();
    }
  };
}
function qi(e) {
  let t, n, i, l, r = (
    /*selected_indices*/
    e[12].length > 0 && Xi(e)
  );
  return i = new ll({}), {
    c() {
      r && r.c(), t = Xe(), n = he("span"), mt(i.$$.fragment), Z(n, "class", "icon-wrap svelte-xtjjyg");
    },
    m(a, s) {
      r && r.m(a, s), we(a, t, s), we(a, n, s), bt(i, n, null), l = !0;
    },
    p(a, s) {
      /*selected_indices*/
      a[12].length > 0 ? r ? (r.p(a, s), s[0] & /*selected_indices*/
      4096 && Q(r, 1)) : (r = Xi(a), r.c(), Q(r, 1), r.m(t.parentNode, t)) : r && (Ft(), le(r, 1, 1, () => {
        r = null;
      }), Gt());
    },
    i(a) {
      l || (Q(r), Q(i.$$.fragment, a), l = !0);
    },
    o(a) {
      le(r), le(i.$$.fragment, a), l = !1;
    },
    d(a) {
      a && (ye(t), ye(n)), r && r.d(a), dt(i);
    }
  };
}
function Xi(e) {
  let t, n, i, l, r, a;
  return n = new rl({}), {
    c() {
      t = he("div"), mt(n.$$.fragment), Z(t, "role", "button"), Z(t, "tabindex", "0"), Z(t, "class", "token-remove remove-all svelte-xtjjyg"), Z(t, "title", i = /*i18n*/
      e[9]("common.clear"));
    },
    m(s, o) {
      we(s, t, o), bt(n, t, null), l = !0, r || (a = [
        ge(
          t,
          "click",
          /*remove_all*/
          e[21]
        ),
        ge(
          t,
          "keydown",
          /*keydown_handler_1*/
          e[36]
        )
      ], r = !0);
    },
    p(s, o) {
      (!l || o[0] & /*i18n*/
      512 && i !== (i = /*i18n*/
      s[9]("common.clear"))) && Z(t, "title", i);
    },
    i(s) {
      l || (Q(n.$$.fragment, s), l = !0);
    },
    o(s) {
      le(n.$$.fragment, s), l = !1;
    },
    d(s) {
      s && ye(t), dt(n), r = !1, Mn(a);
    }
  };
}
function zu(e) {
  let t, n, i, l, r, a, s, o, u, f, h, d, b, y, w;
  n = new il({
    props: {
      show_label: (
        /*show_label*/
        e[5]
      ),
      info: (
        /*info*/
        e[1]
      ),
      $$slots: { default: [Vu] },
      $$scope: { ctx: e }
    }
  });
  let p = Ui(
    /*selected_indices*/
    e[12]
  ), m = [];
  for (let _ = 0; _ < p.length; _ += 1)
    m[_] = Vi(ji(e, p, _));
  const v = (_) => le(m[_], 1, 1, () => {
    m[_] = null;
  });
  let c = !/*disabled*/
  e[4] && qi(e);
  return d = new el({
    props: {
      show_options: (
        /*show_options*/
        e[14]
      ),
      choices: (
        /*choices*/
        e[3]
      ),
      filtered_indices: (
        /*filtered_indices*/
        e[11]
      ),
      disabled: (
        /*disabled*/
        e[4]
      ),
      selected_indices: (
        /*selected_indices*/
        e[12]
      ),
      active_index: (
        /*active_index*/
        e[16]
      )
    }
  }), d.$on(
    "change",
    /*handle_option_selected*/
    e[20]
  ), {
    c() {
      t = he("label"), mt(n.$$.fragment), i = Xe(), l = he("div"), r = he("div");
      for (let _ = 0; _ < m.length; _ += 1)
        m[_].c();
      a = Xe(), s = he("div"), o = he("input"), f = Xe(), c && c.c(), h = Xe(), mt(d.$$.fragment), Z(o, "class", "border-none svelte-xtjjyg"), o.disabled = /*disabled*/
      e[4], Z(o, "autocomplete", "off"), o.readOnly = u = !/*filterable*/
      e[8], Fe(o, "subdued", !/*choices_names*/
      e[15].includes(
        /*input_text*/
        e[10]
      ) && !/*allow_custom_value*/
      e[7] || /*selected_indices*/
      e[12].length === /*max_choices*/
      e[2]), Z(s, "class", "secondary-wrap svelte-xtjjyg"), Z(r, "class", "wrap-inner svelte-xtjjyg"), Fe(
        r,
        "show_options",
        /*show_options*/
        e[14]
      ), Z(l, "class", "wrap svelte-xtjjyg"), Z(t, "class", "svelte-xtjjyg"), Fe(
        t,
        "container",
        /*container*/
        e[6]
      );
    },
    m(_, E) {
      we(_, t, E), bt(n, t, null), ce(t, i), ce(t, l), ce(l, r);
      for (let g = 0; g < m.length; g += 1)
        m[g] && m[g].m(r, null);
      ce(r, a), ce(r, s), ce(s, o), Fi(
        o,
        /*input_text*/
        e[10]
      ), e[34](o), ce(s, f), c && c.m(s, null), ce(l, h), bt(d, l, null), b = !0, y || (w = [
        ge(
          o,
          "input",
          /*input_input_handler*/
          e[33]
        ),
        ge(
          o,
          "keydown",
          /*handle_key_down*/
          e[23]
        ),
        ge(
          o,
          "keyup",
          /*keyup_handler*/
          e[35]
        ),
        ge(
          o,
          "blur",
          /*handle_blur*/
          e[18]
        ),
        ge(
          o,
          "focus",
          /*handle_focus*/
          e[22]
        )
      ], y = !0);
    },
    p(_, E) {
      const g = {};
      if (E[0] & /*show_label*/
      32 && (g.show_label = /*show_label*/
      _[5]), E[0] & /*info*/
      2 && (g.info = /*info*/
      _[1]), E[0] & /*label*/
      1 | E[1] & /*$$scope*/
      4096 && (g.$$scope = { dirty: E, ctx: _ }), n.$set(g), E[0] & /*i18n, selected_indices, remove_selected_choice, disabled, choices_names*/
      561680) {
        p = Ui(
          /*selected_indices*/
          _[12]
        );
        let A;
        for (A = 0; A < p.length; A += 1) {
          const k = ji(_, p, A);
          m[A] ? (m[A].p(k, E), Q(m[A], 1)) : (m[A] = Vi(k), m[A].c(), Q(m[A], 1), m[A].m(r, a));
        }
        for (Ft(), A = p.length; A < m.length; A += 1)
          v(A);
        Gt();
      }
      (!b || E[0] & /*disabled*/
      16) && (o.disabled = /*disabled*/
      _[4]), (!b || E[0] & /*filterable*/
      256 && u !== (u = !/*filterable*/
      _[8])) && (o.readOnly = u), E[0] & /*input_text*/
      1024 && o.value !== /*input_text*/
      _[10] && Fi(
        o,
        /*input_text*/
        _[10]
      ), (!b || E[0] & /*choices_names, input_text, allow_custom_value, selected_indices, max_choices*/
      38020) && Fe(o, "subdued", !/*choices_names*/
      _[15].includes(
        /*input_text*/
        _[10]
      ) && !/*allow_custom_value*/
      _[7] || /*selected_indices*/
      _[12].length === /*max_choices*/
      _[2]), /*disabled*/
      _[4] ? c && (Ft(), le(c, 1, 1, () => {
        c = null;
      }), Gt()) : c ? (c.p(_, E), E[0] & /*disabled*/
      16 && Q(c, 1)) : (c = qi(_), c.c(), Q(c, 1), c.m(s, null)), (!b || E[0] & /*show_options*/
      16384) && Fe(
        r,
        "show_options",
        /*show_options*/
        _[14]
      );
      const P = {};
      E[0] & /*show_options*/
      16384 && (P.show_options = /*show_options*/
      _[14]), E[0] & /*choices*/
      8 && (P.choices = /*choices*/
      _[3]), E[0] & /*filtered_indices*/
      2048 && (P.filtered_indices = /*filtered_indices*/
      _[11]), E[0] & /*disabled*/
      16 && (P.disabled = /*disabled*/
      _[4]), E[0] & /*selected_indices*/
      4096 && (P.selected_indices = /*selected_indices*/
      _[12]), E[0] & /*active_index*/
      65536 && (P.active_index = /*active_index*/
      _[16]), d.$set(P), (!b || E[0] & /*container*/
      64) && Fe(
        t,
        "container",
        /*container*/
        _[6]
      );
    },
    i(_) {
      if (!b) {
        Q(n.$$.fragment, _);
        for (let E = 0; E < p.length; E += 1)
          Q(m[E]);
        Q(c), Q(d.$$.fragment, _), b = !0;
      }
    },
    o(_) {
      le(n.$$.fragment, _), m = m.filter(Boolean);
      for (let E = 0; E < m.length; E += 1)
        le(m[E]);
      le(c), le(d.$$.fragment, _), b = !1;
    },
    d(_) {
      _ && ye(t), dt(n), Uu(m, _), e[34](null), c && c.d(), dt(d), y = !1, Mn(w);
    }
  };
}
function Zu(e, t, n) {
  let { label: i } = t, { info: l = void 0 } = t, { value: r = [] } = t, a = [], { value_is_output: s = !1 } = t, { max_choices: o = null } = t, { choices: u } = t, f, { disabled: h = !1 } = t, { show_label: d } = t, { container: b = !0 } = t, { allow_custom_value: y = !1 } = t, { filterable: w = !0 } = t, { i18n: p } = t, m, v = "", c = "", _ = !1, E, g, P = [], A = null, k = [], q = [];
  const C = xu();
  Array.isArray(r) && r.forEach((S) => {
    const re = u.map((Qt) => Qt[1]).indexOf(S);
    re !== -1 ? k.push(re) : k.push(S);
  });
  function G() {
    y || n(10, v = ""), y && v !== "" && (W(v), n(10, v = "")), n(14, _ = !1), n(16, A = null), C("blur");
  }
  function z(S) {
    n(12, k = k.filter((re) => re !== S)), C("select", {
      index: typeof S == "number" ? S : -1,
      value: typeof S == "number" ? g[S] : S,
      selected: !1
    });
  }
  function W(S) {
    (o === null || k.length < o) && (n(12, k = [...k, S]), C("select", {
      index: typeof S == "number" ? S : -1,
      value: typeof S == "number" ? g[S] : S,
      selected: !0
    })), k.length === o && (n(14, _ = !1), n(16, A = null), m.blur());
  }
  function Y(S) {
    const re = parseInt(S.detail.target.dataset.index);
    pe(re);
  }
  function pe(S) {
    k.includes(S) ? z(S) : W(S), n(10, v = "");
  }
  function Ee(S) {
    n(12, k = []), n(10, v = ""), S.preventDefault();
  }
  function Se(S) {
    n(11, P = u.map((re, Qt) => Qt)), (o === null || k.length < o) && n(14, _ = !0), C("focus");
  }
  function T(S) {
    n(14, [_, A] = ol(S, A, P), _, (n(16, A), n(3, u), n(27, f), n(10, v), n(28, c), n(7, y), n(11, P))), S.key === "Enter" && (A !== null ? pe(A) : y && (W(v), n(10, v = ""))), S.key === "Backspace" && v === "" && n(12, k = [...k.slice(0, -1)]), k.length === o && (n(14, _ = !1), n(16, A = null));
  }
  function B() {
    r === void 0 ? n(12, k = []) : Array.isArray(r) && n(12, k = r.map((S) => {
      const re = g.indexOf(S);
      if (re !== -1)
        return re;
      if (y)
        return S;
    }).filter((S) => S !== void 0));
  }
  ju(() => {
    n(25, s = !1);
  });
  const K = (S) => z(S), U = (S, re) => {
    re.key === "Enter" && z(S);
  };
  function H() {
    v = this.value, n(10, v);
  }
  function F(S) {
    Du[S ? "unshift" : "push"](() => {
      m = S, n(13, m);
    });
  }
  const D = (S) => C("key_up", { key: S.key, input_value: v }), lt = (S) => {
    S.key === "Enter" && Ee(S);
  };
  return e.$$set = (S) => {
    "label" in S && n(0, i = S.label), "info" in S && n(1, l = S.info), "value" in S && n(24, r = S.value), "value_is_output" in S && n(25, s = S.value_is_output), "max_choices" in S && n(2, o = S.max_choices), "choices" in S && n(3, u = S.choices), "disabled" in S && n(4, h = S.disabled), "show_label" in S && n(5, d = S.show_label), "container" in S && n(6, b = S.container), "allow_custom_value" in S && n(7, y = S.allow_custom_value), "filterable" in S && n(8, w = S.filterable), "i18n" in S && n(9, p = S.i18n);
  }, e.$$.update = () => {
    e.$$.dirty[0] & /*choices*/
    8 && (n(15, E = u.map((S) => S[0])), n(29, g = u.map((S) => S[1]))), e.$$.dirty[0] & /*choices, old_choices, input_text, old_input_text, allow_custom_value, filtered_indices*/
    402656392 && (u !== f || v !== c) && (n(11, P = hn(u, v)), n(27, f = u), n(28, c = v), y || n(16, A = P[0])), e.$$.dirty[0] & /*selected_indices, old_selected_index, choices_values*/
    1610616832 && JSON.stringify(k) != JSON.stringify(q) && (n(24, r = k.map((S) => typeof S == "number" ? g[S] : S)), n(30, q = k.slice())), e.$$.dirty[0] & /*value, old_value, value_is_output*/
    117440512 && JSON.stringify(r) != JSON.stringify(a) && (sl(C, r, s), n(26, a = Array.isArray(r) ? r.slice() : r)), e.$$.dirty[0] & /*value*/
    16777216 && B();
  }, [
    i,
    l,
    o,
    u,
    h,
    d,
    b,
    y,
    w,
    p,
    v,
    P,
    k,
    m,
    _,
    E,
    A,
    C,
    G,
    z,
    Y,
    Ee,
    Se,
    T,
    r,
    s,
    a,
    f,
    c,
    g,
    q,
    K,
    U,
    H,
    F,
    D,
    lt
  ];
}
class mf extends Ru {
  constructor(t) {
    super(), Gu(
      this,
      t,
      Zu,
      zu,
      Fu,
      {
        label: 0,
        info: 1,
        value: 24,
        value_is_output: 25,
        max_choices: 2,
        choices: 3,
        disabled: 4,
        show_label: 5,
        container: 6,
        allow_custom_value: 7,
        filterable: 8,
        i18n: 9
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Wu,
  add_flush_callback: Qu,
  append: ee,
  assign: Ju,
  attr: X,
  bind: Yu,
  binding_callbacks: Ku,
  check_outros: jl,
  create_component: zt,
  destroy_component: Zt,
  detach: $e,
  element: _e,
  empty: $u,
  get_spread_object: ef,
  get_spread_update: tf,
  group_outros: xl,
  init: nf,
  insert: et,
  listen: Hn,
  mount_component: Wt,
  run_all: lf,
  safe_not_equal: rf,
  set_input_value: zi,
  space: Be,
  text: sf,
  transition_in: be,
  transition_out: Pe
} = window.__gradio__svelte__internal;
function Zi(e) {
  let t, n, i, l, r, a, s, o, u, f, h, d, b, y, w;
  function p(_) {
    e[19](_);
  }
  let m = {
    choices: (
      /*pipelines*/
      e[7]
    ),
    label: "Select the pipeline to use: ",
    info: (
      /*info*/
      e[3]
    ),
    show_label: (
      /*show_label*/
      e[8]
    ),
    container: (
      /*container*/
      e[10]
    ),
    disabled: !/*interactive*/
    e[15]
  };
  /*value_is_output*/
  e[2] !== void 0 && (m.value_is_output = /*value_is_output*/
  e[2]), s = new Fs({ props: m }), Ku.push(() => Yu(s, "value_is_output", p)), s.$on(
    "input",
    /*input_handler*/
    e[20]
  ), s.$on(
    "select",
    /*select_handler*/
    e[21]
  ), s.$on(
    "blur",
    /*blur_handler*/
    e[22]
  ), s.$on(
    "focus",
    /*focus_handler*/
    e[23]
  ), s.$on(
    "key_up",
    /*key_up_handler*/
    e[24]
  );
  let v = (
    /*enable_edition*/
    e[9] && Wi(e)
  ), c = (
    /*value*/
    e[0].name !== "" && Qi(e)
  );
  return {
    c() {
      t = _e("div"), n = _e("label"), n.textContent = "Enter your Hugging Face token:", i = Be(), l = _e("input"), a = Be(), zt(s.$$.fragment), u = Be(), v && v.c(), f = Be(), h = _e("div"), d = Be(), c && c.c(), X(n, "for", "token"), X(n, "class", "label svelte-1nstxj7"), X(l, "data-testid", "textbox"), X(l, "type", "text"), X(l, "class", "text-area svelte-1nstxj7"), X(l, "name", "token"), X(l, "id", "token"), X(l, "placeholder", "hf_xxxxxxx..."), X(l, "aria-label", "Enter your Hugging Face token"), X(l, "maxlength", "50"), l.disabled = r = !/*interactive*/
      e[15], X(h, "class", "params-control svelte-1nstxj7"), X(h, "id", "params-control"), X(t, "class", "form svelte-1nstxj7");
    },
    m(_, E) {
      et(_, t, E), ee(t, n), ee(t, i), ee(t, l), zi(
        l,
        /*value*/
        e[0].token
      ), ee(t, a), Wt(s, t, null), ee(t, u), v && v.m(t, null), ee(t, f), ee(t, h), ee(t, d), c && c.m(t, null), b = !0, y || (w = Hn(
        l,
        "input",
        /*input_input_handler*/
        e[18]
      ), y = !0);
    },
    p(_, E) {
      (!b || E[0] & /*interactive*/
      32768 && r !== (r = !/*interactive*/
      _[15])) && (l.disabled = r), E[0] & /*value*/
      1 && l.value !== /*value*/
      _[0].token && zi(
        l,
        /*value*/
        _[0].token
      );
      const g = {};
      E[0] & /*pipelines*/
      128 && (g.choices = /*pipelines*/
      _[7]), E[0] & /*info*/
      8 && (g.info = /*info*/
      _[3]), E[0] & /*show_label*/
      256 && (g.show_label = /*show_label*/
      _[8]), E[0] & /*container*/
      1024 && (g.container = /*container*/
      _[10]), E[0] & /*interactive*/
      32768 && (g.disabled = !/*interactive*/
      _[15]), !o && E[0] & /*value_is_output*/
      4 && (o = !0, g.value_is_output = /*value_is_output*/
      _[2], Qu(() => o = !1)), s.$set(g), /*enable_edition*/
      _[9] ? v ? v.p(_, E) : (v = Wi(_), v.c(), v.m(t, f)) : v && (v.d(1), v = null), /*value*/
      _[0].name !== "" ? c ? (c.p(_, E), E[0] & /*value*/
      1 && be(c, 1)) : (c = Qi(_), c.c(), be(c, 1), c.m(t, null)) : c && (xl(), Pe(c, 1, 1, () => {
        c = null;
      }), jl());
    },
    i(_) {
      b || (be(s.$$.fragment, _), be(c), b = !0);
    },
    o(_) {
      Pe(s.$$.fragment, _), Pe(c), b = !1;
    },
    d(_) {
      _ && $e(t), Zt(s), v && v.d(), c && c.d(), y = !1, w();
    }
  };
}
function Wi(e) {
  let t, n, i, l, r, a, s, o, u, f, h;
  return {
    c() {
      t = _e("div"), n = _e("p"), n.textContent = "Show configuration", i = Be(), l = _e("label"), r = _e("input"), s = Be(), o = _e("span"), X(r, "type", "checkbox"), r.disabled = a = /*value*/
      e[0].name == "", X(r, "class", "svelte-1nstxj7"), X(o, "class", "slider round svelte-1nstxj7"), X(l, "class", "switch svelte-1nstxj7"), X(l, "title", u = /*value*/
      e[0].name == "" ? "Please select a pipeline first" : "Show pipeline config"), X(t, "class", "toggle-config svelte-1nstxj7");
    },
    m(d, b) {
      et(d, t, b), ee(t, n), ee(t, i), ee(t, l), ee(l, r), r.checked = /*show_config*/
      e[1], ee(l, s), ee(l, o), f || (h = [
        Hn(
          r,
          "change",
          /*input_change_handler*/
          e[25]
        ),
        Hn(
          r,
          "input",
          /*input_handler_1*/
          e[26]
        )
      ], f = !0);
    },
    p(d, b) {
      b[0] & /*value*/
      1 && a !== (a = /*value*/
      d[0].name == "") && (r.disabled = a), b[0] & /*show_config*/
      2 && (r.checked = /*show_config*/
      d[1]), b[0] & /*value*/
      1 && u !== (u = /*value*/
      d[0].name == "" ? "Please select a pipeline first" : "Show pipeline config") && X(l, "title", u);
    },
    d(d) {
      d && $e(t), f = !1, lf(h);
    }
  };
}
function Qi(e) {
  let t, n, i;
  return n = new Fo({
    props: {
      elem_id: (
        /*elem_id*/
        e[4]
      ),
      elem_classes: (
        /*elem_classes*/
        e[5]
      ),
      scale: (
        /*scale*/
        e[11]
      ),
      min_width: (
        /*min_width*/
        e[12]
      ),
      visible: (
        /*show_config*/
        e[1]
      ),
      $$slots: { default: [of] },
      $$scope: { ctx: e }
    }
  }), n.$on(
    "click",
    /*click_handler*/
    e[27]
  ), {
    c() {
      t = _e("div"), zt(n.$$.fragment), X(t, "class", "validation svelte-1nstxj7");
    },
    m(l, r) {
      et(l, t, r), Wt(n, t, null), i = !0;
    },
    p(l, r) {
      const a = {};
      r[0] & /*elem_id*/
      16 && (a.elem_id = /*elem_id*/
      l[4]), r[0] & /*elem_classes*/
      32 && (a.elem_classes = /*elem_classes*/
      l[5]), r[0] & /*scale*/
      2048 && (a.scale = /*scale*/
      l[11]), r[0] & /*min_width*/
      4096 && (a.min_width = /*min_width*/
      l[12]), r[0] & /*show_config*/
      2 && (a.visible = /*show_config*/
      l[1]), r[1] & /*$$scope*/
      2 && (a.$$scope = { dirty: r, ctx: l }), n.$set(a);
    },
    i(l) {
      i || (be(n.$$.fragment, l), i = !0);
    },
    o(l) {
      Pe(n.$$.fragment, l), i = !1;
    },
    d(l) {
      l && $e(t), Zt(n);
    }
  };
}
function of(e) {
  let t;
  return {
    c() {
      t = sf("Update parameters");
    },
    m(n, i) {
      et(n, t, i);
    },
    d(n) {
      n && $e(t);
    }
  };
}
function af(e) {
  let t, n, i, l;
  const r = [
    {
      autoscroll: (
        /*gradio*/
        e[14].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      e[14].i18n
    ) },
    /*loading_status*/
    e[13]
  ];
  let a = {};
  for (let o = 0; o < r.length; o += 1)
    a = Ju(a, r[o]);
  t = new To({ props: a });
  let s = (
    /*visible*/
    e[6] && Zi(e)
  );
  return {
    c() {
      zt(t.$$.fragment), n = Be(), s && s.c(), i = $u();
    },
    m(o, u) {
      Wt(t, o, u), et(o, n, u), s && s.m(o, u), et(o, i, u), l = !0;
    },
    p(o, u) {
      const f = u[0] & /*gradio, loading_status*/
      24576 ? tf(r, [
        u[0] & /*gradio*/
        16384 && {
          autoscroll: (
            /*gradio*/
            o[14].autoscroll
          )
        },
        u[0] & /*gradio*/
        16384 && { i18n: (
          /*gradio*/
          o[14].i18n
        ) },
        u[0] & /*loading_status*/
        8192 && ef(
          /*loading_status*/
          o[13]
        )
      ]) : {};
      t.$set(f), /*visible*/
      o[6] ? s ? (s.p(o, u), u[0] & /*visible*/
      64 && be(s, 1)) : (s = Zi(o), s.c(), be(s, 1), s.m(i.parentNode, i)) : s && (xl(), Pe(s, 1, 1, () => {
        s = null;
      }), jl());
    },
    i(o) {
      l || (be(t.$$.fragment, o), be(s), l = !0);
    },
    o(o) {
      Pe(t.$$.fragment, o), Pe(s), l = !1;
    },
    d(o) {
      o && ($e(n), $e(i)), Zt(t, o), s && s.d(o);
    }
  };
}
function uf(e) {
  let t, n;
  return t = new Br({
    props: {
      visible: (
        /*visible*/
        e[6]
      ),
      elem_id: (
        /*elem_id*/
        e[4]
      ),
      elem_classes: (
        /*elem_classes*/
        e[5]
      ),
      padding: (
        /*container*/
        e[10]
      ),
      allow_overflow: !1,
      scale: (
        /*scale*/
        e[11]
      ),
      min_width: (
        /*min_width*/
        e[12]
      ),
      $$slots: { default: [af] },
      $$scope: { ctx: e }
    }
  }), {
    c() {
      zt(t.$$.fragment);
    },
    m(i, l) {
      Wt(t, i, l), n = !0;
    },
    p(i, l) {
      const r = {};
      l[0] & /*visible*/
      64 && (r.visible = /*visible*/
      i[6]), l[0] & /*elem_id*/
      16 && (r.elem_id = /*elem_id*/
      i[4]), l[0] & /*elem_classes*/
      32 && (r.elem_classes = /*elem_classes*/
      i[5]), l[0] & /*container*/
      1024 && (r.padding = /*container*/
      i[10]), l[0] & /*scale*/
      2048 && (r.scale = /*scale*/
      i[11]), l[0] & /*min_width*/
      4096 && (r.min_width = /*min_width*/
      i[12]), l[0] & /*elem_id, elem_classes, scale, min_width, show_config, gradio, value, paramsViewNeedUpdate, enable_edition, pipelines, info, show_label, container, interactive, value_is_output, visible, loading_status*/
      131071 | l[1] & /*$$scope*/
      2 && (r.$$scope = { dirty: l, ctx: i }), t.$set(r);
    },
    i(i) {
      n || (be(t.$$.fragment, i), n = !0);
    },
    o(i) {
      Pe(t.$$.fragment, i), n = !1;
    },
    d(i) {
      Zt(t, i);
    }
  };
}
function Bn(e) {
  const t = /* @__PURE__ */ new Map();
  if (!e)
    return t;
  for (const n in e)
    e.hasOwnProperty(n) && (typeof e[n] == "object" && e[n] !== null ? t.set(n, Bn(e[n])) : t.set(n, e[n]));
  return t;
}
function Vl(e) {
  return Object.fromEntries(Array.from(e.entries(), ([n, i]) => i instanceof Map ? [n, Vl(i)] : [n, i]));
}
function kn(e, t) {
  const n = document.createElement("label");
  n.textContent = t, e.appendChild(n);
}
function ff(e, t, n) {
  const i = document.createElement("input"), l = e.id;
  kn(e, l.split("-").at(-1)), i.type = "number", i.value = t, i.contentEditable = String(n), e.appendChild(i);
}
function cf(e, t, n) {
  let { info: i = void 0 } = t, { elem_id: l = "" } = t, { elem_classes: r = [] } = t, { visible: a = !0 } = t, { value: s = new Ao({ name: "", token: "" }) } = t, { value_is_output: o = !1 } = t, { pipelines: u } = t, { show_label: f } = t, { show_config: h = !1 } = t, { enable_edition: d = !1 } = t, { container: b = !0 } = t, { scale: y = null } = t, { min_width: w = void 0 } = t, { loading_status: p } = t, { gradio: m } = t, { interactive: v } = t, c = !1;
  function _(T) {
    T !== "" && (n(0, s.name = T, s), n(0, s.param_specs = {}, s), m.dispatch("select", s), n(16, c = !0));
  }
  function E(T, B) {
    const K = T.split("-");
    let U = Bn(s.param_specs);
    var H = U;
    K.forEach((F) => {
      H = H.get(F);
    }), H.set("value", B), n(0, s.param_specs = Vl(U), s);
  }
  function g(T, B, K) {
    const U = document.createElement("select"), H = T.id;
    kn(T, H.split("-").at(-1)), B.forEach((F) => {
      const D = document.createElement("option");
      D.textContent = F, D.value = F, U.appendChild(D), F === K && (D.selected = !0);
    }), U.addEventListener("change", (F) => {
      E(H, U.value);
    }), T.appendChild(U);
  }
  function P(T, B, K, U, H) {
    const F = document.createElement("input"), D = document.createElement("input"), lt = T.id;
    kn(T, lt.split("-").at(-1)), F.type = "range", F.min = B, F.max = K, F.value = U, F.step = H, F.addEventListener("input", (S) => {
      D.value = F.value, E(lt, F.value);
    }), T.appendChild(F), D.type = "number", D.min = B, D.max = K, D.value = U, D.step = H, D.contentEditable = "true", D.addEventListener("input", (S) => {
      F.value = D.value, E(lt, F.value);
    }), T.appendChild(D);
  }
  function A(T, B, K) {
    B.forEach((U, H) => {
      const F = (K ? K + "-" : "") + H;
      if (U.values().next().value instanceof Map) {
        const D = document.createElement("fieldset");
        D.innerHTML = "<legend>" + F + "<legend>", D.id = F, T.appendChild(D), A(D, U, H);
      } else {
        const D = document.createElement("div");
        switch (D.id = F, D.classList.add("param"), T.appendChild(D), U.get("component")) {
          case "slider":
            P(D, U.get("min"), U.get("max"), U.get("value"), U.get("step"));
            break;
          case "dropdown":
            g(D, U.get("choices"), U.get("value"));
            break;
          case "textbox":
            ff(D, U.get("value"), !1);
            break;
        }
      }
    });
  }
  function k() {
    s.token = this.value, n(0, s);
  }
  function q(T) {
    o = T, n(2, o);
  }
  const C = () => m.dispatch("input"), G = (T) => _(T.detail.value), z = () => m.dispatch("blur"), W = () => m.dispatch("focus"), Y = (T) => m.dispatch("key_up", T.detail);
  function pe() {
    h = this.checked, n(1, h);
  }
  const Ee = () => {
    n(16, c = !0), n(1, h = !h);
  }, Se = () => m.dispatch("change", s);
  return e.$$set = (T) => {
    "info" in T && n(3, i = T.info), "elem_id" in T && n(4, l = T.elem_id), "elem_classes" in T && n(5, r = T.elem_classes), "visible" in T && n(6, a = T.visible), "value" in T && n(0, s = T.value), "value_is_output" in T && n(2, o = T.value_is_output), "pipelines" in T && n(7, u = T.pipelines), "show_label" in T && n(8, f = T.show_label), "show_config" in T && n(1, h = T.show_config), "enable_edition" in T && n(9, d = T.enable_edition), "container" in T && n(10, b = T.container), "scale" in T && n(11, y = T.scale), "min_width" in T && n(12, w = T.min_width), "loading_status" in T && n(13, p = T.loading_status), "gradio" in T && n(14, m = T.gradio), "interactive" in T && n(15, v = T.interactive);
  }, e.$$.update = () => {
    if (e.$$.dirty[0] & /*value, paramsViewNeedUpdate, show_config*/
    65539 && Object.keys(s.param_specs).length > 0 && c) {
      const T = document.getElementById("params-control");
      if (T.replaceChildren(), h) {
        let B = Bn(s.param_specs);
        A(T, B), n(16, c = !1);
      }
    }
  }, [
    s,
    h,
    o,
    i,
    l,
    r,
    a,
    u,
    f,
    d,
    b,
    y,
    w,
    p,
    m,
    v,
    c,
    _,
    k,
    q,
    C,
    G,
    z,
    W,
    Y,
    pe,
    Ee,
    Se
  ];
}
class df extends Wu {
  constructor(t) {
    super(), nf(
      this,
      t,
      cf,
      uf,
      rf,
      {
        info: 3,
        elem_id: 4,
        elem_classes: 5,
        visible: 6,
        value: 0,
        value_is_output: 2,
        pipelines: 7,
        show_label: 8,
        show_config: 1,
        enable_edition: 9,
        container: 10,
        scale: 11,
        min_width: 12,
        loading_status: 13,
        gradio: 14,
        interactive: 15
      },
      null,
      [-1, -1]
    );
  }
}
export {
  Fs as BaseDropdown,
  _f as BaseExample,
  mf as BaseMultiselect,
  df as default
};
