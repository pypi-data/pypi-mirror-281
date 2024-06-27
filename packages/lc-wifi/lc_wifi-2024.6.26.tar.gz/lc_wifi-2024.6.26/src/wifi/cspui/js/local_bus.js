axui.bus_el = document.getElementById(`${axui.id_ui}-local-evts`);
axui.bus = function (typ, data) {
  const evt = data || {};
  console.log("⬆️", typ, evt);
  evt.typ = typ;
  axui.cur_event = evt; // easier to pass to hx via this, than within evt details
  axui.bus_el.click();
};
// when main server's componets called local bus before htmx actually connected
// (which is faster than triggering WITH the first htmx, when lots of other stuff is happening at load)
for (const [compid, config] of Object.entries(axui.server_comps)) {
  console.log("Server component", compid, config);
  axui.bus(compid, config);
}
