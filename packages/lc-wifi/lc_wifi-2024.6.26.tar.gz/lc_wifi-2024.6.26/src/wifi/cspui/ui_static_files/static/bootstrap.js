//.catch(error => console.error('Could not load XTRM UI:', error));
//console.log("stopping refresher to AXESS");
//window.pause_axwifi_evts_refresh = 1;
window.axui = {
  orig_href: window.location.href,
  byid: document.getElementById.bind(document),
  //huburl: window.location.href.split('#')[0].split('?')[0],
  huburl: "/lc-csp/csp/assets/static/",
  server_comps: {},
  // app will eval server comps as well and fire axui.bus
  // we want dev reload => keep server_comps, fastest way to get them into the dom,
  // while dom is busy loading server stuff.
  // Those can be registered before or after app is loaded:
  add_server_comp: (comp, cfg) => {
    axui.server_comps[comp] = cfg; // when run before app, app will call bus on them
    if (axui.bus) axui.bus(comp, cfg); // server registered AFTER app
  },
  fetch_libs: function (libs, then) {
    // get the prism hiliter files, served by the hub.js
    //ax.css copied into node_modules by ops i -m hub
    function fp(base, pth) {
      let typ = "style";
      if (pth.endsWith(".js")) typ = "script";
      const url = axui.huburl + base + pth;
      console.log("fetching", base + pth);
      fetch(url)
        .then((response) => response.text())
        .then((data) => {
          const elmt = document.createElement(typ);
          elmt.textContent = data;
          document.head.appendChild(elmt);
          console.log("got", base + pth);
          // if (pth === 'prism.js') {
          //     fp(base, 'components/prism-python.js')
          //     fp(base, 'components/prism-javascript.js')
          // }
          if (pth === "htmx.js") {
            htmx.config.wsReconnectDelay = (cnt) => {
              console.log("retry ws con.");
              return 1000;
            };
            fp(base, "ext/ws.js");
            //fp(base, 'ext/debug.js')
          }
          if (pth === "ext/ws.js") setTimeout(then, 1000);
        })
        .catch((err) => console.log(err));
    }
    libs.forEach(([base, pth]) => fp(base, pth));
  },
  make_ui: async function (anchor) {
    const ws_ui = "/ws-lc-csp/csp/ws/cspui";
    //const ws_ui = "ws://127.0.0.1:3800/csp/ws/cspui";

    // // dev reload handling - when server goes down:
    // htmx.on("htmx:wsOpen", function (event) {

    htmx.on("htmx:wsClose", function (event) {
      if (!axui.close_cleared) {
        axui.viz_observer?.disconnect();
        console.log("RELOAD. Stopped Viz Checkers.");
        const els = ["streaming"];
        els.forEach((eid) => {
          const el = document.getElementById(eid);
          if (el) el.innerHTML = "";
        }); // todo: from server
        axui.close_cleared = true;
      }
    });
    // we add the app div within here, not body. htmx works outside as well
    //const node = document.body;
    //node = node || document.body;
    const node = document.getElementById("main");
    // console.log("have main", node);
    // delivered by actual server into the anchor element, we checked for presence
    // contains e.g. cpe infos for the hx server:
    // // Add hx-ext and ws-connect attributes
    cpeid = location.href.split("/cpeid/")[1].split("?")[0].split("/")[0];
    node.setAttribute("hx-ext", "ws");
    node.setAttribute("hx-trigger", "load");
    node.setAttribute("ws-connect", `${ws_ui}/cpeid/${cpeid}`);
    //node.setAttribute("hx-vals", `js:${cfg}`);
    axui.domroot = '<div id="🟢ui" />'; // hx-trigger="load once" ws-send></div>';
    node.insertAdjacentHTML("beforeend", axui.domroot);
    console.log("connecting to", ws_ui);
    htmx.process(node); // triggers first ui loading hx req
  },
};
//document.addEventListener("DOMContentLoaded", function () {
// window.addEventListener("load", function () {
//   console.log("loading streaming component");
//   //axui.bus("streaming", {});
//   //   axui.fetch_libs(libs, axui.make_ui);
// });
console.log("featching ui libs");
axui.fetch_libs(
  [
    //["kendo/", "styles/kendo.common.min.css"],
    //["kendo/", "styles/kendo.bootstrap.min.css"],
    //["kendo/", "js/kendo.all.min.js"],
    //['prismjs/', 'themes/ax.css'],
    //['prismjs/', 'prism.js'],
    // ['vis/'    , 'vis-timeline-graph2d.min.css'],
    // ['vis/'    , 'vis.js'],
    ["rxjs/", "_UP_/bundles/rxjs.umd.min.js"],
    //['prismjs/', 'prism.js'],
    ["htmx.org/", "htmx.js"],
  ],

  () => {
    console.log("libs loaded");
    load_ui();
  },
);
function load_ui() {
  const ui_present = setInterval(function () {
    //const domcheckid = "load-hx-ui";
    const domcheckid = "main"; // in instantly, before angular mess happens!
    const ui = document.getElementById(domcheckid);
    console.log("checking for element id", domcheckid);
    if (ui) {
      console.log("🎇 DOM built - requesting ui now");
      clearInterval(ui_present);
      axui.make_ui(ui);
    }
  }, 500);
}

//});
