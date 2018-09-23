<?php

include('lib/common.php');
// written by GTusername3

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
    $user_name = $row['firstname'] . " " . $row['lastname'];
} else {
        array_push($error_msg,  "SELECT ERROR: user profile " . __FILE__ ." : ". __LINE__ );
}

	$query = "SELECT regularuser.email, firstname, lastname, hometown " .
			 "FROM user " .
			 "INNER JOIN regularuser ON regularuser.email = user.email " .
			 "WHERE regularuser.email NOT IN " .
			 "	(SELECT friendemail FROM friendship WHERE email = '{$_SESSION['email']}') " . 
			 "AND regularuser.email <> '{$_SESSION['email']}' ORDER BY lastname, firstname";
			 
	$result = mysqli_query($db, $query);

    if (!empty($result) && (mysqli_num_rows($result) == 0) ) {
        array_push($error_msg,  "SELECT ERROR: Failed to find friends " . __FILE__ ." : ". __LINE__ );
	}
	

/* if form was submitted, then execute query to search for friends */
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    
	$name = mysqli_real_escape_string($db, $_POST['name']);
	$email = mysqli_real_escape_string($db, $_POST['email']);
	$hometown = mysqli_real_escape_string($db, $_POST['hometown']);
		
	$query = "SELECT regularuser.email, firstname, lastname, hometown " .
			 "FROM user " .
			 "INNER JOIN regularuser ON regularuser.email = user.email " .
			 "WHERE regularuser.email NOT IN " .
			 "	(SELECT friendemail FROM friendship WHERE email = '{$_SESSION['email']}') " . 
			 "AND regularuser.email <> '{$_SESSION['email']}'";
			 
	if (!empty($name) or !empty($email) or !empty($hometown)) {
		$query = $query . " AND (1=0 ";
		
		if (!empty($name)) {
			$query = $query . " OR firstname LIKE '%$name%' OR lastname LIKE '%$name%' ";
		}
		if (!empty($email)) {
			$query = $query . " OR regularuser.email LIKE '%$email%' ";
		}
		if (!empty($hometown)) {
			$query = $query . " OR hometown LIKE '%$hometown%' ";
		}
		$query = $query . ") ";
	}
	
	$query = $query . " ORDER BY lastname, firstname";

	$result = mysqli_query($db, $query);
    include('lib/show_queries.php');

    if (!empty($result) && (mysqli_num_rows($result) == 0) ) {
        array_push($error_msg,  "SELECT ERROR: Failed to find friends " . __FILE__ ." : ". __LINE__ );
	}
		
}
?>

<?php include("lib/header.php"); ?>
		<title>GTOnline Friend Search</title>
	</head>
	
	<body>
    	<div id="main_container">
            <?php include("lib/menu.php"); ?>
			
			<div class="center_content">
				<div class="center_left">
					<div class="title_name"><?php print $user_name; ?></div>          			
					<div class="features">   
						
						<div class="profile_section">						
							<div class="subtitle">Search for Friends</div> 
							
							<form name="searchform" action="search_friends.php" method="POST">
								<table>								
									<tr>
										<td class="item_label">Name</td>
										<td><input type="text" name="name" /></td>
									</tr>
									<tr>
										<td class="item_label">Email</td>
										<td><input type="text" name="email" /></td>
									</tr>
									<tr>
										<td class="item_label">Hometown</td>
										<td><input type="text" name="hometown" /></td>
									</tr>
									
								</table>
									<a href="javascript:searchform.submit();" class="fancy_button">Search</a> 					
							</form>							
						</div>
						
						<div class='profile_section'>
						<div class='subtitle'>Search Results</div>
						<table>
							<tr>
								<td class='heading'>Name</td>
								<td class='heading'>Hometown</td>
							</tr>
								<?php
									if (isset($result)) {
										while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)){
											$friendemail = urlencode($row['email']);
											print "<tr>";
											print "<td><a href='request_friend.php?friendemail=$friendemail'>{$row['firstname']} {$row['lastname']}</a></td>";
											print "<td>{$row['hometown']}</td>";									
											print "</tr>";
										}
									}	?>
							</table>
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