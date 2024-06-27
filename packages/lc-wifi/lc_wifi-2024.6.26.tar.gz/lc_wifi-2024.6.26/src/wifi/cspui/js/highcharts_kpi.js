axui.chart = Highcharts.chart("%(id)s", {
  chart: {
    zoomType: "x",
    panning: true,
    panKey: "shift",
    zooming: {
      type: "x",
    },
  },
  title: {
    text: "%(title)s",
    align: "left",
  },
  subtitle: {
    text:
      document.ontouchstart === undefined
        ? "Click and drag in the plot area to zoom in. Hold ctrl while hovering to update the stations table."
        : "Pinch the chart to zoom in",
    align: "left",
  },
  xAxis: {
    type: "datetime",
    // events: {
    //   setExtremes: axui.hc_sync_extremes,
    // },
  },
  // navigator: {
  //   adaptToUpdatedData: false,
  //   enabled: 1,
  //   xAxis: {
  //     min: `%${ts_oldest}s`,
  //     max: `%${ts_newest}s`,
  //   },
  // },
  yAxis: {
    title: {
      text: "%(y_title)s",
    },
  },
  legend: { enabled: true },
  plotOptions: {
    series: {
      point: { events: `%${point_evts}s` },
    },
    area: {
      fillColor: {
        linearGradient: {
          x1: 0,
          y1: 0,
          x2: 0,
          y2: 1,
        },
        stops: [
          [0, Highcharts.getOptions().colors[0]],
          [
            1,
            Highcharts.color(Highcharts.getOptions().colors[0])
              .setOpacity(0)
              .get("rgba"),
          ],
        ],
      },
      marker: {
        radius: 2,
      },
      lineWidth: 1,
      states: {
        hover: {
          lineWidth: 1,
        },
      },
      threshold: null,
    },
  },
  series: `%${data}s`,
});
