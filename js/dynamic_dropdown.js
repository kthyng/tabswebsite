
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
    "BURL1": ["ndbc"],
    "g06010": ["ports"],
    "mc0101": ["ports"],
    "sn0101": ["ports"],
    "sn0201": ["ports"],
    "sn0301": ["ports"],
    "sn0401": ["ports"],
    "sn0501": ["ports"],
    "sn0701": ["ports"],
    "lc0101": ["ports"],
    "lc0201": ["ports"],
    "mg0101": ["ports"],
    '8770475': ["tcoon"],
    '8770520': ["tcoon"],
    '8770733': ["tcoon"],
    '8770777': ["tcoon"],
    '8770808': ["tcoon"],
    '8770822': ["tcoon"],
    '8770971': ["tcoon"],
    '8771486': ["tcoon"],
    '8771972': ["tcoon"],
    '8772985': ["tcoon"],
    '8773037': ["tcoon"],
    '8773146': ["tcoon"],
    '8773259': ["tcoon"],
    '8773701': ["tcoon"],
    '8774230': ["tcoon"],
    '8774513': ["tcoon"],
    '8775237': ["tcoon"],
    '8775241': ["tcoon"],
    '8775244': ["tcoon"],
    '8775283': ["tcoon"],
    '8775296': ["tcoon"],
    '8775792': ["tcoon"],
    '8776139': ["tcoon"],
    '8776604': ["tcoon"],
    '8777812': ["tcoon"],
    '8778490': ["tcoon"],
    '8779280': ["tcoon"],
    '8779748': ["tcoon"],
    '8779749': ["tcoon"],
    '8734673': ["nos"],
    '8735180': ["nos"],
    '8741003': ["nos"],
    '8741041': ["nos"],
    '8741094': ["nos"],
    '8741501': ["nos"],
    '8741533': ["nos"],
    '8747437': ["nos"],
    '8760721': ["nos"],
    '8760922': ["nos"],
    '8761305': ["nos"],
    '8761724': ["nos"],
    '8764227': ["nos"],
    '8764314': ["nos"],
    '8766072': ["nos"],
    '8768094': ["nos"],
    '8770570': ["nos"],
    '8770613': ["nos"],
    '8771013': ["nos"],
    '8771341': ["nos"],
    '8771450': ["nos"],
    '8773767': ["nos"],
    '8775870': ["nos"],
    '8779770': ["nos"]
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
        else if (valorig == "ports"){
          valnameorig = "PORTS buoy"
        }
        else if (valorig == "tcoon"){
          valnameorig = "TCOON buoy"
        }
        else if (valorig == "nos"){
          valnameorig = "NOS buoy"
        }
        // only create html if initial table value exists
        // also only use table variable if it is an option for the buoy
        if (valorig && $.inArray(valorig, vals) != -1){
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
              else if (val == "ports"){
                valname = "PORTS buoy"
              }
              else if (val == "tcoon"){
                valname = "TCOON buoy"
              }
              else if (val == "nos"){
                valname = "NOS buoy"
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
