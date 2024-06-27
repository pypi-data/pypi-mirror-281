axui.localtime = function (eid, ts) {
  const el = axui.byid(eid);
  el.innerText = moment.unix(ts).format("YYYY-MM-DD HH:mm:ss");
};

axui.ago_updaters = {}; // Store interval IDs

axui.ago = function (eid) {
  const el = axui.byid(eid);
  const ts = el?.innerText;
  if (!ts) return;
  if (axui.ago_updaters[eid]) clearInterval(axui.ago_updaters[eid]);
  el.innerText = `(${moment.unix(ts).fromNow()})`;
  // Update the text every interval
  axui.ago_updaters[eid] = setInterval(function () {
    el.innerText = `(${moment.unix(ts).fromNow()})`;
  }, 10 * 1000);
};

// begin_archive
// Idiotic attempt to do toggle state locally. See the cpe live stream component regarding the htmx way
// axui.toggles = {};
// axui.handle_toggle = function (eid, stropts) {
//   let opts = axui.toggles[eid];
//   if (!opts) opts = axui.toggles[eid] = axui.deser_stropts(stropts);
//   const el = axui.byid(eid);
//   if (opts.state) el.classList.remove(opts.cls);
//   else el.classList.add(opts.cls);
//   opts.state = !opts.state;
//   axui.bus(eid, { state: opts.state });
// };
//
// axui.deser_stropts = function (stropts) {
//   /* 'foo:bar,..'  -> {foo: 'bar', ...} helper for e.g. onclick=myfunc('foo:bar,bar:baz') i.e. can be rendered into attrs so that we don't need to send custom js down. In use e.g. for toggle onclick listeners */
//   return stropts.split(",").reduce(function (acc, item) {
//     const parts = item.split(":");
//     if (parts[1] === "false") parts[1] = false;
//     acc[parts[0]] = parts[1];
//     return acc;
//   }, {});
// };
