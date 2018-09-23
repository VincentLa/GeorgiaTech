<?php

include('lib/common.php');
// written by GTusername4

if (!isset($_SESSION['email'])) {
	header('Location: login.php');
	exit();
}

    $query = "SELECT firstname, lastname, sex, birthdate, currentcity, hometown " .
		 "FROM user " .
		 "INNER JOIN regularuser ON user.email = regularuser.email " .
		 "WHERE user.email = '{$_SESSION['email']}'";

    $result = mysqli_query($db, $query);
    include('lib/show_queries.php');
 
    if (!empty($result) && (mysqli_num_rows($result) > 0) ) {
        $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
    } else {
        array_push($error_msg,  "Query ERROR: Failed to get user profile..." . __FILE__ ." : ". __LINE__ );
    }
    
	
if ($_SERVER['REQUEST_METHOD'] == 'POST') {

	$comment = mysqli_real_escape_string($db, $_POST['comment']);

	if (empty($comment)) {
		 array_push($error_msg,  "Error: You must provide a comment ");
	}
	else{
		$query = "INSERT INTO statusupdate (email, dateandtime, text) " .
					 "VALUES ('{$_SESSION['email']}', NOW(), '$comment')";
					 
		$commentID = mysqli_query($db, $query);
		 if($showQueries){
			  array_push($query_msg,  $query);
		 }
		
		 if (is_numeric($commentID) && (mysqli_num_rows($commentID) == 1) ) {
			array_push($error_msg,  "Error: Failed to add comment ..." . __FILE__ ." : ". __LINE__ );
		}
	}
}

?>

<?php include("lib/header.php"); ?>
		<title>GTOnline Status Updates</title>
	</head>
	
	<body>
		<div id="main_container">
        <?php include("lib/menu.php"); ?>
			
        <div class="center_content">
            <div class="center_left">
                <div class="title_name">
                    <?php print $row['firstname'] . ' ' . $row['lastname']; ?>
                </div>          
                <div class="features">   
                        
                            <div class="profile_section">						
                                <div class="subtitle">Status Updates    (Note: intentionally missing functionality)</div>
                                <form name="searchform" action="view_updates.php" method="POST">
                                    <table >								
                                        <tr>
                                            <td class="item_label">Add Comment</td>
                                            <td><input type="textbox" name="comment" /></td>
                                        </tr>
                                    </table>
                                    <a href="javascript:searchform.submit();" class="fancy_button">Update</a> 					
                                    </form>							
                            </div>
                        
            
                        <div class="profile_section">
                                <div class="subtitle">Prior Status Updates</div>
                                
                                <?php			
                                    $query = "SELECT dateandtime, text " .
                                             "FROM statusupdate " .
                                             "WHERE statusupdate.email = '{$_SESSION['email']}' ";
                                    
                                    $result = mysqli_query($db, $query);
                                    if (!empty($result) && (mysqli_num_rows($result) == 0) ) {
                                       
                                        array_push($error_msg,  "Query ERROR: Failed to get freind requests you sent" . __FILE__ ." : ". __LINE__ );
                                    }
                                    
                                    $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
                                    $count = mysqli_num_rows($result);
                                   
                                   if ($row) {
                                                            
                                        print '<table>';
                                        print '<tr>';
                                        print '<td class="heading">Date</td>';
                                        print '<td class="heading">Status</td>';
                                        print '</tr>';
                                    
                                        while ($row){            
                                            print '<tr>';
                                            print '<td>' . $row['dateandtime'] . '</td>';
                                            print '<td>' . $row['text'] . '</td>';
                                            print '</tr>';
                                            
                                            $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
                                        }
                                            print '</table>';
                                   }
                                    ?>
                              </div>     
                        </div> 			
                    </div> 

                    <?php include("lib/error.php"); ?>
                        
                    <div class="clear"></div> 		
            </div>    

               <?php include("lib/footer.php"); ?>
				 
		</div>
	</body>
</html>