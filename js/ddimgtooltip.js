/* Image w/ description tooltip v2.0
* Created: April 23rd, 2010. This notice must stay intact for usage
* Author: Dynamic Drive at http://www.dynamicdrive.com/
* Visit http://www.dynamicdrive.com/ for full source code
*/

// Read in active buoy list from buoys.csv file to array csvData
var url = "includes/buoys.csv";

// https://stackoverflow.com/questions/26416304/reading-csv-file-in-to-an-array-using-javascript
var request = new XMLHttpRequest();
request.open("GET", url, false);
request.send();

var buoylist = new Array();
var jsonObject = request.responseText.split(/\r?\n|\r/);
// get first line for header info
var colnames = jsonObject[0].split(',');
// loop over colnames to find "active" column
for (var j = 0; j < colnames.length; j++) {
  // save column number for "buoy" name column
  if (colnames[j] == 'buoy') {
    var ibuoycol = j;
  }
  // save column number for "active" column
  else if (colnames[j] == 'active') {
    var iactivecol = j;
  }
}

// search for active buoys and save them to buoylist
for (var i = 1; i < jsonObject.length; i++) {
  var line = jsonObject[i].split(',');
  // loop over columns in line
  if (line[iactivecol] == "TRUE") {
    buoylist.push(line[ibuoycol]);
  }
}

var ddimgtooltip={

	tiparray:function(){
		var tooltips=[]
		//define each tooltip below: tooltip[inc]=['path_to_image', 'optional desc', optional_CSS_object]
		//For desc parameter, backslash any special characters inside your text such as apotrophes ('). Example: "I\'m the king of the world"
		//For CSS object, follow the syntax: {property1:"cssvalue1", property2:"cssvalue2", etc}
        // tooltips[0]=["http://tabs.gerg.tamu.edu/tglo/DailyData/Data/tabs_B_ven.png", "", {width:'auto', height: 650}]

        for (var i = 0; i < buoylist.length; i++) {
          // figure out form of filename
          if (buoylist[i].length == 1) {
            filename = "daily/tabs_" + buoylist[i] + "_sum_low.png";
          }
          else {
            filename = "daily/" + buoylist[i] + "_low.png";
          }
          tooltips.push([filename, "", {width:'auto', height: 'auto'}]);
        }

		return tooltips //do not remove/change this line
	}(),

	tooltipoffsets: [20, -30], //additional x and y offset from mouse cursor for tooltips

	//***** NO NEED TO EDIT BEYOND HERE

	tipprefix: 'imgtip', //tooltip ID prefixes

	createtip:function($, tipid, tipinfo){
		if ($('#'+tipid).length==0){ //if this tooltip doesn't exist yet
			return $('<div id="' + tipid + '" class="ddimgtooltip" />').html(
				'<div style="text-align:center"><img src="' + tipinfo[0] + '" /></div>'
				+ ((tipinfo[1])? '<div style="text-align:left; margin-top:5px">'+tipinfo[1]+'</div>' : '')
				)
			.css(tipinfo[2] || {})
			.appendTo(document.body)
		}
		return null
	},

	positiontooltip:function($, $tooltip, e){
		var x=e.pageX+this.tooltipoffsets[0], y=e.pageY+this.tooltipoffsets[1]
		var tipw=$tooltip.outerWidth(), tiph=$tooltip.outerHeight(),
		x=(x+tipw>$(document).scrollLeft()+$(window).width())? x-tipw-(ddimgtooltip.tooltipoffsets[0]*2) : x
		y=(y+tiph>$(document).scrollTop()+$(window).height())? $(document).scrollTop()+$(window).height()-tiph-10 : y
		$tooltip.css({left:x, top:y})
	},

	showbox:function($, $tooltip, e){
		$tooltip.show()
		this.positiontooltip($, $tooltip, e)
	},

	hidebox:function($, $tooltip){
		$tooltip.hide()
	},


	init:function(targetselector){
		jQuery(document).ready(function($){
			var tiparray=ddimgtooltip.tiparray
			var $targets=$(targetselector)
			if ($targets.length==0)
				return
			var tipids=[]
			$targets.each(function(){
				var $target=$(this)
				$target.attr('rel').match(/\[(\d+)\]/) //match d of attribute rel="imgtip[d]"
				var tipsuffix=parseInt(RegExp.$1) //get d as integer
				var tipid=this._tipid=ddimgtooltip.tipprefix+tipsuffix //construct this tip's ID value and remember it
				var $tooltip=ddimgtooltip.createtip($, tipid, tiparray[tipsuffix])
				$target.mouseenter(function(e){
					var $tooltip=$("#"+this._tipid)
					ddimgtooltip.showbox($, $tooltip, e)
				})
				$target.mouseleave(function(e){
					var $tooltip=$("#"+this._tipid)
					ddimgtooltip.hidebox($, $tooltip)
				})
				$target.mousemove(function(e){
					var $tooltip=$("#"+this._tipid)
					ddimgtooltip.positiontooltip($, $tooltip, e)
				})
				if ($tooltip){ //add mouseenter to this tooltip (only if event hasn't already been added)
					$tooltip.mouseenter(function(){
						ddimgtooltip.hidebox($, $(this))
					})
				}
			})

		}) //end dom ready
	}
}

//ddimgtooltip.init("targetElementSelector")
ddimgtooltip.init("*[rel^=imgtip]")
