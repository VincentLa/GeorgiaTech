<?php

include('lib/common.php');
// written by GTusername4

if (!isset($_SESSION['email'])) {
	header('Location: login.php');
	exit();
}

    $query = "SELECT firstname, lastname " .
             "FROM user " .
             "WHERE user.email = '{$_SESSION['email']}'";
             
    $result = mysqli_query($db, $query);
        include('lib/show_queries.php');
        
    if (!empty($result) && (mysqli_num_rows($result) > 0) ) {
        $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
        $count = mysqli_num_rows($result);
    } else {
            array_push($error_msg,  "SELECT ERROR: user profile..." . __FILE__ ." : ". __LINE__ );
    }

    $user_name = $row['firstname'] . " " . $row['lastname'];

if (!empty($_GET['accept_request'])) {

	$email = mysqli_real_escape_string($db, $_GET['accept_request']);

	$query = "UPDATE friendship " .
			 "SET dateconnected = NOW() " .
			 "WHERE friendemail = '{$_SESSION['email']}' " .
			 "AND email = '$email'";

	$result = mysqli_query($db, $query);
    include('lib/show_queries.php');

     if (mysqli_affected_rows($db) < 1) {
        array_push($error_msg,  "UPDATE ERROR: accept friendship ..." . __FILE__ ." : ". __LINE__ );
	}
	
        //SELECT relationship FROM friendship WHERE friendship.friendemail ='michael@bluthco.com' AND  friendship.email = 'pam@dundermifflin.com';
         $query = "SELECT relationship FROM friendship WHERE friendship.email = '$email' AND friendship.friendemail = '{$_SESSION['email']}' ";
         $result = mysqli_query($db, $query);
         $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
         $relationship = $row['relationship']; 

		$query = "INSERT INTO friendship (email, friendemail, relationship, dateconnected) " .
				 "VALUES ('{$_SESSION['email']}', '$email', '$relationship', NOW() )";
        $queryID = mysqli_query($db, $query);
            
		if (mysqli_affected_rows($db) > 0) {
			 include('lib/show_queries.php');
		} else{
			array_push($error_msg, "INSERT ERROR: friendship " . __FILE__ ." : ". __LINE__ );
		}
}

if (!empty($_GET['reject_request'])) {

	$email = mysqli_real_escape_string($db, $_GET['reject_request']);

	$query = "DELETE FROM friendship " .
			 "WHERE dateconnected IS NULL " .
			 "AND friendemail = '{$_SESSION['email']}' " .
			 "AND email = '$email'";

	$result = mysqli_query($db, $query);
    include('lib/show_queries.php');
 
     if (mysqli_affected_rows($db) < 1) {
        array_push($error_msg,  "DELETE ERROR: reject request... " . __FILE__ ." : ". __LINE__ );
	}
	
}

if (!empty($_GET['cancel_request'])) {

	$email = mysqli_real_escape_string($db, $_GET['cancel_request']);

	$query = "DELETE FROM friendship " .
			 "WHERE email = '{$_SESSION['email']}' " .
			 "AND friendemail = '$email'";
    
	$result = mysqli_query($db, $query);
    include('lib/show_queries.php');
    
     if (mysqli_affected_rows($db) < 1) {
        array_push($error_msg,  "DELETE ERROR: cancel request..." . __FILE__ ." : ". __LINE__ );
	}
}

?>

<?php include("lib/header.php"); ?>

		<title>GTOnline Friend Requests</title>
	</head>
	
	<body>
		<div id="main_container">
    <?php include("lib/menu.php"); ?>
			
			<div class="center_content">	
				<div class="center_left">
					<div class="title_name"><?php print $user_name; ?></div>          
					<div class="features">   
						<div class="profile_section">						
							<div class="subtitle">Friend Requests Received</div>
							
							<?php
                                $query = "SELECT firstname, lastname, hometown, relationship, friendship.email " .
                                         "FROM friendship " .
                                         "INNER JOIN regularuser ON regularuser.email = friendship.email " .
                                         "INNER JOIN user ON user.email = regularuser.email " .
                                         "WHERE friendship.friendemail = '{$_SESSION['email']}' " .
                                         "AND dateconnected IS NULL " .
                                         "ORDER BY lastname, firstname";
                                
                                $result = mysqli_query($db, $query);
								include('lib/show_queries.php');

                                if (!empty($result) && (mysqli_num_rows($result) == 0) ) {
                                      //false positive if no friends
                                      //array_push($error_msg,  "Query ERROR: Failed to get freind request to you" . __FILE__ ." : ". __LINE__ );
                                }
                                
                                $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
                                $count = mysqli_num_rows($result);
                                if ($row) {
                                                        
                                    print '<table>';
                                    print '<tr>';
                                    print '<td class="heading">Name</td>';
                                    print '<td class="heading">Hometown</td>';
                                    print '<td class="heading">Relationship</td>';
                                    print '<td class="heading">Accept?</td>';
                                    print '<td class="heading">Reject?</td>';
                                    print '</tr>';
                                
                                    while ($row){
                                                            
                                        print '<tr>';
                                        print '<td>' . $row['firstname'] . ' ' . $row['lastname'] . '</td>';
                                        print '<td>' . $row['hometown'] . '</td>';
                                        print '<td>' . $row['relationship'] . '</td>';
                                        print '<td><a href="view_requests.php?accept_request=' . urlencode($row['email']) . '">Accept</a></td>';
                                        print '<td><a href="view_requests.php?reject_request=' . urlencode($row['email']) . '">Reject</a></td>';
                                        print '</tr>';

                                        $row = mysqli_fetch_array($result, MYSQLI_ASSOC);   
                                    
                                    }
                                    print '</table>';
                                }
                                else {
                                    print "<br/>None!";
                                }
							?>
				
						</div>
						<div class="profile_section">
							<div class="subtitle">Friend Requests Sent</div>
							
							<?php			
                                $query = "SELECT firstname, lastname, hometown, relationship, user.email " .
                                         "FROM friendship " .
                                         "INNER JOIN regularuser ON regularuser.email = friendship.friendemail " .
                                         "INNER JOIN user ON user.email = regularuser.email " .
                                         "WHERE friendship.email = '{$_SESSION['email']}' " .
                                         "AND dateconnected IS NULL " .
                                         "ORDER BY lastname, firstname";
                                
                                $result = mysqli_query($db, $query);
								include('lib/show_queries.php');

                                if (!empty($result) && (mysqli_num_rows($result) == 0) ) {
                                    //false positive if no friends
                                    //array_push($error_msg,  "Query ERROR: Failed to get friend requests you sent" . __FILE__ ." : ". __LINE__ );
                                }
                                
                                $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
                                $count = mysqli_num_rows($result);
                                
                                if ($row) {
                                                        
                                    print '<table>';
                                    print '<tr>';
                                    print '<td class="heading">Name</td>';
                                    print '<td class="heading">Hometown</td>';
                                    print '<td class="heading">Relationship</td>';
                                    print '<td class="heading">Cancel?</td>';
                                    print '</tr>';
                                
                                    while ($row){
                                                            
                                        print '<tr>';
                                        print '<td>' . $row['firstname'] . ' ' . $row['lastname'] . '</td>';
                                        print '<td>' . $row['hometown'] . '</td>';
                                        print '<td>' . $row['relationship'] . '</td>';
                                        print '<td><a href="view_requests.php?cancel_request=' . urlencode($row['email']) . '">Cancel</a></td>';
                                        print '</tr>';
                                        
                                        $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
                                    
                                    }
                                    print '</table>';
                                }
                                else {
                                    print "<br/>None!";
                                }
							?>												
						</div>	
                    
                    <div class="profile_section">
							<div class="subtitle">Friend Requests Accepted</div>
							
							<?php			
                                $query = "SELECT firstname, lastname, hometown, relationship, user.email " .
                                         "FROM friendship " .
                                         "INNER JOIN regularuser ON regularuser.email = friendship.friendemail " .
                                         "INNER JOIN user ON user.email = regularuser.email " .
                                         "WHERE friendship.email = '{$_SESSION['email']}' " .
                                         "AND dateconnected IS NOT NULL " .
                                         "ORDER BY lastname, firstname";
                                
                                $result = mysqli_query($db, $query);
								include('lib/show_queries.php');
	 
                                if (!empty($result) && (mysqli_num_rows($result) == 0) ) {
                                    //false positive if no friends
                                    //array_push($error_msg,  "Query ERROR: Failed to get friend requests you accepted" . __FILE__ ." : ". __LINE__ );
                                }
                                
                                $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
                                $count = mysqli_num_rows($result);
                                
                                if ($row) {
                                                        
                                    print '<table>';
                                    print '<tr>';
                                    print '<td class="heading">Name</td>';
                                    print '<td class="heading">Hometown</td>';
                                    print '<td class="heading">Relationship</td>';
                                    print '<td class="heading">Cancel?</td>';
                                    print '</tr>';
                                
                                    while ($row){
                                                            
                                        print '<tr>';
                                        print '<td>' . $row['firstname'] . ' ' . $row['lastname'] . '</td>';
                                        print '<td>' . $row['hometown'] . '</td>';
                                        print '<td>' . $row['relationship'] . '</td>';
                                        print '<td><a href="view_requests.php?cancel_request=' . urlencode($row['email']) . '">Cancel</a></td>';
                                        print '</tr>';
                                        
                                        $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
                                    
                                    }
                                    print '</table>';
                                }
                                else {
                                    print "<br/>None!";
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