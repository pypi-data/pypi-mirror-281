# vi: ft=html

style = """
    .ch_table thead tr th  { padding-right: 1rem; padding-left: 0rem}
    .ch_table tbody tr td span {
      text-align: left;
      padding-right: 1rem;
      font-size: small!IMPORTANT;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); color: black; }
        50% { color: #8bd124; }
        100% { transform: rotate(360deg); color: black; }
    }
    .is-live { animation: spin 2s linear infinite; }

"""

t_head = '<tr role="row"> %s </tr>'

# rendered only when live, so that the live toggle is not destroyed:
t_stations_table_data = """
      <div id="%(id)s">
          <table 
            aria-describedby="data-overview_info" 
            id="data-overview" 
            class="ch_table table table-striped table-responsive rigid-table">
            %(head)s
            <tbody>%(rows)s</tbody>
            %(head)s
          </table>
          <script>
            axui.localtime('%(id)s-ts', %(ts)s)
            axui.ago('%(id)s-ago')
          </script>
      </div>
"""

t_stations_table = """
  <div class="col-lg-12">
    <div class="panel panel-default remote-table">
        <div class="panel-heading clearfix">
            <dl style="margin-bottom:0px;">
                <dt>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="white-space: nowrap;">%(title)s</span>
                        <small> <span> <b id="%(id)s-ts"></b> <span id="%(id)s-ago">%(ts)s</span> </span> </small>
                        <!--input type="range" min="1" max="100" value="50" class="ch-table-date-slider" id="%(id)s-slider"-->
                        %(live_toggle)s
                    </div>
                </dt>
            </dl>
        </div>
        <div class="panel panel-default no_bottom_margin">
            <div class="panel-body" style="padding: 0px;padding-left:1rem">
                t_stations_table_data
             </div>
        </div>
    </div>
  </div>
""".replace('t_stations_table_data', t_stations_table_data)


t_cell = """ <td ng-style="{{'text-align': 'col.align'}}"> <span>%s</span></td> """
