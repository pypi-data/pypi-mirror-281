$(document)
  .keydown(function (e) {
    if (e.ctrlKey) {
      console.log("ctrl down");
      axui.ctrl_key_down = true;
    }
  })
  .keyup(function () {
    console.log("ctrl up");
    axui.ctrl_key_down = false;
  });
