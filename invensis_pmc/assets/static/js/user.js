
	$(document).ready(function () {
        var oTable = $('#example_data').dataTable({
            "oLanguage": {
                "sSearch": "Search:"
            },
            "aoColumnDefs": [
                {
                    'bSortable': false,
                    'aTargets': [0]
                } //disables sorting for column one
            ],
            'iDisplayLength': 12,
            "sPaginationType": "full_numbers",
            //"dom": 'T<"clear">lfrtip',
            //"tableTools": {
             //   "sSwfPath": "{% static 'js/datatables/tools/swf/copy_csv_xls.swf' %}"
            //}
        });
        $("tfoot input").keyup(function () {
            /* Filter on the column based on the index of this element's parent <th> */
            oTable.fnFilter(this.value, $("tfoot th").index($(this).parent()));
        });
        $("tfoot input").each(function (i) {
            asInitVals[i] = this.value;
        });
        $("tfoot input").focus(function () {
            if (this.className == "search_init") {
                this.className = "";
                this.value = "";
            }
        });
        $("tfoot input").blur(function (i) {
            if (this.value == "") {
                this.className = "search_init";
                this.value = asInitVals[$("tfoot input").index(this)];
            }
        });
    });

    $(document).ready(function() {
        $('#example').DataTable();
    } );



// jQuery(function($) {
//     $('form[data-async]').live('submit', function(event) {
//         var $form = $(this);
//         var $target = $($form.attr('data-target'));

//         $.ajax({
//             type: $form.attr('method'),
//             url: $form.attr('action'),
//             data: $form.serialize(),

//             success: function(data, status) {
//                 $target.html(data);
//             }
//         });

//         event.preventDefault();
//     });
// });



