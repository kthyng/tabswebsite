
var data = {
    "base" : ["Please choose from above"],
    "A": ["ven", "eng"],
    "B": ["ven", "eng", "met", "salt"],
    "C": ["ven", "eng"],
    "D": ["ven", "eng", "salt"],
    "E": ["ven", "eng"],
    "F": ["ven", "eng", "salt"],
    "G": ["ven", "eng"],
    "H": ["ven", "eng", "met"],
    "J": ["ven", "eng", "met", "salt"],
    "K": ["ven", "eng", "met", "salt", "wave"],
    "N": ["ven", "eng", "met", "salt", "wave"],
    "P": ["ven", "eng"],
    "R": ["ven", "eng", "salt"],
    "S": ["ven", "eng"],
    "V": ["ven", "eng", "met", "salt", "wave"],
    "W": ["ven", "eng", "salt"],
    "X": ["ven", "eng", "met", "salt", "wave"],
}

$(function() {
https://css-tricks.com/dynamic-dropdowns/
http://jsfiddle.net/NaUAL/

    $("#json-one").change(function() {

        var first = $(this),
            second = $("#json-two"),
            key = first.val(),
            // instead of the original switch code
            vals = data[key] == undefined ? data.base : data[key],
            html = [];
         // create insert html before adding
         $.each(vals,function(i,val){
              if (val == "eng"){
                valname = "System data"
              }
              else if (val == "met"){
                valname = "Meteorological data"
              }
              else if (val == "ven"){
                valname = "Velocity data"
              }
              else if (val == "salt"){
                valname = "Water property data"
              }
              else if (val == "wave"){
                valname = "Wave data"
              }
              html.push('<option value=' + val + '>'+valname+'</option>')
            // //   html.push('<option>'+val+'</option>')
            //   html.push('<input type=radio name="table" value=' + val + ' checked>' + val)

         });
         // no need to empty the element before adding the new content
         second.html(html.join());
    });


});