<?php

include('lib/common.php');
// written by GTusername2

if (!isset($_SESSION['email'])) {
	header('Location: login.php');
	exit();
}

    $friendemail = mysqli_real_escape_string($db, $_REQUEST['friendemail']);

    $query = "SELECT firstname, lastname, hometown " . 
		 "FROM user " .
		 "INNER JOIN regularuser on regularuser.email = user.email " .
		 "WHERE regularuser.email = '$friendemail'";

    $result = mysqli_query($db, $query);
    include('lib/show_queries.php');

if (!empty($result) && (mysqli_num_rows($result) > 0) ) {
    $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
    $count = mysqli_num_rows($result);
    
    $friend_name = $row['firstname'] . " " . $row['lastname'];
    $hometown = $row['hometown'] ;
} else {
    array_push($error_msg,  "SELECT ERROR: friend email: " . $friendemail . __FILE__ ." : ". __LINE__ );
}


if ($_SERVER['REQUEST_METHOD'] == 'POST') {
	
	$relationship = mysqli_real_escape_string($db, $_REQUEST['relationship']);
	$friendemail = mysqli_real_escape_string($db, $_REQUEST['friendemail']);

	if (empty($relationship)) {
        array_push($error_msg,  "Error: You must provide a relationship ");
	}
	
	if ( !empty($friendemail) && !empty($relationship) )   { 
		$friend_name = mysqli_real_escape_string($db, $_POST['friend_name']);
		$hometown = mysqli_real_escape_string($db, $_POST['hometown']);

		$query = "INSERT INTO friendship (email, friendemail, relationship, dateconnected) " .
				 "VALUES ('{$_SESSION['email']}', '$friendemail', '$relationship', NULL)";

        $queryID = mysqli_query($db, $query);
            
		if (mysqli_affected_rows($db) > 0) {
			if($showQueries){
					array_push($query_msg,  $query);
					array_push($query_msg, "sending request ... ");
				}
		} else{
					array_push($error_msg, "INSERT ERROR: friend email: " . $friendemail.  " relation: " . $relationship . __FILE__ ." : ". __LINE__ );
		}
            header(REFRESH_TIME . 'url=view_requests.php');		
	}

}
?>

<?php include("lib/header.php"); ?>
		<title>GTOnline Friend Request</title>
	</head>

	<body>
		<div id="main_container">
        <?php include("lib/menu.php"); ?>
    
			<div class="center_content">
				<div class="center_left">
					<div class="title_name">Request Friend</div>          
					<div class="features">   
						
						<div class="profile_section">
							<div class="subtitle">Request Friend</div>   
							<form name="requestform" action="request_friend.php" method="POST">
							<table>								
								<tr>
									<td class="item_label">Name</td>
									<td><?php print $friend_name; ?></td>
								</tr>
								<tr>
									<td class="item_label">Hometown</td>
									<td><?php print $hometown; ?></td>
								</tr>
								<tr>
									<td class="item_label">Relationship</td>
									<td><input type="text" name="relationship" /></td>
								</tr>
							</table>
							
							<input type="hidden" name="friend_name" value="<?php print $friend_name; ?>" />
							<input type="hidden" name="hometown" value="<?php print $hometown; ?>" />
							<input type="hidden" name="friendemail" value="<?php print $friendemail; ?>" />
							
							<a href="javascript:requestform.submit();" class="fancy_button">Send</a> 
							</form>														
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