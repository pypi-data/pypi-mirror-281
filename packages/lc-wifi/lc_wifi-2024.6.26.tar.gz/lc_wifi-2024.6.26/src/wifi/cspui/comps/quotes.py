from wifi.cspui import tools as t
from devapp.app import app
from operators.ctrl import hpstreams

P = t.partial
div = t.div


def on_nxt_live(msg, S):
    dom = div('quote', msg['payload']['h'])  # zenquote format has h(tml)
    S.send(dom)


class quotes:
    def on_vis(req):
        S = req['S']
        h = {'nxt': P(on_nxt_live, S=S), 'sid': S.id}
        p = {'chn': 'local', 'dt': '10000', 'ident': 'quotes', 'mode': 'geek'}
        stream = {'action': 'fun/quote', 'params': p, 'handler': h}
        # return t.div('quotes', t.div('quote', 'fetching quote...'))
        cancel = hpstreams.listen(stream)
        S.subs['quotes'] = cancel  # remember,so system will unsub at socket close
        return t.div('quotes', t.div('quote', 'fetching quote...'))

    def on_invis(req):
        cancel = req['S'].subs.get('quotes')
        cancel() if cancel else 0


t.add_comp(quotes)


#
# T = """
#
#         <div id="example">
#
#             <div class="box wide">
#                 <div class="box-col">
#                 <h4>Selection</h4>
#                 <ul class="options">
#                     <li>
#                         <input type="text" value="0" id="selectRow" class="k-textbox"/>
#                         <button class="selectRow k-button">Select row</button>
#                     </li>
#                     <li>
#                         <button class="clearSelection k-button">Clear selected rows</button>
#                     </li>
#                 </ul>
#                 </div>
#                 <div class="box-col">
#                 <h4>Expand / Collapse</h4>
#                 <ul class="options">
#                     <li>
#                         <input type="text" value="0" id="groupRow" class="k-textbox"/>
#                         <button class="toggleGroup k-button">Collapse/Expand group</button>
#                     </li>
#                 </ul>
#                 </div>
#             </div>
#
#             <div id="grid"></div>
#
#             <script>
#                     $("#grid").kendoGrid({
#                         dataSource: {
#                             transport: {
#                                 read: {
#                                     url: "https://demos.telerik.com/kendo-ui/service/Products",
#                                     dataType: "jsonp"
#                                 }
#                             },
#                             pageSize: 5,
#                             group: {
#                                 field: "UnitsInStock",
#                                 dir: "asc"
#                             }
#                         },
#                         selectable: "multiple row",
#                         pageable: {
#                             buttonCount: 5
#                         },
#                         scrollable: false,
#                         groupable: true,
#                         columns: [
#                             {
#                                 field: "ProductName",
#                                 title: "Product Name"
#                             },
#                             {
#                                 field: "UnitPrice",
#                                 title: "Unit Price",
#                                 format: "{0:c}"
#                             },
#                             {
#                                 field: "UnitsInStock",
#                                 title: "Units In Stock"
#                             }
#                         ]
#                     });
#
#                     $(".clearSelection").click(function () {
#                         $("#grid").data("kendoGrid").clearSelection();
#                     });
#
#                     var selectRow = function (e) {
#                         if (e.type != "keypress" || kendo.keys.ENTER == e.keyCode) {
#                             var grid = $("#grid").data("kendoGrid"),
#                                     rowIndex = $("#selectRow").val(),
#                                     row = grid.tbody.find(">tr:not(.k-grouping-row)").eq(rowIndex);
#
#                             grid.select(row);
#                         }
#                     },
#                         toggleGroup = function (e) {
#                             if (e.type != "keypress" || kendo.keys.ENTER == e.keyCode) {
#                                 var grid = $("#grid").data("kendoGrid"),
#                                     rowIndex = $("#groupRow").val(),
#                                     row = grid.tbody.find(">tr.k-grouping-row").eq(rowIndex);
#
#                                 if (row.has(".k-i-collapse").length) {
#                                     grid.collapseGroup(row);
#                                 } else {
#                                     grid.expandGroup(row);
#                                 }
#                             }
#                         };
#
#
#                     $(".selectRow").click(selectRow);
#                     $("#selectRow").keypress(selectRow);
#
#                     $(".toggleGroup").click(toggleGroup);
#                     $("#groupRow").keypress(toggleGroup);
#             </script>
#
#         </div>
#
#
#
#
# """
#
#
#
