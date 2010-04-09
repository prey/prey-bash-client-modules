BEGIN { 
UNIT = 0
ORS = "#"}

/Vendor/ { UNIT+=1 ; print UNIT"_Vendor="$2 ; cap=0}
/Model: /{ print UNIT"_Model="$2" "$3 }
/Capacity: / && cap==0 { print UNIT"_Capacity="$2$3 ; cap=1}
                                         
END {  }