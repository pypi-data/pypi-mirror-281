const {
  SvelteComponent: Jt,
  assign: Xt,
  create_slot: Yt,
  detach: Gt,
  element: Rt,
  get_all_dirty_from_scope: Ht,
  get_slot_changes: Kt,
  get_spread_update: Qt,
  init: Ut,
  insert: Wt,
  safe_not_equal: xt,
  set_dynamic_element_data: Qe,
  set_style: T,
  toggle_class: W,
  transition_in: yt,
  transition_out: qt,
  update_slot_base: $t
} = window.__gradio__svelte__internal;
function el(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), s = Yt(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let a = [
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
      l[3].join(" ") + " svelte-nl1om8"
    }
  ], r = {};
  for (let f = 0; f < a.length; f += 1)
    r = Xt(r, a[f]);
  return {
    c() {
      e = Rt(
        /*tag*/
        l[14]
      ), s && s.c(), Qe(
        /*tag*/
        l[14]
      )(e, r), W(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), W(
        e,
        "padded",
        /*padding*/
        l[6]
      ), W(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), W(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), W(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), T(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), T(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), T(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), T(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), T(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), T(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), T(e, "border-width", "var(--block-border-width)");
    },
    m(f, o) {
      Wt(f, e, o), s && s.m(e, null), n = !0;
    },
    p(f, o) {
      s && s.p && (!n || o & /*$$scope*/
      131072) && $t(
        s,
        i,
        f,
        /*$$scope*/
        f[17],
        n ? Kt(
          i,
          /*$$scope*/
          f[17],
          o,
          null
        ) : Ht(
          /*$$scope*/
          f[17]
        ),
        null
      ), Qe(
        /*tag*/
        f[14]
      )(e, r = Qt(a, [
        (!n || o & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          f[7]
        ) },
        (!n || o & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          f[2]
        ) },
        (!n || o & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        f[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), W(
        e,
        "hidden",
        /*visible*/
        f[10] === !1
      ), W(
        e,
        "padded",
        /*padding*/
        f[6]
      ), W(
        e,
        "border_focus",
        /*border_mode*/
        f[5] === "focus"
      ), W(
        e,
        "border_contrast",
        /*border_mode*/
        f[5] === "contrast"
      ), W(e, "hide-container", !/*explicit_call*/
      f[8] && !/*container*/
      f[9]), o & /*height*/
      1 && T(
        e,
        "height",
        /*get_dimension*/
        f[15](
          /*height*/
          f[0]
        )
      ), o & /*width*/
      2 && T(e, "width", typeof /*width*/
      f[1] == "number" ? `calc(min(${/*width*/
      f[1]}px, 100%))` : (
        /*get_dimension*/
        f[15](
          /*width*/
          f[1]
        )
      )), o & /*variant*/
      16 && T(
        e,
        "border-style",
        /*variant*/
        f[4]
      ), o & /*allow_overflow*/
      2048 && T(
        e,
        "overflow",
        /*allow_overflow*/
        f[11] ? "visible" : "hidden"
      ), o & /*scale*/
      4096 && T(
        e,
        "flex-grow",
        /*scale*/
        f[12]
      ), o & /*min_width*/
      8192 && T(e, "min-width", `calc(min(${/*min_width*/
      f[13]}px, 100%))`);
    },
    i(f) {
      n || (yt(s, f), n = !0);
    },
    o(f) {
      qt(s, f), n = !1;
    },
    d(f) {
      f && Gt(e), s && s.d(f);
    }
  };
}
function tl(l) {
  let e, t = (
    /*tag*/
    l[14] && el(l)
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
      e || (yt(t, n), e = !0);
    },
    o(n) {
      qt(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function ll(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: s = void 0 } = e, { width: a = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: f = [] } = e, { variant: o = "solid" } = e, { border_mode: u = "base" } = e, { padding: _ = !0 } = e, { type: m = "normal" } = e, { test_id: b = void 0 } = e, { explicit_call: q = !1 } = e, { container: V = !0 } = e, { visible: v = !0 } = e, { allow_overflow: I = !0 } = e, { scale: d = null } = e, { min_width: c = 0 } = e, S = m === "fieldset" ? "fieldset" : "div";
  const z = (h) => {
    if (h !== void 0) {
      if (typeof h == "number")
        return h + "px";
      if (typeof h == "string")
        return h;
    }
  };
  return l.$$set = (h) => {
    "height" in h && t(0, s = h.height), "width" in h && t(1, a = h.width), "elem_id" in h && t(2, r = h.elem_id), "elem_classes" in h && t(3, f = h.elem_classes), "variant" in h && t(4, o = h.variant), "border_mode" in h && t(5, u = h.border_mode), "padding" in h && t(6, _ = h.padding), "type" in h && t(16, m = h.type), "test_id" in h && t(7, b = h.test_id), "explicit_call" in h && t(8, q = h.explicit_call), "container" in h && t(9, V = h.container), "visible" in h && t(10, v = h.visible), "allow_overflow" in h && t(11, I = h.allow_overflow), "scale" in h && t(12, d = h.scale), "min_width" in h && t(13, c = h.min_width), "$$scope" in h && t(17, i = h.$$scope);
  }, [
    s,
    a,
    r,
    f,
    o,
    u,
    _,
    b,
    q,
    V,
    v,
    I,
    d,
    c,
    S,
    z,
    m,
    i,
    n
  ];
}
class nl extends Jt {
  constructor(e) {
    super(), Ut(this, e, ll, tl, xt, {
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
  SvelteComponent: il,
  attr: fl,
  create_slot: sl,
  detach: ol,
  element: al,
  get_all_dirty_from_scope: rl,
  get_slot_changes: ul,
  init: _l,
  insert: cl,
  safe_not_equal: dl,
  transition_in: ml,
  transition_out: bl,
  update_slot_base: gl
} = window.__gradio__svelte__internal;
function hl(l) {
  let e, t;
  const n = (
    /*#slots*/
    l[1].default
  ), i = sl(
    n,
    l,
    /*$$scope*/
    l[0],
    null
  );
  return {
    c() {
      e = al("div"), i && i.c(), fl(e, "class", "svelte-1hnfib2");
    },
    m(s, a) {
      cl(s, e, a), i && i.m(e, null), t = !0;
    },
    p(s, [a]) {
      i && i.p && (!t || a & /*$$scope*/
      1) && gl(
        i,
        n,
        s,
        /*$$scope*/
        s[0],
        t ? ul(
          n,
          /*$$scope*/
          s[0],
          a,
          null
        ) : rl(
          /*$$scope*/
          s[0]
        ),
        null
      );
    },
    i(s) {
      t || (ml(i, s), t = !0);
    },
    o(s) {
      bl(i, s), t = !1;
    },
    d(s) {
      s && ol(e), i && i.d(s);
    }
  };
}
function wl(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  return l.$$set = (s) => {
    "$$scope" in s && t(0, i = s.$$scope);
  }, [i, n];
}
class pl extends il {
  constructor(e) {
    super(), _l(this, e, wl, hl, dl, {});
  }
}
const {
  SvelteComponent: kl,
  attr: Ue,
  check_outros: vl,
  create_component: yl,
  create_slot: ql,
  destroy_component: Cl,
  detach: ze,
  element: Fl,
  empty: Ll,
  get_all_dirty_from_scope: Sl,
  get_slot_changes: zl,
  group_outros: Ml,
  init: Vl,
  insert: Me,
  mount_component: Nl,
  safe_not_equal: Il,
  set_data: Zl,
  space: jl,
  text: Pl,
  toggle_class: ue,
  transition_in: we,
  transition_out: Ve,
  update_slot_base: Bl
} = window.__gradio__svelte__internal;
function We(l) {
  let e, t;
  return e = new pl({
    props: {
      $$slots: { default: [Al] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      yl(e.$$.fragment);
    },
    m(n, i) {
      Nl(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i & /*$$scope, info*/
      10 && (s.$$scope = { dirty: i, ctx: n }), e.$set(s);
    },
    i(n) {
      t || (we(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ve(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Cl(e, n);
    }
  };
}
function Al(l) {
  let e;
  return {
    c() {
      e = Pl(
        /*info*/
        l[1]
      );
    },
    m(t, n) {
      Me(t, e, n);
    },
    p(t, n) {
      n & /*info*/
      2 && Zl(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && ze(e);
    }
  };
}
function Dl(l) {
  let e, t, n, i;
  const s = (
    /*#slots*/
    l[2].default
  ), a = ql(
    s,
    l,
    /*$$scope*/
    l[3],
    null
  );
  let r = (
    /*info*/
    l[1] && We(l)
  );
  return {
    c() {
      e = Fl("span"), a && a.c(), t = jl(), r && r.c(), n = Ll(), Ue(e, "data-testid", "block-info"), Ue(e, "class", "svelte-22c38v"), ue(e, "sr-only", !/*show_label*/
      l[0]), ue(e, "hide", !/*show_label*/
      l[0]), ue(
        e,
        "has-info",
        /*info*/
        l[1] != null
      );
    },
    m(f, o) {
      Me(f, e, o), a && a.m(e, null), Me(f, t, o), r && r.m(f, o), Me(f, n, o), i = !0;
    },
    p(f, [o]) {
      a && a.p && (!i || o & /*$$scope*/
      8) && Bl(
        a,
        s,
        f,
        /*$$scope*/
        f[3],
        i ? zl(
          s,
          /*$$scope*/
          f[3],
          o,
          null
        ) : Sl(
          /*$$scope*/
          f[3]
        ),
        null
      ), (!i || o & /*show_label*/
      1) && ue(e, "sr-only", !/*show_label*/
      f[0]), (!i || o & /*show_label*/
      1) && ue(e, "hide", !/*show_label*/
      f[0]), (!i || o & /*info*/
      2) && ue(
        e,
        "has-info",
        /*info*/
        f[1] != null
      ), /*info*/
      f[1] ? r ? (r.p(f, o), o & /*info*/
      2 && we(r, 1)) : (r = We(f), r.c(), we(r, 1), r.m(n.parentNode, n)) : r && (Ml(), Ve(r, 1, 1, () => {
        r = null;
      }), vl());
    },
    i(f) {
      i || (we(a, f), we(r), i = !0);
    },
    o(f) {
      Ve(a, f), Ve(r), i = !1;
    },
    d(f) {
      f && (ze(e), ze(t), ze(n)), a && a.d(f), r && r.d(f);
    }
  };
}
function El(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { show_label: s = !0 } = e, { info: a = void 0 } = e;
  return l.$$set = (r) => {
    "show_label" in r && t(0, s = r.show_label), "info" in r && t(1, a = r.info), "$$scope" in r && t(3, i = r.$$scope);
  }, [s, a, n, i];
}
class Tl extends kl {
  constructor(e) {
    super(), Vl(this, e, El, Dl, Il, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: Ol,
  append: De,
  attr: te,
  bubble: Jl,
  create_component: Xl,
  destroy_component: Yl,
  detach: Ct,
  element: Ee,
  init: Gl,
  insert: Ft,
  listen: Rl,
  mount_component: Hl,
  safe_not_equal: Kl,
  set_data: Ql,
  set_style: _e,
  space: Ul,
  text: Wl,
  toggle_class: A,
  transition_in: xl,
  transition_out: $l
} = window.__gradio__svelte__internal;
function xe(l) {
  let e, t;
  return {
    c() {
      e = Ee("span"), t = Wl(
        /*label*/
        l[1]
      ), te(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      Ft(n, e, i), De(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && Ql(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && Ct(e);
    }
  };
}
function en(l) {
  let e, t, n, i, s, a, r, f = (
    /*show_label*/
    l[2] && xe(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = Ee("button"), f && f.c(), t = Ul(), n = Ee("div"), Xl(i.$$.fragment), te(n, "class", "svelte-1lrphxw"), A(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), A(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), A(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], te(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), te(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), te(
        e,
        "title",
        /*label*/
        l[1]
      ), te(e, "class", "svelte-1lrphxw"), A(
        e,
        "pending",
        /*pending*/
        l[3]
      ), A(
        e,
        "padded",
        /*padded*/
        l[5]
      ), A(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), A(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), _e(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), _e(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), _e(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(o, u) {
      Ft(o, e, u), f && f.m(e, null), De(e, t), De(e, n), Hl(i, n, null), s = !0, a || (r = Rl(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), a = !0);
    },
    p(o, [u]) {
      /*show_label*/
      o[2] ? f ? f.p(o, u) : (f = xe(o), f.c(), f.m(e, t)) : f && (f.d(1), f = null), (!s || u & /*size*/
      16) && A(
        n,
        "small",
        /*size*/
        o[4] === "small"
      ), (!s || u & /*size*/
      16) && A(
        n,
        "large",
        /*size*/
        o[4] === "large"
      ), (!s || u & /*size*/
      16) && A(
        n,
        "medium",
        /*size*/
        o[4] === "medium"
      ), (!s || u & /*disabled*/
      128) && (e.disabled = /*disabled*/
      o[7]), (!s || u & /*label*/
      2) && te(
        e,
        "aria-label",
        /*label*/
        o[1]
      ), (!s || u & /*hasPopup*/
      256) && te(
        e,
        "aria-haspopup",
        /*hasPopup*/
        o[8]
      ), (!s || u & /*label*/
      2) && te(
        e,
        "title",
        /*label*/
        o[1]
      ), (!s || u & /*pending*/
      8) && A(
        e,
        "pending",
        /*pending*/
        o[3]
      ), (!s || u & /*padded*/
      32) && A(
        e,
        "padded",
        /*padded*/
        o[5]
      ), (!s || u & /*highlight*/
      64) && A(
        e,
        "highlight",
        /*highlight*/
        o[6]
      ), (!s || u & /*transparent*/
      512) && A(
        e,
        "transparent",
        /*transparent*/
        o[9]
      ), u & /*disabled, _color*/
      4224 && _e(e, "color", !/*disabled*/
      o[7] && /*_color*/
      o[12] ? (
        /*_color*/
        o[12]
      ) : "var(--block-label-text-color)"), u & /*disabled, background*/
      1152 && _e(e, "--bg-color", /*disabled*/
      o[7] ? "auto" : (
        /*background*/
        o[10]
      )), u & /*offset*/
      2048 && _e(
        e,
        "margin-left",
        /*offset*/
        o[11] + "px"
      );
    },
    i(o) {
      s || (xl(i.$$.fragment, o), s = !0);
    },
    o(o) {
      $l(i.$$.fragment, o), s = !1;
    },
    d(o) {
      o && Ct(e), f && f.d(), Yl(i), a = !1, r();
    }
  };
}
function tn(l, e, t) {
  let n, { Icon: i } = e, { label: s = "" } = e, { show_label: a = !1 } = e, { pending: r = !1 } = e, { size: f = "small" } = e, { padded: o = !0 } = e, { highlight: u = !1 } = e, { disabled: _ = !1 } = e, { hasPopup: m = !1 } = e, { color: b = "var(--block-label-text-color)" } = e, { transparent: q = !1 } = e, { background: V = "var(--background-fill-primary)" } = e, { offset: v = 0 } = e;
  function I(d) {
    Jl.call(this, l, d);
  }
  return l.$$set = (d) => {
    "Icon" in d && t(0, i = d.Icon), "label" in d && t(1, s = d.label), "show_label" in d && t(2, a = d.show_label), "pending" in d && t(3, r = d.pending), "size" in d && t(4, f = d.size), "padded" in d && t(5, o = d.padded), "highlight" in d && t(6, u = d.highlight), "disabled" in d && t(7, _ = d.disabled), "hasPopup" in d && t(8, m = d.hasPopup), "color" in d && t(13, b = d.color), "transparent" in d && t(9, q = d.transparent), "background" in d && t(10, V = d.background), "offset" in d && t(11, v = d.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = u ? "var(--color-accent)" : b);
  }, [
    i,
    s,
    a,
    r,
    f,
    o,
    u,
    _,
    m,
    q,
    V,
    v,
    n,
    b,
    I
  ];
}
class ln extends Ol {
  constructor(e) {
    super(), Gl(this, e, tn, en, Kl, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: nn,
  append: Pe,
  attr: G,
  detach: fn,
  init: sn,
  insert: on,
  noop: Be,
  safe_not_equal: an,
  set_style: x,
  svg_element: Fe
} = window.__gradio__svelte__internal;
function rn(l) {
  let e, t, n, i;
  return {
    c() {
      e = Fe("svg"), t = Fe("g"), n = Fe("path"), i = Fe("path"), G(n, "d", "M18,6L6.087,17.913"), x(n, "fill", "none"), x(n, "fill-rule", "nonzero"), x(n, "stroke-width", "2px"), G(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), G(i, "d", "M4.364,4.364L19.636,19.636"), x(i, "fill", "none"), x(i, "fill-rule", "nonzero"), x(i, "stroke-width", "2px"), G(e, "width", "100%"), G(e, "height", "100%"), G(e, "viewBox", "0 0 24 24"), G(e, "version", "1.1"), G(e, "xmlns", "http://www.w3.org/2000/svg"), G(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), G(e, "xml:space", "preserve"), G(e, "stroke", "currentColor"), x(e, "fill-rule", "evenodd"), x(e, "clip-rule", "evenodd"), x(e, "stroke-linecap", "round"), x(e, "stroke-linejoin", "round");
    },
    m(s, a) {
      on(s, e, a), Pe(e, t), Pe(t, n), Pe(e, i);
    },
    p: Be,
    i: Be,
    o: Be,
    d(s) {
      s && fn(e);
    }
  };
}
class un extends nn {
  constructor(e) {
    super(), sn(this, e, null, rn, an, {});
  }
}
const _n = [
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
], $e = {
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
_n.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: $e[e][t],
      secondary: $e[e][n]
    }
  }),
  {}
);
function de(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function Ne() {
}
function cn(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const Lt = typeof window < "u";
let et = Lt ? () => window.performance.now() : () => Date.now(), St = Lt ? (l) => requestAnimationFrame(l) : Ne;
const be = /* @__PURE__ */ new Set();
function zt(l) {
  be.forEach((e) => {
    e.c(l) || (be.delete(e), e.f());
  }), be.size !== 0 && St(zt);
}
function dn(l) {
  let e;
  return be.size === 0 && St(zt), {
    promise: new Promise((t) => {
      be.add(e = { c: l, f: t });
    }),
    abort() {
      be.delete(e);
    }
  };
}
const ce = [];
function mn(l, e = Ne) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(r) {
    if (cn(l, r) && (l = r, t)) {
      const f = !ce.length;
      for (const o of n)
        o[1](), ce.push(o, l);
      if (f) {
        for (let o = 0; o < ce.length; o += 2)
          ce[o][0](ce[o + 1]);
        ce.length = 0;
      }
    }
  }
  function s(r) {
    i(r(l));
  }
  function a(r, f = Ne) {
    const o = [r, f];
    return n.add(o), n.size === 1 && (t = e(i, s) || Ne), r(l), () => {
      n.delete(o), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: s, subscribe: a };
}
function tt(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function Te(l, e, t, n) {
  if (typeof t == "number" || tt(t)) {
    const i = n - t, s = (t - e) / (l.dt || 1 / 60), a = l.opts.stiffness * i, r = l.opts.damping * s, f = (a - r) * l.inv_mass, o = (s + f) * l.dt;
    return Math.abs(o) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, tt(t) ? new Date(t.getTime() + o) : t + o);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, s) => Te(l, e[s], t[s], n[s])
      );
    if (typeof t == "object") {
      const i = {};
      for (const s in t)
        i[s] = Te(l, e[s], t[s], n[s]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function lt(l, e = {}) {
  const t = mn(l), { stiffness: n = 0.15, damping: i = 0.8, precision: s = 0.01 } = e;
  let a, r, f, o = l, u = l, _ = 1, m = 0, b = !1;
  function q(v, I = {}) {
    u = v;
    const d = f = {};
    return l == null || I.hard || V.stiffness >= 1 && V.damping >= 1 ? (b = !0, a = et(), o = v, t.set(l = u), Promise.resolve()) : (I.soft && (m = 1 / ((I.soft === !0 ? 0.5 : +I.soft) * 60), _ = 0), r || (a = et(), b = !1, r = dn((c) => {
      if (b)
        return b = !1, r = null, !1;
      _ = Math.min(_ + m, 1);
      const S = {
        inv_mass: _,
        opts: V,
        settled: !0,
        dt: (c - a) * 60 / 1e3
      }, z = Te(S, o, l, u);
      return a = c, o = l, t.set(l = z), S.settled && (r = null), !S.settled;
    })), new Promise((c) => {
      r.promise.then(() => {
        d === f && c();
      });
    }));
  }
  const V = {
    set: q,
    update: (v, I) => q(v(u, l), I),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: s
  };
  return V;
}
const {
  SvelteComponent: bn,
  append: R,
  attr: M,
  component_subscribe: nt,
  detach: gn,
  element: hn,
  init: wn,
  insert: pn,
  noop: it,
  safe_not_equal: kn,
  set_style: Le,
  svg_element: H,
  toggle_class: ft
} = window.__gradio__svelte__internal, { onMount: vn } = window.__gradio__svelte__internal;
function yn(l) {
  let e, t, n, i, s, a, r, f, o, u, _, m;
  return {
    c() {
      e = hn("div"), t = H("svg"), n = H("g"), i = H("path"), s = H("path"), a = H("path"), r = H("path"), f = H("g"), o = H("path"), u = H("path"), _ = H("path"), m = H("path"), M(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), M(i, "fill", "#FF7C00"), M(i, "fill-opacity", "0.4"), M(i, "class", "svelte-43sxxs"), M(s, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), M(s, "fill", "#FF7C00"), M(s, "class", "svelte-43sxxs"), M(a, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), M(a, "fill", "#FF7C00"), M(a, "fill-opacity", "0.4"), M(a, "class", "svelte-43sxxs"), M(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), M(r, "fill", "#FF7C00"), M(r, "class", "svelte-43sxxs"), Le(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), M(o, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), M(o, "fill", "#FF7C00"), M(o, "fill-opacity", "0.4"), M(o, "class", "svelte-43sxxs"), M(u, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), M(u, "fill", "#FF7C00"), M(u, "class", "svelte-43sxxs"), M(_, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), M(_, "fill", "#FF7C00"), M(_, "fill-opacity", "0.4"), M(_, "class", "svelte-43sxxs"), M(m, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), M(m, "fill", "#FF7C00"), M(m, "class", "svelte-43sxxs"), Le(f, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), M(t, "viewBox", "-1200 -1200 3000 3000"), M(t, "fill", "none"), M(t, "xmlns", "http://www.w3.org/2000/svg"), M(t, "class", "svelte-43sxxs"), M(e, "class", "svelte-43sxxs"), ft(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(b, q) {
      pn(b, e, q), R(e, t), R(t, n), R(n, i), R(n, s), R(n, a), R(n, r), R(t, f), R(f, o), R(f, u), R(f, _), R(f, m);
    },
    p(b, [q]) {
      q & /*$top*/
      2 && Le(n, "transform", "translate(" + /*$top*/
      b[1][0] + "px, " + /*$top*/
      b[1][1] + "px)"), q & /*$bottom*/
      4 && Le(f, "transform", "translate(" + /*$bottom*/
      b[2][0] + "px, " + /*$bottom*/
      b[2][1] + "px)"), q & /*margin*/
      1 && ft(
        e,
        "margin",
        /*margin*/
        b[0]
      );
    },
    i: it,
    o: it,
    d(b) {
      b && gn(e);
    }
  };
}
function qn(l, e, t) {
  let n, i;
  var s = this && this.__awaiter || function(b, q, V, v) {
    function I(d) {
      return d instanceof V ? d : new V(function(c) {
        c(d);
      });
    }
    return new (V || (V = Promise))(function(d, c) {
      function S(P) {
        try {
          h(v.next(P));
        } catch (N) {
          c(N);
        }
      }
      function z(P) {
        try {
          h(v.throw(P));
        } catch (N) {
          c(N);
        }
      }
      function h(P) {
        P.done ? d(P.value) : I(P.value).then(S, z);
      }
      h((v = v.apply(b, q || [])).next());
    });
  };
  let { margin: a = !0 } = e;
  const r = lt([0, 0]);
  nt(l, r, (b) => t(1, n = b));
  const f = lt([0, 0]);
  nt(l, f, (b) => t(2, i = b));
  let o;
  function u() {
    return s(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 140]), f.set([-125, -140])]), yield Promise.all([r.set([-125, 140]), f.set([125, -140])]), yield Promise.all([r.set([-125, 0]), f.set([125, -0])]), yield Promise.all([r.set([125, 0]), f.set([-125, 0])]);
    });
  }
  function _() {
    return s(this, void 0, void 0, function* () {
      yield u(), o || _();
    });
  }
  function m() {
    return s(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 0]), f.set([-125, 0])]), _();
    });
  }
  return vn(() => (m(), () => o = !0)), l.$$set = (b) => {
    "margin" in b && t(0, a = b.margin);
  }, [a, n, i, r, f];
}
class Cn extends bn {
  constructor(e) {
    super(), wn(this, e, qn, yn, kn, { margin: 0 });
  }
}
const {
  SvelteComponent: Fn,
  append: oe,
  attr: K,
  binding_callbacks: st,
  check_outros: Mt,
  create_component: Vt,
  create_slot: Ln,
  destroy_component: Nt,
  destroy_each: It,
  detach: C,
  element: ee,
  empty: ge,
  ensure_array_like: Ie,
  get_all_dirty_from_scope: Sn,
  get_slot_changes: zn,
  group_outros: Zt,
  init: Mn,
  insert: F,
  mount_component: jt,
  noop: Oe,
  safe_not_equal: Vn,
  set_data: X,
  set_style: ie,
  space: Q,
  text: j,
  toggle_class: J,
  transition_in: ae,
  transition_out: re,
  update_slot_base: Nn
} = window.__gradio__svelte__internal, { tick: In } = window.__gradio__svelte__internal, { onDestroy: Zn } = window.__gradio__svelte__internal, { createEventDispatcher: jn } = window.__gradio__svelte__internal, Pn = (l) => ({}), ot = (l) => ({});
function at(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n[43] = t, n;
}
function rt(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n;
}
function Bn(l) {
  let e, t, n, i, s = (
    /*i18n*/
    l[1]("common.error") + ""
  ), a, r, f;
  t = new ln({
    props: {
      Icon: un,
      label: (
        /*i18n*/
        l[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[32]
  );
  const o = (
    /*#slots*/
    l[30].error
  ), u = Ln(
    o,
    l,
    /*$$scope*/
    l[29],
    ot
  );
  return {
    c() {
      e = ee("div"), Vt(t.$$.fragment), n = Q(), i = ee("span"), a = j(s), r = Q(), u && u.c(), K(e, "class", "clear-status svelte-1yk38uw"), K(i, "class", "error svelte-1yk38uw");
    },
    m(_, m) {
      F(_, e, m), jt(t, e, null), F(_, n, m), F(_, i, m), oe(i, a), F(_, r, m), u && u.m(_, m), f = !0;
    },
    p(_, m) {
      const b = {};
      m[0] & /*i18n*/
      2 && (b.label = /*i18n*/
      _[1]("common.clear")), t.$set(b), (!f || m[0] & /*i18n*/
      2) && s !== (s = /*i18n*/
      _[1]("common.error") + "") && X(a, s), u && u.p && (!f || m[0] & /*$$scope*/
      536870912) && Nn(
        u,
        o,
        _,
        /*$$scope*/
        _[29],
        f ? zn(
          o,
          /*$$scope*/
          _[29],
          m,
          Pn
        ) : Sn(
          /*$$scope*/
          _[29]
        ),
        ot
      );
    },
    i(_) {
      f || (ae(t.$$.fragment, _), ae(u, _), f = !0);
    },
    o(_) {
      re(t.$$.fragment, _), re(u, _), f = !1;
    },
    d(_) {
      _ && (C(e), C(n), C(i), C(r)), Nt(t), u && u.d(_);
    }
  };
}
function An(l) {
  let e, t, n, i, s, a, r, f, o, u = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && ut(l)
  );
  function _(c, S) {
    if (
      /*progress*/
      c[7]
    )
      return Tn;
    if (
      /*queue_position*/
      c[2] !== null && /*queue_size*/
      c[3] !== void 0 && /*queue_position*/
      c[2] >= 0
    )
      return En;
    if (
      /*queue_position*/
      c[2] === 0
    )
      return Dn;
  }
  let m = _(l), b = m && m(l), q = (
    /*timer*/
    l[5] && dt(l)
  );
  const V = [Yn, Xn], v = [];
  function I(c, S) {
    return (
      /*last_progress_level*/
      c[15] != null ? 0 : (
        /*show_progress*/
        c[6] === "full" ? 1 : -1
      )
    );
  }
  ~(s = I(l)) && (a = v[s] = V[s](l));
  let d = !/*timer*/
  l[5] && kt(l);
  return {
    c() {
      u && u.c(), e = Q(), t = ee("div"), b && b.c(), n = Q(), q && q.c(), i = Q(), a && a.c(), r = Q(), d && d.c(), f = ge(), K(t, "class", "progress-text svelte-1yk38uw"), J(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), J(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(c, S) {
      u && u.m(c, S), F(c, e, S), F(c, t, S), b && b.m(t, null), oe(t, n), q && q.m(t, null), F(c, i, S), ~s && v[s].m(c, S), F(c, r, S), d && d.m(c, S), F(c, f, S), o = !0;
    },
    p(c, S) {
      /*variant*/
      c[8] === "default" && /*show_eta_bar*/
      c[18] && /*show_progress*/
      c[6] === "full" ? u ? u.p(c, S) : (u = ut(c), u.c(), u.m(e.parentNode, e)) : u && (u.d(1), u = null), m === (m = _(c)) && b ? b.p(c, S) : (b && b.d(1), b = m && m(c), b && (b.c(), b.m(t, n))), /*timer*/
      c[5] ? q ? q.p(c, S) : (q = dt(c), q.c(), q.m(t, null)) : q && (q.d(1), q = null), (!o || S[0] & /*variant*/
      256) && J(
        t,
        "meta-text-center",
        /*variant*/
        c[8] === "center"
      ), (!o || S[0] & /*variant*/
      256) && J(
        t,
        "meta-text",
        /*variant*/
        c[8] === "default"
      );
      let z = s;
      s = I(c), s === z ? ~s && v[s].p(c, S) : (a && (Zt(), re(v[z], 1, 1, () => {
        v[z] = null;
      }), Mt()), ~s ? (a = v[s], a ? a.p(c, S) : (a = v[s] = V[s](c), a.c()), ae(a, 1), a.m(r.parentNode, r)) : a = null), /*timer*/
      c[5] ? d && (d.d(1), d = null) : d ? d.p(c, S) : (d = kt(c), d.c(), d.m(f.parentNode, f));
    },
    i(c) {
      o || (ae(a), o = !0);
    },
    o(c) {
      re(a), o = !1;
    },
    d(c) {
      c && (C(e), C(t), C(i), C(r), C(f)), u && u.d(c), b && b.d(), q && q.d(), ~s && v[s].d(c), d && d.d(c);
    }
  };
}
function ut(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = ee("div"), K(e, "class", "eta-bar svelte-1yk38uw"), ie(e, "transform", t);
    },
    m(n, i) {
      F(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && ie(e, "transform", t);
    },
    d(n) {
      n && C(e);
    }
  };
}
function Dn(l) {
  let e;
  return {
    c() {
      e = j("processing |");
    },
    m(t, n) {
      F(t, e, n);
    },
    p: Oe,
    d(t) {
      t && C(e);
    }
  };
}
function En(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, s, a;
  return {
    c() {
      e = j("queue: "), n = j(t), i = j("/"), s = j(
        /*queue_size*/
        l[3]
      ), a = j(" |");
    },
    m(r, f) {
      F(r, e, f), F(r, n, f), F(r, i, f), F(r, s, f), F(r, a, f);
    },
    p(r, f) {
      f[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && X(n, t), f[0] & /*queue_size*/
      8 && X(
        s,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (C(e), C(n), C(i), C(s), C(a));
    }
  };
}
function Tn(l) {
  let e, t = Ie(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = ct(rt(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = ge();
    },
    m(i, s) {
      for (let a = 0; a < n.length; a += 1)
        n[a] && n[a].m(i, s);
      F(i, e, s);
    },
    p(i, s) {
      if (s[0] & /*progress*/
      128) {
        t = Ie(
          /*progress*/
          i[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const r = rt(i, t, a);
          n[a] ? n[a].p(r, s) : (n[a] = ct(r), n[a].c(), n[a].m(e.parentNode, e));
        }
        for (; a < n.length; a += 1)
          n[a].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && C(e), It(n, i);
    }
  };
}
function _t(l) {
  let e, t = (
    /*p*/
    l[41].unit + ""
  ), n, i, s = " ", a;
  function r(u, _) {
    return (
      /*p*/
      u[41].length != null ? Jn : On
    );
  }
  let f = r(l), o = f(l);
  return {
    c() {
      o.c(), e = Q(), n = j(t), i = j(" | "), a = j(s);
    },
    m(u, _) {
      o.m(u, _), F(u, e, _), F(u, n, _), F(u, i, _), F(u, a, _);
    },
    p(u, _) {
      f === (f = r(u)) && o ? o.p(u, _) : (o.d(1), o = f(u), o && (o.c(), o.m(e.parentNode, e))), _[0] & /*progress*/
      128 && t !== (t = /*p*/
      u[41].unit + "") && X(n, t);
    },
    d(u) {
      u && (C(e), C(n), C(i), C(a)), o.d(u);
    }
  };
}
function On(l) {
  let e = de(
    /*p*/
    l[41].index || 0
  ) + "", t;
  return {
    c() {
      t = j(e);
    },
    m(n, i) {
      F(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = de(
        /*p*/
        n[41].index || 0
      ) + "") && X(t, e);
    },
    d(n) {
      n && C(t);
    }
  };
}
function Jn(l) {
  let e = de(
    /*p*/
    l[41].index || 0
  ) + "", t, n, i = de(
    /*p*/
    l[41].length
  ) + "", s;
  return {
    c() {
      t = j(e), n = j("/"), s = j(i);
    },
    m(a, r) {
      F(a, t, r), F(a, n, r), F(a, s, r);
    },
    p(a, r) {
      r[0] & /*progress*/
      128 && e !== (e = de(
        /*p*/
        a[41].index || 0
      ) + "") && X(t, e), r[0] & /*progress*/
      128 && i !== (i = de(
        /*p*/
        a[41].length
      ) + "") && X(s, i);
    },
    d(a) {
      a && (C(t), C(n), C(s));
    }
  };
}
function ct(l) {
  let e, t = (
    /*p*/
    l[41].index != null && _t(l)
  );
  return {
    c() {
      t && t.c(), e = ge();
    },
    m(n, i) {
      t && t.m(n, i), F(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].index != null ? t ? t.p(n, i) : (t = _t(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && C(e), t && t.d(n);
    }
  };
}
function dt(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = j(
        /*formatted_timer*/
        l[20]
      ), n = j(t), i = j("s");
    },
    m(s, a) {
      F(s, e, a), F(s, n, a), F(s, i, a);
    },
    p(s, a) {
      a[0] & /*formatted_timer*/
      1048576 && X(
        e,
        /*formatted_timer*/
        s[20]
      ), a[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      s[0] ? `/${/*formatted_eta*/
      s[19]}` : "") && X(n, t);
    },
    d(s) {
      s && (C(e), C(n), C(i));
    }
  };
}
function Xn(l) {
  let e, t;
  return e = new Cn({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      Vt(e.$$.fragment);
    },
    m(n, i) {
      jt(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i[0] & /*variant*/
      256 && (s.margin = /*variant*/
      n[8] === "default"), e.$set(s);
    },
    i(n) {
      t || (ae(e.$$.fragment, n), t = !0);
    },
    o(n) {
      re(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Nt(e, n);
    }
  };
}
function Yn(l) {
  let e, t, n, i, s, a = `${/*last_progress_level*/
  l[15] * 100}%`, r = (
    /*progress*/
    l[7] != null && mt(l)
  );
  return {
    c() {
      e = ee("div"), t = ee("div"), r && r.c(), n = Q(), i = ee("div"), s = ee("div"), K(t, "class", "progress-level-inner svelte-1yk38uw"), K(s, "class", "progress-bar svelte-1yk38uw"), ie(s, "width", a), K(i, "class", "progress-bar-wrap svelte-1yk38uw"), K(e, "class", "progress-level svelte-1yk38uw");
    },
    m(f, o) {
      F(f, e, o), oe(e, t), r && r.m(t, null), oe(e, n), oe(e, i), oe(i, s), l[31](s);
    },
    p(f, o) {
      /*progress*/
      f[7] != null ? r ? r.p(f, o) : (r = mt(f), r.c(), r.m(t, null)) : r && (r.d(1), r = null), o[0] & /*last_progress_level*/
      32768 && a !== (a = `${/*last_progress_level*/
      f[15] * 100}%`) && ie(s, "width", a);
    },
    i: Oe,
    o: Oe,
    d(f) {
      f && C(e), r && r.d(), l[31](null);
    }
  };
}
function mt(l) {
  let e, t = Ie(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = pt(at(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = ge();
    },
    m(i, s) {
      for (let a = 0; a < n.length; a += 1)
        n[a] && n[a].m(i, s);
      F(i, e, s);
    },
    p(i, s) {
      if (s[0] & /*progress_level, progress*/
      16512) {
        t = Ie(
          /*progress*/
          i[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const r = at(i, t, a);
          n[a] ? n[a].p(r, s) : (n[a] = pt(r), n[a].c(), n[a].m(e.parentNode, e));
        }
        for (; a < n.length; a += 1)
          n[a].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && C(e), It(n, i);
    }
  };
}
function bt(l) {
  let e, t, n, i, s = (
    /*i*/
    l[43] !== 0 && Gn()
  ), a = (
    /*p*/
    l[41].desc != null && gt(l)
  ), r = (
    /*p*/
    l[41].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null && ht()
  ), f = (
    /*progress_level*/
    l[14] != null && wt(l)
  );
  return {
    c() {
      s && s.c(), e = Q(), a && a.c(), t = Q(), r && r.c(), n = Q(), f && f.c(), i = ge();
    },
    m(o, u) {
      s && s.m(o, u), F(o, e, u), a && a.m(o, u), F(o, t, u), r && r.m(o, u), F(o, n, u), f && f.m(o, u), F(o, i, u);
    },
    p(o, u) {
      /*p*/
      o[41].desc != null ? a ? a.p(o, u) : (a = gt(o), a.c(), a.m(t.parentNode, t)) : a && (a.d(1), a = null), /*p*/
      o[41].desc != null && /*progress_level*/
      o[14] && /*progress_level*/
      o[14][
        /*i*/
        o[43]
      ] != null ? r || (r = ht(), r.c(), r.m(n.parentNode, n)) : r && (r.d(1), r = null), /*progress_level*/
      o[14] != null ? f ? f.p(o, u) : (f = wt(o), f.c(), f.m(i.parentNode, i)) : f && (f.d(1), f = null);
    },
    d(o) {
      o && (C(e), C(t), C(n), C(i)), s && s.d(o), a && a.d(o), r && r.d(o), f && f.d(o);
    }
  };
}
function Gn(l) {
  let e;
  return {
    c() {
      e = j(" /");
    },
    m(t, n) {
      F(t, e, n);
    },
    d(t) {
      t && C(e);
    }
  };
}
function gt(l) {
  let e = (
    /*p*/
    l[41].desc + ""
  ), t;
  return {
    c() {
      t = j(e);
    },
    m(n, i) {
      F(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[41].desc + "") && X(t, e);
    },
    d(n) {
      n && C(t);
    }
  };
}
function ht(l) {
  let e;
  return {
    c() {
      e = j("-");
    },
    m(t, n) {
      F(t, e, n);
    },
    d(t) {
      t && C(e);
    }
  };
}
function wt(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[43]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = j(e), n = j("%");
    },
    m(i, s) {
      F(i, t, s), F(i, n, s);
    },
    p(i, s) {
      s[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && X(t, e);
    },
    d(i) {
      i && (C(t), C(n));
    }
  };
}
function pt(l) {
  let e, t = (
    /*p*/
    (l[41].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null) && bt(l)
  );
  return {
    c() {
      t && t.c(), e = ge();
    },
    m(n, i) {
      t && t.m(n, i), F(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[43]
      ] != null ? t ? t.p(n, i) : (t = bt(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && C(e), t && t.d(n);
    }
  };
}
function kt(l) {
  let e, t;
  return {
    c() {
      e = ee("p"), t = j(
        /*loading_text*/
        l[9]
      ), K(e, "class", "loading svelte-1yk38uw");
    },
    m(n, i) {
      F(n, e, i), oe(e, t);
    },
    p(n, i) {
      i[0] & /*loading_text*/
      512 && X(
        t,
        /*loading_text*/
        n[9]
      );
    },
    d(n) {
      n && C(e);
    }
  };
}
function Rn(l) {
  let e, t, n, i, s;
  const a = [An, Bn], r = [];
  function f(o, u) {
    return (
      /*status*/
      o[4] === "pending" ? 0 : (
        /*status*/
        o[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = f(l)) && (n = r[t] = a[t](l)), {
    c() {
      e = ee("div"), n && n.c(), K(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-1yk38uw"), J(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), J(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), J(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), J(
        e,
        "border",
        /*border*/
        l[12]
      ), ie(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), ie(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(o, u) {
      F(o, e, u), ~t && r[t].m(e, null), l[33](e), s = !0;
    },
    p(o, u) {
      let _ = t;
      t = f(o), t === _ ? ~t && r[t].p(o, u) : (n && (Zt(), re(r[_], 1, 1, () => {
        r[_] = null;
      }), Mt()), ~t ? (n = r[t], n ? n.p(o, u) : (n = r[t] = a[t](o), n.c()), ae(n, 1), n.m(e, null)) : n = null), (!s || u[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      o[8] + " " + /*show_progress*/
      o[6] + " svelte-1yk38uw")) && K(e, "class", i), (!s || u[0] & /*variant, show_progress, status, show_progress*/
      336) && J(e, "hide", !/*status*/
      o[4] || /*status*/
      o[4] === "complete" || /*show_progress*/
      o[6] === "hidden"), (!s || u[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && J(
        e,
        "translucent",
        /*variant*/
        o[8] === "center" && /*status*/
        (o[4] === "pending" || /*status*/
        o[4] === "error") || /*translucent*/
        o[11] || /*show_progress*/
        o[6] === "minimal"
      ), (!s || u[0] & /*variant, show_progress, status*/
      336) && J(
        e,
        "generating",
        /*status*/
        o[4] === "generating"
      ), (!s || u[0] & /*variant, show_progress, border*/
      4416) && J(
        e,
        "border",
        /*border*/
        o[12]
      ), u[0] & /*absolute*/
      1024 && ie(
        e,
        "position",
        /*absolute*/
        o[10] ? "absolute" : "static"
      ), u[0] & /*absolute*/
      1024 && ie(
        e,
        "padding",
        /*absolute*/
        o[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(o) {
      s || (ae(n), s = !0);
    },
    o(o) {
      re(n), s = !1;
    },
    d(o) {
      o && C(e), ~t && r[t].d(), l[33](null);
    }
  };
}
var Hn = function(l, e, t, n) {
  function i(s) {
    return s instanceof t ? s : new t(function(a) {
      a(s);
    });
  }
  return new (t || (t = Promise))(function(s, a) {
    function r(u) {
      try {
        o(n.next(u));
      } catch (_) {
        a(_);
      }
    }
    function f(u) {
      try {
        o(n.throw(u));
      } catch (_) {
        a(_);
      }
    }
    function o(u) {
      u.done ? s(u.value) : i(u.value).then(r, f);
    }
    o((n = n.apply(l, e || [])).next());
  });
};
let Se = [], Ae = !1;
function Kn(l) {
  return Hn(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (Se.push(e), !Ae)
        Ae = !0;
      else
        return;
      yield In(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < Se.length; i++) {
          const a = Se[i].getBoundingClientRect();
          (i === 0 || a.top + window.scrollY <= n[0]) && (n[0] = a.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), Ae = !1, Se = [];
      });
    }
  });
}
function Qn(l, e, t) {
  let n, { $$slots: i = {}, $$scope: s } = e;
  this && this.__awaiter;
  const a = jn();
  let { i18n: r } = e, { eta: f = null } = e, { queue_position: o } = e, { queue_size: u } = e, { status: _ } = e, { scroll_to_output: m = !1 } = e, { timer: b = !0 } = e, { show_progress: q = "full" } = e, { message: V = null } = e, { progress: v = null } = e, { variant: I = "default" } = e, { loading_text: d = "Loading..." } = e, { absolute: c = !0 } = e, { translucent: S = !1 } = e, { border: z = !1 } = e, { autoscroll: h } = e, P, N = !1, B = 0, y = 0, Z = null, Y = null, le = 0, E = null, g, k = null, p = !0;
  const U = () => {
    t(0, f = t(27, Z = t(19, ve = null))), t(25, B = performance.now()), t(26, y = 0), N = !0, He();
  };
  function He() {
    requestAnimationFrame(() => {
      t(26, y = (performance.now() - B) / 1e3), N && He();
    });
  }
  function Ke() {
    t(26, y = 0), t(0, f = t(27, Z = t(19, ve = null))), N && (N = !1);
  }
  Zn(() => {
    N && Ke();
  });
  let ve = null;
  function Pt(w) {
    st[w ? "unshift" : "push"](() => {
      k = w, t(16, k), t(7, v), t(14, E), t(15, g);
    });
  }
  const Bt = () => {
    a("clear_status");
  };
  function At(w) {
    st[w ? "unshift" : "push"](() => {
      P = w, t(13, P);
    });
  }
  return l.$$set = (w) => {
    "i18n" in w && t(1, r = w.i18n), "eta" in w && t(0, f = w.eta), "queue_position" in w && t(2, o = w.queue_position), "queue_size" in w && t(3, u = w.queue_size), "status" in w && t(4, _ = w.status), "scroll_to_output" in w && t(22, m = w.scroll_to_output), "timer" in w && t(5, b = w.timer), "show_progress" in w && t(6, q = w.show_progress), "message" in w && t(23, V = w.message), "progress" in w && t(7, v = w.progress), "variant" in w && t(8, I = w.variant), "loading_text" in w && t(9, d = w.loading_text), "absolute" in w && t(10, c = w.absolute), "translucent" in w && t(11, S = w.translucent), "border" in w && t(12, z = w.border), "autoscroll" in w && t(24, h = w.autoscroll), "$$scope" in w && t(29, s = w.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (f === null && t(0, f = Z), f != null && Z !== f && (t(28, Y = (performance.now() - B) / 1e3 + f), t(19, ve = Y.toFixed(1)), t(27, Z = f))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, le = Y === null || Y <= 0 || !y ? null : Math.min(y / Y, 1)), l.$$.dirty[0] & /*progress*/
    128 && v != null && t(18, p = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (v != null ? t(14, E = v.map((w) => {
      if (w.index != null && w.length != null)
        return w.index / w.length;
      if (w.progress != null)
        return w.progress;
    })) : t(14, E = null), E ? (t(15, g = E[E.length - 1]), k && (g === 0 ? t(16, k.style.transition = "0", k) : t(16, k.style.transition = "150ms", k))) : t(15, g = void 0)), l.$$.dirty[0] & /*status*/
    16 && (_ === "pending" ? U() : Ke()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && P && m && (_ === "pending" || _ === "complete") && Kn(P, h), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = y.toFixed(1));
  }, [
    f,
    r,
    o,
    u,
    _,
    b,
    q,
    v,
    I,
    d,
    c,
    S,
    z,
    P,
    E,
    g,
    k,
    le,
    p,
    ve,
    n,
    a,
    m,
    V,
    h,
    B,
    y,
    Z,
    Y,
    s,
    i,
    Pt,
    Bt,
    At
  ];
}
class Un extends Fn {
  constructor(e) {
    super(), Mn(
      this,
      e,
      Qn,
      Rn,
      Vn,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Wn,
  append: O,
  assign: xn,
  attr: L,
  create_component: Je,
  destroy_component: Xe,
  detach: pe,
  element: $,
  get_spread_object: $n,
  get_spread_update: ei,
  init: ti,
  insert: ke,
  listen: D,
  mount_component: Ye,
  run_all: li,
  safe_not_equal: ni,
  set_data: ii,
  set_input_value: ne,
  space: se,
  text: fi,
  to_number: me,
  toggle_class: vt,
  transition_in: Ge,
  transition_out: Re
} = window.__gradio__svelte__internal;
function si(l) {
  let e;
  return {
    c() {
      e = fi(
        /*label*/
        l[4]
      );
    },
    m(t, n) {
      ke(t, e, n);
    },
    p(t, n) {
      n & /*label*/
      16 && ii(
        e,
        /*label*/
        t[4]
      );
    },
    d(t) {
      t && pe(e);
    }
  };
}
function oi(l) {
  let e, t, n, i, s, a, r, f, o, u, _, m, b, q, V, v, I, d, c, S, z, h, P, N, B, y, Z, Y;
  const le = [
    { autoscroll: (
      /*gradio*/
      l[0].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      l[0].i18n
    ) },
    /*loading_status*/
    l[14]
  ];
  let E = {};
  for (let g = 0; g < le.length; g += 1)
    E = xn(E, le[g]);
  return e = new Un({ props: E }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    l[24]
  ), s = new Tl({
    props: {
      show_label: (
        /*show_label*/
        l[12]
      ),
      info: (
        /*info*/
        l[5]
      ),
      $$slots: { default: [si] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Je(e.$$.fragment), t = se(), n = $("div"), i = $("div"), Je(s.$$.fragment), a = se(), r = $("div"), f = $("input"), _ = se(), m = $("input"), V = se(), v = $("div"), I = $("div"), d = se(), c = $("div"), S = se(), z = $("input"), P = se(), N = $("input"), L(f, "aria-label", o = `max input for ${/*label*/
      l[4]}`), L(f, "data-testid", "max-input"), L(f, "type", "number"), L(
        f,
        "min",
        /*minimum*/
        l[9]
      ), L(
        f,
        "max",
        /*maximum*/
        l[10]
      ), f.disabled = u = !/*interactive*/
      l[13], L(f, "class", "svelte-4wk6so"), L(m, "aria-label", b = `min input for ${/*label*/
      l[4]}`), L(m, "data-testid", "min-input"), L(m, "type", "number"), L(
        m,
        "min",
        /*minimum*/
        l[9]
      ), L(
        m,
        "max",
        /*maximum*/
        l[10]
      ), m.disabled = q = !/*interactive*/
      l[13], L(m, "class", "svelte-4wk6so"), L(r, "class", "numbers svelte-4wk6so"), L(i, "class", "head svelte-4wk6so"), L(n, "class", "wrap svelte-4wk6so"), L(I, "class", "range-bg svelte-4wk6so"), L(c, "class", "range-line svelte-4wk6so"), L(
        c,
        "style",
        /*rangeLine*/
        l[17]
      ), vt(c, "disabled", !/*interactive*/
      l[13]), L(z, "type", "range"), z.disabled = h = !/*interactive*/
      l[13], L(
        z,
        "min",
        /*minimum*/
        l[9]
      ), L(
        z,
        "max",
        /*maximum*/
        l[10]
      ), L(
        z,
        "step",
        /*step*/
        l[11]
      ), L(z, "class", "svelte-4wk6so"), L(N, "type", "range"), N.disabled = B = !/*interactive*/
      l[13], L(
        N,
        "min",
        /*minimum*/
        l[9]
      ), L(
        N,
        "max",
        /*maximum*/
        l[10]
      ), L(
        N,
        "step",
        /*step*/
        l[11]
      ), L(N, "class", "svelte-4wk6so"), L(v, "class", "range-slider svelte-4wk6so");
    },
    m(g, k) {
      Ye(e, g, k), ke(g, t, k), ke(g, n, k), O(n, i), Ye(s, i, null), O(i, a), O(i, r), O(r, f), ne(
        f,
        /*selected_max*/
        l[16]
      ), O(r, _), O(r, m), ne(
        m,
        /*selected_min*/
        l[15]
      ), ke(g, V, k), ke(g, v, k), O(v, I), O(v, d), O(v, c), O(v, S), O(v, z), ne(
        z,
        /*selected_min*/
        l[15]
      ), O(v, P), O(v, N), ne(
        N,
        /*selected_max*/
        l[16]
      ), y = !0, Z || (Y = [
        D(
          f,
          "input",
          /*input0_input_handler*/
          l[25]
        ),
        D(
          f,
          "pointerup",
          /*handle_release*/
          l[20]
        ),
        D(
          f,
          "blur",
          /*handle_release*/
          l[20]
        ),
        D(
          m,
          "input",
          /*input1_input_handler*/
          l[26]
        ),
        D(
          m,
          "pointerup",
          /*handle_release*/
          l[20]
        ),
        D(
          m,
          "blur",
          /*handle_release*/
          l[20]
        ),
        D(
          z,
          "change",
          /*input2_change_input_handler*/
          l[27]
        ),
        D(
          z,
          "input",
          /*input2_change_input_handler*/
          l[27]
        ),
        D(
          z,
          "input",
          /*handle_min_change*/
          l[18]
        ),
        D(
          z,
          "pointerup",
          /*handle_release*/
          l[20]
        ),
        D(
          N,
          "change",
          /*input3_change_input_handler*/
          l[28]
        ),
        D(
          N,
          "input",
          /*input3_change_input_handler*/
          l[28]
        ),
        D(
          N,
          "input",
          /*handle_max_change*/
          l[19]
        ),
        D(
          N,
          "pointerup",
          /*handle_release*/
          l[20]
        )
      ], Z = !0);
    },
    p(g, k) {
      const p = k & /*gradio, loading_status*/
      16385 ? ei(le, [
        k & /*gradio*/
        1 && { autoscroll: (
          /*gradio*/
          g[0].autoscroll
        ) },
        k & /*gradio*/
        1 && { i18n: (
          /*gradio*/
          g[0].i18n
        ) },
        k & /*loading_status*/
        16384 && $n(
          /*loading_status*/
          g[14]
        )
      ]) : {};
      e.$set(p);
      const U = {};
      k & /*show_label*/
      4096 && (U.show_label = /*show_label*/
      g[12]), k & /*info*/
      32 && (U.info = /*info*/
      g[5]), k & /*$$scope, label*/
      1073741840 && (U.$$scope = { dirty: k, ctx: g }), s.$set(U), (!y || k & /*label*/
      16 && o !== (o = `max input for ${/*label*/
      g[4]}`)) && L(f, "aria-label", o), (!y || k & /*minimum*/
      512) && L(
        f,
        "min",
        /*minimum*/
        g[9]
      ), (!y || k & /*maximum*/
      1024) && L(
        f,
        "max",
        /*maximum*/
        g[10]
      ), (!y || k & /*interactive*/
      8192 && u !== (u = !/*interactive*/
      g[13])) && (f.disabled = u), k & /*selected_max*/
      65536 && me(f.value) !== /*selected_max*/
      g[16] && ne(
        f,
        /*selected_max*/
        g[16]
      ), (!y || k & /*label*/
      16 && b !== (b = `min input for ${/*label*/
      g[4]}`)) && L(m, "aria-label", b), (!y || k & /*minimum*/
      512) && L(
        m,
        "min",
        /*minimum*/
        g[9]
      ), (!y || k & /*maximum*/
      1024) && L(
        m,
        "max",
        /*maximum*/
        g[10]
      ), (!y || k & /*interactive*/
      8192 && q !== (q = !/*interactive*/
      g[13])) && (m.disabled = q), k & /*selected_min*/
      32768 && me(m.value) !== /*selected_min*/
      g[15] && ne(
        m,
        /*selected_min*/
        g[15]
      ), (!y || k & /*rangeLine*/
      131072) && L(
        c,
        "style",
        /*rangeLine*/
        g[17]
      ), (!y || k & /*interactive*/
      8192) && vt(c, "disabled", !/*interactive*/
      g[13]), (!y || k & /*interactive*/
      8192 && h !== (h = !/*interactive*/
      g[13])) && (z.disabled = h), (!y || k & /*minimum*/
      512) && L(
        z,
        "min",
        /*minimum*/
        g[9]
      ), (!y || k & /*maximum*/
      1024) && L(
        z,
        "max",
        /*maximum*/
        g[10]
      ), (!y || k & /*step*/
      2048) && L(
        z,
        "step",
        /*step*/
        g[11]
      ), k & /*selected_min*/
      32768 && ne(
        z,
        /*selected_min*/
        g[15]
      ), (!y || k & /*interactive*/
      8192 && B !== (B = !/*interactive*/
      g[13])) && (N.disabled = B), (!y || k & /*minimum*/
      512) && L(
        N,
        "min",
        /*minimum*/
        g[9]
      ), (!y || k & /*maximum*/
      1024) && L(
        N,
        "max",
        /*maximum*/
        g[10]
      ), (!y || k & /*step*/
      2048) && L(
        N,
        "step",
        /*step*/
        g[11]
      ), k & /*selected_max*/
      65536 && ne(
        N,
        /*selected_max*/
        g[16]
      );
    },
    i(g) {
      y || (Ge(e.$$.fragment, g), Ge(s.$$.fragment, g), y = !0);
    },
    o(g) {
      Re(e.$$.fragment, g), Re(s.$$.fragment, g), y = !1;
    },
    d(g) {
      g && (pe(t), pe(n), pe(V), pe(v)), Xe(e, g), Xe(s), Z = !1, li(Y);
    }
  };
}
function ai(l) {
  let e, t;
  return e = new nl({
    props: {
      visible: (
        /*visible*/
        l[3]
      ),
      elem_id: (
        /*elem_id*/
        l[1]
      ),
      elem_classes: (
        /*elem_classes*/
        l[2]
      ),
      container: (
        /*container*/
        l[6]
      ),
      scale: (
        /*scale*/
        l[7]
      ),
      min_width: (
        /*min_width*/
        l[8]
      ),
      $$slots: { default: [oi] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Je(e.$$.fragment);
    },
    m(n, i) {
      Ye(e, n, i), t = !0;
    },
    p(n, [i]) {
      const s = {};
      i & /*visible*/
      8 && (s.visible = /*visible*/
      n[3]), i & /*elem_id*/
      2 && (s.elem_id = /*elem_id*/
      n[1]), i & /*elem_classes*/
      4 && (s.elem_classes = /*elem_classes*/
      n[2]), i & /*container*/
      64 && (s.container = /*container*/
      n[6]), i & /*scale*/
      128 && (s.scale = /*scale*/
      n[7]), i & /*min_width*/
      256 && (s.min_width = /*min_width*/
      n[8]), i & /*$$scope, interactive, minimum, maximum, step, selected_max, selected_min, rangeLine, label, show_label, info, gradio, loading_status*/
      1074003505 && (s.$$scope = { dirty: i, ctx: n }), e.$set(s);
    },
    i(n) {
      t || (Ge(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Re(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Xe(e, n);
    }
  };
}
function ri(l, e, t) {
  let n, { gradio: i } = e, { elem_id: s = "" } = e, { elem_classes: a = [] } = e, { visible: r = !0 } = e, { value: f } = e, { label: o = i.i18n("slider.slider") } = e, { info: u = void 0 } = e, { container: _ = !0 } = e, { scale: m = null } = e, { min_width: b = void 0 } = e, { minimum: q = 0 } = e, { maximum: V = 100 } = e, { step: v } = e, { show_label: I } = e, { interactive: d } = e, { loading_status: c } = e, { value_is_output: S = !1 } = e;
  function z(p, U) {
    t(21, f = [p, U]), i.dispatch("change", [p, U]), S || i.dispatch("input", [p, U]);
  }
  function h(p) {
    t(15, y = parseFloat(p.target.value)), y > Z && t(16, Z = y);
  }
  function P(p) {
    t(16, Z = parseFloat(p.target.value)), Z < y && t(15, y = Z);
  }
  function N(p) {
    i.dispatch("release", f);
  }
  let B = f, [y, Z] = f;
  const Y = () => i.dispatch("clear_status", c);
  function le() {
    Z = me(this.value), t(16, Z), t(23, B), t(21, f);
  }
  function E() {
    y = me(this.value), t(15, y), t(23, B), t(21, f);
  }
  function g() {
    y = me(this.value), t(15, y), t(23, B), t(21, f);
  }
  function k() {
    Z = me(this.value), t(16, Z), t(23, B), t(21, f);
  }
  return l.$$set = (p) => {
    "gradio" in p && t(0, i = p.gradio), "elem_id" in p && t(1, s = p.elem_id), "elem_classes" in p && t(2, a = p.elem_classes), "visible" in p && t(3, r = p.visible), "value" in p && t(21, f = p.value), "label" in p && t(4, o = p.label), "info" in p && t(5, u = p.info), "container" in p && t(6, _ = p.container), "scale" in p && t(7, m = p.scale), "min_width" in p && t(8, b = p.min_width), "minimum" in p && t(9, q = p.minimum), "maximum" in p && t(10, V = p.maximum), "step" in p && t(11, v = p.step), "show_label" in p && t(12, I = p.show_label), "interactive" in p && t(13, d = p.interactive), "loading_status" in p && t(14, c = p.loading_status), "value_is_output" in p && t(22, S = p.value_is_output);
  }, l.$$.update = () => {
    l.$$.dirty & /*old_value, value*/
    10485760 && JSON.stringify(B) !== JSON.stringify(f) && (t(15, [y, Z] = f, y, (t(16, Z), t(23, B), t(21, f))), t(23, B = f)), l.$$.dirty & /*selected_min, selected_max*/
    98304 && z(y, Z), l.$$.dirty & /*selected_min, minimum, maximum, selected_max*/
    99840 && t(17, n = `
      left: ${(y - q) / (V - q) * 100}%;
      width: ${(Z - y) / (V - q) * 100}%;
    `);
  }, [
    i,
    s,
    a,
    r,
    o,
    u,
    _,
    m,
    b,
    q,
    V,
    v,
    I,
    d,
    c,
    y,
    Z,
    n,
    h,
    P,
    N,
    f,
    S,
    B,
    Y,
    le,
    E,
    g,
    k
  ];
}
class ui extends Wn {
  constructor(e) {
    super(), ti(this, e, ri, ai, ni, {
      gradio: 0,
      elem_id: 1,
      elem_classes: 2,
      visible: 3,
      value: 21,
      label: 4,
      info: 5,
      container: 6,
      scale: 7,
      min_width: 8,
      minimum: 9,
      maximum: 10,
      step: 11,
      show_label: 12,
      interactive: 13,
      loading_status: 14,
      value_is_output: 22
    });
  }
}
export {
  ui as default
};
