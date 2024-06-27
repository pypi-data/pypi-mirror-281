axui.vis_observer = new IntersectionObserver(
  (entries) => {
    let vis;
    for (const el of entries) {
      vis = false;
      if (el.isIntersecting === true) vis = true;
      //if (!vis) return;
      axui.bus("vis-change", {
        id: el.target.id.replace("-vis", ""),
        vis: vis,
      });
      //axui.cur_event = { id: el.target.id.replace("-vis", ""), vis: vis };
      //axui.bus_el.click();
      //console.log(axui.cur_event);
    }
  },
  { threshold: [0] },
);
axui.vis_check = function (eid) {
  /* we add a -vis span BEFORE that actual element under observation.
   That way, we can return htmx with the actual id, that element would
   otherwise fall out of the observation, when recreated by htmx:
  */
  console.log("vis checking:", eid);
  //const el = axui.byid(eid);
  const vid = `${eid}-vis`;
  //const span = `<span id="${vid}"></span>`;
  //el.insertAdjacentHTML("beforebegin", span);
  const sel = axui.byid(vid);
  axui.vis_observer.observe(sel);
};
