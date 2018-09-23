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
  
        $sex = mysqli_real_escape_string($db, $_POST['sex']);
        $birthdate = mysqli_real_escape_string($db, $_POST['birthdate']);  
        $currentcity = mysqli_real_escape_string($db, $_POST['currentcity']);
        $hometown = mysqli_real_escape_string($db, $_POST['hometown']);
        
        if (empty($sex)) {
                array_push($error_msg,  "Please enter a sex.");
        }
        
        if (!is_date($birthdate)) {
            array_push($error_msg,  "Error: Invalid birthdate ");
        }
        
         if (empty($currentcity)) {
            array_push($error_msg,  "Please enter a currentcity.");
        }
        
        if (empty($hometown)) {
                array_push($error_msg,  "Please enter an hometown.");
        }

         if ( !empty($birthdate) && !empty($currentcity) && !empty($hometown) )   { 
            $query = "UPDATE regularuser " .
                     "SET sex='$sex ', " .
                     "birthdate='$birthdate', " .
                     "hometown='$hometown', " .
                     "currentcity='$currentcity' " .
                     "WHERE email='{$_SESSION['email']}'";

            $result = mysqli_query($db, $query);
            include('lib/show_queries.php');
         }
         
         
        $interest = mysqli_real_escape_string($db, $_POST['add_interest']);
        if (empty($interest)) {
            array_push($error_msg,  "Error: You must enter an interest ");
        }
        
        // if (!empty($_POST['add_interest']) and $_POST['add_interest'] != '(add interest)' and trim($_POST['add_interest']) != '') {
        if (!empty($_POST['add_interest']) and $_POST['add_interest'] != '(add interest)' and trim($_POST['add_interest']) != '' ) {
             
            $query = "INSERT INTO userinterests (email, interest) " .
                         "VALUES('{$_SESSION['email']}', '$interest')";
                
            $queryID = mysqli_query($db, $query);

            //if (is_numeric($queryID) && (mysqli_num_rows($queryID) > 0) ) {
            if (mysqli_affected_rows($db) > 0) {
                    include('lib/show_queries.php');
                } else{
                        array_push($error_msg, "INSERT ERROR:  interest " . __FILE__ ." : ". __LINE__ );
                }
            }

        $query = "SELECT firstname, lastname, sex, birthdate, currentcity, hometown " .
		 "FROM user " .
		 "INNER JOIN regularuser ON user.email = regularuser.email " .
		 "WHERE user.email = '{$_SESSION['email']}'";

    $result = mysqli_query($db, $query);
    
    if (!empty($result) && (mysqli_num_rows($result) > 0) ) {
        $row = mysqli_fetch_array($result, MYSQLI_ASSOC);
    } else {
        array_push($error_msg,  "SELECT ERROR: user profile..." . __FILE__ ." : ". __LINE__ );
    }
    
}  //end of if($_POST)

if (!empty($_GET['delete_interest'])) {
	
	$interest = mysqli_real_escape_string($db, $_GET['delete_interest']);
	$query = "DELETE FROM userinterests " .
			 "WHERE email = '{$_SESSION['email']}' " .
			 "AND interest = '$interest'";
	
    $result = mysqli_query($db, $query);
    include('lib/show_queries.php');
 
     if (mysqli_affected_rows($db) < 1) {
        array_push($error_msg,  "DELETE ERROR: interest..." . __FILE__ ." : ". __LINE__ );
    }
    
}

function is_date( $str ) { 
	$stamp = strtotime( $str ); 
	if (!is_numeric($stamp)) { 
		return false; 
	} 
	$month = date( 'm', $stamp ); 
	$day   = date( 'd', $stamp ); 
	$year  = date( 'Y', $stamp ); 
  
	if (checkdate($month, $day, $year)) { 
		return true; 
	} 
	return false; 
} 

?>

<?php include("lib/header.php"); ?>
		<title>GTOnline Edit Profile</title>
	</head>
	
	<body>
    	<div id="main_container">
        <?php include("lib/menu.php"); ?>
    
			<div class="center_content">	
				<div class="center_left">
					<div class="title_name"><?php print $row['firstname'] . ' ' . $row['lastname']; ?></div>          
					<div class="features">   
						
                        <div class="profile_section">
							<div class="subtitle">Edit Profile (Note: intentionally missing functionality)</div>   
                            
							<form name="profileform" action="edit_profile.php" method="post">
								<table>
									<tr>
										<td class="item_label">Sex</td>
										<td>
											<select name="sex">
												<option value="M" <?php if ($row['sex'] == 'M') { print 'selected="true"';} ?>>Male</option>
												<option value="F" <?php if ($row['sex'] == 'F') { print 'selected="true"';} ?>>Female</option>
											</select>
										</td>
									</tr>
									<tr>
										<td class="item_label">Birthdate</td>
										<td>
											<input type="text" name="birthdate" value="<?php if ($row['birthdate']) { print $row['birthdate']; } ?>" />										
										</td>
									</tr>
									<tr>
										<td class="item_label">Current City</td>
										<td>
											<input type="text" name="currentcity" value="<?php if ($row['currentcity']) { print $row['currentcity']; } ?>" />	
										</td>
									</tr>

									<tr>
										<td class="item_label">Hometown</td>
										<td>
											<input type="text" name="hometown" value="<?php if ($row['hometown']) { print $row['hometown']; } ?>" />	
										</td>
									</tr>
									
									<tr>
										<td class="item_label">Interests</td>
										<td>
											<ul>
											<?php
												$query = "SELECT interest FROM userinterests WHERE email='{$_SESSION['email']}'";
												$result = mysqli_query($db, $query);
												 include('lib/show_queries.php');
												 
												 while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
													print "<li>{$row['interest']} <a href='edit_profile.php?delete_interest=" . 
														urlencode($row['interest']) . "'>delete</a></li>";
												}
											?>
											<li><input type="text" name="add_interest" value="(add interest)" 
													onclick="if(this.value=='(add interest)'){this.value=''}"
													onblur="if(this.value==''){this.value='(add interest)'}"/></li>
											</ul>
										</td>
									</tr>
								</table>
								
								<a href="javascript:profileform.submit();" class="fancy_button">Save</a> 
							
							</form>
						</div>
                        
                        <div class="profile_section">
							<div class="subtitle">Education</div>  
							<table>
								<tr>
									<td class="heading">School</td>
									<td class="heading">Year Graduated</td>
								</tr>							
						
								<?php
									    $query = "SELECT schoolname, yeargraduated " . 
											 "FROM attend " .
											 "WHERE email = '" . $_SESSION['email'] . "' " .
											 "ORDER BY yeargraduated DESC";
									    $result = mysqli_query($db, $query);
                                        include('lib/show_queries.php');
                                        
									while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
										print "<tr>";
										print "<td>" . $row['schoolname'] . "</td>";
										print "<td>" . $row['yeargraduated'] . "</td>";
										print "</tr>";
									}
								?>
							</table>						
						</div>	
                    
						<div class="profile_section">
							<div class="subtitle">Professional</div>  
							<table width="80%">
								<tr>
									<td class="heading">Employer</td>
									<td class="heading">Job Title</td>
								</tr>							
						
								<?php
									    $query = "SELECT employername, jobtitle " . 
											 "FROM employment " .
											 "WHERE email = '" . $_SESSION['email'] . "' " .
											 "ORDER BY employername DESC";
									    $result = mysqli_query($db, $query);
                                        include('lib/show_queries.php');
									while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
										print "<tr>";
										print "<td>" . $row['employername'] . "</td>";
										print "<td>" . $row['jobtitle'] . "</td>";
										print "</tr>";
									}
								?>
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