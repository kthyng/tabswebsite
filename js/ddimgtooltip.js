/* Image w/ description tooltip v2.0
* Created: April 23rd, 2010. This notice must stay intact for usage
* Author: Dynamic Drive at http://www.dynamicdrive.com/
* Visit http://www.dynamicdrive.com/ for full source code
*/


var ddimgtooltip={

	tiparray:function(){
		var tooltips=[]
		//define each tooltip below: tooltip[inc]=['path_to_image', 'optional desc', optional_CSS_object]
		//For desc parameter, backslash any special characters inside your text such as apotrophes ('). Example: "I\'m the king of the world"
		//For CSS object, follow the syntax: {property1:"cssvalue1", property2:"cssvalue2", etc}
        // tooltips[0]=["http://tabs.gerg.tamu.edu/tglo/DailyData/Data/tabs_B_ven.png", "", {width:'auto', height: 650}]
        tooltips[0]=["daily/tabs_B_ven_low.png", "", {width:'auto', height: 'auto'}]
		tooltips[1]=["daily/tabs_D_ven_low.png", "", {width:'auto', height: 'auto'}]
		tooltips[2]=["daily/tabs_F_ven_low.png", "", {width:'auto', height: 'auto'}]
		tooltips[3]=["daily/tabs_J_ven_low.png", "", {width:'auto', height: 'auto'}]
		tooltips[4]=["daily/tabs_K_ven_low.png", "", {width:'auto', height: 'auto'}]
		tooltips[5]=["daily/tabs_R_ven_low.png", "", {width:'auto', height: 'auto'}]
		tooltips[6]=["daily/tabs_V_ven_low.png", "", {width:'auto', height: 'auto'}]
		tooltips[7]=["daily/tabs_W_ven_low.png", "", {width:'auto', height: 'auto'}]
		tooltips[8]=["daily/tabs_X_ven_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[9]=["daily/ndbc_42001_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[10]=["daily/ndbc_42002_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[11]=["daily/ndbc_42019_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[12]=["daily/ndbc_42020_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[13]=["daily/ndbc_42035_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[14]=["daily/ndbc_42036_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[15]=["daily/ndbc_42039_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[16]=["daily/ndbc_42040_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[17]=["daily/ndbc_SRST2_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[18]=["daily/ndbc_PTAT2_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[19]=["daily/ndbc_BURL1_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[20]=["daily/ndbc_GISL1_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[21]=["daily/ndbc_AMRL1_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[22]=["daily/ndbc_PSTL1_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[23]=["daily/tcoon_8770475_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[24]=["daily/tcoon_8770520_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[25]=["daily/tcoon_8770733_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[26]=["daily/tcoon_8770777_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[27]=["daily/tcoon_8770808_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[28]=["daily/tcoon_8770822_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[29]=["daily/tcoon_8770971_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[30]=["daily/tcoon_8771486_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[31]=["daily/tcoon_8771972_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[32]=["daily/tcoon_8772985_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[33]=["daily/tcoon_8773037_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[34]=["daily/tcoon_8773146_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[35]=["daily/tcoon_8773259_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[36]=["daily/tcoon_8773701_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[37]=["daily/tcoon_8774230_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[38]=["daily/tcoon_8774513_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[39]=["daily/tcoon_8775237_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[40]=["daily/tcoon_8775241_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[41]=["daily/tcoon_8775244_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[42]=["daily/tcoon_8775283_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[43]=["daily/tcoon_8775296_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[44]=["daily/tcoon_8775792_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[45]=["daily/tcoon_8776139_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[46]=["daily/tcoon_8776604_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[47]=["daily/tcoon_8777812_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[48]=["daily/tcoon_8778490_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[49]=["daily/tcoon_8779280_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[50]=["daily/tcoon_8779748_low.png", "", {width:'auto', height: 'auto'}]
        tooltips[51]=["daily/tcoon_8779749_low.png", "", {width:'auto', height: 'auto'}]







		//tooltips[0]=["red_balloon.gif", "Here is a red balloon<br /> on a white background", {background:"#FFFFFF", color:"black", border:"5px ridge darkblue"}]
		//tooltips[1]=["duck2.gif", "Here is a duck on a light blue background.", {background:"#DDECFF", width:"200px"}]
		//tooltips[2]=["../dynamicindex14/winter.jpg"]
		//tooltips[3]=["../dynamicindex17/bridge.gif", "Bridge to somewhere.", {background:"white", font:"bold 12px Arial"}]

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
