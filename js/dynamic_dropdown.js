
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
    "L": ["ven", "eng"],
    "M": ["ven", "eng"],
    "N": ["ven", "eng", "met", "salt", "wave"],
    "P": ["ven", "eng"],
    "R": ["ven", "eng", "salt"],
    "S": ["ven", "eng"],
    "V": ["ven", "eng", "met", "salt", "wave"],
    "W": ["ven", "eng", "salt"],
    "X": ["ven", "eng", "met", "salt", "wave"],
    "42001": ["ndbc"],
    "42002": ["ndbc"],
    "42007": ["ndbc"],
    "42019": ["ndbc"],
    "42020": ["ndbc"],
    "42035": ["ndbc"],
    "42036": ["ndbc"],
    "42038": ["ndbc"],
    "42039": ["ndbc"],
    "42040": ["ndbc"],
    "SRST2": ["ndbc"],
    "PTAT2": ["ndbc"],
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
        // Include at the top the initial input value if it exists
        valorig = document.getElementsByName("table")[0].value;
        if (valorig == "eng"){
          valnameorig = "System data"
        }
        else if (valorig == "met"){
          valnameorig = "Atmospheric conditions"
        }
        else if (valorig == "ven"){
          valnameorig = "Velocities"
        }
        else if (valorig == "salt"){
          valnameorig = "Water properties"
        }
        else if (valorig == "wave"){
          valnameorig = "Waves"
        }
        else if (valorig == "ndbc"){
          valnameorig = "NDBC buoy"
        }
        // only create html if initial table value exists
        if (valorig){
            html.push('<option value=' + valorig + '>'+valnameorig+'</option>')
        }
         // create insert html before adding
         $.each(vals,function(i,val){
              // skip if already included
              if (val == valorig){
                return true
              }
              if (val == "eng"){
                valname = "System data"
              }
              else if (val == "met"){
                valname = "Atmospheric conditions"
              }
              else if (val == "ven"){
                valname = "Velocities"
              }
              else if (val == "salt"){
                valname = "Water properties"
              }
              else if (val == "wave"){
                valname = "Waves"
              }
              else if (val == "ndbc"){
                valname = "NDBC buoy"
              }
              html.push('<option value=' + val + '>'+valname+'</option>')
            // //   html.push('<option>'+val+'</option>')
            //   html.push('<input type=radio name="table" value=' + val + ' checked>' + val)

         });
         // no need to empty the element before adding the new content
         second.html(html.join());
    });
    $("#json-one").change();

});
