<?php   
     
     if($dumpResults){  
        ob_start();
        var_dump($result);
        $debug = ob_get_clean();
        //$debug = var_export($result, true);
        array_push($query_msg, $debug . NEWLINE);
      }
    
    if($showQueries){
        
        if(is_bool($result)) {
            array_push($query_msg,  $query . ';' . NEWLINE);
        } else {
            
                 if($showCounts){
                    array_push($query_msg,  $query . ';');
                    array_push($query_msg,  "Result Set Count: ". mysqli_num_rows($result). NEWLINE);
                 } else {
                     array_push($query_msg,  $query . ';'. NEWLINE);
                 }
            } 
        }
?>