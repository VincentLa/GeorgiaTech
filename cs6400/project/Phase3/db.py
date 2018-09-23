import web, hashlib, datetime, re

dbh = web.database(dbn='mysql', db='cs6400_sp17_team010', user='developer', pw='stardust4')
#dbh = web.database(dbn='mysql', db='cs6400_sp17_team010', user='root', pw='', host='127.0.0.1') # This is for vincent because for some reason he can't get a new user/password to work

salt = '15974630salt'

def isUserExists(username, password):
    sql = """
        SELECT UserName, Password
        FROM User
        WHERE UserName = $username
    """

    vars = {
        'username':username
    }

    results = dbh.query(sql, vars = vars)

    for record in results:
        if record['UserName'] == username and hashlib.sha1(salt + record['Password']).hexdigest() == password:
            return True
    else:
        return False

def getCurrentSite(username):
    sql = """
        SELECT s.SiteID, s.Name
        FROM User u INNER JOIN Site s ON u.SiteID=s.SiteID
        WHERE u.UserName = $UserName
    """
    vars = {
        'UserName':username
    }

    results = dbh.query(sql, vars = vars)

    if len(results) > 0:
        res = results[0]
        return res['SiteID'], res['Name']
    else:
        return None, None


def getServices(username, site):
    sql = """
        SELECT DISTINCT sk.ServiceID AS skID,
                        sk.Name AS skName,
                        sk.Address AS skAddress,
                        sk.HoursOfOperation AS skHours,
                        sk.ConditionsForUse AS skConditions,
                        sh.ServiceID AS shID,
                        sh.Name AS shName,
                        sh.Address AS shAddress,
                        sh.HoursOfOperation AS shHours,
                        sh.ConditionsForUse AS shConditions,
                        fp.ServiceID AS fpID,
                        fp.Name AS fpName,
                        fp.Address AS fpAddress,
                        fp.HoursOfOperation AS fpHours,
                        fp.ConditionsForUse AS fpConditions,
                        fb.ServiceID AS fbID
        FROM User u
        LEFT JOIN Shelter sh on u.SiteID = sh.SiteID
        LEFT JOIN SoupKitchen sk on u.SiteID = sk.SiteID
        LEFT JOIN FoodPantry fp on u.SiteID = fp.SiteID
        LEFT JOIN FoodBank fb on u.SiteID = fb.SiteID
        WHERE u.UserName = $UserName AND u.SiteID = $Site
    """

    vars = {
        'UserName':username,
        'Site':site
    }

    results = dbh.query(sql, vars = vars)

    if len(results) > 0:
        return results[0]
    else:
        return None


def modifySoupKitchen(Site,Name,Address,Hours,Conditions):
    sql = """
        UPDATE SoupKitchen
        SET Name = $Name, Address = $Address, HoursOfOperation = $Hours, ConditionsForUse = $Conditions
        WHERE SiteID = $Site
        """

    vars = {
        'Name': Name,
        'Address': Address,
        'Hours': Hours,
        'Conditions': Conditions,
        'Site': Site
    }

    dbh.query(sql, vars = vars)


def modifyFoodPantry(Site, Name, Address, Hours, Conditions):
    sql = """
        UPDATE FoodPantry
        SET Name = $Name, Address = $Address, HoursOfOperation = $Hours, ConditionsForUse = $Conditions
        WHERE SiteID = $Site
        """

    vars = {
        'Name': Name,
        'Address': Address,
        'Hours': Hours,
        'Conditions': Conditions,
        'Site': Site
    }

    dbh.query(sql, vars=vars)

def modifyShelter(Site, Name, Address, Hours, Conditions):
    sql = """
        UPDATE Shelter
        SET Name = $Name, Address = $Address, HoursOfOperation = $Hours, ConditionsForUse = $Conditions
        WHERE SiteID = $Site
        """

    vars = {
        'Name': Name,
        'Address': Address,
        'Hours': Hours,
        'Conditions': Conditions,
        'Site': Site
    }

    dbh.query(sql, vars=vars)

def deleteSoupKitchen(Site):
    sql = """DELETE FROM SoupKitchen WHERE SiteID = $Site"""
    vars = {'Site': Site}
    dbh.query(sql, vars=vars)


def deleteFoodBank(Site):
    sql = """DELETE FROM FoodBank WHERE SiteID = $Site"""
    vars = {'Site': Site}
    dbh.query(sql, vars=vars)


def deleteFoodPantry(Site):
    sql = """DELETE FROM FoodPantry WHERE SiteID = $Site"""
    vars = {'Site': Site}
    dbh.query(sql, vars=vars)


def deleteShelter(Site):
    sql = """DELETE FROM Shelter WHERE SiteID = $Site"""
    vars = {'Site': Site}
    dbh.query(sql, vars=vars)


def addSoupKitchen(Site, Name, Address, Hours, Conditions, SeatCapacity, SeatsAvailable):
    sql = """SELECT * FROM SoupKitchen WHERE SiteID = $Site"""
    vars = {'Site': Site}
    results = dbh.query(sql, vars = vars)
    if len(results)>0:
        return "Cannot add more than one same service to the same site!"
    else:
        try:
            SeatCapacity = int(SeatCapacity)
        except ValueError:
            SeatCapacity = 0
        try:
            SeatsAvailable = int(SeatsAvailable)
        except ValueError:
            SeatsAvailable = 0
        sql2 = """INSERT INTO SoupKitchen (Name, Address, HoursOfOperation, ConditionsForUse, SeatCapacity, SeatsAvailable, SiteID)
                  VALUES ($Name,$Address,$Hours, $Conditions, $SeatCapacity, $SeatsAvailable,$Site)"""
        vars2 = {
            'Site': Site,
            'Name': Name,
            'Address': Address,
            'Hours': Hours,
            'Conditions': Conditions,
            'SeatCapacity': SeatCapacity,
            'SeatsAvailable': SeatsAvailable
        }
        dbh.query(sql2,vars = vars2)

def addFoodPantry(Site, Name, Address, Hours, Conditions):
    sql = """SELECT * FROM FoodPantry WHERE SiteID = $Site"""
    vars = {'Site': Site}
    results = dbh.query(sql, vars = vars)
    if len(results)>0:
        return "Cannot add more than one same service to the same site!"
    else:
        sql2 = """INSERT INTO FoodPantry (Name, Address, HoursOfOperation, ConditionsForUse, SiteID)
                  VALUES ($Name,$Address,$Hours, $Conditions,$Site)"""
        vars2 = {
            'Site': Site,
            'Name': Name,
            'Address': Address,
            'Hours': Hours,
            'Conditions': Conditions
        }
        dbh.query(sql2,vars = vars2)


def addShelter(Site, Name, Address, Hours, Conditions, Number):
    sql = """SELECT * FROM Shelter WHERE SiteID = $Site"""
    vars = {'Site': Site}
    results = dbh.query(sql, vars = vars)
    if len(results)>0:
        return "Cannot add more than one same service to the same site!"
    else:
        try:
            Number = int(Number)
        except ValueError:
            Number = 0
        sql2 = """INSERT INTO Shelter (Name, Address, HoursOfOperation, ConditionsForUse, RoomsAvailable, SiteID)
                  VALUES ($Name,$Address,$Hours, $Conditions, $Number,$Site)"""
        vars2 = {
            'Site': Site,
            'Name': Name,
            'Address': Address,
            'Hours': Hours,
            'Conditions': Conditions,
            'Number': Number
        }
        try:
            dbh.query(sql2,vars = vars2)
        except Exception:
            return "Invalid input."

def addFoodBank(Site):
    sql = """SELECT * FROM FoodBank WHERE SiteID = $Site"""
    vars = {'Site': Site}
    results = dbh.query(sql, vars = vars)
    if len(results)>0:
        return "Cannot add more than one same service to the same site!"
    else:
        sql2 = """INSERT INTO FoodBank (SiteID) VALUES ($Site)"""
        vars2 = {
            'Site': Site,
        }
        dbh.query(sql2,vars = vars2)

def addbunkroom(Site, RoomNumber, BunksAvailable, BunkCapacity, bunktype):
    sql = """SELECT ServiceID FROM Shelter WHERE SiteID = $Site"""
    vars = {'Site': Site}
    results = dbh.query(sql, vars=vars)
    sql2 = """INSERT INTO BunkRoom (RoomNumber,ServiceID,BunksAvailable, BunkCapacity, BunkType)
             VALUES ($RoomNumber, $ServiceID,$BunksAvailable, $BunkCapacity, $bunktype)"""
    vars2 = {'RoomNumber': RoomNumber,
             'ServiceID': results[0]['ServiceID'],
             'BunksAvailable': BunksAvailable,
             'BunkCapacity': BunkCapacity,
             'bunktype': bunktype}
    dbh.query(sql2, vars=vars2)

def addfamilyroom(Site, RoomNumber):
    sql = """SELECT ServiceID FROM Shelter WHERE SiteID = $Site"""
    vars = {'Site': Site}
    results = dbh.query(sql, vars=vars)
    sql2 = """INSERT INTO FamilyRoom (RoomNumber,ServiceID)
             VALUES ($RoomNumber, $ServiceID)"""
    vars2 = {'RoomNumber': RoomNumber,
             'ServiceID': results[0]['ServiceID']}
    dbh.query(sql2, vars=vars2)


def getSoupKitchenAvailability(Site):
    sql = """
        SELECT ServiceID
        FROM SoupKitchen sk INNER JOIN Site s on sk.SiteID = s.SiteID
        WHERE s.SiteID = $SiteID
    """

    vars = {'SiteID': Site}

    results = dbh.query(sql, vars = vars)

    if len(results) > 0:
        return results[0]['ServiceID']
    else:
        return None

def getShelterAvailability(site):
    sql = """
        SELECT ServiceID
        FROM Shelter sh INNER JOIN Site s ON sh.SiteID=s.SiteID
        WHERE s.SiteID=$SiteID
    """

    vars = {'SiteID': site}

    results = dbh.query(sql, vars = vars)

    if len(results) > 0:
        return results[0]['ServiceID']
    else:
        return None

## Client related DB Queries
def _checkExistingClient(id_number, description):
    """Given client id number and description, checks if client is an existing one

    Returns True if existing client, else False.
    """
    sql = """
        SELECT *
        FROM Client
        WHERE IDNumber = $id_number
            AND IDDescription = $description;
    """

    vars = {
        'id_number': id_number,
        'description': description,
    }
    results = dbh.query(sql, vars = vars)
    if len(results) > 0:
        return True
    else:
        return False


def __convert_rows_to_list(rows):
    rec = []
    for record in rows:
        rec.append(record)
    return rec


def addClient(first_name, last_name, id_number, phone_number, description):
    sql = """
        INSERT INTO Client (IDDescription, IDNumber, FirstName, LastName, PhoneNumber)
        VALUES ($description, $id_number, $first_name, $last_name, $phone_number);
    """

    vars = {
        'first_name': first_name,
        'last_name': last_name,
        'id_number': id_number,
        'phone_number': phone_number,
        'description': description,
    }

    if _checkExistingClient(id_number, description):
        print("Error: Already Existing Client")
        return None
    else:
        dbh.query(sql, vars = vars)
        print("Added Client")


def searchClient(first_name, last_name, id_number):
    client_display_sql = """
        SELECT FirstName, LastName, IDNumber, IDDescription, ClientID
        FROM Client
        WHERE INSTR(IDNumber,  CASE WHEN $id_number = '' THEN NULL ELSE $id_number END) > 0
            OR INSTR(FirstName, CASE WHEN $first_name = '' THEN NULL ELSE $first_name END) > 0
            OR INSTR(LastName, CASE WHEN $last_name = '' THEN NULL ELSE $last_name END) > 0
    """

    vars = {
        'first_name': first_name,
        'last_name': last_name,
        'id_number': id_number,
    }

    results_client_search = dbh.query(client_display_sql, vars = vars)
    if len(results_client_search) < 5:
        return __convert_rows_to_list(results_client_search)
    else:
        print("More than 4 Clients match search criteria. Please enter more unique information")
        return None


def viewEditClient(clientid):
    client_info_sql = """
        SELECT FirstName, LastName, IDNumber, IDDescription, ClientID, PhoneNumber
        FROM Client
        WHERE ClientId = $clientid
    """

    log_services_sql = """
        SELECT ClientID, LogDateTime, SiteName, ServiceDescription, Notes
        FROM Log
        WHERE ClientID = $clientid
        ORDER BY LogDateTime desc;
    """

    waitlist_sql = """
        SELECT Shelter.Name, Waitlist.WaitListPosition
        FROM WaitList
        INNER JOIN Shelter
            ON Waitlist.ServiceID = Shelter.ServiceID
        WHERE Waitlist.ClientID = $clientid;
    """

    vars = {
        'clientid': clientid,
    }

    results_client_info = dbh.query(client_info_sql, vars = vars)
    results_log_services = dbh.query(log_services_sql, vars = vars)
    results_waitlist = dbh.query(waitlist_sql, vars = vars)

    return __convert_rows_to_list(results_client_info), __convert_rows_to_list(results_log_services), __convert_rows_to_list(results_waitlist)


def editClient(first_name, last_name, id_number, phone_number, id_description, client_id):
    sql = """
        UPDATE CLIENT SET
            FirstName = $first_name,
            LastName = $last_name,
            IDNumber = $id_number,
            PhoneNumber = $phone_number,
            IDDescription = $id_description
        WHERE ClientID = $client_id
        ;
    """

    vars = {
        'first_name': first_name,
        'last_name': last_name,
        'id_number': id_number,
        'id_description': id_description,
        'phone_number': phone_number,
        'client_id': client_id
    }

    dbh.query(sql, vars = vars)
    return None

def addServicesLog(client_id, log_date_time, site_name, service_description, notes):
    sql = """
        INSERT INTO LOG
        SELECT
          $client_id as ClientID,
          STR_TO_DATE($log_date_time,'%Y-%m-%d_%H:%i:%s') as LogDateTime,
          $site_name as SiteName,
          $service_description as ServiceDescription,
          $notes as Notes
        ;
    """
    vars = {
        'client_id': client_id,
        'log_date_time': log_date_time,
        'site_name': site_name,
        'service_description': service_description,
        'notes': notes,
    }

    dbh.query(sql, vars = vars)
    return None

def getSeats(site):
    serviceID = getSoupKitchenAvailability(site)
    if serviceID is None:
        return None

    vars = {'ServiceID': serviceID}
    sql = """
          SELECT seatsAvailable,seatCapacity FROM SoupKitchen WHERE ServiceID=$ServiceID;
    """
    results = dbh.query(sql, vars = vars)
    record = results[0]
    return {'serviceID': serviceID,
            'seatsAvailable': record['seatsAvailable'],
            'seatCapacity': record['seatCapacity']}

def modifySeats(serviceID, seatsnum):
    sql = """
        UPDATE SoupKitchen
        SET SeatsAvailable=$seatsnum
        WHERE ServiceID = $ServiceID AND SeatCapacity >= $seatsnum;
    """
    vars = {
      'ServiceID': serviceID,
      'seatsnum': seatsnum
     }
    try:
        dbh.query(sql, vars = vars)
    except Exception:
        return "Invalid input."

def getBunks(site):
    serviceID = getShelterAvailability(site)
    if serviceID is None:
        return None
    vars = {'ServiceID': serviceID}
    sql = """
          SELECT BunkType, BunksAvailable, BunkCapacity, RoomNumber FROM BunkRoom
          WHERE ServiceID=$ServiceID;
    """
    results = dbh.query(sql, vars = vars)
    BunkRooms = []
    for record in results:
        BunkRooms.append(record)
    return {'serviceID': serviceID,
            'BunkRooms': BunkRooms}

def modifyBunks(serviceID, BunksAvailable):
    for key, value in BunksAvailable.iteritems():
        sql = """
                 UPDATE BunkRoom SET BunksAvailable = $Value
                 WHERE ServiceID=$ServiceID
                       AND RoomNumber = $Key
                       AND $Value >= 0
                       AND BunkCapacity >= $Value;"""
        vars = {
            'ServiceID': serviceID,
            'Value': value,
            'Key': key
        }
        dbh.query(sql, vars = vars)

def getRooms(site):
    # Check for Shelter at current Site
    serviceID = getShelterAvailability(site)
    if serviceID is None:
        return None

    # if found, query for rooms available
    vars = {'ServiceID': serviceID}
    sql = """
          SELECT RoomsAvailable
          FROM Shelter s
          WHERE ServiceID = $ServiceID
    """
    results = dbh.query(sql, vars=vars)
    roomsAvailable = results[0]['RoomsAvailable']

    # and family room information
    sql = """
          SELECT f.RoomNumber, f.OccupationStatus
          FROM FamilyRoom f
          WHERE ServiceID = $ServiceID
    """
    results = dbh.query(sql, vars=vars)

    familyRooms = []
    for record in results:
        familyRooms.append(record)

    return {'serviceID': serviceID,
            'roomsAvailable': roomsAvailable,
            'familyRooms': familyRooms}

def modifyRooms(serviceID, rnumOccupied):
    # update occupation status
    if len(rnumOccupied) > 0:
        sql = """
            UPDATE FamilyRoom
            SET OccupationStatus = (RoomNumber IN $RnumOccupied)
            WHERE ServiceID = $ServiceID
        """
    else:
        sql = """
            UPDATE FamilyRoom
            SET OccupationStatus = FALSE
            WHERE ServiceID = $ServiceID
        """
    vars = {
        'ServiceID': serviceID,
        'RnumOccupied': rnumOccupied
    }
    dbh.query(sql, vars = vars)

    # update rooms available.  This could maybe be a transaction.
    sql = """
        UPDATE Shelter
        SET RoomsAvailable =
            (SELECT COUNT(*)
             FROM FamilyRoom F
             WHERE NOT F.OccupationStatus AND F.ServiceID = $ServiceID)
        WHERE ServiceID = $ServiceID
    """
    vars = {
        'ServiceID': serviceID,
        'RnumOccupied': rnumOccupied
    }
    dbh.query(sql, vars = vars)

def getWaitlist(site):
    # Check for Shelter at current Site
    serviceID = getShelterAvailability(site)
    if serviceID is None:
        return None

    # Check for FamilyRooms at current Site
    sql = """
        SELECT *
        FROM FamilyRoom
        WHERE ServiceID=$ServiceID
    """
    vars = {'ServiceID': serviceID}
    results = dbh.query(sql, vars=vars)
    if len(results)==0:
        return None

    # Query for waitlist information
    sql = """
        SELECT C.ClientID, C.FirstName, C.LastName, W.WaitListPosition, W.ServiceID
        FROM  WaitList AS W, Client AS C, Shelter AS S
        WHERE W.ServiceID=S.ServiceID AND S.SiteID=$Site AND W.ClientID=C.ClientID
        ORDER BY WaitListPosition
    """
    vars = {'Site': site}
    results = dbh.query(sql, vars=vars)

    waitlist = []
    for record in results:
        waitlist.append(record)

    return {'serviceID': serviceID,
            'waitlist': waitlist}

def _waitlistPosition(serviceID, clientID):
    # Variables for query
    vars = {'ServiceID': serviceID, 'ClientID': clientID}

    # Get length of waitlist
    sql = """
        SELECT COUNT(*) AS Length
        FROM WaitList
        WHERE ServiceID=$ServiceID
    """
    result = dbh.query(sql, vars=vars)
    if len(result)>0:
        length = result[0]['Length']
    else:
        length = 0

    # Get current position of client
    sql = """
        SELECT WaitListPosition
        FROM WaitList
        WHERE ClientID=$ClientID AND ServiceID=$ServiceID
    """
    result = dbh.query(sql, vars = vars)
    if len(result)>0:
        pos = result[0]['WaitListPosition']
    else:
        pos = length + 1

    return pos, length

def deleteFromWaitlist(serviceID, clientID):
    # Get current position
    position, length = _waitlistPosition(serviceID, clientID)

    # Variables for query
    vars = {'ServiceID': serviceID,
            'ClientID': clientID,
            'Position': position}

    # Delete selected client
    sql = """
        DELETE FROM WaitList
        WHERE ClientID=$ClientID AND ServiceID=$ServiceID
    """
    dbh.query(sql, vars=vars)

    # Move everyone else up
    sql = """
        UPDATE WaitList
        SET WaitListPosition = WaitListPosition - 1
        WHERE ClientID<>$ClientID AND ServiceID=$ServiceID
              AND WaitListPosition > $Position
    """
    dbh.query(sql, vars=vars)


def moveUpWaitlist(serviceID, clientID):
    # Get current position
    position, length = _waitlistPosition(serviceID, clientID)

    # Do nothing if already at top
    if position==1:
        return

    # Variables for query
    vars = {'ServiceID': serviceID,
            'ClientID': clientID,
            'Position': position}

    # Move client above down
    sql = """
        UPDATE WaitList
        SET WaitListPosition = WaitListPosition + 1
        WHERE ClientID<>$ClientID AND ServiceID=$ServiceID
              AND WaitListPosition = $Position - 1
    """
    dbh.query(sql, vars=vars)

    # Move selected client up
    sql = """
        UPDATE WaitList
        SET WaitListPosition = WaitListPosition - 1
        WHERE ClientID=$ClientID AND ServiceID=$ServiceID
    """
    dbh.query(sql, vars=vars)

def moveDownWaitlist(serviceID, clientID):
    # Get current position
    position, length = _waitlistPosition(serviceID, clientID)

    # Do nothing if already at bottom
    if position==length:
        return

    # Variables for query
    vars = {'ServiceID': serviceID,
            'ClientID': clientID,
            'Position': position}

    # Move client below up
    sql = """
        UPDATE WaitList
        SET WaitListPosition = WaitListPosition - 1
        WHERE ClientID<>$ClientID AND ServiceID=$ServiceID
              AND WaitListPosition = $Position + 1
    """
    dbh.query(sql, vars=vars)

    # Move selected client down
    sql = """
        UPDATE WaitList
        SET WaitListPosition = WaitListPosition + 1
        WHERE ClientID=$ClientID AND ServiceID=$ServiceID
    """
    dbh.query(sql, vars=vars)


def addToWaitlist(username, clientID):
    # Get current shelter from username
    siteID = getCurrentSite(username)[0]
    if siteID is None:
        return
    services = getServices(username, siteID)
    if 'shID' not in services or services['shID'] is None:
        return
    serviceID = services['shID']


    # Check for family rooms
    vars = {'ServiceID': serviceID}
    sql = """
        SELECT *
        FROM FamilyRoom
        WHERE ServiceID=$ServiceID
    """
    results = dbh.query(sql, vars=vars)
    if len(results)==0:
        return

    # Get current position
    position, length = _waitlistPosition(serviceID, clientID)
    if position <= length:
        return

    # Add selected client to bottom of list
    vars = {'ServiceID': serviceID,
            'ClientID': clientID,
            'Position': position}
    sql = """
        INSERT INTO WaitList (ServiceID, ClientID, WaitListPosition)
        VALUES ($ServiceID, $ClientID, $Position)
    """
    dbh.query(sql, vars=vars)

def getBedsReport():
    # Compile beds/rooms info
    sql = """
        SELECT H.Name, S.Name AS SiteName,
               CONCAT(S.StreetAddress, " ", H.Address, " ", S.City, ", ", S.State, " ", S.ZipCode) AS Address,
               S.PrimaryPhone, H.HoursOfOperation,
               H.ConditionsForUse, H.RoomsAvailable,
               SUM(CASE WHEN B.BunkType='Male' THEN B.BunksAvailable ELSE 0 END) AS MaleBunks,
               SUM(CASE WHEN B.BunkType='Female' THEN B.BunksAvailable ELSE 0 END) AS FemaleBunks,
               SUM(CASE WHEN B.BunkType='Mix' THEN B.BunksAvailable ELSE 0 END) AS MixedBunks
        FROM Shelter as H, Site as S, BunkRoom as B
        WHERE (H.SiteID = S.SiteID) AND (H.ServiceID = B.ServiceID) AND (H.RoomsAvailable > 0 OR B.BunksAvailable > 0)
        GROUP BY H.ServiceID
        ORDER BY H.Name ASC;
    """

    result = dbh.query(sql)
    rec = []
    for record in result:
        rec.append(record)
    return rec

def getMealsReport():
    # Compile meals info
    sql = """
        SELECT Meal.Counts, Meal.Category
        FROM ((SELECT SUM(NumberOfUnit) AS Counts, ItemSubType AS Category
              FROM (SELECT NumberOfUnit, 'Meat/Seafood or Dairy/Eggs' AS ItemSubType
                    FROM Item
                    WHERE ItemType='Food' AND (ItemSubType='Meat/Seafood' OR
                                              ItemSubType='Dairy/Eggs')) AS P
              GROUP BY ItemSubType)
             UNION
             (SELECT SUM(NumberOfUnit) AS Counts, ItemSubType AS Category
              FROM Item
              WHERE ItemType='Food' AND ItemSubType='Vegetables'
              GROUP BY ItemSubType)
             UNION
             (SELECT SUM(NumberOfUnit) AS Counts, ItemSubType AS Category
              FROM Item
              WHERE ItemType='Food' AND ItemSubType='Nuts/Grains/Beans'
              GROUP BY ItemSubType)) AS Meal
        ORDER BY Meal.Counts ASC
        LIMIT 1;
    """

    result = dbh.query(sql)
    if len(result) > 0:
        return result[0]
    else:
        return None

def getReorderReport():
    # Compile reorder info
    sql = """
        SELECT I.Name, I.ItemType, I.ItemSubType
        FROM
             (SELECT Name, ItemType, ItemSubType, 0 AS NumberOfUnit
              FROM Item
              WHERE ExpirationDate <= CURDATE()
              UNION
              SELECT Name, ItemType, ItemSubType, NumberOfUnit
              FROM Item
              WHERE ExpirationDate > CURDATE()) AS I
        GROUP BY Name, ItemType, ItemSubType
        HAVING SUM(NumberOfUnit) = 0
        ORDER BY I.ItemType, I.ItemSubType, I.Name;
    """
    result = dbh.query(sql)
    rec = []
    for record in result:
        rec.append(record)
    return rec

def getFoodBank():
    sql = """
        SELECT Site.Name, Site.SiteID
        FROM Site
        INNER JOIN FoodBank
        ON Site.SiteID = FoodBank.SiteID
    """

    results = dbh.query(sql)

    if len(results) > 0:
        return list(results)
    else:
        return None

def getAllItemNames():
    sql = """
        SELECT Name
        FROM Item
        GROUP BY Name
    """

    results = dbh.query(sql)

    if len(results) > 0:
        return list(results)
    else:
        return None

def getItemByForm(inputData):
    sql = """
        SELECT s.Name SiteName
             , i.ItemType
             , i.ItemSubType
             , i.ItemID
             , i.Name ItemName
             , i.NumberOfUnit AvailableCount
             , i.UnitType
             , i.ExpirationDate
             , i.StorageType
             , f.SiteID SiteID
        FROM Item i
        INNER JOIN FoodBank f
         ON i.ServiceID = f.ServiceID
        INNER JOIN Site s
         ON s.SiteID = f.SiteID
        WHERE s.Name LIKE $siteName
        AND i.ItemType LIKE $itemType
        AND i.StorageType LIKE $storageType
        AND i.ItemSubType LIKE $itemSubType
        AND i.Name LIKE $itemName
    """

    if 'OrderByCol' in inputData:
        sql = sql + ' ORDER BY %s ' % inputData['OrderByCol']

    vars = {
        'siteName':'%' + (inputData['tbFoodBank'] if inputData['tbFoodBank'] != 'All' else '') + '%',
        'itemType':'%' + (inputData['tbItemType'] if inputData['tbItemType'] != 'All' else '') + '%',
        'storageType':'%' + (inputData['tbStorageType'] if inputData['tbStorageType'] != 'All' else '') + '%',
        'itemSubType':'%' + (inputData['tbItemSubType'] if inputData['tbItemSubType'] != 'All' else '') + '%',
        'itemName':'%' + (inputData['tbItemName'] if inputData['tbItemName'] != 'All' else '') + '%'
    }

    if inputData['tbExpirationDate']:
        sql = sql + ' AND i.ExpirationDate <= $expirationDate'
        try:
            mth, day, yr = inputData['tbExpirationDate'].split('/')
            mth, day, yr = int(mth), int(day), int(yr)
            dt = datetime.date(yr, mth, day).strftime("%Y-%m-%d")
        except ValueError:
            dt = inputData['tbExpirationDate']
        vars['expirationDate'] = dt

    results = dbh.query(sql, vars=vars)

    if len(results) > 0:
        return list(results)
    else:
        return None

def getSiteServices(userName):
    siteServices = {}
    services = ['FoodBank', 'Shelter', 'FoodPantry', 'SoupKitchen']

    for service in services:
        sql = """
            SELECT *
            FROM User u
            INNER JOIN %s s
             ON u.SiteID = s.SiteID
            WHERE u.UserName = $username
        """ % service

        results = dbh.query(sql, vars={'username':userName})

        if len(results) > 0:
            siteServices[service] = True
        else:
            siteServices[service] = False

    return siteServices

def getHighRequests(username):
    sql = """
        SELECT i.ItemID
        FROM User u
        INNER JOIN Site s
         ON u.SiteID = s.SiteID
        INNER JOIN Requests r
         ON u.UserName = r.UserName
        INNER JOIN Item i
         ON r.ItemID = i.ItemID
        WHERE u.UserName = $UserName
        AND r.Status = $Status
        GROUP BY i.ItemID, i.NumberOfUnit
        HAVING SUM(r.CountRequested) > i.NumberOfUnit
    """

    results = list(dbh.query(sql, vars={'UserName':username, 'Status':'Pending'}))

    if len(results) > 0:
        highRequests = [v['ItemID'] for v in results]
        return highRequests
    else:
        return None

def getHighOutstandingRequests(username):
    sql = """
        SELECT i.ItemID
        FROM User u
        INNER JOIN Site s
         ON u.SiteID = s.SiteID
        INNER JOIN FoodBank f
         ON u.SiteID = f.SiteID
        INNER JOIN Item i
         ON f.ServiceID = i.ServiceID
        INNER JOIN Requests r
         ON r.ItemID = i.ItemID
        INNER JOIN User ureq
         ON ureq.UserName = r.UserName
        INNER JOIN Site sreq
         ON ureq.SiteID = sreq.SiteID
        WHERE u.UserName = $UserName
        AND r.Status = $Status
        GROUP BY i.ItemID, i.NumberOfUnit
        HAVING SUM(r.CountRequested) > i.NumberOfUnit
    """

    results = list(dbh.query(sql, vars={'UserName':username, 'Status':'Pending'}))

    if len(results) > 0:
        highRequests = [v['ItemID'] for v in results]
        return highRequests
    else:
        return None

def getRequests(userName):
    sql = """
        SELECT s.Name SiteName
             , i.Name ItemName
             , r.RequestDateTime
             , i.ItemID
             , i.ItemType
             , i.ItemSubType
             , i.StorageType
             , i.ExpirationDate
             , i.NumberOfUnit AvailableCount
             , r.CountRequested
             , r.CountProvided
             , r.Status
        FROM User u
        INNER JOIN Site s
         ON u.SiteID = s.SiteID
        INNER JOIN Requests r
         ON u.UserName = r.UserName
        INNER JOIN Item i
         ON r.ItemID = i.ItemID
        WHERE u.UserName = $username
    """
    # AND r.Status = $Status

    results = list(dbh.query(sql, vars={'username':userName})) # , 'Status':'Pending'}

    if len(results) > 0:
        return list(results)
    else:
        return None

def getRequestToFulfill(userName, sortBy):
    sql = """
        SELECT u.UserName
             , s.Name 'Site Name'
             , ureq.UserName Requestor
             , sreq.Name 'Requestor Site'
             , r.RequestDateTime 'Request DateTime'
             , i.ItemID
             , i.Name 'Item Name'
             , i.ItemType 'Item Type'
             , i.ItemSubType 'Sub Type'
             , i.StorageType 'Storage Type'
             , i.ExpirationDate 'Expiration Date'
             , i.NumberOfUnit 'Available Count'
             , r.CountRequested 'Count Requested'
             , r.CountProvided 'Count Provided'
             , r.Status
        FROM User u
        INNER JOIN Site s
         ON u.SiteID = s.SiteID
        INNER JOIN FoodBank f
         ON u.SiteID = f.SiteID
        INNER JOIN Item i
         ON f.ServiceID = i.ServiceID
        INNER JOIN Requests r
         ON r.ItemID = i.ItemID
        INNER JOIN User ureq
         ON ureq.UserName = r.UserName
        INNER JOIN Site sreq
         ON ureq.SiteID = sreq.SiteID
        WHERE u.UserName = $username
        AND r.Status = $status
    """

    if sortBy:
        if sortBy in ['i.NumberOfUnit', 'r.CountRequested', 'r.CountProvided']:
            sql = sql + ' ORDER BY %s' % sortBy # number type columns
        else:
            sql = sql + ' ORDER BY CAST(%s AS CHAR)' % sortBy

    results = dbh.query(sql, vars={'username':userName , 'status':'Pending'})

    if len(results) > 0:
        return list(results)
    else:
        return None

def addRequest(userName, inputData): #itemID, countRequested):
    itemsUpdated = {'deleted':{}, 'updated':{}, 'old':{}, 'new':{}}
    addItems = {int(k):int(v) for k,v in zip(inputData['ItemID'], inputData['CountRequested']) if v != '' and v != '0' and int(v) > 0}
    updateItems = {
        int(k):{'AvailableCount':int(v),'OldCount':int(o)}
        for k,v,o
        in zip(inputData['ItemID'], inputData['AvailableCount'], inputData['OldCount'])
        if v != '' and int(v) >= 0 and v != o
        #if v != '' and v != '0' and int(v) > 0 and v != o
    }

    """ Add new requests """
    for itemID, countRequested in addItems.items():
        sql = """
            INSERT INTO Requests (UserName, ItemID, CountRequested)
            VALUES($userName, $itemID, $countRequested)
        """

        vars = {'userName':userName, 'itemID':itemID, 'countRequested':countRequested}
        dbh.query(sql, vars=vars)
        itemName = getItemNameByID(itemID) + ' (ID: %s)' % str(itemID)
        itemsUpdated['new'][itemName] = countRequested

    """ Update inventory counts """
    for itemID, cnt in updateItems.items():
        itemName = getItemNameByID(itemID) + ' (ID: %s)' % str(itemID)

        sql = """
            UPDATE Item
            SET NumberOfUnit = $NumberOfUnit
            WHERE ItemID = $ItemID
        """

        dbh.query(sql, vars={'NumberOfUnit':cnt['AvailableCount'], 'ItemID':itemID})
        itemsUpdated['old'][itemName] = cnt['OldCount']
        itemsUpdated['updated'][itemName] = cnt['AvailableCount']

    return itemsUpdated

def fulFillRequest(inputData):
    dataObject = [
        {'UserName':u,'RequestDateTime':r,'ItemID':int(i),'CountToProvide':int(c),'Status':s}
        for u,r,i,c,s
        in zip(inputData['Requestor'], inputData['RequestDateTime'], inputData['ItemID'], inputData['CountToProvide'], inputData['Status'])
        if (c != '' and c != '0') or s != 'Pending'
    ]

    """ Check it see if total requested count for each item is higher than availability """
    isRequestCountGood = True
    itemRequests = {}
    itemAvails = {}
    itemHigh = {}
    msg = ''

    for record in dataObject:
        itemRequests[record['ItemID']] = (itemRequests[record['ItemID']] if record['ItemID'] in itemRequests else 0) + record['CountToProvide']

    for itemID in itemRequests.keys():
        sql = """
            SELECT ItemID, Name, SUM(NumberOfUnit) Qty
            FROM Item
            WHERE ItemID = $ItemID
            GROUP BY ItemID, Name
        """

        results = list(dbh.query(sql, vars={'ItemID':itemID}))
        itemAvails[itemID] = {'name':results[0]['Name'], 'qty':results[0]['Qty']}

    for itemID, count in itemRequests.items():
        if count > itemAvails[itemID]['qty']:
            itemHigh[itemAvails[itemID]['name'] + ' (ID: ' + str(itemID) + ')'] = {'request':str(count), 'available':str(itemAvails[itemID]['qty'])}

    if len(itemHigh) > 0:
        isRequestCountGood = False

        for i, v in itemHigh.items():
            msg = msg + ' ' + i + ': requested = ' + v['request'] + ', available = ' + v['available'] + '.'

    if isRequestCountGood:
        """ Updating Requests """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        vars = {}

        for record in dataObject:
            for k, v in record.items():
                vars[k] = int(v) if k in ['ItemID'] else v

            sql = """
                UPDATE Requests
                SET Status = $Status
                  , CountProvided = IFNULL(CountProvided, 0) + $CountToProvide
                WHERE UserName = $UserName
                AND RequestDateTime = $RequestDateTime
                AND ItemID = $ItemID
            """

            dbh.query(sql, vars=vars)

            sql = """
                UPDATE Item
                SET NumberOfUnit = NumberOfUnit - $CountToProvide
                WHERE ItemID = $ItemID
            """

            dbh.query(sql, vars={'CountToProvide':record['CountToProvide'], 'ItemID':record['ItemID']})

        """ Status Filled """
        sql = """
            UPDATE Requests
            SET Status = $Status
            WHERE CountProvided = CountRequested
        """

        dbh.query(sql, vars={'Status':'Filled'})

        """ Status Partially Filled """
        sql = """
            UPDATE Requests
            SET Status = $Status
            WHERE CountProvided < CountRequested
            AND CountProvided > $CountProvided
        """

        dbh.query(sql, vars={'Status':'Partially Filled', 'CountProvided':0})

    return msg

def updateRequest(username, inputData):
    msg = ''
    itemsUpdated = {'deleted':{}, 'updated':{}, 'old':{}, 'new':{}}
    deletes = [{'UserName':username, 'RequestDateTime':d.split('|')[0], 'ItemID':int(d.split('|')[1])} for d in inputData['delRequest']]
    updates = [
        {(username, r,int(i)):int(c)}
        for r,i,c,o
        in zip(inputData['RequestDateTime'], inputData['ItemID'], inputData['CountRequested'], inputData['OldCountRequested'])
        if c != o
    ]

    for u in updates:
        for k, v in u.items():
            sql = """
                UPDATE Requests
                SET CountRequested = $CountRequested
                WHERE UserName = $UserName
                AND RequestDateTime = $RequestDateTime
                AND ItemID = $ItemID
                AND CountRequested != $CountRequested
            """

            vars = {
                'CountRequested':v,
                'UserName':k[0],
                'RequestDateTime':k[1],
                'ItemID':k[2]
            }

            itemID = k[2]
            itemName = getItemNameByID(itemID) + ' (ID: %s)' % str(itemID)

            """ Current / Old """
            itemsUpdated['old'][itemName] = getCountRequestByPK(k[0], k[1], k[2])

            """ Updated """
            itemsUpdated['updated'][itemName] = v

            dbh.query(sql, vars=vars)

    for d in deletes:
        sql = """
            DELETE
            FROM Requests
            WHERE UserName = $UserName
            AND RequestDateTime = $RequestDateTime
            AND ItemID = $ItemID
        """

        vars = {
            'UserName':d['UserName'],
            'RequestDateTime':d['RequestDateTime'],
            'ItemID':d['ItemID']
        }

        itemID = d['ItemID']
        itemName = getItemNameByID(itemID) + ' (ID: %s)' % str(itemID)
        itemsUpdated['deleted'][itemName] = {'RequestDateTime':d['RequestDateTime'], 'CountRequested':getCountRequestByPK(d['UserName'], d['RequestDateTime'], itemID)}

        dbh.query(sql, vars=vars)

    return itemsUpdated

def addInventory(username, inputData):
    items = {'new':{}, 'old':{}, 'msg':[]}
    missingFields = [k for k,v in inputData.items() if v == '' or '--' in v]

    if len(missingFields) > 0:
        items['msg'].append('Please enter a value for the following fields: ' + ', '.join(missingFields))
    else:
        currYr = int(datetime.date.today().strftime('%Y'))
        datePattern = re.compile('\d{1,2}[-/]\d{1,2}[-/]\d{1,4}')

        if datePattern.findall(inputData['ExpirationDate']):
            isSetRun = False
            formatExpirationDate = '9999-01-01'

            if inputData['ExpirationDate']:
                mth, day, yr = re.findall('[\d]+', inputData['ExpirationDate']) #inputData['ExpirationDate'].split('/')
                mth, day, yr = int(mth), int(day), int(yr)

                if mth in xrange(1,13) and day in xrange(1,32) and yr >= currYr:
                    try:
                        formatExpirationDate = datetime.date(yr, mth, day).strftime("%Y-%m-%d")
                        isSetRun = True
                    except ValueError:
                        items['msg'].append('Date value is out of bound. Please use a realistic date.')
                else:
                    yr, mth, day = re.findall('[\d]+', inputData['ExpirationDate']) #inputData['ExpirationDate'].split('/')
                    mth, day, yr = int(mth), int(day), int(yr)

                    if mth in xrange(1,13) and day in xrange(1,32) and yr >= currYr:
                        try:
                            formatExpirationDate = datetime.date(yr, mth, day).strftime("%Y-%m-%d")
                            isSetRun = True
                        except ValueError:
                            items['msg'].append('Date value is out of bound. Please use a realistic date.')
                    else:
                        items['msg'].append('Date value is out of bound. Please use a realistic date.')

            if (inputData['ItemType']=='Food' and inputData['ItemSubType'] not in
                ['Vegetables', 'Nuts/Grains/Beans', 'Meat/Seafood', 'Dairy/Eggs',
                 'Sauce/Condiment/Seasoning', 'Juice/Drink']):
                items['msg'].append('Sub Type does not match Type.  Please select a Food sub type.')
                isSetRun = False
            if (inputData['ItemType']=='Supplies' and inputData['ItemSubType'] not in
                ['Personal Hygiene', 'Clothing', 'Shelter', 'Other']):
                items['msg'].append('Sub Type does not match Type.  Please select a Supplies sub type.')
                isSetRun = False

            if isSetRun:
                """ Get FoodBank ServiceID """
                sql = """
                    SELECT f.ServiceID
                    FROM User u
                    INNER JOIN FoodBank f
                     ON u.SiteID = f.SiteID
                    WHERE u.UserName = $UserName
                """

                serviceID = list(dbh.query(sql, vars={'UserName':username}))[0]['ServiceID']

                """ Check if item already exists """
                sql = """
                    SELECT ItemID, ServiceID, Name, NumberOfUnit
                    FROM Item
                    WHERE Name LIKE $Name
                    AND ServiceID = $ServiceID
                """

                vars = {
                    'Name':'%' + inputData['Name'] + '%',
                    'ServiceID':serviceID
                }

                if formatExpirationDate != '9999-01-01':
                    sql = sql + ' AND ExpirationDate = $ExpirationDate'
                    vars['ExpirationDate'] = formatExpirationDate

                results = list(dbh.query(sql, vars=vars))

                if len(results) > 0:
                    """ Update current inventory """

                    items['old'] = {'ItemID':results[0]['ItemID'],'ServiceID':serviceID,'Name':results[0]['Name'],'NumberOfUnit':results[0]['NumberOfUnit']}

                    sql = """
                        UPDATE Item
                        SET NumberOfUnit = NumberOfUnit + $NumberOfUnit
                        WHERE Name LIKE $Name
                        AND ServiceID = $ServiceID
                    """

                    vars = {
                        'Name':'%' + inputData['Name'] + '%',
                        'ServiceID':serviceID,
                        'NumberOfUnit':int(inputData['NumberOfUnit'])
                    }

                    dbh.query(sql, vars=vars)
                    items['msg'].append('Current item %s (ID: %i) count has been updated from %i to %i for service ID %i' % (results[0]['Name'], results[0]['ItemID'], results[0]['NumberOfUnit'], results[0]['NumberOfUnit'] + int(inputData['NumberOfUnit']), serviceID))

                else:
                    """ Insert new inventory """

                    sql = 'SELECT MAX(ItemID) MaxItemID FROM Item'
                    maxItemID = list(dbh.query(sql))[0]['MaxItemID']
                    newItemID = maxItemID + 1
                    items['new'] = {'ItemID':newItemID,'ServiceID':serviceID,'Name':inputData['Name'],'NumberOfUnit':int(inputData['NumberOfUnit'])}

                    sql = """
                        INSERT INTO Item (ItemType, ItemSubType, Name, NumberOfUnit, UnitType, ExpirationDate, StorageType, ServiceID)
                        VALUES ($ItemType, $ItemSubType, $Name, $NumberOfUnit, $UnitType, $ExpirationDate, $StorageType, $ServiceID)
                    """

                    vars = {
                        'ItemType':inputData['ItemType'],
                        'ItemSubType':inputData['ItemSubType'],
                        'Name':inputData['Name'],
                        'NumberOfUnit':int(inputData['NumberOfUnit']),
                        'UnitType':inputData['UnitType'],
                        'ExpirationDate':formatExpirationDate,
                        'StorageType':inputData['StorageType'],
                        'ServiceID':serviceID
                    }

                    dbh.query(sql, vars=vars)
                    items['msg'].append('New item %s (ID: %i) has been inserted with count %i for service ID %i' % (inputData['Name'], newItemID, int(inputData['NumberOfUnit']), serviceID))
        else:
            items['msg'].append('Date format entered is incorrect. Please use format of 01-01-9999 or 01/01/9999.')

    return items

def getCountRequestByPK(UserName, RequestDateTime, ItemID):
    sql = """
        SELECT r.CountRequested
        FROM Requests r
        WHERE r.UserName = $UserName
        AND r.RequestDateTime = $RequestDateTime
        AND r.ItemID = $ItemID
    """

    vars = {
        'UserName':UserName,
        'RequestDateTime':RequestDateTime,
        'ItemID':ItemID
    }

    results = list(dbh.query(sql, vars=vars))

    return results[0]['CountRequested']

def getItemNameByID(itemID):
    sql = """
        SELECT i.Name
        FROM Item i
        WHERE i.ItemID = $itemID
    """

    results = list(dbh.query(sql, vars={'itemID':itemID}))

    return results[0]['Name']

def getSiteIDByUser(username):
    sql = """
        SELECT SiteID
        FROM User
        WHERE UserName = $UserName
    """

    results = list(dbh.query(sql, vars={'UserName':username}))

    return results[0]['SiteID']
