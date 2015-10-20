<?php
$stnid = $argv[1];
$mospage = fopen("http://www.nws.noaa.gov/cgi-bin/mos/getall.pl?sta=$stnid","r");
$precipout = fopen("precip.dat","w");

fwrite($precipout,"$stnid\n");

$numfcst = 0;

while(!feof($mospage) && $numfcst < 3){
	$line = fgets($mospage);
	$words = preg_split("/\s/",$line,NULL,PREG_SPLIT_NO_EMPTY);
	if(count($words) > 0){
		if($words[0] == $stnid){
			$numfcst++;
			$model = $words[1];
			$runtime = $words[5];
			if($runtime >= 100)	$runtime = $runtime / 100;
		} elseif($words[0] == "HR"){
			$hrs = $words;
		} elseif($words[0] == "N/X"){
			$hi = max($words[1],$words[2]);
			$lo = min($words[1],$words[2]);
                } elseif($words[0] == "X/N"){
                        $hi = max($words[2],$words[3]);
                        $lo = min($words[2],$words[3]);
		} elseif($words[0] == "TMP"){
			$temp = $words;
		} elseif($words[0] == "WSP"){
			$wind = $words;
		} elseif($words[0] == "Q06"){
			$precip6 = $words;
		} elseif($words[0] == "Q12"){
			$precip12 = $words;
//		} elseif($words[0] == "T12"){	//do calculations and flush
                } elseif($words[0] == "VIS"){   //T12 not present in Alaska
			$startindex = -1;
			$endindex = -1;
			$i = 2;
			while($endindex == -1){
				if($hrs[$i] == "06" && $startindex == -1){
					$startindex = $i;
					$startq = floor(($startindex - 3)/ 2) + 2;
					$startq12 = floor(($startindex + 2)/ 4) ;
				} elseif($hrs[$i] == "06"){
					$endindex = $i;
				}//end if
				$i++;
			}//end while
			$daylength = $endindex - $startindex;
			$temp = array_slice($temp,$startindex,$daylength+1);
			$wind = array_slice($wind,$startindex,$daylength+1);
			$precip6 = array_slice($precip6,$startq,4);
			$precip12 = array_slice($precip12,$startq12,3);
			$maxtemp = max($temp);
			$maxtemp = max($maxtemp, $hi);
			$mintemp = min($temp);
			$mintemp = min($mintemp, $lo);
			$maxwind = max($wind);
			$preciptally6 = array_count_values($precip6);
			//'@' symbol suppresses warnings about accessing non-existent array indices
			@$precipmin6=$preciptally6[1] * 0.01 + $preciptally6[2] * 0.10 + $preciptally6[3] * 0.25 + $preciptally6[4] * 0.50 + $preciptally6[5] * 1.00 + $preciptally6[6] * 2.00;
			@$precipmax6=$preciptally6[1] * 0.09 + $preciptally6[2] * 0.24 + $preciptally6[3] * 0.49 + $preciptally6[4] * 0.99 + $preciptally6[5] * 1.99 + $preciptally6[6] * 2.00;
			$preciptally12 = array_count_values($precip12);
			@$precipmin12=$preciptally12[1] * 0.01 + $preciptally12[2] * 0.10 + $preciptally12[3] * 0.25 + $preciptally12[4] * 0.50 + $preciptally12[5] * 1.00 + $preciptally12[6] * 2.00;
			@$precipmax12=$preciptally12[1] * 0.09 + $preciptally12[2] * 0.24 + $preciptally12[3] * 0.49 + $preciptally12[4] * 0.99 + $preciptally12[5] * 1.99 + $preciptally12[6] * 2.00;
			$precipmin=min($precipmin6,$precipmin12);
			$precipmax=min($precipmax6,$precipmax12);
			if($precipmin == $precipmax){
				print("$model ${runtime}Z MOS: $maxtemp/$mintemp/$maxwind/$precipmin\n");
			}else{
				print("$model ${runtime}Z MOS: $maxtemp/$mintemp/$maxwind/($precipmin\" to $precipmax\")\n");
			}// end if
                        fwrite($precipout,"$precipmin\n$precipmax\n");
		}// end if
	}//end if
}// end while

fclose($precipout);
fclose($mospage);
?>
