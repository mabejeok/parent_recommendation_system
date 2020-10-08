$('#form-for-parsley').parsley();

let childcareArray = jsonResult["fullChildcareList"];

let childcareTable = $('#relevant-results').DataTable({
    "data" : childcareArray,
    "columns" : [
         {
            "className":      'details-control',
            "orderable":      false,
            "data":           null,
            "defaultContent": ''
        },
        { "data": "rank", title: "Rank"},
        { "data": "full_relevance", title: "Meets all requirements"},
        { "data": "centreName", title: "Centre Name"},
        { "data" : "centreAddress", "title" : "Centre Address" },
        { "data" : "distance", "title" : "Distance from ideal location"},
        { "data":  "studyLevel", "title": "Selected study level"},
        { "data":  "typeOfService", "title": "Selected service type"},
        { "data" : "fee", "title" : "Fee" },
        { "data" : "food", "title" : "Dietary Restrictions"},
        { "data" : "secondLanguage", "title" : "Second Language"},
        { "data" : "infantVacancy", "title" : "Infant vacancy"},
        { "data" : "pgVacancy", "title" : "Playgroup vacancy"},
        { "data" : "n1Vacancy", "title" : "Pre-Nursery vacancy"},
        { "data" : "n2Vacancy", "title" : "Nursery vacancy"},
        { "data" : "k1Vacancy", "title" : "K1 vacancy"},
        { "data" : "k2Vacancy", "title" : "K2 vacancy"},
    ],
    "paging": false,
    "columnDefs": [ {
          "targets": 2,
          // If fully meets requirements, then check. Else, show a cross for Meets all requirements column
          "render": function (data, type, row, meta){
                                  if(data){
                                    return '<i class="fas fa-check"></i>';
                                  } else {
                                    return '<i class="fas fa-times"></i>';
                                  }
                  }
       }, {
          "targets": 1,
          "render": function (data, type, row, meta){
                                  var $select = $(`<select id=${row["centreCode"]} name=${row["centreCode"]} class="action" data-parsley-rank_validation=""></select>`, {
                                  });
                                  $select.append($("<option></option>", {
                                      "text": "",
                                      "value": ""
                                  }));
                                  for (let i=1; i < 11; i++){
                                    var $option = $("<option></option>", {
                                          "text": i,
                                          "value": i
                                      });
                                      $select.append($option);
                                  }
                                  $('.action').change(function(){
                                       var value = $(this).val();
                                   });
                                  return $select.prop("outerHTML");
                                  }
       }]
});

// Here we force open all details
// Enumerate all rows
childcareTable.rows().every(function(){
    // If row has details collapsed
    if(!this.child.isShown()){
        // Open this row
        this.child(format(this.data())).show();
        $(this.node()).addClass('shown');
    }
});

// Add event listener for opening and closing details
$('#relevant-results tbody').on('click', 'td.details-control', function () {
    var tr = $(this).closest('tr');
    var row = childcareTable.row( tr );

    if ( row.child.isShown() ) {
        // This row is already open - close it
        row.child.hide();
        tr.removeClass('shown');
    }
    else {
        // Open this row
        row.child( format(row.data()) ).show();
        tr.addClass('shown');
    }
} );


// Custom validator for date range
window.Parsley.addValidator('rank_validation', {
  validateString: function(value) {
    var allowed = true;
    let ek = $('.action').map((_,el) => el.value).get().filter(Boolean);
    allowed = ek.length === new Set(ek).size;
    return allowed;
  },
  messages: {
    en: "Please ensure the ranks for childcares are different.",
  }
});

// Format for when user open details
function format ( d ) {
    if(Object.keys(d.reviews).length === 0){
        return "No reviews";
    } else {
        let table = '<table cellpadding="5" cellspacing="0" border="1" style="padding-left:50px;">';
        $.each( d.reviews, function( key, value ) {
          table = table + '<tr>'+
                     `<td>${key}</td>`+
                     `<td>${value}</td>`+
                  '</tr>'
        });
        table += '</table>';

        return table;
    }

}