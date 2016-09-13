<?
include('settings.php'); // so por causa de lang
#if (isset($_REQUEST['lang']))
#$lang=$_REQUEST['lang'];
#echo "lang=$lang";


$OOF='/home/mma/public_html/oof';
$oof='/~mma/oof';
?>
<head>
<link rel="stylesheet" type="text/css" href="calendar.css">
<link rel="stylesheet" type="text/css" href="../share/styles/nept.css">
<SCRIPT LANGUAGE="JavaScript" SRC="CalendarPopup.js"></SCRIPT>
<SCRIPT LANGUAGE="JavaScript">
function overimg(ob){
  ob.style.borderColor='red';
}
function outimg(ob){
  ob.style.borderColor='#cccccc';
}

function show_main_elem(id,vis){
   ob=this.parent.document.getElementById(id);
   if (vis)
     ob.style.display='';
   else
     ob.style.display='none';
}


function setdata(vari,level,pred,submit){
	document.getElementById('var').value   = vari;
	document.getElementById('level').value = level;
	document.getElementById('pred').value  = pred;
	
        if (vari=='sst'){
          show_main_elem('div_osi_saf_info',1);
        }else{
          show_main_elem('div_osi_saf_info',0);
        }

	if (submit){
//		document.main_form.submit();
          submit_form();
	}
}

function setdate(date,submit){
	document.getElementById('date1xx').value   = date;
	
	if (submit){
		document.main_form.submit();
//             submit_form();
	}
}

function setsome(id,value,submit){
	document.getElementById(id).value   = value;
	
	if (submit){
		submit_form();
	}
}

function setdaily(id,value,submit){
	document.getElementById(id).value   = value;
	
	/*b=document.getElementById('evol_submit');
    if (value)
    b.disabled=true;
    else
    b.disabled=false;
	*/

	if (submit){
		submit_form();
	}
}

function submit_form(){
	sd=document.getElementById('showDaily').value;
	ifr=parent.document.getElementById('data_output');
	mtd=parent.document.getElementById('main_td');

	sd=parseInt(sd);
	if (sd){
		//alert('hhhh 1 =='+sd+'==');
		ifr.style.position='relative';
		ifr.style.width='100%';
        h=440+120;
		ifr.style.height=h+'px'
		mtd.style.height=h+'px';

	}else{
		//alert('hhhh 2 =='+sd+'==');
		ncols=document.getElementById('ncolumns').value;
		nims=document.getElementById('nshown').value;
                vname=document.getElementById('var').value;
                if (vname=='windr'){
                  imW=120;
                  imH=99;
                }else{
 //                 imW=112;
//                  imH=160;

                  imW=144;
                  imH=140;
                }

		nlines=Math.ceil(nims/ncols);
		w=ncols*(imW+15) +10;
		h=nlines*(imH+25) + 150;

		w=Math.max(w,590);
                //alert(w);
		ifr.style.position='absolute';
		ifr.style.width=w+'px';
//                alert(w);
		ifr.style.height=h+'px';
		mtd.style.height=h+20+'px';

		//alert(w)
		//alert(nlines+'  '+ncols);
	}

	
	document.main_form.submit();
}

function OpenNewWindow(cPicture,nWidth,nHeight,cMessage,nBorder){
    NewWindow=window.open("","NewOne","HEIGHT="+nHeight+",WIDTH="+nWidth+",scrollbars=no,resizable=no,top=5,left=5");
    NewWindow.document.write ("<HTML><HEAD><TITLE>"+cMessage);
    NewWindow.document.write ("</TITLE></HEAD>");
    NewWindow.document.write ("<BODY'>");    
    NewWindow.document.write ("<P ALIGN=CENTER>");

    str=document.getElementById(cPicture).src;
    cPicture=str.replace(/_thumb.png/, ".png");
      
    NewWindow.document.write ("<IMG SRC=");
    NewWindow.document.write (cPicture);
    NewWindow.document.write (">");
       

    NewWindow.document.write ("</P>");
    NewWindow.document.write ("<center><FORM><INPUT TYPE='button' VALUE='Close This Window' onClick='self.close()'>");
    NewWindow.document.write ("</FORM></CENTER></BODY></HTML>");
    NewWindow.document.write ("</BODY></HTML>");
    NewWindow.document.close();

    return false;
}

function newsst(id,val){
	document.getElementById(id).src=val;
}


</SCRIPT>
</head>
<body style='background-color: white'>

<?php

//ini_set('display_errors','on');

if (isset($_REQUEST['date']))  $date=$_REQUEST['date'];
elseif (isset($_REQUEST['date1xx']))  $date=$_REQUEST['date1xx'];
else $date=date('d-m-Y');

//print date('d-m-Y');

if (isset($_REQUEST['var']))   $var=$_REQUEST['var'];
else $var='temp';

if (isset($_REQUEST['level'])) $level=$_REQUEST['level'];
else $level='s';

if (isset($_REQUEST['pred']))  $pred=$_REQUEST['pred'];
else $pred=0;

if (isset($_REQUEST['showCurr']))  $showCurr=$_REQUEST['showCurr'];
else $showCurr=0;

if (isset($_REQUEST['showSST']))  $showSST=$_REQUEST['showSST'];
else $showSST=0;

if (isset($_REQUEST['showWind']))  $showWind=$_REQUEST['showWind'];
else $showWind=0;

if (isset($_REQUEST['showDaily']))  $showDaily=$_REQUEST['showDaily'];
else $showDaily=0;

if (isset($_REQUEST['nshown']))  $nims=$_REQUEST['nshown'];
else $nims=8;

if (isset($_REQUEST['ncolumns']))  $ncols=$_REQUEST['ncolumns'];
else $ncols=4;

if (isset($_REQUEST['dtdays']))  $DT=$_REQUEST['dtdays'];
else $DT=1;

$place_default='aveiro';
if (isset($_REQUEST['wrplace']))  $WRPlace=$_REQUEST['wrplace'];
else $WRPlace=$place_default;

if ($showWind) {
	$showHideWind='0';
	$showHideWindStr='hide wind';
}
else{
	$showHideWind='1';
	$showHideWindStr='show wind';
}

if ($showCurr) {
	$showHideCurr='0';
        if ($lang=='pt')
          $showHideCurrStr='ocultar correntes ';
        elseif ($lang=='es')
          $showHideCurrStr='ocultar corrientes';
        else
          $showHideCurrStr='hide currents ';
}
else{
	$showHideCurr='1';
        if ($lang=='pt')
          $showHideCurrStr='ver correntes ';
        elseif ($lang=='es')
          $showHideCurrStr='mostrar corrientes';
        else
          $showHideCurrStr='show currents ';
}

if ($showSST) {
	$showHideSST='0';
	$showHideSSTStr='hide SST';
}
else{
	$showHideSST='1';
	$showHideSSTStr='show SST';
}

if ($showDaily) {
	$showHideDaily='0';
        if ($lang=='pt')
          $showHideDailyStr='evolu&ccedil;&atilde;o';
        elseif ($lang=='es')
          $showHideDailyStr='evoluci&oacute;n';
        else
          $showHideDailyStr='show evolution';

	$evol_submit_disabled='disabled';
}
else{
	$showHideDaily='1';
        if ($lang=='pt')
	  $showHideDailyStr='di&aacute;rio';
        elseif ($lang=='es')
	  $showHideDailyStr='diario';
        else
	  $showHideDailyStr='show daily';

	$evol_submit_disabled='';
}


$DATE=explode('-',$date);

$datePrev=date('d-m-Y',mktime(0,0,0,$DATE[1],$DATE[0]-1,$DATE[2]));
$dateNext=date('d-m-Y',mktime(0,0,0,$DATE[1],$DATE[0]+1,$DATE[2]));

$DATE=implode('',array_reverse($DATE));

if ($level=='s') $depth='surface';
else $depth=-$level;

$today=date('Ymd',time());

$scriptsPath="py_scripts";
$python="/usr/bin/python";

if ($var!='sst' & $var!='wind' & $var!='flt' & $var!='windr')
$isHSLICE=true;
else 
$isHSLICE=false;

if ($showDaily){ ///////////                daily
	
	$cmd_hslice  = "find_files_.py daily hslice  $DATE $showCurr 0 0";
	$cmd_hslicev = "find_files_.py daily hslicev $DATE $var $showCurr $depth 0 0";
	$cmd_flts    = "find_files_.py daily flts    $DATE 0 0";
	$cmd_wind    = "find_files_.py daily wind    $DATE 0 0";
	$cmd_windr   = "find_files_.py daily windr   $DATE 0 0 $WRPlace";
	$cmd_sst     = "find_safofiles.py            $DATE";
	
	$res_hslice = shell_exec("$python $scriptsPath/$cmd_hslice");  $res_hslice  = explode('#',$res_hslice);
	$res_hslicev= shell_exec("$python $scriptsPath/$cmd_hslicev"); $res_hslicev = explode('#',$res_hslicev);
	$res_flts   = shell_exec("$python $scriptsPath/$cmd_flts");    $res_flts    = explode('#',$res_flts);
	$res_wind   = shell_exec("$python $scriptsPath/$cmd_wind");    $res_wind    = explode('#',$res_wind);
	$res_windr  = shell_exec("$python $scriptsPath/$cmd_windr");   $res_windr   = explode('#',$res_windr);
	$res_sst    = shell_exec("$python $scriptsPath/$cmd_sst");     $res_sst     = explode('#',$res_sst);

//        print "$python $scriptsPath/$cmd_hslice";
//        print_r($res_hslice);

print "$python $scriptsPath/$cmd_sst";

}else{           ///////////                evolution
$NFOREC=5;
	if ($level=='s') $depth='surface';
	else $depth=-$level;
	
	// if today, show more 2 days (the forecast !!)
	if ($DATE>=$today){
		$tmp=explode('-',$date);
		$datePred=date('d-m-Y',mktime(0,0,0,$tmp[1],$tmp[0]+$NFOREC-1,$tmp[2]));
		$datePred=explode('-',$datePred);
		$datePred=implode('',array_reverse($datePred));
	}else $datePred=$DATE;
		
	$cmd_hslicev = "find_files_.py evol hslice $datePred $nims $DT $var $showCurr $depth 0 1";
	$cmd_flts    = "find_files_.py evol flts   $datePred $nims $DT 0 1";
	$cmd_wind    = "find_files_.py evol wind   $datePred $nims $DT 0 1";
	$cmd_windr   = "find_files_.py evol windr  $datePred $nims $DT 0 1 $WRPlace";
	$cmd_sst     = "find_safofiles.py          $datePred $nims $DT";
	
	if     ($var=='flt')   $cmd=$cmd_flts;
	elseif ($var=='wind')  $cmd=$cmd_wind;
	elseif ($var=='windr') $cmd=$cmd_windr;
	elseif ($var=='sst')   $cmd=$cmd_sst;
	else                   $cmd=$cmd_hslicev;
//	print "$python $scriptsPath/$cmd";	
	$res = shell_exec("$python $scriptsPath/$cmd"); $res = explode('#',$res);

//        print "$python $scriptsPath/$cmd";
//        print "$python $scriptsPath/$cmd_sst";
//        print_r($res);
}

if ($showDaily){
	// hslice:
	$is_hslice=array();
	foreach ($res_hslice as $r){
//                print "$r<br>";
		if ($r=="$oof/plots/plt0.png")
		$is_hslice[]=False;
		else 
		$is_hslice[]=True;
	}	
	
	// flts:
	if ($res_flts[0]=="$oof/plots/plt0.png")
	$is_flts = FALSE;
	else 
	$is_flts=TRUE;
	
	// wind:
	if ($res_wind[0]=="$oof/plots/plt0.png")
	$is_wind = FALSE;
	else 
	$is_wind=TRUE;	
	
	// sst:
//	if (rtrim($res_sst[sizeof($res_sst)-1]) ==$_SERVER['DOCUMENT_ROOT'].'/~mma/oof/safo_outputs/plt0.png')
	if (basename(rtrim($res_sst[sizeof($res_sst)-1])) =='plt0.png')
	$is_sst = FALSE;
	else 
	$is_sst=TRUE;

	// windR:
	if ($res_windr[0]=="$oof/plots/plt0_wr.png")
	$is_windr = FALSE;
	else 
	$is_windr=TRUE;	

	
}else{
	$is_hslice = array(1,1,1,1,1,1,1,1,1);
	$is_flts   = TRUE;
	$is_wind   = TRUE;
	$is_sst    = TRUE;
	$is_windr  = TRUE;
}

	$is_hslice = array(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1); # etc... not working for now!!

$true = "$oof/share/images/true3_.gif";
$false = "$oof/share/images/false3.gif";


$trueOpts    = 'onmouseover=overimg(this) onmouseout=outimg(this) style="border: 1px solid #cccccc; cursor: pointer" ';
$trueOptsSel = 'style="border: 1px solid red; cursor: pointer" ';

?>

<?//<div style='color: red; font-weight: bold'>TEMPORARY DEVELOPMENT VERSION * * * TEMPORARY DEVELOPMENT VERSION</div>?>

<?//<div style="background: Yellow; padding: 5px; border: 1px solid Orange;">operational model down because HYCOM data storage systems are currently offline</div>?>

<form name='main_form' id='main_form' method="get">

<table border=0 width=100% cellpadding=5 bgcolor='white'>
<tr>
<td>   

<table border=0 width=570px  cellspacing=1 bgcolor='#002266'>
<tr  bgcolor=white>
  <td valign=top>

	<table border=0 width=200px cellpadding=0 cellspacing=0 bgcolor=white height=65px>
	<tr>
	<td valign=top bgcolor='#f5f5f5'>
	
	<table border=0 width=122px cellpadding=0 cellspacing=0 >
	<tr>
		<td>&nbsp;</td>
		<td>0</td>
		<td>10</td>
		<td>50</td>
		<td>100</td>
		<td>200</td>
		<td>bot</td>
		<? //<td>zeta</td>?>
	</tr>
	
	<tr>
		<td>temp</td>
		<td>
		<?php
		if ($var=='temp' and $level=='s') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
		if ($is_hslice[0]) $TF=$true; else $TF=$false;			
		echo "<img onclick='setdata(\"temp\",\"s\",$pred,1)' src='$TF' $true_opts>";	
		?>
		</td>
		<td>
		<?php
		if ($var=='temp' and $level=='10') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
		if ($is_hslice[1]) $TF=$true; else $TF=$false;			
		echo "<img onclick='setdata(\"temp\",10,$pred,1)' src='$TF' $true_opts>";		
		?>		
		</td>		
		<td>
		<?php
		if ($var=='temp' and $level=='50') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
		if ($is_hslice[2]) $TF=$true; else $TF=$false;			
		echo "<img onclick='setdata(\"temp\",50,$pred,1)' src='$TF' $true_opts>";	
		?>		
		</td>
		<td>
		<?php
		if ($var=='temp' and $level=='100') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
		if ($is_hslice[3]) $TF=$true; else $TF=$false;			
		echo "<img onclick='setdata(\"temp\",100,$pred,1)' src='$TF' $true_opts>";			
		?>
		</td>
		<td>
		<?php
		if ($var=='temp' and $level=='200') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
		if ($is_hslice[3]) $TF=$true; else $TF=$false;			
		echo "<img onclick='setdata(\"temp\",200,$pred,1)' src='$TF' $true_opts>";			
		?>
		</td>
                <td>&nbsp;</td>

	</tr>
	<tr>
		<td>salt</td>
		<td>
		<?php
		if ($var=='salt' and $level=='s') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
		if ($is_hslice[4]) $TF=$true; else $TF=$false;			
		echo "<img onclick='setdata(\"salt\",\"s\",$pred,1)' src='$TF' $true_opts>";			
		?>
		</td>
		<td>
		<?php
		if ($var=='salt' and $level=='10') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
		if ($is_hslice[5]) $TF=$true; else $TF=$false;			
		echo "<img onclick='setdata(\"salt\",10,$pred,1)' src='$TF' $true_opts>";			
		?>		
		</td>		
		<td>
		<?php
		if ($var=='salt' and $level=='50') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
		if ($is_hslice[6]) $TF=$true; else $TF=$false;			
		echo "<img onclick='setdata(\"salt\",50,$pred,1)' src='$TF' $true_opts>";			
		?>		
		</td>
		<td>
		<?php
		if ($var=='salt' and $level=='100') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
		if ($is_hslice[7]) $TF=$true; else $TF=$false;			
		echo "<img onclick='setdata(\"salt\",100,$pred,1)' src='$TF' $true_opts>";	
		?>
		</td>
		<td>
		<?php
		if ($var=='salt' and $level=='200') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
		if ($is_hslice[7]) $TF=$true; else $TF=$false;			
		echo "<img onclick='setdata(\"salt\",200,$pred,1)' src='$TF' $true_opts>";	
		?>
		</td>
                <td>&nbsp;</td>
	</tr>

        <tr>
          <td>zeta</td>
          <td colspan=6>
          <?
		if ($var=='zeta') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
		if ($is_hslice[8]) $TF=$true; else $TF=$false;			
		echo "<img onclick='setdata(\"zeta\",\"s\",$pred,1)' src='$TF' $true_opts>";
          ?>
          </td>
        </tr>


        <tr>
          <td>O2</td>
          <td>
          <?php
#          if ($var=='dye_01' and $level=='s') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
#          if ($is_hslice[4]) $TF=$true; else $TF=$false;
#          echo "<img onclick='setdata(\"dye_01\",\"s\",$pred,1)' src='$TF' $true_opts>";
          ?>
          </td>
          <td>
          <?php
#          if ($var=='dye_01' and $level=='10') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
#          if ($is_hslice[5]) $TF=$true; else $TF=$false;
#          echo "<img onclick='setdata(\"dye_01\",10,$pred,1)' src='$TF' $true_opts>";
          ?>
          </td>
          <td>
          <?php
#          if ($var=='dye_01' and $level=='50') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
#          if ($is_hslice[6]) $TF=$true; else $TF=$false;
#          echo "<img onclick='setdata(\"dye_01\",50,$pred,1)' src='$TF' $true_opts>";
          ?>
          </td>
          <td>
          <?php
#          if ($var=='dye_01' and $level=='100') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
#          if ($is_hslice[7]) $TF=$true; else $TF=$false;
#          echo "<img onclick='setdata(\"dye_01\",100,$pred,1)' src='$TF' $true_opts>";
          ?>
         </td>
          <td>
          <?php
#          if ($var=='dye_01' and $level=='200') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
#          if ($is_hslice[7]) $TF=$true; else $TF=$false;
#          echo "<img onclick='setdata(\"dye_01\",200,$pred,1)' src='$TF' $true_opts>";
          ?>
         </td>
          <td>
          <?php
          if ($var=='dye_01' and $level=='0') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
          if ($is_hslice[7]) $TF=$true; else $TF=$false;
          echo "<img onclick='setdata(\"dye_01\",0,$pred,1)' src='$TF' $true_opts>";
          ?>
         </td>
       </tr>

        <tr>
          <td>Miss</td>
          <td>
          <?php
          if ($var=='dye_02' and $level=='s') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
          if ($is_hslice[4]) $TF=$true; else $TF=$false;
          echo "<img onclick='setdata(\"dye_02\",\"s\",$pred,1)' src='$TF' $true_opts>";
          ?>
          </td>
          <td>
          <?php
          if ($var=='dye_02' and $level=='10') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
          if ($is_hslice[5]) $TF=$true; else $TF=$false;
          echo "<img onclick='setdata(\"dye_02\",10,$pred,1)' src='$TF' $true_opts>";
          ?>
          </td>
          <td>
          <?php
          if ($var=='dye_02' and $level=='50') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
          if ($is_hslice[6]) $TF=$true; else $TF=$false;
          echo "<img onclick='setdata(\"dye_02\",50,$pred,1)' src='$TF' $true_opts>";
          ?>
          </td>
          <td>
          <?php
          if ($var=='dye_02' and $level=='100') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
          if ($is_hslice[7]) $TF=$true; else $TF=$false;
          echo "<img onclick='setdata(\"dye_02\",100,$pred,1)' src='$TF' $true_opts>";
          ?>
         </td>
          <td>
          <?php
          if ($var=='dye_02' and $level=='200') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
          if ($is_hslice[7]) $TF=$true; else $TF=$false;
          echo "<img onclick='setdata(\"dye_02\",200,$pred,1)' src='$TF' $true_opts>";
          ?>
         </td>
         <td>&nbsp;</td>
       </tr>








	<tr>
		<td colspan=6 align="right">
		<?php 
		if ($isHSLICE){ 
		echo "
		<div style='cursor:pointer; width: 100px' onclick='setsome(\"showCurr\",$showHideCurr,1)'>
		$showHideCurrStr &nbsp;
		</div>";
		}else echo "<div>&nbsp</div>";
		?>
		</td>	
	</tr>	
	</table>
	
	</td>
	<td valign=top bgcolor='#e2e2e2'>
	  	<table border=0 width=100% cellpadding=0 cellspacing=0>
			<tr>
			<td style='padding-left: 5px'>sst</td>
			<td>
			<?php
			/*
			if ($is_sst){					
				if ($var=='sst') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
				echo "<img onclick='setdata(\"sst\",0,$pred,1)' src='$true' $true_opts>";
			}else echo "<img src='$false' border=0>";
			*/

			if ($var=='sst') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
			if ($is_sst) $TF=$true; else $TF=$false;			
			echo "<img onclick='setdata(\"sst\",0,$pred,1)' src='$TF' $true_opts>";		
			?>		
			</td>
			</tr>
			<tr>
                        <?
                        if ($lang=='pt'){
                           $wind_str='vento';
                           $windr_str='vento (rv)';
                        }elseif($lang=='es'){
                           $wind_str='viento';
                           $windr_str='viento (rv)';
                        }else{
                           $wind_str='wind';
                           $windr_str='wind (wr)';
                        }
                        ?>
			<td style='padding-left: 5px'><?echo $wind_str?></td>
			<td>
			<?php
			/*
			if ($is_wind){					
				if ($var=='wind') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
				echo "<img onclick='setdata(\"wind\",0,$pred,1)' src='$true' $true_opts>";
			}else echo "<img src='$false' border=0>";
			*/

			if ($var=='wind') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
			if ($is_wind) $TF=$true; else $TF=$false;
			echo "<img onclick='setdata(\"wind\",0,$pred,1)' src='$TF' $true_opts>";	
			?>				
			</td>
			</tr>


                        <?/*
                        <tr>
                          <td style='padding-left: 5px'>flts</td>
                          <td>
                          <?php

                          if ($var=='flt') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
                          if ($is_flts) $TF=$true; else $TF=$false;
                          echo "<img onclick='setdata(\"flt\",0,$pred,1)' src='$TF' $true_opts>";
                          ?>
                          </td>
                        </tr>
                        <tr style='background-color: #d4d4d4'>
                          <td style='padding-left: 5px'><? echo $windr_str?></td>
                          <td>
                          <?php
                          if ($var=='windr') $true_opts=$trueOptsSel; else $true_opts=$trueOpts;
                          if ($is_windr) $TF=$true; else $TF=$false;
                          echo "<img onclick='setdata(\"windr\",0,$pred,1)' src='$TF' $true_opts>";
                          ?>
                          </td>
                        </tr>

                        <tr style='background-color: #d4d4d4'>
                          <td colspan=2  style='padding-left: 5px; padding-bottom: 1px'>
                            <select onchange='setdata("windr",0,0,1)'  name='wrplace' id='wrplace'  class=sel style='width:70px'>
                            <?php
                            //$Places=array('gibraltar','s_vicente','cascais','aveiro','viana_cast','bayona','finisterre','a_coruna');
                            $Places=array('a_coruna','finisterre','bayona','viana_cast','aveiro','cascais','s_vicente','gibraltar');
                            $PlacesStr=array('A Coru&ntilde;a','Finisterre','Bayona','Viana do Castelo','Aveiro','Cascais','S&atilde;o Vicente','Gibraltar');

                            $Places=array('salvador____','rio_janeiro_','porto_alegre');
                            $PlacesStr=array('Salvador','Rio de Janeiro','Porto Alegre');

                            $n=-1;
                            foreach ($Places as $p){
                              $n++;
                              if ($p==$WRPlace) $sel='selected';
                              else $sel='';
                              echo "<option value='$p' $sel>$PlacesStr[$n]</option>";
                            }
                            ?>
                           </select>
                         </td>
                       </tr>

                       */?>

		</table>
	
	<td>
	</td>
	</tr>
	</table>

  </td>

  
  <td valign=top width=140px>
    <style>
    	.sel {height: 15px; width:40px;
    		border: 1px solid #002266;
    		background-color: #f5f5f5;
    	}
    </style>
    

    <?
    if ($lang=='pt'){
      $evtopts_str = 'op&ccedil;&otilde;es de evol.';
      $nshown_str  = 'n. de dias';
      $ncols_str   = 'n. colunas';
      $dtdays_str  = 'dt dias';
    }elseif ($lang=='es'){
      $evtopts_str = 'opciones de evol.';
      $nshown_str  = 'n. de d&iacute;as';
      $ncols_str   = 'n. columnas';
      $dtdays_str  = 'dt d&iacute;as';
    }else{
      $evtopts_str='evolution options';
      $nshown_str  = 'n showm';
      $ncols_str   = 'n columns';
      $dtdays_str  = 'dt days';
    }
    ?>

    <table border=0 width=100% cellpadding=0 cellspacing=1 >
    <tr>
    	<td colspan=3><?echo $evtopts_str?></td>
    </tr>
    <tr>
    	<td><?echo $nshown_str?></td>
    	<td>
    	<select name='nshown' id='nshown'  class=sel>
    	<?php 
    	$nshownOps=array(3,5,7,8,10,14);
    	foreach ($nshownOps as $n){
    		if ($n==$nims) $sel='selected';
    		else $sel='';
    		echo "<option value='$n' $sel>$n</option>";
    		
    	}
    	?>
		</select>
    	</td>
    	<td>&nbsp;</td>
    </tr>   
    <tr>
    	<td><?echo $ncols_str?></td>
    	<td>
    	<select name='ncolumns' id='ncolumns'  class=sel>
    	<?php 
    	$ncolsOps=array(3,4,5,6,7);
    	foreach ($ncolsOps as $n){
    		if ($n==$ncols) $sel='selected';
    		else $sel='';
    		echo "<option value='$n' $sel>$n</option>";
    		
    	}
    	?>
		</select>
    	</td>
    	<td>&nbsp;</td>
    </tr> 
    <tr>
    	<td><?echo $dtdays_str?></td>
    	<td>
    	<select name='dtdays' id='dtdays'  class=sel>
    	<?php 
    	$dtOps=array(1,2,3,4,7,14);
    	foreach ($dtOps as $n){
    		if ($n==$DT) $sel='selected';
    		else $sel='';
    		echo "<option value='$n' $sel>$n</option>";
    		
    	}
    	?>
		</select>
    	</td>
<?
if ($lang=='pt'){
$ok_str='ir';
$go_str='ir';
}elseif ($lang=='es'){
$ok_str='ir';
$go_str='ir';
}else{
$ok_str='ok';
$go_str='go';
}
?>
    	<td><input <?php echo $evol_submit_disabled ?> id='evol_submit' type="button" onclick="submit_form()" value='<?echo $ok_str?>' class='sel' style='width: 20px'></td>
    </tr>            
    </table>
    
  </td>  
  
  <td valign=top>
  
  	<table border=0 width=100% cellpadding=0 cellspacing=0>
	<tr>
		<td>

		<SCRIPT LANGUAGE="JavaScript" ID="jscal1xx">
		var cal1xx = new CalendarPopup("testdiv1");
		//cal1xx.showNavigationDropdowns();
		cal1xx.showYearNavigation();
		</SCRIPT>
		
<?if  ($_SERVER['REMOTE_ADDR']=='193.136.173.43')
$inDevel=true;
else
$inDevel=false;

$inDevel=false;
?>

<?if ($inDevel)
echo "        <table border=1>";
else
echo "        <table border=0";
?>
		<tr>
		<td>
			<img src=<?echo "$oof/share/images/go_r15_.gif"?> border=0 onclick='setdate("<?php echo $datePrev?>",1)' style='cursor:pointer'>
		</td>
		<td>
			<INPUT TYPE="text" NAME="date1xx" id="date1xx" value="<?php echo $date?>" SIZE=10 style='border: 1px solid #cccccc'>
		</td>
		<td>
			<img src=<?echo "$oof/share/images/go_r15.gif"?> border=0 onclick='setdate("<?php echo $dateNext?>",1)' style='cursor:pointer'>
		</td>
		<td>
			<A HREF="#" onClick="cal1xx.select(document.forms[0].date1xx,'anchor1xx','dd-MM-yyyy'); return false;" TITLE="" NAME="anchor1xx" ID="anchor1xx">
			<img src=<?echo "$oof/share/images/calendar.gif"?> border=0>
			</A>
		</td>
		<td>
			<input type=submit value='<?echo $go_str?>'>
		</td>
		</tr>
		

                <tr>
                  <td colspan=2>&nbsp;</td>
                  <td colspan=3><img border=0 style='vertical-align: middle' src=<?echo "$oof/share/images/interr_.gif"?>><a href='usage.php?lang=<?echo $lang?>' target='_top'><? echo $usage_str?></a></td>
                </tr>
                <tr>
                  <td colspan=2>
                    <div style='cursor:pointer' onclick='setdaily("showDaily",<?php echo $showHideDaily?>,1)'>
                    <?php echo $showHideDailyStr?>
                    </div>
                  </td>
                  <td colspan=3>
                    <a href='disclaimer.php?lang=<?echo $lang?>' target='_top'><img border=0 style='vertical-align: middle' src=<?echo "$oof/share/images/excl_.gif"?>><? echo $disclaimer_str?></a>
                  </td>
                </tr>

		</table>

		<DIV ID="testdiv1" STYLE="position:absolute;visibility:hidden;background-color:white;layer-background-color:white;"></DIV>
		
		
		<input type="hidden" name='var'   id='var'   value='<?php echo $var   ?>'>
		<input type="hidden" name='level' id='level' value='<?php echo $level ?>'>
		<input type="hidden" name='pred'  id='pred'  value='<?php echo $pred  ?>'>

		<input type="hidden" name='showCurr'  id='showCurr'  value='<?php echo $showCurr   ?>'>
		<input type="hidden" name='showDaily' id='showDaily' value='<?php echo $showDaily  ?>'>
		
		
		
		</td>
	</tr>
	</table>
	
  </td>  
</tr>
</table>


</td>
</tr>
<tr  bgcolor=white>
<td>

<?php
if (!$showDaily){
	
	//print_r($res);
	//print "<p>$cmd<p>";
	
	$DATE=explode('-',$date);

	echo "<table border=0 bgcolor='#002266' cellpadding=5 cellspacing=0>";

	$n=0;
	for ($i=-($nims-1); $i<=0; $i++){		
		
		if ($n/$ncols==floor($n/$ncols)){
			echo "<tr bgcolor='white'>";
			$Col=0;
		}
		$Col++;
		$res2=explode('%',$res[$n]);		
			
		if ($var!='sst'){
			$im   = $res2[0];
			$tag  = $res2[1];
			$prd  = $res2[2];
			$Date = $res2[3];

                        $date_=explode('-',$Date);
                        $date_=implode('/',array($date_[1],$date_[0],$date_[2]));
                        #The DateTime class
                        #(PHP 5 >= 5.2.0)
                        #$datetime=date_create($date_);
                        #$Date=$datetime->format('D d M Y');
                        $date_=strtotime($date_);
                        $Date=strftime('%a %e %b %Y',$date_);

                        $im = str_replace('_thumb.png','.png',$im); // if find_files looks for trhumbs

                        //$IM  = str_replace('/~mma','/home/mma/public_html',$im);	
//                        $IM=$_SERVER['DOCUMENT_ROOT'].$im;
//                        $IM=str_replace('/~mma','/home_neptuno/mma/public_html',$im);

                        $IM=str_replace('/oof','..',$im);
                        $IM=str_replace($oof,$OOF,$im);


			$im_ = str_replace('.png','_thumb.png',$im);
	
			$is = getimagesize($IM);
//                        print "++++++ $IM";
			$h=$is[1]+10;
			$w=$is[0];								
			$newWindowWidth  = $w+40;
			$newWindowHeight = $h+70;
		
			// forec bg:
			if ($tag=='2') $divbg='#d0b3b3';
			else $divbg='#f0f0f0';
		
			$msg='no title';
			echo "<td align=center  style='padding-left: 0px; padding-right: 10px'>
			<div style='border: 1px solid #d2d9e7'>
			<div style='background-color: $divbg; border-bottom: 1px solid #d2d9e7'>$Date</div>
			<a  onClick=\"OpenNewWindow('im_$n',$newWindowWidth,$newWindowHeight,'$msg', 0);return false;\" style='cursor: pointer'>
			<img id='im_$n' src='$im_' border=0>
			</div>
			</a> 
			</td>";
		}else{
				$Date=$res2[0];
				$Date=substr($Date,6).'-'.substr($Date,4,2);
				$best=$res2[sizeof($res2)-1];
				
				// other ims:
				$ims=array_slice($res2,1,sizeof($res2)-2);
				sort($ims);
				$hours=array();
				foreach ($ims as $I){
					$hours[]=substr($I,sizeof($I)-9,2);
				}
				//print "$Date $best<br>";
				
				$best=rtrim($best); // one last char in the last image
				
				$IM=$best;
#				$im  = str_replace($_SERVER['DOCUMENT_ROOT'],$_SERVER['SERVER_NAME'],$best);
#				$im  = str_replace($_SERVER['DOCUMENT_ROOT'],'',$best);
//                              $im=str_replace('/home_neptuno/mma/public_html','/~mma',$best);
                                $im=str_replace('/oper/roms/web/oof','/oof',$best);
//print " $im<br>";
				$im_ = str_replace('.png','_thumb.png',$im);
//print " $im_<br>";
				
				$hour=substr($IM,sizeof($IM)-9,2);				
	
				$is = getimagesize($IM);
				$h=$is[1]+10;
				$w=$is[0];								
				$newWindowWidth  = $w+40;
				$newWindowHeight = $h+70;
		
				$divbg='#f0f0f0';
		
				$msg='no title';
				echo "<td align=center  style='padding-left: 0px; padding-right: 10px'>
				<div style='border: 1px solid #d2d9e7'>
				<div style='background-color: $divbg; border-bottom: 1px solid #d2d9e7'>$Date";
				
				if (sizeof($ims)>1){
					//echo " $hour h";
					echo " &nbsp; ";
					for ($I=0; $I<sizeof($ims);$I++){
#						$tmp = str_replace($_SERVER['DOCUMENT_ROOT'],'',$ims[$I]);					
//						$tmp = str_replace('/home_neptuno/mma/public_html','/~mma',$ims[$I]);
                                                $tmp=str_replace('/oper/roms/web/oof','/oof',$ims[$I]);

				    	$tmp = str_replace('.png','_thumb.png',$tmp);
				    	if ($hours[$I]==$hour)
							echo " <small style='cursor: pointer; color: green' onclick=newsst('im_$n','$tmp')>";
				    	else 
							echo " <small style='cursor: pointer; color: #A60202' onclick=newsst('im_$n','$tmp')>";
						echo $hours[$I] ."";
						echo "</small>";
					}
				}
				
				echo "
				</div>
				<a onClick=\"OpenNewWindow('im_$n',$newWindowWidth,$newWindowHeight,'$msg', 0);return false;\" style='cursor: pointer'>
				<img id='im_$n' src='$im_' border=0>
				</div>
				</a> 
				</td>";
				
				
			//}
			
			
		}
		if ($n/$ncols==floor($n/$ncols))
		echo "</tr'>";	
		$n++;
	}
	if ($Col<$ncols){
		for ($i=1;$i<=$ncols-$Col;$i++)
		echo "<td>&nbsp;</td>";
		echo "</tr>";
	} 
	
	echo "</table>";	
}else{
	
	
		
		if ($var=='flt'){
			$im=$res_flts[0];
//		}elseif ($var=='wind'){
//			$im=$res_wind[0];

//                }elseif ($var=='windr'){
//                  $im=$res_windr[0];

		}elseif ($var=='sst'){
			$best=$res_sst[sizeof($res_sst)-1];
			$hour=substr($best,sizeof($best)-10,2);
				
			// other ims:
			$ims=array_slice($res_sst,0,sizeof($res_sst)-1);		
			sort($ims);
		
			$hours=array();
			foreach ($ims as $I){
				$hours[]=substr($I,sizeof($I)-9,2);
			}
		
			$s='';
			if (sizeof($ims)>1){
				for ($I=0; $I<sizeof($ims);$I++){
//					$tmp = str_replace($_SERVER['DOCUMENT_ROOT'],'',$ims[$I]);
//                                      $tmp=str_replace('/home_neptuno/mma/public_html','/~mma',$ims[$I]);
                                        $tmp=str_replace('/oper/roms/web/oof','/oof',$ims[$I]);
					
							if ($hours[$I]==$hour) $cor='green';
					else $cor='#A60202';
					
					$s=$s." <small style='cursor: pointer; color: $cor' onclick=newsst('im_daily','$tmp')>$hours[$I]</small>";
				}
			}				
			$im=str_replace($_SERVER['DOCUMENT_ROOT'],'',$best);
//			$im=str_replace('/home_neptuno/mma/public_html','/~mma',$best);
                        $im=str_replace('/oper/roms/web/oof','/oof',$best);
			
		}elseif ($var=='wind' | $var=='windr' | $isHSLICE){ // hslicev
                  $s='';
		
			if ($isHSLICE){
				$im  = $res_hslicev[0];
				$tag = $res_hslicev[1];
				$prd = $res_hslicev[2];
			}elseif ($var=='wind'){
				$im  = $res_wind[0];
				$tag = $res_wind[1];
				$prd = $res_wind[2];
			}elseif ($var=='windr'){
				$im  = $res_windr[0];
				$tag = $res_windr[1];
				$prd = $res_windr[2];
			}


			if ($tag==2){
	  			$dd=$prd;

	  			$tmp=basename($im);
	  			if ($isHSLICE){	  			
	  				$ytmp = substr($tmp,0,4);
	  				$mtmp = substr($tmp,4,2); 
	  				$dtmp = substr($tmp,6,2); 
	  			}elseif ($var=='wind'){
	  				$ytmp = substr($tmp,5,4);
	  				$mtmp = substr($tmp,9,2);
	  				$dtmp = substr($tmp,11,2);		  				
	  			}elseif ($var=='windr'){
	  				$ytmp = substr($tmp,10,4);
	  				$mtmp = substr($tmp,14,2);
	  				$dtmp = substr($tmp,16,2);		  				
                                }
	  			//print "$dtmp $mtmp $ytmp";
	  			//$imdate = date('d-m-Y',mktime(0,0,0,$dtmp,$mtmp,$ytmp));
	  			$imdate="$dtmp-$mtmp-$ytmp";
	  		
	  			if ($DATE === $today) $sdate='today';
	  			else $sdate=$date;
	  		
				if ($dd==0)
				$s="Forecast for $sdate";
				elseif ($dd==1)
				$s="Forecast for $sdate ($imdate + $prd day)";
				else
				$s="Forecast for $sdate ($imdate + $prd days)"; 
				//$s="Forecast (today + $dd days)";
			}
		
		}
		

if (!isset($s))
$s='&nbsp;';

		echo "<table cellpadding=0 cellspacing=0><tr>";
		echo "<td valign=top><img  id=im_daily src='$im' align=left></td>";
		echo "<td valign=top class=subtitles>$s</td>";		
		echo "</tr></table>";
}


?>


</td>
</tr>
</table>

</form>

<?//<div style='color: red; font-weight: bold'>TEMPORARY DEVELOPMENT VERSION * * * TEMPORARY DEVELOPMENT VERSION</div>?>
