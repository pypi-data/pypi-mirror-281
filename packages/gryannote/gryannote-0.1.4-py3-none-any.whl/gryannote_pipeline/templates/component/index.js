function st() {
}
function hn(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
function Jt(l) {
  const e = typeof l == "string" && l.match(/^\s*(-?[\d.]+)([^\s]*)\s*$/);
  return e ? [parseFloat(e[1]), e[2] || "px"] : [
    /** @type {number} */
    l,
    "px"
  ];
}
const Hl = typeof window < "u";
let Rt = Hl ? () => window.performance.now() : () => Date.now(), Jl = Hl ? (l) => requestAnimationFrame(l) : st;
const Ze = /* @__PURE__ */ new Set();
function Rl(l) {
  Ze.forEach((e) => {
    e.c(l) || (Ze.delete(e), e.f());
  }), Ze.size !== 0 && Jl(Rl);
}
function gn(l) {
  let e;
  return Ze.size === 0 && Jl(Rl), {
    promise: new Promise((t) => {
      Ze.add(e = { c: l, f: t });
    }),
    abort() {
      Ze.delete(e);
    }
  };
}
function wn(l) {
  const e = l - 1;
  return e * e * e + 1;
}
function Xt(l, { delay: e = 0, duration: t = 400, easing: n = wn, x: i = 0, y: f = 0, opacity: u = 0 } = {}) {
  const o = getComputedStyle(l), s = +o.opacity, r = o.transform === "none" ? "" : o.transform, a = s * (1 - u), [d, k] = Jt(i), [h, C] = Jt(f);
  return {
    delay: e,
    duration: t,
    easing: n,
    css: (y, b) => `
			transform: ${r} translate(${(1 - y) * d}${k}, ${(1 - y) * h}${C});
			opacity: ${s - a * b}`
  };
}
const Le = [];
function pn(l, e = st) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(o) {
    if (hn(l, o) && (l = o, t)) {
      const s = !Le.length;
      for (const r of n)
        r[1](), Le.push(r, l);
      if (s) {
        for (let r = 0; r < Le.length; r += 2)
          Le[r][0](Le[r + 1]);
        Le.length = 0;
      }
    }
  }
  function f(o) {
    i(o(l));
  }
  function u(o, s = st) {
    const r = [o, s];
    return n.add(r), n.size === 1 && (t = e(i, f) || st), o(l), () => {
      n.delete(r), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: f, subscribe: u };
}
function Yt(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function Ft(l, e, t, n) {
  if (typeof t == "number" || Yt(t)) {
    const i = n - t, f = (t - e) / (l.dt || 1 / 60), u = l.opts.stiffness * i, o = l.opts.damping * f, s = (u - o) * l.inv_mass, r = (f + s) * l.dt;
    return Math.abs(r) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, Yt(t) ? new Date(t.getTime() + r) : t + r);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, f) => Ft(l, e[f], t[f], n[f])
      );
    if (typeof t == "object") {
      const i = {};
      for (const f in t)
        i[f] = Ft(l, e[f], t[f], n[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Gt(l, e = {}) {
  const t = pn(l), { stiffness: n = 0.15, damping: i = 0.8, precision: f = 0.01 } = e;
  let u, o, s, r = l, a = l, d = 1, k = 0, h = !1;
  function C(b, m = {}) {
    a = b;
    const w = s = {};
    return l == null || m.hard || y.stiffness >= 1 && y.damping >= 1 ? (h = !0, u = Rt(), r = b, t.set(l = a), Promise.resolve()) : (m.soft && (k = 1 / ((m.soft === !0 ? 0.5 : +m.soft) * 60), d = 0), o || (u = Rt(), h = !1, o = gn((_) => {
      if (h)
        return h = !1, o = null, !1;
      d = Math.min(d + k, 1);
      const c = {
        inv_mass: d,
        opts: y,
        settled: !0,
        dt: (_ - u) * 60 / 1e3
      }, v = Ft(c, r, l, a);
      return u = _, r = l, t.set(l = v), c.settled && (o = null), !c.settled;
    })), new Promise((_) => {
      o.promise.then(() => {
        w === s && _();
      });
    }));
  }
  const y = {
    set: C,
    update: (b, m) => C(b(a, l), m),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: f
  };
  return y;
}
const {
  SvelteComponent: kn,
  add_render_callback: Xl,
  append: lt,
  attr: x,
  binding_callbacks: Kt,
  check_outros: vn,
  create_bidirectional_transition: Qt,
  destroy_each: yn,
  detach: Ke,
  element: rt,
  empty: jn,
  ensure_array_like: Wt,
  group_outros: Cn,
  init: qn,
  insert: Qe,
  listen: Lt,
  prevent_default: Sn,
  run_all: En,
  safe_not_equal: Fn,
  set_data: Ln,
  set_style: ve,
  space: Nt,
  text: Nn,
  toggle_class: oe,
  transition_in: yt,
  transition_out: xt
} = window.__gradio__svelte__internal, { createEventDispatcher: zn } = window.__gradio__svelte__internal;
function $t(l, e, t) {
  const n = l.slice();
  return n[26] = e[t], n;
}
function el(l) {
  let e, t, n, i, f, u = Wt(
    /*filtered_indices*/
    l[1]
  ), o = [];
  for (let s = 0; s < u.length; s += 1)
    o[s] = tl($t(l, u, s));
  return {
    c() {
      e = rt("ul");
      for (let s = 0; s < o.length; s += 1)
        o[s].c();
      x(e, "class", "options svelte-yuohum"), x(e, "role", "listbox"), ve(
        e,
        "top",
        /*top*/
        l[9]
      ), ve(
        e,
        "bottom",
        /*bottom*/
        l[10]
      ), ve(e, "max-height", `calc(${/*max_height*/
      l[11]}px - var(--window-padding))`), ve(
        e,
        "width",
        /*input_width*/
        l[8] + "px"
      );
    },
    m(s, r) {
      Qe(s, e, r);
      for (let a = 0; a < o.length; a += 1)
        o[a] && o[a].m(e, null);
      l[23](e), n = !0, i || (f = Lt(e, "mousedown", Sn(
        /*mousedown_handler*/
        l[22]
      )), i = !0);
    },
    p(s, r) {
      if (r & /*filtered_indices, choices, selected_indices, active_index*/
      51) {
        u = Wt(
          /*filtered_indices*/
          s[1]
        );
        let a;
        for (a = 0; a < u.length; a += 1) {
          const d = $t(s, u, a);
          o[a] ? o[a].p(d, r) : (o[a] = tl(d), o[a].c(), o[a].m(e, null));
        }
        for (; a < o.length; a += 1)
          o[a].d(1);
        o.length = u.length;
      }
      r & /*top*/
      512 && ve(
        e,
        "top",
        /*top*/
        s[9]
      ), r & /*bottom*/
      1024 && ve(
        e,
        "bottom",
        /*bottom*/
        s[10]
      ), r & /*max_height*/
      2048 && ve(e, "max-height", `calc(${/*max_height*/
      s[11]}px - var(--window-padding))`), r & /*input_width*/
      256 && ve(
        e,
        "width",
        /*input_width*/
        s[8] + "px"
      );
    },
    i(s) {
      n || (s && Xl(() => {
        n && (t || (t = Qt(e, Xt, { duration: 200, y: 5 }, !0)), t.run(1));
      }), n = !0);
    },
    o(s) {
      s && (t || (t = Qt(e, Xt, { duration: 200, y: 5 }, !1)), t.run(0)), n = !1;
    },
    d(s) {
      s && Ke(e), yn(o, s), l[23](null), s && t && t.end(), i = !1, f();
    }
  };
}
function tl(l) {
  let e, t, n, i = (
    /*choices*/
    l[0][
      /*index*/
      l[26]
    ][0] + ""
  ), f, u, o, s, r;
  return {
    c() {
      e = rt("li"), t = rt("span"), t.textContent = "✓", n = Nt(), f = Nn(i), u = Nt(), x(t, "class", "inner-item svelte-yuohum"), oe(t, "hide", !/*selected_indices*/
      l[4].includes(
        /*index*/
        l[26]
      )), x(e, "class", "item svelte-yuohum"), x(e, "data-index", o = /*index*/
      l[26]), x(e, "aria-label", s = /*choices*/
      l[0][
        /*index*/
        l[26]
      ][0]), x(e, "data-testid", "dropdown-option"), x(e, "role", "option"), x(e, "aria-selected", r = /*selected_indices*/
      l[4].includes(
        /*index*/
        l[26]
      )), oe(
        e,
        "selected",
        /*selected_indices*/
        l[4].includes(
          /*index*/
          l[26]
        )
      ), oe(
        e,
        "active",
        /*index*/
        l[26] === /*active_index*/
        l[5]
      ), oe(
        e,
        "bg-gray-100",
        /*index*/
        l[26] === /*active_index*/
        l[5]
      ), oe(
        e,
        "dark:bg-gray-600",
        /*index*/
        l[26] === /*active_index*/
        l[5]
      );
    },
    m(a, d) {
      Qe(a, e, d), lt(e, t), lt(e, n), lt(e, f), lt(e, u);
    },
    p(a, d) {
      d & /*selected_indices, filtered_indices*/
      18 && oe(t, "hide", !/*selected_indices*/
      a[4].includes(
        /*index*/
        a[26]
      )), d & /*choices, filtered_indices*/
      3 && i !== (i = /*choices*/
      a[0][
        /*index*/
        a[26]
      ][0] + "") && Ln(f, i), d & /*filtered_indices*/
      2 && o !== (o = /*index*/
      a[26]) && x(e, "data-index", o), d & /*choices, filtered_indices*/
      3 && s !== (s = /*choices*/
      a[0][
        /*index*/
        a[26]
      ][0]) && x(e, "aria-label", s), d & /*selected_indices, filtered_indices*/
      18 && r !== (r = /*selected_indices*/
      a[4].includes(
        /*index*/
        a[26]
      )) && x(e, "aria-selected", r), d & /*selected_indices, filtered_indices*/
      18 && oe(
        e,
        "selected",
        /*selected_indices*/
        a[4].includes(
          /*index*/
          a[26]
        )
      ), d & /*filtered_indices, active_index*/
      34 && oe(
        e,
        "active",
        /*index*/
        a[26] === /*active_index*/
        a[5]
      ), d & /*filtered_indices, active_index*/
      34 && oe(
        e,
        "bg-gray-100",
        /*index*/
        a[26] === /*active_index*/
        a[5]
      ), d & /*filtered_indices, active_index*/
      34 && oe(
        e,
        "dark:bg-gray-600",
        /*index*/
        a[26] === /*active_index*/
        a[5]
      );
    },
    d(a) {
      a && Ke(e);
    }
  };
}
function Mn(l) {
  let e, t, n, i, f;
  Xl(
    /*onwindowresize*/
    l[20]
  );
  let u = (
    /*show_options*/
    l[2] && !/*disabled*/
    l[3] && el(l)
  );
  return {
    c() {
      e = rt("div"), t = Nt(), u && u.c(), n = jn(), x(e, "class", "reference");
    },
    m(o, s) {
      Qe(o, e, s), l[21](e), Qe(o, t, s), u && u.m(o, s), Qe(o, n, s), i || (f = [
        Lt(
          window,
          "scroll",
          /*scroll_listener*/
          l[13]
        ),
        Lt(
          window,
          "resize",
          /*onwindowresize*/
          l[20]
        )
      ], i = !0);
    },
    p(o, [s]) {
      /*show_options*/
      o[2] && !/*disabled*/
      o[3] ? u ? (u.p(o, s), s & /*show_options, disabled*/
      12 && yt(u, 1)) : (u = el(o), u.c(), yt(u, 1), u.m(n.parentNode, n)) : u && (Cn(), xt(u, 1, 1, () => {
        u = null;
      }), vn());
    },
    i(o) {
      yt(u);
    },
    o(o) {
      xt(u);
    },
    d(o) {
      o && (Ke(e), Ke(t), Ke(n)), l[21](null), u && u.d(o), i = !1, En(f);
    }
  };
}
function On(l, e, t) {
  var n, i;
  let { choices: f } = e, { filtered_indices: u } = e, { show_options: o = !1 } = e, { disabled: s = !1 } = e, { selected_indices: r = [] } = e, { active_index: a = null } = e, d, k, h, C, y, b, m, w, _, c;
  function v() {
    const { top: N, bottom: J } = y.getBoundingClientRect();
    t(17, d = N), t(18, k = c - J);
  }
  let g = null;
  function F() {
    o && (g !== null && clearTimeout(g), g = setTimeout(
      () => {
        v(), g = null;
      },
      10
    ));
  }
  const j = zn();
  function L() {
    t(12, c = window.innerHeight);
  }
  function U(N) {
    Kt[N ? "unshift" : "push"](() => {
      y = N, t(6, y);
    });
  }
  const Z = (N) => j("change", N);
  function ee(N) {
    Kt[N ? "unshift" : "push"](() => {
      b = N, t(7, b);
    });
  }
  return l.$$set = (N) => {
    "choices" in N && t(0, f = N.choices), "filtered_indices" in N && t(1, u = N.filtered_indices), "show_options" in N && t(2, o = N.show_options), "disabled" in N && t(3, s = N.disabled), "selected_indices" in N && t(4, r = N.selected_indices), "active_index" in N && t(5, a = N.active_index);
  }, l.$$.update = () => {
    if (l.$$.dirty & /*show_options, refElement, listElement, selected_indices, _a, _b, distance_from_bottom, distance_from_top, input_height*/
    1016020) {
      if (o && y) {
        if (b && r.length > 0) {
          let J = b.querySelectorAll("li");
          for (const R of Array.from(J))
            if (R.getAttribute("data-index") === r[0].toString()) {
              t(15, n = b?.scrollTo) === null || n === void 0 || n.call(b, 0, R.offsetTop);
              break;
            }
        }
        v();
        const N = t(16, i = y.parentElement) === null || i === void 0 ? void 0 : i.getBoundingClientRect();
        t(19, h = N?.height || 0), t(8, C = N?.width || 0);
      }
      k > d ? (t(9, m = `${d}px`), t(11, _ = k), t(10, w = null)) : (t(10, w = `${k + h}px`), t(11, _ = d - h), t(9, m = null));
    }
  }, [
    f,
    u,
    o,
    s,
    r,
    a,
    y,
    b,
    C,
    m,
    w,
    _,
    c,
    F,
    j,
    n,
    i,
    d,
    k,
    h,
    L,
    U,
    Z,
    ee
  ];
}
class Yl extends kn {
  constructor(e) {
    super(), qn(this, e, On, Mn, Fn, {
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
  SvelteComponent: An,
  assign: Vn,
  create_slot: Dn,
  detach: Bn,
  element: Tn,
  get_all_dirty_from_scope: Un,
  get_slot_changes: Zn,
  get_spread_update: Pn,
  init: In,
  insert: Hn,
  safe_not_equal: Jn,
  set_dynamic_element_data: ll,
  set_style: Q,
  toggle_class: ye,
  transition_in: Gl,
  transition_out: Kl,
  update_slot_base: Rn
} = window.__gradio__svelte__internal;
function Xn(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), f = Dn(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let u = [
    { "data-testid": (
      /*test_id*/
      l[7]
    ) },
    { id: (
      /*elem_id*/
      l[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      l[3].join(" ") + " svelte-1t38q2d"
    }
  ], o = {};
  for (let s = 0; s < u.length; s += 1)
    o = Vn(o, u[s]);
  return {
    c() {
      e = Tn(
        /*tag*/
        l[14]
      ), f && f.c(), ll(
        /*tag*/
        l[14]
      )(e, o), ye(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), ye(
        e,
        "padded",
        /*padding*/
        l[6]
      ), ye(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), ye(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), Q(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), Q(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), Q(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), Q(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), Q(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), Q(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), Q(e, "border-width", "var(--block-border-width)");
    },
    m(s, r) {
      Hn(s, e, r), f && f.m(e, null), n = !0;
    },
    p(s, r) {
      f && f.p && (!n || r & /*$$scope*/
      131072) && Rn(
        f,
        i,
        s,
        /*$$scope*/
        s[17],
        n ? Zn(
          i,
          /*$$scope*/
          s[17],
          r,
          null
        ) : Un(
          /*$$scope*/
          s[17]
        ),
        null
      ), ll(
        /*tag*/
        s[14]
      )(e, o = Pn(u, [
        (!n || r & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          s[7]
        ) },
        (!n || r & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          s[2]
        ) },
        (!n || r & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        s[3].join(" ") + " svelte-1t38q2d")) && { class: t }
      ])), ye(
        e,
        "hidden",
        /*visible*/
        s[10] === !1
      ), ye(
        e,
        "padded",
        /*padding*/
        s[6]
      ), ye(
        e,
        "border_focus",
        /*border_mode*/
        s[5] === "focus"
      ), ye(e, "hide-container", !/*explicit_call*/
      s[8] && !/*container*/
      s[9]), r & /*height*/
      1 && Q(
        e,
        "height",
        /*get_dimension*/
        s[15](
          /*height*/
          s[0]
        )
      ), r & /*width*/
      2 && Q(e, "width", typeof /*width*/
      s[1] == "number" ? `calc(min(${/*width*/
      s[1]}px, 100%))` : (
        /*get_dimension*/
        s[15](
          /*width*/
          s[1]
        )
      )), r & /*variant*/
      16 && Q(
        e,
        "border-style",
        /*variant*/
        s[4]
      ), r & /*allow_overflow*/
      2048 && Q(
        e,
        "overflow",
        /*allow_overflow*/
        s[11] ? "visible" : "hidden"
      ), r & /*scale*/
      4096 && Q(
        e,
        "flex-grow",
        /*scale*/
        s[12]
      ), r & /*min_width*/
      8192 && Q(e, "min-width", `calc(min(${/*min_width*/
      s[13]}px, 100%))`);
    },
    i(s) {
      n || (Gl(f, s), n = !0);
    },
    o(s) {
      Kl(f, s), n = !1;
    },
    d(s) {
      s && Bn(e), f && f.d(s);
    }
  };
}
function Yn(l) {
  let e, t = (
    /*tag*/
    l[14] && Xn(l)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (Gl(t, n), e = !0);
    },
    o(n) {
      Kl(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function Gn(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: f = void 0 } = e, { width: u = void 0 } = e, { elem_id: o = "" } = e, { elem_classes: s = [] } = e, { variant: r = "solid" } = e, { border_mode: a = "base" } = e, { padding: d = !0 } = e, { type: k = "normal" } = e, { test_id: h = void 0 } = e, { explicit_call: C = !1 } = e, { container: y = !0 } = e, { visible: b = !0 } = e, { allow_overflow: m = !0 } = e, { scale: w = null } = e, { min_width: _ = 0 } = e, c = k === "fieldset" ? "fieldset" : "div";
  const v = (g) => {
    if (g !== void 0) {
      if (typeof g == "number")
        return g + "px";
      if (typeof g == "string")
        return g;
    }
  };
  return l.$$set = (g) => {
    "height" in g && t(0, f = g.height), "width" in g && t(1, u = g.width), "elem_id" in g && t(2, o = g.elem_id), "elem_classes" in g && t(3, s = g.elem_classes), "variant" in g && t(4, r = g.variant), "border_mode" in g && t(5, a = g.border_mode), "padding" in g && t(6, d = g.padding), "type" in g && t(16, k = g.type), "test_id" in g && t(7, h = g.test_id), "explicit_call" in g && t(8, C = g.explicit_call), "container" in g && t(9, y = g.container), "visible" in g && t(10, b = g.visible), "allow_overflow" in g && t(11, m = g.allow_overflow), "scale" in g && t(12, w = g.scale), "min_width" in g && t(13, _ = g.min_width), "$$scope" in g && t(17, i = g.$$scope);
  }, [
    f,
    u,
    o,
    s,
    r,
    a,
    d,
    h,
    C,
    y,
    b,
    m,
    w,
    _,
    c,
    v,
    k,
    i,
    n
  ];
}
class Kn extends An {
  constructor(e) {
    super(), In(this, e, Gn, Yn, Jn, {
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
  SvelteComponent: Qn,
  attr: Wn,
  create_slot: xn,
  detach: $n,
  element: ei,
  get_all_dirty_from_scope: ti,
  get_slot_changes: li,
  init: ni,
  insert: ii,
  safe_not_equal: si,
  transition_in: oi,
  transition_out: fi,
  update_slot_base: ui
} = window.__gradio__svelte__internal;
function ri(l) {
  let e, t;
  const n = (
    /*#slots*/
    l[1].default
  ), i = xn(
    n,
    l,
    /*$$scope*/
    l[0],
    null
  );
  return {
    c() {
      e = ei("div"), i && i.c(), Wn(e, "class", "svelte-1hnfib2");
    },
    m(f, u) {
      ii(f, e, u), i && i.m(e, null), t = !0;
    },
    p(f, [u]) {
      i && i.p && (!t || u & /*$$scope*/
      1) && ui(
        i,
        n,
        f,
        /*$$scope*/
        f[0],
        t ? li(
          n,
          /*$$scope*/
          f[0],
          u,
          null
        ) : ti(
          /*$$scope*/
          f[0]
        ),
        null
      );
    },
    i(f) {
      t || (oi(i, f), t = !0);
    },
    o(f) {
      fi(i, f), t = !1;
    },
    d(f) {
      f && $n(e), i && i.d(f);
    }
  };
}
function ai(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  return l.$$set = (f) => {
    "$$scope" in f && t(0, i = f.$$scope);
  }, [i, n];
}
class _i extends Qn {
  constructor(e) {
    super(), ni(this, e, ai, ri, si, {});
  }
}
const {
  SvelteComponent: ci,
  attr: nl,
  check_outros: di,
  create_component: mi,
  create_slot: bi,
  destroy_component: hi,
  detach: ot,
  element: gi,
  empty: wi,
  get_all_dirty_from_scope: pi,
  get_slot_changes: ki,
  group_outros: vi,
  init: yi,
  insert: ft,
  mount_component: ji,
  safe_not_equal: Ci,
  set_data: qi,
  space: Si,
  text: Ei,
  toggle_class: Ne,
  transition_in: Ye,
  transition_out: ut,
  update_slot_base: Fi
} = window.__gradio__svelte__internal;
function il(l) {
  let e, t;
  return e = new _i({
    props: {
      $$slots: { default: [Li] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      mi(e.$$.fragment);
    },
    m(n, i) {
      ji(e, n, i), t = !0;
    },
    p(n, i) {
      const f = {};
      i & /*$$scope, info*/
      10 && (f.$$scope = { dirty: i, ctx: n }), e.$set(f);
    },
    i(n) {
      t || (Ye(e.$$.fragment, n), t = !0);
    },
    o(n) {
      ut(e.$$.fragment, n), t = !1;
    },
    d(n) {
      hi(e, n);
    }
  };
}
function Li(l) {
  let e;
  return {
    c() {
      e = Ei(
        /*info*/
        l[1]
      );
    },
    m(t, n) {
      ft(t, e, n);
    },
    p(t, n) {
      n & /*info*/
      2 && qi(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && ot(e);
    }
  };
}
function Ni(l) {
  let e, t, n, i;
  const f = (
    /*#slots*/
    l[2].default
  ), u = bi(
    f,
    l,
    /*$$scope*/
    l[3],
    null
  );
  let o = (
    /*info*/
    l[1] && il(l)
  );
  return {
    c() {
      e = gi("span"), u && u.c(), t = Si(), o && o.c(), n = wi(), nl(e, "data-testid", "block-info"), nl(e, "class", "svelte-22c38v"), Ne(e, "sr-only", !/*show_label*/
      l[0]), Ne(e, "hide", !/*show_label*/
      l[0]), Ne(
        e,
        "has-info",
        /*info*/
        l[1] != null
      );
    },
    m(s, r) {
      ft(s, e, r), u && u.m(e, null), ft(s, t, r), o && o.m(s, r), ft(s, n, r), i = !0;
    },
    p(s, [r]) {
      u && u.p && (!i || r & /*$$scope*/
      8) && Fi(
        u,
        f,
        s,
        /*$$scope*/
        s[3],
        i ? ki(
          f,
          /*$$scope*/
          s[3],
          r,
          null
        ) : pi(
          /*$$scope*/
          s[3]
        ),
        null
      ), (!i || r & /*show_label*/
      1) && Ne(e, "sr-only", !/*show_label*/
      s[0]), (!i || r & /*show_label*/
      1) && Ne(e, "hide", !/*show_label*/
      s[0]), (!i || r & /*info*/
      2) && Ne(
        e,
        "has-info",
        /*info*/
        s[1] != null
      ), /*info*/
      s[1] ? o ? (o.p(s, r), r & /*info*/
      2 && Ye(o, 1)) : (o = il(s), o.c(), Ye(o, 1), o.m(n.parentNode, n)) : o && (vi(), ut(o, 1, 1, () => {
        o = null;
      }), di());
    },
    i(s) {
      i || (Ye(u, s), Ye(o), i = !0);
    },
    o(s) {
      ut(u, s), ut(o), i = !1;
    },
    d(s) {
      s && (ot(e), ot(t), ot(n)), u && u.d(s), o && o.d(s);
    }
  };
}
function zi(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { show_label: f = !0 } = e, { info: u = void 0 } = e;
  return l.$$set = (o) => {
    "show_label" in o && t(0, f = o.show_label), "info" in o && t(1, u = o.info), "$$scope" in o && t(3, i = o.$$scope);
  }, [f, u, n, i];
}
class Ql extends ci {
  constructor(e) {
    super(), yi(this, e, zi, Ni, Ci, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: Mi,
  append: Oi,
  attr: ze,
  detach: Ai,
  init: Vi,
  insert: Di,
  noop: jt,
  safe_not_equal: Bi,
  svg_element: sl
} = window.__gradio__svelte__internal;
function Ti(l) {
  let e, t;
  return {
    c() {
      e = sl("svg"), t = sl("path"), ze(t, "d", "M5 8l4 4 4-4z"), ze(e, "class", "dropdown-arrow svelte-145leq6"), ze(e, "xmlns", "http://www.w3.org/2000/svg"), ze(e, "width", "100%"), ze(e, "height", "100%"), ze(e, "viewBox", "0 0 18 18");
    },
    m(n, i) {
      Di(n, e, i), Oi(e, t);
    },
    p: jt,
    i: jt,
    o: jt,
    d(n) {
      n && Ai(e);
    }
  };
}
class Wl extends Mi {
  constructor(e) {
    super(), Vi(this, e, null, Ti, Bi, {});
  }
}
const {
  SvelteComponent: Ui,
  append: Zi,
  attr: Ct,
  detach: Pi,
  init: Ii,
  insert: Hi,
  noop: qt,
  safe_not_equal: Ji,
  svg_element: ol
} = window.__gradio__svelte__internal;
function Ri(l) {
  let e, t;
  return {
    c() {
      e = ol("svg"), t = ol("path"), Ct(t, "d", "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"), Ct(e, "xmlns", "http://www.w3.org/2000/svg"), Ct(e, "viewBox", "0 0 24 24");
    },
    m(n, i) {
      Hi(n, e, i), Zi(e, t);
    },
    p: qt,
    i: qt,
    o: qt,
    d(n) {
      n && Pi(e);
    }
  };
}
class xl extends Ui {
  constructor(e) {
    super(), Ii(this, e, null, Ri, Ji, {});
  }
}
const Xi = [
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
], fl = {
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
Xi.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: fl[e][t],
      secondary: fl[e][n]
    }
  }),
  {}
);
function Yi(l, e) {
  return (l % e + e) % e;
}
function zt(l, e) {
  return l.reduce((t, n, i) => ((!e || n[0].toLowerCase().includes(e.toLowerCase())) && t.push(i), t), []);
}
function $l(l, e, t) {
  l("change", e), t || l("input");
}
function en(l, e, t) {
  if (l.key === "Escape")
    return [!1, e];
  if ((l.key === "ArrowDown" || l.key === "ArrowUp") && t.length >= 0)
    if (e === null)
      e = l.key === "ArrowDown" ? t[0] : t[t.length - 1];
    else {
      const n = t.indexOf(e), i = l.key === "ArrowUp" ? -1 : 1;
      e = t[Yi(n + i, t.length)];
    }
  return [!0, e];
}
const {
  SvelteComponent: Gi,
  append: Ee,
  attr: W,
  binding_callbacks: Ki,
  check_outros: Qi,
  create_component: Mt,
  destroy_component: Ot,
  detach: Ut,
  element: Ve,
  group_outros: Wi,
  init: xi,
  insert: Zt,
  listen: Xe,
  mount_component: At,
  run_all: $i,
  safe_not_equal: es,
  set_data: ts,
  set_input_value: ul,
  space: St,
  text: ls,
  toggle_class: Me,
  transition_in: De,
  transition_out: Ge
} = window.__gradio__svelte__internal, { createEventDispatcher: ns, afterUpdate: is } = window.__gradio__svelte__internal;
function ss(l) {
  let e;
  return {
    c() {
      e = ls(
        /*label*/
        l[0]
      );
    },
    m(t, n) {
      Zt(t, e, n);
    },
    p(t, n) {
      n[0] & /*label*/
      1 && ts(
        e,
        /*label*/
        t[0]
      );
    },
    d(t) {
      t && Ut(e);
    }
  };
}
function rl(l) {
  let e, t, n;
  return t = new Wl({}), {
    c() {
      e = Ve("div"), Mt(t.$$.fragment), W(e, "class", "icon-wrap svelte-1m1zvyj");
    },
    m(i, f) {
      Zt(i, e, f), At(t, e, null), n = !0;
    },
    i(i) {
      n || (De(t.$$.fragment, i), n = !0);
    },
    o(i) {
      Ge(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && Ut(e), Ot(t);
    }
  };
}
function os(l) {
  let e, t, n, i, f, u, o, s, r, a, d, k, h, C;
  t = new Ql({
    props: {
      show_label: (
        /*show_label*/
        l[4]
      ),
      info: (
        /*info*/
        l[1]
      ),
      $$slots: { default: [ss] },
      $$scope: { ctx: l }
    }
  });
  let y = !/*disabled*/
  l[3] && rl();
  return d = new Yl({
    props: {
      show_options: (
        /*show_options*/
        l[12]
      ),
      choices: (
        /*choices*/
        l[2]
      ),
      filtered_indices: (
        /*filtered_indices*/
        l[10]
      ),
      disabled: (
        /*disabled*/
        l[3]
      ),
      selected_indices: (
        /*selected_index*/
        l[11] === null ? [] : [
          /*selected_index*/
          l[11]
        ]
      ),
      active_index: (
        /*active_index*/
        l[14]
      )
    }
  }), d.$on(
    "change",
    /*handle_option_selected*/
    l[16]
  ), {
    c() {
      e = Ve("div"), Mt(t.$$.fragment), n = St(), i = Ve("div"), f = Ve("div"), u = Ve("div"), o = Ve("input"), r = St(), y && y.c(), a = St(), Mt(d.$$.fragment), W(o, "role", "listbox"), W(o, "aria-controls", "dropdown-options"), W(
        o,
        "aria-expanded",
        /*show_options*/
        l[12]
      ), W(
        o,
        "aria-label",
        /*label*/
        l[0]
      ), W(o, "class", "border-none svelte-1m1zvyj"), o.disabled = /*disabled*/
      l[3], W(o, "autocomplete", "off"), o.readOnly = s = !/*filterable*/
      l[7], Me(o, "subdued", !/*choices_names*/
      l[13].includes(
        /*input_text*/
        l[9]
      ) && !/*allow_custom_value*/
      l[6]), W(u, "class", "secondary-wrap svelte-1m1zvyj"), W(f, "class", "wrap-inner svelte-1m1zvyj"), Me(
        f,
        "show_options",
        /*show_options*/
        l[12]
      ), W(i, "class", "wrap svelte-1m1zvyj"), W(e, "class", "svelte-1m1zvyj"), Me(
        e,
        "container",
        /*container*/
        l[5]
      );
    },
    m(b, m) {
      Zt(b, e, m), At(t, e, null), Ee(e, n), Ee(e, i), Ee(i, f), Ee(f, u), Ee(u, o), ul(
        o,
        /*input_text*/
        l[9]
      ), l[29](o), Ee(u, r), y && y.m(u, null), Ee(i, a), At(d, i, null), k = !0, h || (C = [
        Xe(
          o,
          "input",
          /*input_input_handler*/
          l[28]
        ),
        Xe(
          o,
          "keydown",
          /*handle_key_down*/
          l[19]
        ),
        Xe(
          o,
          "keyup",
          /*keyup_handler*/
          l[30]
        ),
        Xe(
          o,
          "blur",
          /*handle_blur*/
          l[18]
        ),
        Xe(
          o,
          "focus",
          /*handle_focus*/
          l[17]
        )
      ], h = !0);
    },
    p(b, m) {
      const w = {};
      m[0] & /*show_label*/
      16 && (w.show_label = /*show_label*/
      b[4]), m[0] & /*info*/
      2 && (w.info = /*info*/
      b[1]), m[0] & /*label*/
      1 | m[1] & /*$$scope*/
      4 && (w.$$scope = { dirty: m, ctx: b }), t.$set(w), (!k || m[0] & /*show_options*/
      4096) && W(
        o,
        "aria-expanded",
        /*show_options*/
        b[12]
      ), (!k || m[0] & /*label*/
      1) && W(
        o,
        "aria-label",
        /*label*/
        b[0]
      ), (!k || m[0] & /*disabled*/
      8) && (o.disabled = /*disabled*/
      b[3]), (!k || m[0] & /*filterable*/
      128 && s !== (s = !/*filterable*/
      b[7])) && (o.readOnly = s), m[0] & /*input_text*/
      512 && o.value !== /*input_text*/
      b[9] && ul(
        o,
        /*input_text*/
        b[9]
      ), (!k || m[0] & /*choices_names, input_text, allow_custom_value*/
      8768) && Me(o, "subdued", !/*choices_names*/
      b[13].includes(
        /*input_text*/
        b[9]
      ) && !/*allow_custom_value*/
      b[6]), /*disabled*/
      b[3] ? y && (Wi(), Ge(y, 1, 1, () => {
        y = null;
      }), Qi()) : y ? m[0] & /*disabled*/
      8 && De(y, 1) : (y = rl(), y.c(), De(y, 1), y.m(u, null)), (!k || m[0] & /*show_options*/
      4096) && Me(
        f,
        "show_options",
        /*show_options*/
        b[12]
      );
      const _ = {};
      m[0] & /*show_options*/
      4096 && (_.show_options = /*show_options*/
      b[12]), m[0] & /*choices*/
      4 && (_.choices = /*choices*/
      b[2]), m[0] & /*filtered_indices*/
      1024 && (_.filtered_indices = /*filtered_indices*/
      b[10]), m[0] & /*disabled*/
      8 && (_.disabled = /*disabled*/
      b[3]), m[0] & /*selected_index*/
      2048 && (_.selected_indices = /*selected_index*/
      b[11] === null ? [] : [
        /*selected_index*/
        b[11]
      ]), m[0] & /*active_index*/
      16384 && (_.active_index = /*active_index*/
      b[14]), d.$set(_), (!k || m[0] & /*container*/
      32) && Me(
        e,
        "container",
        /*container*/
        b[5]
      );
    },
    i(b) {
      k || (De(t.$$.fragment, b), De(y), De(d.$$.fragment, b), k = !0);
    },
    o(b) {
      Ge(t.$$.fragment, b), Ge(y), Ge(d.$$.fragment, b), k = !1;
    },
    d(b) {
      b && Ut(e), Ot(t), l[29](null), y && y.d(), Ot(d), h = !1, $i(C);
    }
  };
}
function fs(l, e, t) {
  let { label: n } = e, { info: i = void 0 } = e, { value: f = [] } = e, u = [], { value_is_output: o = !1 } = e, { choices: s } = e, r, { disabled: a = !1 } = e, { show_label: d } = e, { container: k = !0 } = e, { allow_custom_value: h = !1 } = e, { filterable: C = !0 } = e, y, b = !1, m, w, _ = "", c = "", v = !1, g = [], F = null, j = null, L;
  const U = ns();
  f ? (L = s.map((E) => E[1]).indexOf(f), j = L, j === -1 ? (u = f, j = null) : ([_, u] = s[j], c = _), ee()) : s.length > 0 && (L = 0, j = 0, [_, f] = s[j], u = f, c = _);
  function Z() {
    t(13, m = s.map((E) => E[0])), t(24, w = s.map((E) => E[1]));
  }
  function ee() {
    Z(), f === void 0 ? (t(9, _ = ""), t(11, j = null)) : w.includes(f) ? (t(9, _ = m[w.indexOf(f)]), t(11, j = w.indexOf(f))) : h ? (t(9, _ = f), t(11, j = null)) : (t(9, _ = ""), t(11, j = null)), t(27, L = j);
  }
  function N(E) {
    if (t(11, j = parseInt(E.detail.target.dataset.index)), isNaN(j)) {
      t(11, j = null);
      return;
    }
    t(12, b = !1), t(14, F = null), y.blur();
  }
  function J(E) {
    t(10, g = s.map((Y, V) => V)), t(12, b = !0), U("focus");
  }
  function R() {
    h ? t(20, f = _) : t(9, _ = m[w.indexOf(f)]), t(12, b = !1), t(14, F = null), U("blur");
  }
  function de(E) {
    t(12, [b, F] = en(E, F, g), b, (t(14, F), t(2, s), t(23, r), t(6, h), t(9, _), t(10, g), t(8, y), t(25, c), t(11, j), t(27, L), t(26, v), t(24, w))), E.key === "Enter" && (F !== null ? (t(11, j = F), t(12, b = !1), y.blur(), t(14, F = null)) : m.includes(_) ? (t(11, j = m.indexOf(_)), t(12, b = !1), t(14, F = null), y.blur()) : h && (t(20, f = _), t(11, j = null), t(12, b = !1), t(14, F = null), y.blur()));
  }
  is(() => {
    t(21, o = !1), t(26, v = !0);
  });
  function we() {
    _ = this.value, t(9, _), t(11, j), t(27, L), t(26, v), t(2, s), t(24, w);
  }
  function pe(E) {
    Ki[E ? "unshift" : "push"](() => {
      y = E, t(8, y);
    });
  }
  const q = (E) => U("key_up", { key: E.key, input_value: _ });
  return l.$$set = (E) => {
    "label" in E && t(0, n = E.label), "info" in E && t(1, i = E.info), "value" in E && t(20, f = E.value), "value_is_output" in E && t(21, o = E.value_is_output), "choices" in E && t(2, s = E.choices), "disabled" in E && t(3, a = E.disabled), "show_label" in E && t(4, d = E.show_label), "container" in E && t(5, k = E.container), "allow_custom_value" in E && t(6, h = E.allow_custom_value), "filterable" in E && t(7, C = E.filterable);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*selected_index, old_selected_index, initialized, choices, choices_values*/
    218105860 && j !== L && j !== null && v && (t(9, [_, f] = s[j], _, (t(20, f), t(11, j), t(27, L), t(26, v), t(2, s), t(24, w))), t(27, L = j), U("select", {
      index: j,
      value: w[j],
      selected: !0
    })), l.$$.dirty[0] & /*value, old_value, value_is_output*/
    7340032 && f != u && (ee(), $l(U, f, o), t(22, u = f)), l.$$.dirty[0] & /*choices*/
    4 && Z(), l.$$.dirty[0] & /*choices, old_choices, allow_custom_value, input_text, filtered_indices, filter_input*/
    8390468 && s !== r && (h || ee(), t(23, r = s), t(10, g = zt(s, _)), !h && g.length > 0 && t(14, F = g[0]), y == document.activeElement && t(12, b = !0)), l.$$.dirty[0] & /*input_text, old_input_text, choices, allow_custom_value, filtered_indices*/
    33556036 && _ !== c && (t(10, g = zt(s, _)), t(25, c = _), !h && g.length > 0 && t(14, F = g[0]));
  }, [
    n,
    i,
    s,
    a,
    d,
    k,
    h,
    C,
    y,
    _,
    g,
    j,
    b,
    m,
    F,
    U,
    N,
    J,
    R,
    de,
    f,
    o,
    u,
    r,
    w,
    c,
    v,
    L,
    we,
    pe,
    q
  ];
}
class us extends Gi {
  constructor(e) {
    super(), xi(
      this,
      e,
      fs,
      os,
      es,
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
function Be(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
const {
  SvelteComponent: rs,
  append: ne,
  attr: A,
  component_subscribe: al,
  detach: as,
  element: _s,
  init: cs,
  insert: ds,
  noop: _l,
  safe_not_equal: ms,
  set_style: nt,
  svg_element: ie,
  toggle_class: cl
} = window.__gradio__svelte__internal, { onMount: bs } = window.__gradio__svelte__internal;
function hs(l) {
  let e, t, n, i, f, u, o, s, r, a, d, k;
  return {
    c() {
      e = _s("div"), t = ie("svg"), n = ie("g"), i = ie("path"), f = ie("path"), u = ie("path"), o = ie("path"), s = ie("g"), r = ie("path"), a = ie("path"), d = ie("path"), k = ie("path"), A(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), A(i, "fill", "#FF7C00"), A(i, "fill-opacity", "0.4"), A(i, "class", "svelte-43sxxs"), A(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), A(f, "fill", "#FF7C00"), A(f, "class", "svelte-43sxxs"), A(u, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), A(u, "fill", "#FF7C00"), A(u, "fill-opacity", "0.4"), A(u, "class", "svelte-43sxxs"), A(o, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), A(o, "fill", "#FF7C00"), A(o, "class", "svelte-43sxxs"), nt(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), A(r, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), A(r, "fill", "#FF7C00"), A(r, "fill-opacity", "0.4"), A(r, "class", "svelte-43sxxs"), A(a, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), A(a, "fill", "#FF7C00"), A(a, "class", "svelte-43sxxs"), A(d, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), A(d, "fill", "#FF7C00"), A(d, "fill-opacity", "0.4"), A(d, "class", "svelte-43sxxs"), A(k, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), A(k, "fill", "#FF7C00"), A(k, "class", "svelte-43sxxs"), nt(s, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), A(t, "viewBox", "-1200 -1200 3000 3000"), A(t, "fill", "none"), A(t, "xmlns", "http://www.w3.org/2000/svg"), A(t, "class", "svelte-43sxxs"), A(e, "class", "svelte-43sxxs"), cl(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(h, C) {
      ds(h, e, C), ne(e, t), ne(t, n), ne(n, i), ne(n, f), ne(n, u), ne(n, o), ne(t, s), ne(s, r), ne(s, a), ne(s, d), ne(s, k);
    },
    p(h, [C]) {
      C & /*$top*/
      2 && nt(n, "transform", "translate(" + /*$top*/
      h[1][0] + "px, " + /*$top*/
      h[1][1] + "px)"), C & /*$bottom*/
      4 && nt(s, "transform", "translate(" + /*$bottom*/
      h[2][0] + "px, " + /*$bottom*/
      h[2][1] + "px)"), C & /*margin*/
      1 && cl(
        e,
        "margin",
        /*margin*/
        h[0]
      );
    },
    i: _l,
    o: _l,
    d(h) {
      h && as(e);
    }
  };
}
function gs(l, e, t) {
  let n, i;
  var f = this && this.__awaiter || function(h, C, y, b) {
    function m(w) {
      return w instanceof y ? w : new y(function(_) {
        _(w);
      });
    }
    return new (y || (y = Promise))(function(w, _) {
      function c(F) {
        try {
          g(b.next(F));
        } catch (j) {
          _(j);
        }
      }
      function v(F) {
        try {
          g(b.throw(F));
        } catch (j) {
          _(j);
        }
      }
      function g(F) {
        F.done ? w(F.value) : m(F.value).then(c, v);
      }
      g((b = b.apply(h, C || [])).next());
    });
  };
  let { margin: u = !0 } = e;
  const o = Gt([0, 0]);
  al(l, o, (h) => t(1, n = h));
  const s = Gt([0, 0]);
  al(l, s, (h) => t(2, i = h));
  let r;
  function a() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([o.set([125, 140]), s.set([-125, -140])]), yield Promise.all([o.set([-125, 140]), s.set([125, -140])]), yield Promise.all([o.set([-125, 0]), s.set([125, -0])]), yield Promise.all([o.set([125, 0]), s.set([-125, 0])]);
    });
  }
  function d() {
    return f(this, void 0, void 0, function* () {
      yield a(), r || d();
    });
  }
  function k() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([o.set([125, 0]), s.set([-125, 0])]), d();
    });
  }
  return bs(() => (k(), () => r = !0)), l.$$set = (h) => {
    "margin" in h && t(0, u = h.margin);
  }, [u, n, i, o, s];
}
class ws extends rs {
  constructor(e) {
    super(), cs(this, e, gs, hs, ms, { margin: 0 });
  }
}
const {
  SvelteComponent: ps,
  append: Fe,
  attr: ae,
  binding_callbacks: dl,
  check_outros: tn,
  create_component: ks,
  create_slot: vs,
  destroy_component: ys,
  destroy_each: ln,
  detach: z,
  element: be,
  empty: Re,
  ensure_array_like: at,
  get_all_dirty_from_scope: js,
  get_slot_changes: Cs,
  group_outros: nn,
  init: qs,
  insert: M,
  mount_component: Ss,
  noop: Vt,
  safe_not_equal: Es,
  set_data: le,
  set_style: Ce,
  space: _e,
  text: T,
  toggle_class: te,
  transition_in: Pe,
  transition_out: Ie,
  update_slot_base: Fs
} = window.__gradio__svelte__internal, { tick: Ls } = window.__gradio__svelte__internal, { onDestroy: Ns } = window.__gradio__svelte__internal, zs = (l) => ({}), ml = (l) => ({});
function bl(l, e, t) {
  const n = l.slice();
  return n[39] = e[t], n[41] = t, n;
}
function hl(l, e, t) {
  const n = l.slice();
  return n[39] = e[t], n;
}
function Ms(l) {
  let e, t = (
    /*i18n*/
    l[1]("common.error") + ""
  ), n, i, f;
  const u = (
    /*#slots*/
    l[29].error
  ), o = vs(
    u,
    l,
    /*$$scope*/
    l[28],
    ml
  );
  return {
    c() {
      e = be("span"), n = T(t), i = _e(), o && o.c(), ae(e, "class", "error svelte-1yserjw");
    },
    m(s, r) {
      M(s, e, r), Fe(e, n), M(s, i, r), o && o.m(s, r), f = !0;
    },
    p(s, r) {
      (!f || r[0] & /*i18n*/
      2) && t !== (t = /*i18n*/
      s[1]("common.error") + "") && le(n, t), o && o.p && (!f || r[0] & /*$$scope*/
      268435456) && Fs(
        o,
        u,
        s,
        /*$$scope*/
        s[28],
        f ? Cs(
          u,
          /*$$scope*/
          s[28],
          r,
          zs
        ) : js(
          /*$$scope*/
          s[28]
        ),
        ml
      );
    },
    i(s) {
      f || (Pe(o, s), f = !0);
    },
    o(s) {
      Ie(o, s), f = !1;
    },
    d(s) {
      s && (z(e), z(i)), o && o.d(s);
    }
  };
}
function Os(l) {
  let e, t, n, i, f, u, o, s, r, a = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && gl(l)
  );
  function d(_, c) {
    if (
      /*progress*/
      _[7]
    ) return Ds;
    if (
      /*queue_position*/
      _[2] !== null && /*queue_size*/
      _[3] !== void 0 && /*queue_position*/
      _[2] >= 0
    ) return Vs;
    if (
      /*queue_position*/
      _[2] === 0
    ) return As;
  }
  let k = d(l), h = k && k(l), C = (
    /*timer*/
    l[5] && kl(l)
  );
  const y = [Zs, Us], b = [];
  function m(_, c) {
    return (
      /*last_progress_level*/
      _[15] != null ? 0 : (
        /*show_progress*/
        _[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = m(l)) && (u = b[f] = y[f](l));
  let w = !/*timer*/
  l[5] && El(l);
  return {
    c() {
      a && a.c(), e = _e(), t = be("div"), h && h.c(), n = _e(), C && C.c(), i = _e(), u && u.c(), o = _e(), w && w.c(), s = Re(), ae(t, "class", "progress-text svelte-1yserjw"), te(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), te(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(_, c) {
      a && a.m(_, c), M(_, e, c), M(_, t, c), h && h.m(t, null), Fe(t, n), C && C.m(t, null), M(_, i, c), ~f && b[f].m(_, c), M(_, o, c), w && w.m(_, c), M(_, s, c), r = !0;
    },
    p(_, c) {
      /*variant*/
      _[8] === "default" && /*show_eta_bar*/
      _[18] && /*show_progress*/
      _[6] === "full" ? a ? a.p(_, c) : (a = gl(_), a.c(), a.m(e.parentNode, e)) : a && (a.d(1), a = null), k === (k = d(_)) && h ? h.p(_, c) : (h && h.d(1), h = k && k(_), h && (h.c(), h.m(t, n))), /*timer*/
      _[5] ? C ? C.p(_, c) : (C = kl(_), C.c(), C.m(t, null)) : C && (C.d(1), C = null), (!r || c[0] & /*variant*/
      256) && te(
        t,
        "meta-text-center",
        /*variant*/
        _[8] === "center"
      ), (!r || c[0] & /*variant*/
      256) && te(
        t,
        "meta-text",
        /*variant*/
        _[8] === "default"
      );
      let v = f;
      f = m(_), f === v ? ~f && b[f].p(_, c) : (u && (nn(), Ie(b[v], 1, 1, () => {
        b[v] = null;
      }), tn()), ~f ? (u = b[f], u ? u.p(_, c) : (u = b[f] = y[f](_), u.c()), Pe(u, 1), u.m(o.parentNode, o)) : u = null), /*timer*/
      _[5] ? w && (w.d(1), w = null) : w ? w.p(_, c) : (w = El(_), w.c(), w.m(s.parentNode, s));
    },
    i(_) {
      r || (Pe(u), r = !0);
    },
    o(_) {
      Ie(u), r = !1;
    },
    d(_) {
      _ && (z(e), z(t), z(i), z(o), z(s)), a && a.d(_), h && h.d(), C && C.d(), ~f && b[f].d(_), w && w.d(_);
    }
  };
}
function gl(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = be("div"), ae(e, "class", "eta-bar svelte-1yserjw"), Ce(e, "transform", t);
    },
    m(n, i) {
      M(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && Ce(e, "transform", t);
    },
    d(n) {
      n && z(e);
    }
  };
}
function As(l) {
  let e;
  return {
    c() {
      e = T("processing |");
    },
    m(t, n) {
      M(t, e, n);
    },
    p: Vt,
    d(t) {
      t && z(e);
    }
  };
}
function Vs(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, f, u;
  return {
    c() {
      e = T("queue: "), n = T(t), i = T("/"), f = T(
        /*queue_size*/
        l[3]
      ), u = T(" |");
    },
    m(o, s) {
      M(o, e, s), M(o, n, s), M(o, i, s), M(o, f, s), M(o, u, s);
    },
    p(o, s) {
      s[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      o[2] + 1 + "") && le(n, t), s[0] & /*queue_size*/
      8 && le(
        f,
        /*queue_size*/
        o[3]
      );
    },
    d(o) {
      o && (z(e), z(n), z(i), z(f), z(u));
    }
  };
}
function Ds(l) {
  let e, t = at(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = pl(hl(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Re();
    },
    m(i, f) {
      for (let u = 0; u < n.length; u += 1)
        n[u] && n[u].m(i, f);
      M(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        t = at(
          /*progress*/
          i[7]
        );
        let u;
        for (u = 0; u < t.length; u += 1) {
          const o = hl(i, t, u);
          n[u] ? n[u].p(o, f) : (n[u] = pl(o), n[u].c(), n[u].m(e.parentNode, e));
        }
        for (; u < n.length; u += 1)
          n[u].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && z(e), ln(n, i);
    }
  };
}
function wl(l) {
  let e, t = (
    /*p*/
    l[39].unit + ""
  ), n, i, f = " ", u;
  function o(a, d) {
    return (
      /*p*/
      a[39].length != null ? Ts : Bs
    );
  }
  let s = o(l), r = s(l);
  return {
    c() {
      r.c(), e = _e(), n = T(t), i = T(" | "), u = T(f);
    },
    m(a, d) {
      r.m(a, d), M(a, e, d), M(a, n, d), M(a, i, d), M(a, u, d);
    },
    p(a, d) {
      s === (s = o(a)) && r ? r.p(a, d) : (r.d(1), r = s(a), r && (r.c(), r.m(e.parentNode, e))), d[0] & /*progress*/
      128 && t !== (t = /*p*/
      a[39].unit + "") && le(n, t);
    },
    d(a) {
      a && (z(e), z(n), z(i), z(u)), r.d(a);
    }
  };
}
function Bs(l) {
  let e = Be(
    /*p*/
    l[39].index || 0
  ) + "", t;
  return {
    c() {
      t = T(e);
    },
    m(n, i) {
      M(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = Be(
        /*p*/
        n[39].index || 0
      ) + "") && le(t, e);
    },
    d(n) {
      n && z(t);
    }
  };
}
function Ts(l) {
  let e = Be(
    /*p*/
    l[39].index || 0
  ) + "", t, n, i = Be(
    /*p*/
    l[39].length
  ) + "", f;
  return {
    c() {
      t = T(e), n = T("/"), f = T(i);
    },
    m(u, o) {
      M(u, t, o), M(u, n, o), M(u, f, o);
    },
    p(u, o) {
      o[0] & /*progress*/
      128 && e !== (e = Be(
        /*p*/
        u[39].index || 0
      ) + "") && le(t, e), o[0] & /*progress*/
      128 && i !== (i = Be(
        /*p*/
        u[39].length
      ) + "") && le(f, i);
    },
    d(u) {
      u && (z(t), z(n), z(f));
    }
  };
}
function pl(l) {
  let e, t = (
    /*p*/
    l[39].index != null && wl(l)
  );
  return {
    c() {
      t && t.c(), e = Re();
    },
    m(n, i) {
      t && t.m(n, i), M(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[39].index != null ? t ? t.p(n, i) : (t = wl(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && z(e), t && t.d(n);
    }
  };
}
function kl(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = T(
        /*formatted_timer*/
        l[20]
      ), n = T(t), i = T("s");
    },
    m(f, u) {
      M(f, e, u), M(f, n, u), M(f, i, u);
    },
    p(f, u) {
      u[0] & /*formatted_timer*/
      1048576 && le(
        e,
        /*formatted_timer*/
        f[20]
      ), u[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && le(n, t);
    },
    d(f) {
      f && (z(e), z(n), z(i));
    }
  };
}
function Us(l) {
  let e, t;
  return e = new ws({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      ks(e.$$.fragment);
    },
    m(n, i) {
      Ss(e, n, i), t = !0;
    },
    p(n, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      n[8] === "default"), e.$set(f);
    },
    i(n) {
      t || (Pe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ie(e.$$.fragment, n), t = !1;
    },
    d(n) {
      ys(e, n);
    }
  };
}
function Zs(l) {
  let e, t, n, i, f, u = `${/*last_progress_level*/
  l[15] * 100}%`, o = (
    /*progress*/
    l[7] != null && vl(l)
  );
  return {
    c() {
      e = be("div"), t = be("div"), o && o.c(), n = _e(), i = be("div"), f = be("div"), ae(t, "class", "progress-level-inner svelte-1yserjw"), ae(f, "class", "progress-bar svelte-1yserjw"), Ce(f, "width", u), ae(i, "class", "progress-bar-wrap svelte-1yserjw"), ae(e, "class", "progress-level svelte-1yserjw");
    },
    m(s, r) {
      M(s, e, r), Fe(e, t), o && o.m(t, null), Fe(e, n), Fe(e, i), Fe(i, f), l[30](f);
    },
    p(s, r) {
      /*progress*/
      s[7] != null ? o ? o.p(s, r) : (o = vl(s), o.c(), o.m(t, null)) : o && (o.d(1), o = null), r[0] & /*last_progress_level*/
      32768 && u !== (u = `${/*last_progress_level*/
      s[15] * 100}%`) && Ce(f, "width", u);
    },
    i: Vt,
    o: Vt,
    d(s) {
      s && z(e), o && o.d(), l[30](null);
    }
  };
}
function vl(l) {
  let e, t = at(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Sl(bl(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = Re();
    },
    m(i, f) {
      for (let u = 0; u < n.length; u += 1)
        n[u] && n[u].m(i, f);
      M(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        t = at(
          /*progress*/
          i[7]
        );
        let u;
        for (u = 0; u < t.length; u += 1) {
          const o = bl(i, t, u);
          n[u] ? n[u].p(o, f) : (n[u] = Sl(o), n[u].c(), n[u].m(e.parentNode, e));
        }
        for (; u < n.length; u += 1)
          n[u].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && z(e), ln(n, i);
    }
  };
}
function yl(l) {
  let e, t, n, i, f = (
    /*i*/
    l[41] !== 0 && Ps()
  ), u = (
    /*p*/
    l[39].desc != null && jl(l)
  ), o = (
    /*p*/
    l[39].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[41]
    ] != null && Cl()
  ), s = (
    /*progress_level*/
    l[14] != null && ql(l)
  );
  return {
    c() {
      f && f.c(), e = _e(), u && u.c(), t = _e(), o && o.c(), n = _e(), s && s.c(), i = Re();
    },
    m(r, a) {
      f && f.m(r, a), M(r, e, a), u && u.m(r, a), M(r, t, a), o && o.m(r, a), M(r, n, a), s && s.m(r, a), M(r, i, a);
    },
    p(r, a) {
      /*p*/
      r[39].desc != null ? u ? u.p(r, a) : (u = jl(r), u.c(), u.m(t.parentNode, t)) : u && (u.d(1), u = null), /*p*/
      r[39].desc != null && /*progress_level*/
      r[14] && /*progress_level*/
      r[14][
        /*i*/
        r[41]
      ] != null ? o || (o = Cl(), o.c(), o.m(n.parentNode, n)) : o && (o.d(1), o = null), /*progress_level*/
      r[14] != null ? s ? s.p(r, a) : (s = ql(r), s.c(), s.m(i.parentNode, i)) : s && (s.d(1), s = null);
    },
    d(r) {
      r && (z(e), z(t), z(n), z(i)), f && f.d(r), u && u.d(r), o && o.d(r), s && s.d(r);
    }
  };
}
function Ps(l) {
  let e;
  return {
    c() {
      e = T(" /");
    },
    m(t, n) {
      M(t, e, n);
    },
    d(t) {
      t && z(e);
    }
  };
}
function jl(l) {
  let e = (
    /*p*/
    l[39].desc + ""
  ), t;
  return {
    c() {
      t = T(e);
    },
    m(n, i) {
      M(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[39].desc + "") && le(t, e);
    },
    d(n) {
      n && z(t);
    }
  };
}
function Cl(l) {
  let e;
  return {
    c() {
      e = T("-");
    },
    m(t, n) {
      M(t, e, n);
    },
    d(t) {
      t && z(e);
    }
  };
}
function ql(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[41]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = T(e), n = T("%");
    },
    m(i, f) {
      M(i, t, f), M(i, n, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[41]
      ] || 0)).toFixed(1) + "") && le(t, e);
    },
    d(i) {
      i && (z(t), z(n));
    }
  };
}
function Sl(l) {
  let e, t = (
    /*p*/
    (l[39].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[41]
    ] != null) && yl(l)
  );
  return {
    c() {
      t && t.c(), e = Re();
    },
    m(n, i) {
      t && t.m(n, i), M(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[39].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[41]
      ] != null ? t ? t.p(n, i) : (t = yl(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && z(e), t && t.d(n);
    }
  };
}
function El(l) {
  let e, t;
  return {
    c() {
      e = be("p"), t = T(
        /*loading_text*/
        l[9]
      ), ae(e, "class", "loading svelte-1yserjw");
    },
    m(n, i) {
      M(n, e, i), Fe(e, t);
    },
    p(n, i) {
      i[0] & /*loading_text*/
      512 && le(
        t,
        /*loading_text*/
        n[9]
      );
    },
    d(n) {
      n && z(e);
    }
  };
}
function Is(l) {
  let e, t, n, i, f;
  const u = [Os, Ms], o = [];
  function s(r, a) {
    return (
      /*status*/
      r[4] === "pending" ? 0 : (
        /*status*/
        r[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = s(l)) && (n = o[t] = u[t](l)), {
    c() {
      e = be("div"), n && n.c(), ae(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-1yserjw"), te(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), te(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), te(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), te(
        e,
        "border",
        /*border*/
        l[12]
      ), Ce(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), Ce(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(r, a) {
      M(r, e, a), ~t && o[t].m(e, null), l[31](e), f = !0;
    },
    p(r, a) {
      let d = t;
      t = s(r), t === d ? ~t && o[t].p(r, a) : (n && (nn(), Ie(o[d], 1, 1, () => {
        o[d] = null;
      }), tn()), ~t ? (n = o[t], n ? n.p(r, a) : (n = o[t] = u[t](r), n.c()), Pe(n, 1), n.m(e, null)) : n = null), (!f || a[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      r[8] + " " + /*show_progress*/
      r[6] + " svelte-1yserjw")) && ae(e, "class", i), (!f || a[0] & /*variant, show_progress, status, show_progress*/
      336) && te(e, "hide", !/*status*/
      r[4] || /*status*/
      r[4] === "complete" || /*show_progress*/
      r[6] === "hidden"), (!f || a[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && te(
        e,
        "translucent",
        /*variant*/
        r[8] === "center" && /*status*/
        (r[4] === "pending" || /*status*/
        r[4] === "error") || /*translucent*/
        r[11] || /*show_progress*/
        r[6] === "minimal"
      ), (!f || a[0] & /*variant, show_progress, status*/
      336) && te(
        e,
        "generating",
        /*status*/
        r[4] === "generating"
      ), (!f || a[0] & /*variant, show_progress, border*/
      4416) && te(
        e,
        "border",
        /*border*/
        r[12]
      ), a[0] & /*absolute*/
      1024 && Ce(
        e,
        "position",
        /*absolute*/
        r[10] ? "absolute" : "static"
      ), a[0] & /*absolute*/
      1024 && Ce(
        e,
        "padding",
        /*absolute*/
        r[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(r) {
      f || (Pe(n), f = !0);
    },
    o(r) {
      Ie(n), f = !1;
    },
    d(r) {
      r && z(e), ~t && o[t].d(), l[31](null);
    }
  };
}
var Hs = function(l, e, t, n) {
  function i(f) {
    return f instanceof t ? f : new t(function(u) {
      u(f);
    });
  }
  return new (t || (t = Promise))(function(f, u) {
    function o(a) {
      try {
        r(n.next(a));
      } catch (d) {
        u(d);
      }
    }
    function s(a) {
      try {
        r(n.throw(a));
      } catch (d) {
        u(d);
      }
    }
    function r(a) {
      a.done ? f(a.value) : i(a.value).then(o, s);
    }
    r((n = n.apply(l, e || [])).next());
  });
};
let it = [], Et = !1;
function Js(l) {
  return Hs(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (it.push(e), !Et) Et = !0;
      else return;
      yield Ls(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < it.length; i++) {
          const u = it[i].getBoundingClientRect();
          (i === 0 || u.top + window.scrollY <= n[0]) && (n[0] = u.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), Et = !1, it = [];
      });
    }
  });
}
function Rs(l, e, t) {
  let n, { $$slots: i = {}, $$scope: f } = e;
  this && this.__awaiter;
  let { i18n: u } = e, { eta: o = null } = e, { queue_position: s } = e, { queue_size: r } = e, { status: a } = e, { scroll_to_output: d = !1 } = e, { timer: k = !0 } = e, { show_progress: h = "full" } = e, { message: C = null } = e, { progress: y = null } = e, { variant: b = "default" } = e, { loading_text: m = "Loading..." } = e, { absolute: w = !0 } = e, { translucent: _ = !1 } = e, { border: c = !1 } = e, { autoscroll: v } = e, g, F = !1, j = 0, L = 0, U = null, Z = null, ee = 0, N = null, J, R = null, de = !0;
  const we = () => {
    t(0, o = t(26, U = t(19, E = null))), t(24, j = performance.now()), t(25, L = 0), F = !0, pe();
  };
  function pe() {
    requestAnimationFrame(() => {
      t(25, L = (performance.now() - j) / 1e3), F && pe();
    });
  }
  function q() {
    t(25, L = 0), t(0, o = t(26, U = t(19, E = null))), F && (F = !1);
  }
  Ns(() => {
    F && q();
  });
  let E = null;
  function Y(S) {
    dl[S ? "unshift" : "push"](() => {
      R = S, t(16, R), t(7, y), t(14, N), t(15, J);
    });
  }
  function V(S) {
    dl[S ? "unshift" : "push"](() => {
      g = S, t(13, g);
    });
  }
  return l.$$set = (S) => {
    "i18n" in S && t(1, u = S.i18n), "eta" in S && t(0, o = S.eta), "queue_position" in S && t(2, s = S.queue_position), "queue_size" in S && t(3, r = S.queue_size), "status" in S && t(4, a = S.status), "scroll_to_output" in S && t(21, d = S.scroll_to_output), "timer" in S && t(5, k = S.timer), "show_progress" in S && t(6, h = S.show_progress), "message" in S && t(22, C = S.message), "progress" in S && t(7, y = S.progress), "variant" in S && t(8, b = S.variant), "loading_text" in S && t(9, m = S.loading_text), "absolute" in S && t(10, w = S.absolute), "translucent" in S && t(11, _ = S.translucent), "border" in S && t(12, c = S.border), "autoscroll" in S && t(23, v = S.autoscroll), "$$scope" in S && t(28, f = S.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    218103809 && (o === null && t(0, o = U), o != null && U !== o && (t(27, Z = (performance.now() - j) / 1e3 + o), t(19, E = Z.toFixed(1)), t(26, U = o))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    167772160 && t(17, ee = Z === null || Z <= 0 || !L ? null : Math.min(L / Z, 1)), l.$$.dirty[0] & /*progress*/
    128 && y != null && t(18, de = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (y != null ? t(14, N = y.map((S) => {
      if (S.index != null && S.length != null)
        return S.index / S.length;
      if (S.progress != null)
        return S.progress;
    })) : t(14, N = null), N ? (t(15, J = N[N.length - 1]), R && (J === 0 ? t(16, R.style.transition = "0", R) : t(16, R.style.transition = "150ms", R))) : t(15, J = void 0)), l.$$.dirty[0] & /*status*/
    16 && (a === "pending" ? we() : q()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    10493968 && g && d && (a === "pending" || a === "complete") && Js(g, v), l.$$.dirty[0] & /*status, message*/
    4194320, l.$$.dirty[0] & /*timer_diff*/
    33554432 && t(20, n = L.toFixed(1));
  }, [
    o,
    u,
    s,
    r,
    a,
    k,
    h,
    y,
    b,
    m,
    w,
    _,
    c,
    g,
    N,
    J,
    R,
    ee,
    de,
    E,
    n,
    d,
    C,
    v,
    j,
    L,
    U,
    Z,
    f,
    i,
    Y,
    V
  ];
}
class Xs extends ps {
  constructor(e) {
    super(), qs(
      this,
      e,
      Rs,
      Is,
      Es,
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
class Ys {
  constructor({
    name: e,
    token: t,
    param_specs: n
  }) {
    this.name = e, this.token = t, this.param_specs = n || new Object();
  }
}
const {
  SvelteComponent: Gs,
  append: sn,
  attr: B,
  bubble: Ks,
  check_outros: Qs,
  create_slot: on,
  detach: et,
  element: ht,
  empty: Ws,
  get_all_dirty_from_scope: fn,
  get_slot_changes: un,
  group_outros: xs,
  init: $s,
  insert: tt,
  listen: eo,
  safe_not_equal: to,
  set_style: G,
  space: rn,
  src_url_equal: _t,
  toggle_class: Te,
  transition_in: ct,
  transition_out: dt,
  update_slot_base: an
} = window.__gradio__svelte__internal;
function lo(l) {
  let e, t, n, i, f, u, o = (
    /*icon*/
    l[7] && Fl(l)
  );
  const s = (
    /*#slots*/
    l[12].default
  ), r = on(
    s,
    l,
    /*$$scope*/
    l[11],
    null
  );
  return {
    c() {
      e = ht("button"), o && o.c(), t = rn(), r && r.c(), B(e, "class", n = /*size*/
      l[4] + " " + /*variant*/
      l[3] + " " + /*elem_classes*/
      l[1].join(" ") + " svelte-8huxfn"), B(
        e,
        "id",
        /*elem_id*/
        l[0]
      ), e.disabled = /*disabled*/
      l[8], Te(e, "hidden", !/*visible*/
      l[2]), G(
        e,
        "flex-grow",
        /*scale*/
        l[9]
      ), G(
        e,
        "width",
        /*scale*/
        l[9] === 0 ? "fit-content" : null
      ), G(e, "min-width", typeof /*min_width*/
      l[10] == "number" ? `calc(min(${/*min_width*/
      l[10]}px, 100%))` : null);
    },
    m(a, d) {
      tt(a, e, d), o && o.m(e, null), sn(e, t), r && r.m(e, null), i = !0, f || (u = eo(
        e,
        "click",
        /*click_handler*/
        l[13]
      ), f = !0);
    },
    p(a, d) {
      /*icon*/
      a[7] ? o ? o.p(a, d) : (o = Fl(a), o.c(), o.m(e, t)) : o && (o.d(1), o = null), r && r.p && (!i || d & /*$$scope*/
      2048) && an(
        r,
        s,
        a,
        /*$$scope*/
        a[11],
        i ? un(
          s,
          /*$$scope*/
          a[11],
          d,
          null
        ) : fn(
          /*$$scope*/
          a[11]
        ),
        null
      ), (!i || d & /*size, variant, elem_classes*/
      26 && n !== (n = /*size*/
      a[4] + " " + /*variant*/
      a[3] + " " + /*elem_classes*/
      a[1].join(" ") + " svelte-8huxfn")) && B(e, "class", n), (!i || d & /*elem_id*/
      1) && B(
        e,
        "id",
        /*elem_id*/
        a[0]
      ), (!i || d & /*disabled*/
      256) && (e.disabled = /*disabled*/
      a[8]), (!i || d & /*size, variant, elem_classes, visible*/
      30) && Te(e, "hidden", !/*visible*/
      a[2]), d & /*scale*/
      512 && G(
        e,
        "flex-grow",
        /*scale*/
        a[9]
      ), d & /*scale*/
      512 && G(
        e,
        "width",
        /*scale*/
        a[9] === 0 ? "fit-content" : null
      ), d & /*min_width*/
      1024 && G(e, "min-width", typeof /*min_width*/
      a[10] == "number" ? `calc(min(${/*min_width*/
      a[10]}px, 100%))` : null);
    },
    i(a) {
      i || (ct(r, a), i = !0);
    },
    o(a) {
      dt(r, a), i = !1;
    },
    d(a) {
      a && et(e), o && o.d(), r && r.d(a), f = !1, u();
    }
  };
}
function no(l) {
  let e, t, n, i, f = (
    /*icon*/
    l[7] && Ll(l)
  );
  const u = (
    /*#slots*/
    l[12].default
  ), o = on(
    u,
    l,
    /*$$scope*/
    l[11],
    null
  );
  return {
    c() {
      e = ht("a"), f && f.c(), t = rn(), o && o.c(), B(
        e,
        "href",
        /*link*/
        l[6]
      ), B(e, "rel", "noopener noreferrer"), B(
        e,
        "aria-disabled",
        /*disabled*/
        l[8]
      ), B(e, "class", n = /*size*/
      l[4] + " " + /*variant*/
      l[3] + " " + /*elem_classes*/
      l[1].join(" ") + " svelte-8huxfn"), B(
        e,
        "id",
        /*elem_id*/
        l[0]
      ), Te(e, "hidden", !/*visible*/
      l[2]), Te(
        e,
        "disabled",
        /*disabled*/
        l[8]
      ), G(
        e,
        "flex-grow",
        /*scale*/
        l[9]
      ), G(
        e,
        "pointer-events",
        /*disabled*/
        l[8] ? "none" : null
      ), G(
        e,
        "width",
        /*scale*/
        l[9] === 0 ? "fit-content" : null
      ), G(e, "min-width", typeof /*min_width*/
      l[10] == "number" ? `calc(min(${/*min_width*/
      l[10]}px, 100%))` : null);
    },
    m(s, r) {
      tt(s, e, r), f && f.m(e, null), sn(e, t), o && o.m(e, null), i = !0;
    },
    p(s, r) {
      /*icon*/
      s[7] ? f ? f.p(s, r) : (f = Ll(s), f.c(), f.m(e, t)) : f && (f.d(1), f = null), o && o.p && (!i || r & /*$$scope*/
      2048) && an(
        o,
        u,
        s,
        /*$$scope*/
        s[11],
        i ? un(
          u,
          /*$$scope*/
          s[11],
          r,
          null
        ) : fn(
          /*$$scope*/
          s[11]
        ),
        null
      ), (!i || r & /*link*/
      64) && B(
        e,
        "href",
        /*link*/
        s[6]
      ), (!i || r & /*disabled*/
      256) && B(
        e,
        "aria-disabled",
        /*disabled*/
        s[8]
      ), (!i || r & /*size, variant, elem_classes*/
      26 && n !== (n = /*size*/
      s[4] + " " + /*variant*/
      s[3] + " " + /*elem_classes*/
      s[1].join(" ") + " svelte-8huxfn")) && B(e, "class", n), (!i || r & /*elem_id*/
      1) && B(
        e,
        "id",
        /*elem_id*/
        s[0]
      ), (!i || r & /*size, variant, elem_classes, visible*/
      30) && Te(e, "hidden", !/*visible*/
      s[2]), (!i || r & /*size, variant, elem_classes, disabled*/
      282) && Te(
        e,
        "disabled",
        /*disabled*/
        s[8]
      ), r & /*scale*/
      512 && G(
        e,
        "flex-grow",
        /*scale*/
        s[9]
      ), r & /*disabled*/
      256 && G(
        e,
        "pointer-events",
        /*disabled*/
        s[8] ? "none" : null
      ), r & /*scale*/
      512 && G(
        e,
        "width",
        /*scale*/
        s[9] === 0 ? "fit-content" : null
      ), r & /*min_width*/
      1024 && G(e, "min-width", typeof /*min_width*/
      s[10] == "number" ? `calc(min(${/*min_width*/
      s[10]}px, 100%))` : null);
    },
    i(s) {
      i || (ct(o, s), i = !0);
    },
    o(s) {
      dt(o, s), i = !1;
    },
    d(s) {
      s && et(e), f && f.d(), o && o.d(s);
    }
  };
}
function Fl(l) {
  let e, t, n;
  return {
    c() {
      e = ht("img"), B(e, "class", "button-icon svelte-8huxfn"), _t(e.src, t = /*icon*/
      l[7].url) || B(e, "src", t), B(e, "alt", n = `${/*value*/
      l[5]} icon`);
    },
    m(i, f) {
      tt(i, e, f);
    },
    p(i, f) {
      f & /*icon*/
      128 && !_t(e.src, t = /*icon*/
      i[7].url) && B(e, "src", t), f & /*value*/
      32 && n !== (n = `${/*value*/
      i[5]} icon`) && B(e, "alt", n);
    },
    d(i) {
      i && et(e);
    }
  };
}
function Ll(l) {
  let e, t, n;
  return {
    c() {
      e = ht("img"), B(e, "class", "button-icon svelte-8huxfn"), _t(e.src, t = /*icon*/
      l[7].url) || B(e, "src", t), B(e, "alt", n = `${/*value*/
      l[5]} icon`);
    },
    m(i, f) {
      tt(i, e, f);
    },
    p(i, f) {
      f & /*icon*/
      128 && !_t(e.src, t = /*icon*/
      i[7].url) && B(e, "src", t), f & /*value*/
      32 && n !== (n = `${/*value*/
      i[5]} icon`) && B(e, "alt", n);
    },
    d(i) {
      i && et(e);
    }
  };
}
function io(l) {
  let e, t, n, i;
  const f = [no, lo], u = [];
  function o(s, r) {
    return (
      /*link*/
      s[6] && /*link*/
      s[6].length > 0 ? 0 : 1
    );
  }
  return e = o(l), t = u[e] = f[e](l), {
    c() {
      t.c(), n = Ws();
    },
    m(s, r) {
      u[e].m(s, r), tt(s, n, r), i = !0;
    },
    p(s, [r]) {
      let a = e;
      e = o(s), e === a ? u[e].p(s, r) : (xs(), dt(u[a], 1, 1, () => {
        u[a] = null;
      }), Qs(), t = u[e], t ? t.p(s, r) : (t = u[e] = f[e](s), t.c()), ct(t, 1), t.m(n.parentNode, n));
    },
    i(s) {
      i || (ct(t), i = !0);
    },
    o(s) {
      dt(t), i = !1;
    },
    d(s) {
      s && et(n), u[e].d(s);
    }
  };
}
function so(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { elem_id: f = "" } = e, { elem_classes: u = [] } = e, { visible: o = !0 } = e, { variant: s = "secondary" } = e, { size: r = "lg" } = e, { value: a = null } = e, { link: d = null } = e, { icon: k = null } = e, { disabled: h = !1 } = e, { scale: C = null } = e, { min_width: y = void 0 } = e;
  function b(m) {
    Ks.call(this, l, m);
  }
  return l.$$set = (m) => {
    "elem_id" in m && t(0, f = m.elem_id), "elem_classes" in m && t(1, u = m.elem_classes), "visible" in m && t(2, o = m.visible), "variant" in m && t(3, s = m.variant), "size" in m && t(4, r = m.size), "value" in m && t(5, a = m.value), "link" in m && t(6, d = m.link), "icon" in m && t(7, k = m.icon), "disabled" in m && t(8, h = m.disabled), "scale" in m && t(9, C = m.scale), "min_width" in m && t(10, y = m.min_width), "$$scope" in m && t(11, i = m.$$scope);
  }, [
    f,
    u,
    o,
    s,
    r,
    a,
    d,
    k,
    h,
    C,
    y,
    i,
    n,
    b
  ];
}
class oo extends Gs {
  constructor(e) {
    super(), $s(this, e, so, io, to, {
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
  SvelteComponent: fo,
  attr: uo,
  detach: ro,
  element: ao,
  init: _o,
  insert: co,
  noop: Nl,
  safe_not_equal: mo,
  toggle_class: Oe
} = window.__gradio__svelte__internal;
function bo(l) {
  let e;
  return {
    c() {
      e = ao("div"), e.textContent = `${/*names_string*/
      l[2]}`, uo(e, "class", "svelte-1gecy8w"), Oe(
        e,
        "table",
        /*type*/
        l[0] === "table"
      ), Oe(
        e,
        "gallery",
        /*type*/
        l[0] === "gallery"
      ), Oe(
        e,
        "selected",
        /*selected*/
        l[1]
      );
    },
    m(t, n) {
      co(t, e, n);
    },
    p(t, [n]) {
      n & /*type*/
      1 && Oe(
        e,
        "table",
        /*type*/
        t[0] === "table"
      ), n & /*type*/
      1 && Oe(
        e,
        "gallery",
        /*type*/
        t[0] === "gallery"
      ), n & /*selected*/
      2 && Oe(
        e,
        "selected",
        /*selected*/
        t[1]
      );
    },
    i: Nl,
    o: Nl,
    d(t) {
      t && ro(e);
    }
  };
}
function ho(l, e, t) {
  let { value: n } = e, { type: i } = e, { selected: f = !1 } = e, { choices: u } = e, r = (n ? Array.isArray(n) ? n : [n] : []).map((a) => {
    var d;
    return (d = u.find((k) => k[1] === a)) === null || d === void 0 ? void 0 : d[0];
  }).filter((a) => a !== void 0).join(", ");
  return l.$$set = (a) => {
    "value" in a && t(3, n = a.value), "type" in a && t(0, i = a.type), "selected" in a && t(1, f = a.selected), "choices" in a && t(4, u = a.choices);
  }, [i, f, r, n, u];
}
class Xo extends fo {
  constructor(e) {
    super(), _o(this, e, ho, bo, mo, {
      value: 3,
      type: 0,
      selected: 1,
      choices: 4
    });
  }
}
const {
  SvelteComponent: go,
  append: fe,
  attr: I,
  binding_callbacks: wo,
  check_outros: mt,
  create_component: We,
  destroy_component: xe,
  destroy_each: po,
  detach: he,
  element: ue,
  ensure_array_like: zl,
  group_outros: bt,
  init: ko,
  insert: ge,
  listen: me,
  mount_component: $e,
  prevent_default: Ml,
  run_all: Pt,
  safe_not_equal: vo,
  set_data: It,
  set_input_value: Ol,
  space: Ue,
  text: Ht,
  toggle_class: Ae,
  transition_in: X,
  transition_out: $
} = window.__gradio__svelte__internal, { afterUpdate: yo, createEventDispatcher: jo } = window.__gradio__svelte__internal;
function Al(l, e, t) {
  const n = l.slice();
  return n[40] = e[t], n;
}
function Co(l) {
  let e;
  return {
    c() {
      e = Ht(
        /*label*/
        l[0]
      );
    },
    m(t, n) {
      ge(t, e, n);
    },
    p(t, n) {
      n[0] & /*label*/
      1 && It(
        e,
        /*label*/
        t[0]
      );
    },
    d(t) {
      t && he(e);
    }
  };
}
function qo(l) {
  let e = (
    /*s*/
    l[40] + ""
  ), t;
  return {
    c() {
      t = Ht(e);
    },
    m(n, i) {
      ge(n, t, i);
    },
    p(n, i) {
      i[0] & /*selected_indices*/
      4096 && e !== (e = /*s*/
      n[40] + "") && It(t, e);
    },
    d(n) {
      n && he(t);
    }
  };
}
function So(l) {
  let e = (
    /*choices_names*/
    l[15][
      /*s*/
      l[40]
    ] + ""
  ), t;
  return {
    c() {
      t = Ht(e);
    },
    m(n, i) {
      ge(n, t, i);
    },
    p(n, i) {
      i[0] & /*choices_names, selected_indices*/
      36864 && e !== (e = /*choices_names*/
      n[15][
        /*s*/
        n[40]
      ] + "") && It(t, e);
    },
    d(n) {
      n && he(t);
    }
  };
}
function Vl(l) {
  let e, t, n, i, f, u;
  t = new xl({});
  function o() {
    return (
      /*click_handler*/
      l[31](
        /*s*/
        l[40]
      )
    );
  }
  function s(...r) {
    return (
      /*keydown_handler*/
      l[32](
        /*s*/
        l[40],
        ...r
      )
    );
  }
  return {
    c() {
      e = ue("div"), We(t.$$.fragment), I(e, "class", "token-remove svelte-xtjjyg"), I(e, "role", "button"), I(e, "tabindex", "0"), I(e, "title", n = /*i18n*/
      l[9]("common.remove") + " " + /*s*/
      l[40]);
    },
    m(r, a) {
      ge(r, e, a), $e(t, e, null), i = !0, f || (u = [
        me(e, "click", Ml(o)),
        me(e, "keydown", Ml(s))
      ], f = !0);
    },
    p(r, a) {
      l = r, (!i || a[0] & /*i18n, selected_indices*/
      4608 && n !== (n = /*i18n*/
      l[9]("common.remove") + " " + /*s*/
      l[40])) && I(e, "title", n);
    },
    i(r) {
      i || (X(t.$$.fragment, r), i = !0);
    },
    o(r) {
      $(t.$$.fragment, r), i = !1;
    },
    d(r) {
      r && he(e), xe(t), f = !1, Pt(u);
    }
  };
}
function Dl(l) {
  let e, t, n, i;
  function f(r, a) {
    return typeof /*s*/
    r[40] == "number" ? So : qo;
  }
  let u = f(l), o = u(l), s = !/*disabled*/
  l[4] && Vl(l);
  return {
    c() {
      e = ue("div"), t = ue("span"), o.c(), n = Ue(), s && s.c(), I(t, "class", "svelte-xtjjyg"), I(e, "class", "token svelte-xtjjyg");
    },
    m(r, a) {
      ge(r, e, a), fe(e, t), o.m(t, null), fe(e, n), s && s.m(e, null), i = !0;
    },
    p(r, a) {
      u === (u = f(r)) && o ? o.p(r, a) : (o.d(1), o = u(r), o && (o.c(), o.m(t, null))), /*disabled*/
      r[4] ? s && (bt(), $(s, 1, 1, () => {
        s = null;
      }), mt()) : s ? (s.p(r, a), a[0] & /*disabled*/
      16 && X(s, 1)) : (s = Vl(r), s.c(), X(s, 1), s.m(e, null));
    },
    i(r) {
      i || (X(s), i = !0);
    },
    o(r) {
      $(s), i = !1;
    },
    d(r) {
      r && he(e), o.d(), s && s.d();
    }
  };
}
function Bl(l) {
  let e, t, n, i, f = (
    /*selected_indices*/
    l[12].length > 0 && Tl(l)
  );
  return n = new Wl({}), {
    c() {
      f && f.c(), e = Ue(), t = ue("span"), We(n.$$.fragment), I(t, "class", "icon-wrap svelte-xtjjyg");
    },
    m(u, o) {
      f && f.m(u, o), ge(u, e, o), ge(u, t, o), $e(n, t, null), i = !0;
    },
    p(u, o) {
      /*selected_indices*/
      u[12].length > 0 ? f ? (f.p(u, o), o[0] & /*selected_indices*/
      4096 && X(f, 1)) : (f = Tl(u), f.c(), X(f, 1), f.m(e.parentNode, e)) : f && (bt(), $(f, 1, 1, () => {
        f = null;
      }), mt());
    },
    i(u) {
      i || (X(f), X(n.$$.fragment, u), i = !0);
    },
    o(u) {
      $(f), $(n.$$.fragment, u), i = !1;
    },
    d(u) {
      u && (he(e), he(t)), f && f.d(u), xe(n);
    }
  };
}
function Tl(l) {
  let e, t, n, i, f, u;
  return t = new xl({}), {
    c() {
      e = ue("div"), We(t.$$.fragment), I(e, "role", "button"), I(e, "tabindex", "0"), I(e, "class", "token-remove remove-all svelte-xtjjyg"), I(e, "title", n = /*i18n*/
      l[9]("common.clear"));
    },
    m(o, s) {
      ge(o, e, s), $e(t, e, null), i = !0, f || (u = [
        me(
          e,
          "click",
          /*remove_all*/
          l[21]
        ),
        me(
          e,
          "keydown",
          /*keydown_handler_1*/
          l[36]
        )
      ], f = !0);
    },
    p(o, s) {
      (!i || s[0] & /*i18n*/
      512 && n !== (n = /*i18n*/
      o[9]("common.clear"))) && I(e, "title", n);
    },
    i(o) {
      i || (X(t.$$.fragment, o), i = !0);
    },
    o(o) {
      $(t.$$.fragment, o), i = !1;
    },
    d(o) {
      o && he(e), xe(t), f = !1, Pt(u);
    }
  };
}
function Eo(l) {
  let e, t, n, i, f, u, o, s, r, a, d, k, h, C, y;
  t = new Ql({
    props: {
      show_label: (
        /*show_label*/
        l[5]
      ),
      info: (
        /*info*/
        l[1]
      ),
      $$slots: { default: [Co] },
      $$scope: { ctx: l }
    }
  });
  let b = zl(
    /*selected_indices*/
    l[12]
  ), m = [];
  for (let c = 0; c < b.length; c += 1)
    m[c] = Dl(Al(l, b, c));
  const w = (c) => $(m[c], 1, 1, () => {
    m[c] = null;
  });
  let _ = !/*disabled*/
  l[4] && Bl(l);
  return k = new Yl({
    props: {
      show_options: (
        /*show_options*/
        l[14]
      ),
      choices: (
        /*choices*/
        l[3]
      ),
      filtered_indices: (
        /*filtered_indices*/
        l[11]
      ),
      disabled: (
        /*disabled*/
        l[4]
      ),
      selected_indices: (
        /*selected_indices*/
        l[12]
      ),
      active_index: (
        /*active_index*/
        l[16]
      )
    }
  }), k.$on(
    "change",
    /*handle_option_selected*/
    l[20]
  ), {
    c() {
      e = ue("label"), We(t.$$.fragment), n = Ue(), i = ue("div"), f = ue("div");
      for (let c = 0; c < m.length; c += 1)
        m[c].c();
      u = Ue(), o = ue("div"), s = ue("input"), a = Ue(), _ && _.c(), d = Ue(), We(k.$$.fragment), I(s, "class", "border-none svelte-xtjjyg"), s.disabled = /*disabled*/
      l[4], I(s, "autocomplete", "off"), s.readOnly = r = !/*filterable*/
      l[8], Ae(s, "subdued", !/*choices_names*/
      l[15].includes(
        /*input_text*/
        l[10]
      ) && !/*allow_custom_value*/
      l[7] || /*selected_indices*/
      l[12].length === /*max_choices*/
      l[2]), I(o, "class", "secondary-wrap svelte-xtjjyg"), I(f, "class", "wrap-inner svelte-xtjjyg"), Ae(
        f,
        "show_options",
        /*show_options*/
        l[14]
      ), I(i, "class", "wrap svelte-xtjjyg"), I(e, "class", "svelte-xtjjyg"), Ae(
        e,
        "container",
        /*container*/
        l[6]
      );
    },
    m(c, v) {
      ge(c, e, v), $e(t, e, null), fe(e, n), fe(e, i), fe(i, f);
      for (let g = 0; g < m.length; g += 1)
        m[g] && m[g].m(f, null);
      fe(f, u), fe(f, o), fe(o, s), Ol(
        s,
        /*input_text*/
        l[10]
      ), l[34](s), fe(o, a), _ && _.m(o, null), fe(i, d), $e(k, i, null), h = !0, C || (y = [
        me(
          s,
          "input",
          /*input_input_handler*/
          l[33]
        ),
        me(
          s,
          "keydown",
          /*handle_key_down*/
          l[23]
        ),
        me(
          s,
          "keyup",
          /*keyup_handler*/
          l[35]
        ),
        me(
          s,
          "blur",
          /*handle_blur*/
          l[18]
        ),
        me(
          s,
          "focus",
          /*handle_focus*/
          l[22]
        )
      ], C = !0);
    },
    p(c, v) {
      const g = {};
      if (v[0] & /*show_label*/
      32 && (g.show_label = /*show_label*/
      c[5]), v[0] & /*info*/
      2 && (g.info = /*info*/
      c[1]), v[0] & /*label*/
      1 | v[1] & /*$$scope*/
      4096 && (g.$$scope = { dirty: v, ctx: c }), t.$set(g), v[0] & /*i18n, selected_indices, remove_selected_choice, disabled, choices_names*/
      561680) {
        b = zl(
          /*selected_indices*/
          c[12]
        );
        let j;
        for (j = 0; j < b.length; j += 1) {
          const L = Al(c, b, j);
          m[j] ? (m[j].p(L, v), X(m[j], 1)) : (m[j] = Dl(L), m[j].c(), X(m[j], 1), m[j].m(f, u));
        }
        for (bt(), j = b.length; j < m.length; j += 1)
          w(j);
        mt();
      }
      (!h || v[0] & /*disabled*/
      16) && (s.disabled = /*disabled*/
      c[4]), (!h || v[0] & /*filterable*/
      256 && r !== (r = !/*filterable*/
      c[8])) && (s.readOnly = r), v[0] & /*input_text*/
      1024 && s.value !== /*input_text*/
      c[10] && Ol(
        s,
        /*input_text*/
        c[10]
      ), (!h || v[0] & /*choices_names, input_text, allow_custom_value, selected_indices, max_choices*/
      38020) && Ae(s, "subdued", !/*choices_names*/
      c[15].includes(
        /*input_text*/
        c[10]
      ) && !/*allow_custom_value*/
      c[7] || /*selected_indices*/
      c[12].length === /*max_choices*/
      c[2]), /*disabled*/
      c[4] ? _ && (bt(), $(_, 1, 1, () => {
        _ = null;
      }), mt()) : _ ? (_.p(c, v), v[0] & /*disabled*/
      16 && X(_, 1)) : (_ = Bl(c), _.c(), X(_, 1), _.m(o, null)), (!h || v[0] & /*show_options*/
      16384) && Ae(
        f,
        "show_options",
        /*show_options*/
        c[14]
      );
      const F = {};
      v[0] & /*show_options*/
      16384 && (F.show_options = /*show_options*/
      c[14]), v[0] & /*choices*/
      8 && (F.choices = /*choices*/
      c[3]), v[0] & /*filtered_indices*/
      2048 && (F.filtered_indices = /*filtered_indices*/
      c[11]), v[0] & /*disabled*/
      16 && (F.disabled = /*disabled*/
      c[4]), v[0] & /*selected_indices*/
      4096 && (F.selected_indices = /*selected_indices*/
      c[12]), v[0] & /*active_index*/
      65536 && (F.active_index = /*active_index*/
      c[16]), k.$set(F), (!h || v[0] & /*container*/
      64) && Ae(
        e,
        "container",
        /*container*/
        c[6]
      );
    },
    i(c) {
      if (!h) {
        X(t.$$.fragment, c);
        for (let v = 0; v < b.length; v += 1)
          X(m[v]);
        X(_), X(k.$$.fragment, c), h = !0;
      }
    },
    o(c) {
      $(t.$$.fragment, c), m = m.filter(Boolean);
      for (let v = 0; v < m.length; v += 1)
        $(m[v]);
      $(_), $(k.$$.fragment, c), h = !1;
    },
    d(c) {
      c && he(e), xe(t), po(m, c), l[34](null), _ && _.d(), xe(k), C = !1, Pt(y);
    }
  };
}
function Fo(l, e, t) {
  let { label: n } = e, { info: i = void 0 } = e, { value: f = [] } = e, u = [], { value_is_output: o = !1 } = e, { max_choices: s = null } = e, { choices: r } = e, a, { disabled: d = !1 } = e, { show_label: k } = e, { container: h = !0 } = e, { allow_custom_value: C = !1 } = e, { filterable: y = !0 } = e, { i18n: b } = e, m, w = "", _ = "", c = !1, v, g, F = [], j = null, L = [], U = [];
  const Z = jo();
  Array.isArray(f) && f.forEach((p) => {
    const H = r.map((ke) => ke[1]).indexOf(p);
    H !== -1 ? L.push(H) : L.push(p);
  });
  function ee() {
    C || t(10, w = ""), C && w !== "" && (J(w), t(10, w = "")), t(14, c = !1), t(16, j = null), Z("blur");
  }
  function N(p) {
    t(12, L = L.filter((H) => H !== p)), Z("select", {
      index: typeof p == "number" ? p : -1,
      value: typeof p == "number" ? g[p] : p,
      selected: !1
    });
  }
  function J(p) {
    (s === null || L.length < s) && (t(12, L = [...L, p]), Z("select", {
      index: typeof p == "number" ? p : -1,
      value: typeof p == "number" ? g[p] : p,
      selected: !0
    })), L.length === s && (t(14, c = !1), t(16, j = null), m.blur());
  }
  function R(p) {
    const H = parseInt(p.detail.target.dataset.index);
    de(H);
  }
  function de(p) {
    L.includes(p) ? N(p) : J(p), t(10, w = "");
  }
  function we(p) {
    t(12, L = []), t(10, w = ""), p.preventDefault();
  }
  function pe(p) {
    t(11, F = r.map((H, ke) => ke)), (s === null || L.length < s) && t(14, c = !0), Z("focus");
  }
  function q(p) {
    t(14, [c, j] = en(p, j, F), c, (t(16, j), t(3, r), t(27, a), t(10, w), t(28, _), t(7, C), t(11, F))), p.key === "Enter" && (j !== null ? de(j) : C && (J(w), t(10, w = ""))), p.key === "Backspace" && w === "" && t(12, L = [...L.slice(0, -1)]), L.length === s && (t(14, c = !1), t(16, j = null));
  }
  function E() {
    f === void 0 ? t(12, L = []) : Array.isArray(f) && t(12, L = f.map((p) => {
      const H = g.indexOf(p);
      if (H !== -1)
        return H;
      if (C)
        return p;
    }).filter((p) => p !== void 0));
  }
  yo(() => {
    t(25, o = !1);
  });
  const Y = (p) => N(p), V = (p, H) => {
    H.key === "Enter" && N(p);
  };
  function S() {
    w = this.value, t(10, w);
  }
  function D(p) {
    wo[p ? "unshift" : "push"](() => {
      m = p, t(13, m);
    });
  }
  const O = (p) => Z("key_up", { key: p.key, input_value: w }), se = (p) => {
    p.key === "Enter" && we(p);
  };
  return l.$$set = (p) => {
    "label" in p && t(0, n = p.label), "info" in p && t(1, i = p.info), "value" in p && t(24, f = p.value), "value_is_output" in p && t(25, o = p.value_is_output), "max_choices" in p && t(2, s = p.max_choices), "choices" in p && t(3, r = p.choices), "disabled" in p && t(4, d = p.disabled), "show_label" in p && t(5, k = p.show_label), "container" in p && t(6, h = p.container), "allow_custom_value" in p && t(7, C = p.allow_custom_value), "filterable" in p && t(8, y = p.filterable), "i18n" in p && t(9, b = p.i18n);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*choices*/
    8 && (t(15, v = r.map((p) => p[0])), t(29, g = r.map((p) => p[1]))), l.$$.dirty[0] & /*choices, old_choices, input_text, old_input_text, allow_custom_value, filtered_indices*/
    402656392 && (r !== a || w !== _) && (t(11, F = zt(r, w)), t(27, a = r), t(28, _ = w), C || t(16, j = F[0])), l.$$.dirty[0] & /*selected_indices, old_selected_index, choices_values*/
    1610616832 && JSON.stringify(L) != JSON.stringify(U) && (t(24, f = L.map((p) => typeof p == "number" ? g[p] : p)), t(30, U = L.slice())), l.$$.dirty[0] & /*value, old_value, value_is_output*/
    117440512 && JSON.stringify(f) != JSON.stringify(u) && ($l(Z, f, o), t(26, u = Array.isArray(f) ? f.slice() : f)), l.$$.dirty[0] & /*value*/
    16777216 && E();
  }, [
    n,
    i,
    s,
    r,
    d,
    k,
    h,
    C,
    y,
    b,
    w,
    F,
    L,
    m,
    c,
    v,
    j,
    Z,
    ee,
    N,
    R,
    we,
    pe,
    q,
    f,
    o,
    u,
    a,
    _,
    g,
    U,
    Y,
    V,
    S,
    D,
    O,
    se
  ];
}
class Yo extends go {
  constructor(e) {
    super(), ko(
      this,
      e,
      Fo,
      Eo,
      vo,
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
  SvelteComponent: Lo,
  add_flush_callback: No,
  append: K,
  assign: zo,
  attr: P,
  bind: Mo,
  binding_callbacks: Oo,
  check_outros: _n,
  create_component: gt,
  destroy_component: wt,
  detach: He,
  element: re,
  empty: Ao,
  get_spread_object: Vo,
  get_spread_update: Do,
  group_outros: cn,
  init: Bo,
  insert: Je,
  listen: Dt,
  mount_component: pt,
  run_all: To,
  safe_not_equal: Uo,
  set_input_value: Ul,
  space: je,
  text: Zo,
  transition_in: ce,
  transition_out: qe
} = window.__gradio__svelte__internal;
function Zl(l) {
  let e, t, n, i, f, u, o, s, r, a, d, k, h, C, y;
  function b(c) {
    l[19](c);
  }
  let m = {
    choices: (
      /*pipelines*/
      l[7]
    ),
    label: "Select the pipeline to use: ",
    info: (
      /*info*/
      l[3]
    ),
    show_label: (
      /*show_label*/
      l[8]
    ),
    container: (
      /*container*/
      l[10]
    ),
    disabled: !/*interactive*/
    l[15]
  };
  /*value_is_output*/
  l[2] !== void 0 && (m.value_is_output = /*value_is_output*/
  l[2]), o = new us({ props: m }), Oo.push(() => Mo(o, "value_is_output", b)), o.$on(
    "input",
    /*input_handler*/
    l[20]
  ), o.$on(
    "select",
    /*select_handler*/
    l[21]
  ), o.$on(
    "blur",
    /*blur_handler*/
    l[22]
  ), o.$on(
    "focus",
    /*focus_handler*/
    l[23]
  ), o.$on(
    "key_up",
    /*key_up_handler*/
    l[24]
  );
  let w = (
    /*enable_edition*/
    l[9] && Pl(l)
  ), _ = (
    /*value*/
    l[0].name !== "" && Il(l)
  );
  return {
    c() {
      e = re("div"), t = re("label"), t.textContent = "Enter your Hugging Face token:", n = je(), i = re("input"), u = je(), gt(o.$$.fragment), r = je(), w && w.c(), a = je(), d = re("div"), k = je(), _ && _.c(), P(t, "for", "token"), P(t, "class", "label svelte-1nstxj7"), P(i, "data-testid", "textbox"), P(i, "type", "text"), P(i, "class", "text-area svelte-1nstxj7"), P(i, "name", "token"), P(i, "id", "token"), P(i, "placeholder", "hf_xxxxxxx..."), P(i, "aria-label", "Enter your Hugging Face token"), P(i, "maxlength", "50"), i.disabled = f = !/*interactive*/
      l[15], P(d, "class", "params-control svelte-1nstxj7"), P(d, "id", "params-control"), P(e, "class", "form svelte-1nstxj7");
    },
    m(c, v) {
      Je(c, e, v), K(e, t), K(e, n), K(e, i), Ul(
        i,
        /*value*/
        l[0].token
      ), K(e, u), pt(o, e, null), K(e, r), w && w.m(e, null), K(e, a), K(e, d), K(e, k), _ && _.m(e, null), h = !0, C || (y = Dt(
        i,
        "input",
        /*input_input_handler*/
        l[18]
      ), C = !0);
    },
    p(c, v) {
      (!h || v[0] & /*interactive*/
      32768 && f !== (f = !/*interactive*/
      c[15])) && (i.disabled = f), v[0] & /*value*/
      1 && i.value !== /*value*/
      c[0].token && Ul(
        i,
        /*value*/
        c[0].token
      );
      const g = {};
      v[0] & /*pipelines*/
      128 && (g.choices = /*pipelines*/
      c[7]), v[0] & /*info*/
      8 && (g.info = /*info*/
      c[3]), v[0] & /*show_label*/
      256 && (g.show_label = /*show_label*/
      c[8]), v[0] & /*container*/
      1024 && (g.container = /*container*/
      c[10]), v[0] & /*interactive*/
      32768 && (g.disabled = !/*interactive*/
      c[15]), !s && v[0] & /*value_is_output*/
      4 && (s = !0, g.value_is_output = /*value_is_output*/
      c[2], No(() => s = !1)), o.$set(g), /*enable_edition*/
      c[9] ? w ? w.p(c, v) : (w = Pl(c), w.c(), w.m(e, a)) : w && (w.d(1), w = null), /*value*/
      c[0].name !== "" ? _ ? (_.p(c, v), v[0] & /*value*/
      1 && ce(_, 1)) : (_ = Il(c), _.c(), ce(_, 1), _.m(e, null)) : _ && (cn(), qe(_, 1, 1, () => {
        _ = null;
      }), _n());
    },
    i(c) {
      h || (ce(o.$$.fragment, c), ce(_), h = !0);
    },
    o(c) {
      qe(o.$$.fragment, c), qe(_), h = !1;
    },
    d(c) {
      c && He(e), wt(o), w && w.d(), _ && _.d(), C = !1, y();
    }
  };
}
function Pl(l) {
  let e, t, n, i, f, u, o, s, r, a, d;
  return {
    c() {
      e = re("div"), t = re("p"), t.textContent = "Show configuration", n = je(), i = re("label"), f = re("input"), o = je(), s = re("span"), P(f, "type", "checkbox"), f.disabled = u = /*value*/
      l[0].name == "", P(f, "class", "svelte-1nstxj7"), P(s, "class", "slider round svelte-1nstxj7"), P(i, "class", "switch svelte-1nstxj7"), P(i, "title", r = /*value*/
      l[0].name == "" ? "Please select a pipeline first" : "Show pipeline config"), P(e, "class", "toggle-config svelte-1nstxj7");
    },
    m(k, h) {
      Je(k, e, h), K(e, t), K(e, n), K(e, i), K(i, f), f.checked = /*show_config*/
      l[1], K(i, o), K(i, s), a || (d = [
        Dt(
          f,
          "change",
          /*input_change_handler*/
          l[25]
        ),
        Dt(
          f,
          "input",
          /*input_handler_1*/
          l[26]
        )
      ], a = !0);
    },
    p(k, h) {
      h[0] & /*value*/
      1 && u !== (u = /*value*/
      k[0].name == "") && (f.disabled = u), h[0] & /*show_config*/
      2 && (f.checked = /*show_config*/
      k[1]), h[0] & /*value*/
      1 && r !== (r = /*value*/
      k[0].name == "" ? "Please select a pipeline first" : "Show pipeline config") && P(i, "title", r);
    },
    d(k) {
      k && He(e), a = !1, To(d);
    }
  };
}
function Il(l) {
  let e, t, n;
  return t = new oo({
    props: {
      elem_id: (
        /*elem_id*/
        l[4]
      ),
      elem_classes: (
        /*elem_classes*/
        l[5]
      ),
      scale: (
        /*scale*/
        l[11]
      ),
      min_width: (
        /*min_width*/
        l[12]
      ),
      visible: (
        /*show_config*/
        l[1]
      ),
      $$slots: { default: [Po] },
      $$scope: { ctx: l }
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[27]
  ), {
    c() {
      e = re("div"), gt(t.$$.fragment), P(e, "class", "validation svelte-1nstxj7");
    },
    m(i, f) {
      Je(i, e, f), pt(t, e, null), n = !0;
    },
    p(i, f) {
      const u = {};
      f[0] & /*elem_id*/
      16 && (u.elem_id = /*elem_id*/
      i[4]), f[0] & /*elem_classes*/
      32 && (u.elem_classes = /*elem_classes*/
      i[5]), f[0] & /*scale*/
      2048 && (u.scale = /*scale*/
      i[11]), f[0] & /*min_width*/
      4096 && (u.min_width = /*min_width*/
      i[12]), f[0] & /*show_config*/
      2 && (u.visible = /*show_config*/
      i[1]), f[1] & /*$$scope*/
      2 && (u.$$scope = { dirty: f, ctx: i }), t.$set(u);
    },
    i(i) {
      n || (ce(t.$$.fragment, i), n = !0);
    },
    o(i) {
      qe(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && He(e), wt(t);
    }
  };
}
function Po(l) {
  let e;
  return {
    c() {
      e = Zo("Update parameters");
    },
    m(t, n) {
      Je(t, e, n);
    },
    d(t) {
      t && He(e);
    }
  };
}
function Io(l) {
  let e, t, n, i;
  const f = [
    {
      autoscroll: (
        /*gradio*/
        l[14].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      l[14].i18n
    ) },
    /*loading_status*/
    l[13]
  ];
  let u = {};
  for (let s = 0; s < f.length; s += 1)
    u = zo(u, f[s]);
  e = new Xs({ props: u });
  let o = (
    /*visible*/
    l[6] && Zl(l)
  );
  return {
    c() {
      gt(e.$$.fragment), t = je(), o && o.c(), n = Ao();
    },
    m(s, r) {
      pt(e, s, r), Je(s, t, r), o && o.m(s, r), Je(s, n, r), i = !0;
    },
    p(s, r) {
      const a = r[0] & /*gradio, loading_status*/
      24576 ? Do(f, [
        r[0] & /*gradio*/
        16384 && {
          autoscroll: (
            /*gradio*/
            s[14].autoscroll
          )
        },
        r[0] & /*gradio*/
        16384 && { i18n: (
          /*gradio*/
          s[14].i18n
        ) },
        r[0] & /*loading_status*/
        8192 && Vo(
          /*loading_status*/
          s[13]
        )
      ]) : {};
      e.$set(a), /*visible*/
      s[6] ? o ? (o.p(s, r), r[0] & /*visible*/
      64 && ce(o, 1)) : (o = Zl(s), o.c(), ce(o, 1), o.m(n.parentNode, n)) : o && (cn(), qe(o, 1, 1, () => {
        o = null;
      }), _n());
    },
    i(s) {
      i || (ce(e.$$.fragment, s), ce(o), i = !0);
    },
    o(s) {
      qe(e.$$.fragment, s), qe(o), i = !1;
    },
    d(s) {
      s && (He(t), He(n)), wt(e, s), o && o.d(s);
    }
  };
}
function Ho(l) {
  let e, t;
  return e = new Kn({
    props: {
      visible: (
        /*visible*/
        l[6]
      ),
      elem_id: (
        /*elem_id*/
        l[4]
      ),
      elem_classes: (
        /*elem_classes*/
        l[5]
      ),
      padding: (
        /*container*/
        l[10]
      ),
      allow_overflow: !1,
      scale: (
        /*scale*/
        l[11]
      ),
      min_width: (
        /*min_width*/
        l[12]
      ),
      $$slots: { default: [Io] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      gt(e.$$.fragment);
    },
    m(n, i) {
      pt(e, n, i), t = !0;
    },
    p(n, i) {
      const f = {};
      i[0] & /*visible*/
      64 && (f.visible = /*visible*/
      n[6]), i[0] & /*elem_id*/
      16 && (f.elem_id = /*elem_id*/
      n[4]), i[0] & /*elem_classes*/
      32 && (f.elem_classes = /*elem_classes*/
      n[5]), i[0] & /*container*/
      1024 && (f.padding = /*container*/
      n[10]), i[0] & /*scale*/
      2048 && (f.scale = /*scale*/
      n[11]), i[0] & /*min_width*/
      4096 && (f.min_width = /*min_width*/
      n[12]), i[0] & /*elem_id, elem_classes, scale, min_width, show_config, gradio, value, paramsViewNeedUpdate, enable_edition, pipelines, info, show_label, container, interactive, value_is_output, visible, loading_status*/
      131071 | i[1] & /*$$scope*/
      2 && (f.$$scope = { dirty: i, ctx: n }), e.$set(f);
    },
    i(n) {
      t || (ce(e.$$.fragment, n), t = !0);
    },
    o(n) {
      qe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      wt(e, n);
    }
  };
}
function Bt(l) {
  const e = /* @__PURE__ */ new Map();
  if (!l)
    return e;
  for (const t in l)
    l.hasOwnProperty(t) && (typeof l[t] == "object" && l[t] !== null ? e.set(t, Bt(l[t])) : e.set(t, l[t]));
  return e;
}
function dn(l) {
  return Object.fromEntries(Array.from(l.entries(), ([t, n]) => n instanceof Map ? [t, dn(n)] : [t, n]));
}
function Tt(l, e) {
  const t = document.createElement("label");
  t.textContent = e, l.appendChild(t);
}
function Jo(l, e, t) {
  const n = document.createElement("input"), i = l.id;
  Tt(l, i.split("-").at(-1)), n.type = "number", n.value = e, n.contentEditable = String(t), l.appendChild(n);
}
function Ro(l, e, t) {
  let { info: n = void 0 } = e, { elem_id: i = "" } = e, { elem_classes: f = [] } = e, { visible: u = !0 } = e, { value: o = new Ys({ name: "", token: "" }) } = e, { value_is_output: s = !1 } = e, { pipelines: r } = e, { show_label: a } = e, { show_config: d = !1 } = e, { enable_edition: k = !1 } = e, { container: h = !0 } = e, { scale: C = null } = e, { min_width: y = void 0 } = e, { loading_status: b } = e, { gradio: m } = e, { interactive: w } = e, _ = !1;
  function c(q) {
    q !== "" && (t(0, o.name = q, o), t(0, o.param_specs = {}, o), m.dispatch("select", o), t(16, _ = !0));
  }
  function v(q, E) {
    const Y = q.split("-");
    let V = Bt(o.param_specs);
    var S = V;
    Y.forEach((D) => {
      S = S.get(D);
    }), S.set("value", E), t(0, o.param_specs = dn(V), o);
  }
  function g(q, E, Y) {
    const V = document.createElement("select"), S = q.id;
    Tt(q, S.split("-").at(-1)), E.forEach((D) => {
      const O = document.createElement("option");
      O.textContent = D, O.value = D, V.appendChild(O), D === Y && (O.selected = !0);
    }), V.addEventListener("change", (D) => {
      v(S, V.value);
    }), q.appendChild(V);
  }
  function F(q, E, Y, V, S) {
    const D = document.createElement("input"), O = document.createElement("input"), se = q.id;
    Tt(q, se.split("-").at(-1)), D.type = "range", D.min = E, D.max = Y, D.value = V, D.step = S, D.addEventListener("input", (p) => {
      O.value = D.value, v(se, D.value);
    }), q.appendChild(D), O.type = "number", O.min = E, O.max = Y, O.value = V, O.step = S, O.contentEditable = "true", O.addEventListener("input", (p) => {
      D.value = O.value, v(se, D.value);
    }), q.appendChild(O);
  }
  function j(q, E, Y) {
    E.forEach((V, S) => {
      const D = (Y ? Y + "-" : "") + S;
      if (V.values().next().value instanceof Map) {
        const O = document.createElement("fieldset");
        O.innerHTML = "<legend>" + D + "<legend>", O.id = D, q.appendChild(O), j(O, V, S);
      } else {
        const O = document.createElement("div");
        switch (O.id = D, O.classList.add("param"), q.appendChild(O), V.get("component")) {
          case "slider":
            F(O, V.get("min"), V.get("max"), V.get("value"), V.get("step"));
            break;
          case "dropdown":
            g(O, V.get("choices"), V.get("value"));
            break;
          case "textbox":
            Jo(O, V.get("value"), !1);
            break;
        }
      }
    });
  }
  function L() {
    o.token = this.value, t(0, o);
  }
  function U(q) {
    s = q, t(2, s);
  }
  const Z = () => m.dispatch("input"), ee = (q) => c(q.detail.value), N = () => m.dispatch("blur"), J = () => m.dispatch("focus"), R = (q) => m.dispatch("key_up", q.detail);
  function de() {
    d = this.checked, t(1, d);
  }
  const we = () => {
    t(16, _ = !0), t(1, d = !d);
  }, pe = () => m.dispatch("change", o);
  return l.$$set = (q) => {
    "info" in q && t(3, n = q.info), "elem_id" in q && t(4, i = q.elem_id), "elem_classes" in q && t(5, f = q.elem_classes), "visible" in q && t(6, u = q.visible), "value" in q && t(0, o = q.value), "value_is_output" in q && t(2, s = q.value_is_output), "pipelines" in q && t(7, r = q.pipelines), "show_label" in q && t(8, a = q.show_label), "show_config" in q && t(1, d = q.show_config), "enable_edition" in q && t(9, k = q.enable_edition), "container" in q && t(10, h = q.container), "scale" in q && t(11, C = q.scale), "min_width" in q && t(12, y = q.min_width), "loading_status" in q && t(13, b = q.loading_status), "gradio" in q && t(14, m = q.gradio), "interactive" in q && t(15, w = q.interactive);
  }, l.$$.update = () => {
    if (l.$$.dirty[0] & /*value, paramsViewNeedUpdate, show_config*/
    65539 && Object.keys(o.param_specs).length > 0 && _) {
      const q = document.getElementById("params-control");
      if (q.replaceChildren(), d) {
        let E = Bt(o.param_specs);
        j(q, E), t(16, _ = !1);
      }
    }
  }, [
    o,
    d,
    s,
    n,
    i,
    f,
    u,
    r,
    a,
    k,
    h,
    C,
    y,
    b,
    m,
    w,
    _,
    c,
    L,
    U,
    Z,
    ee,
    N,
    J,
    R,
    de,
    we,
    pe
  ];
}
class Go extends Lo {
  constructor(e) {
    super(), Bo(
      this,
      e,
      Ro,
      Ho,
      Uo,
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
  us as BaseDropdown,
  Xo as BaseExample,
  Yo as BaseMultiselect,
  Go as default
};
