"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
   Team Name: Team 010
Member Names: Melanie Clarke, Ye Wang, Vincent La, Khanh Nguyen
Created Date: 03/10/2017
     Purpose: A web app for ASACS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import web, db, hashlib, datetime
# from web import form

web.config.debug = False

urls = (
    '/', 'Index',
    '/db/', 'DB',
    '/login/', 'Login',
    '/logout/', 'Logout',
    '/home/', 'Home',
    '/services/', 'Services',
    '/services/modifyseats/', 'ModifySeats',
    '/services/servicelog/', 'ServiceLog',
    '/services/modifybunks/', 'ModifyBunks',
    '/services/modifyrooms/', 'ModifyRooms',
    '/services/waitlist/', 'ViewEditWaitlist',
    '/services/addbunkroom/', 'addbunkroom',
    '/services/addfamilyroom/', 'addfamilyroom',
    '/services/checkintoroom/', 'CheckIntoRoom',
    '/services/checkavailablerooms/', 'CheckAvailableRooms',
    '/client/', 'Client',
    '/client/add/', 'ClientAdd',
    '/client/checkin/', 'ClientCheckIn',
    '/client/search/', 'ClientSearch',
    '/client/viewedit/', 'ClientViewEdit',
    '/client/edit/', 'ClientEdit',
    '/client/addwaitlist/', 'ClientAddWaitlist',
    '/inventory/', 'Inventory',
    '/inventory/requests/', 'Requests',
    '/inventory/requests/(.*)', 'RequestsBySort',
    '/inventory/searchItem/', 'SearchItem',
    '/inventory/addInventory/', 'AddInventory',
    '/inventory/addRequest/', 'AddRequest',
    '/inventory/viewRequest/', 'ViewRequest',
    '/inventory/fulfillRequest/', 'FulFillRequest',
    '/inventory/clearDataInput/', 'ClearDataInput',
    '/reports/', 'PublicReports',
    '/reports/beds/', 'BedsReport',
    '/reports/meals/', 'MealsReport',
    '/reports/reorder/', 'ReorderReport',
    '/services/addsoupkitchen/', 'addsoupkitchen',
    '/services/addshelter/', 'addshelter',
    '/services/addfoodbank/', 'addfoodbank',
    '/services/addfoodpantry/', 'addfoodpantry',
    '/services/delete/', 'DeleteServices'
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('session'))
globals = {'session':session}
render = web.template.render('templates/', globals=globals, base='base')
renderNoBase = web.template.render('templates/', globals=globals)

class Index:
    def GET(self):
        if session.get('username'):
            raise web.seeother('/home/')
        else:
            return render.index()

class Home:
    def GET(self):
        if session.get('username'):
            return render.home()
        else:
            raise web.seeother('/')

class Logout:
    def GET(self):
        if session:
            session.kill()

        raise web.seeother('/')

class Login:
    def GET(self):
        raise web.seeother('/')

    def POST(self):
        inputData = web.input()

        if db.isUserExists(inputData.username, hashlib.sha1(db.salt + inputData.password).hexdigest()):
            session.loginMessage = None
            session.username = inputData.username
            raise web.seeother('/home/')
        else:
            session.loginMessage = 'User / Password combination not found!'
            raise web.seeother('/')

class Services:
    def GET(self):
        if session.get('username'):
            session.siteID, session.siteName = db.getCurrentSite(session.username)
            session.currentServices = db.getServices(session.username, session.siteID)
            session.serviceToDelete = None
            return render.services()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()
        session.siteID, session.siteName = db.getCurrentSite(session.username)
        if 'fpDelete' in inputData:
            svcs = db.getServices(session.username, session.siteID)
            session.serviceToDelete = {'name': 'Food Pantry '+svcs['fpName'],
                                       'type': 'fpDelete'}
            raise web.seeother('/services/delete/')
        if 'skDelete' in inputData:
            svcs = db.getServices(session.username, session.siteID)
            session.serviceToDelete = {'name': 'Soup Kitchen '+svcs['skName'],
                                       'type': 'skDelete'}
            raise web.seeother('/services/delete/')
        if 'shDelete' in inputData:
            svcs = db.getServices(session.username, session.siteID)
            session.serviceToDelete = {'name': 'Shelter '+svcs['shName'],
                                       'type': 'shDelete'}
            raise web.seeother('/services/delete/')
        if 'fbDelete' in inputData:
            svcs = db.getServices(session.username, session.siteID)
            session.serviceToDelete = {'name': 'Food Bank', 'type': 'fbDelete'}
            raise web.seeother('/services/delete/')
        if 'fpupdate' in inputData:
            db.modifyFoodPantry(session.siteID, inputData['fpName'], inputData['fpAddress'], inputData['fpHours'], inputData['fpConditions'])
            session.siteID, session.siteName = db.getCurrentSite(session.username)
            session.currentServices = db.getServices(session.username, session.siteID)
            return render.services()
        if 'skupdate' in inputData:
            db.modifySoupKitchen(session.siteID, inputData['skName'], inputData['skAddress'], inputData['skHours'], inputData['skConditions'])
            session.siteID, session.siteName = db.getCurrentSite(session.username)
            session.currentServices = db.getServices(session.username, session.siteID)
            return render.services()
        if 'shupdate' in inputData:
            db.modifyShelter(session.siteID, inputData['shName'], inputData['shAddress'], inputData['shHours'], inputData['shConditions'])
            session.siteID, session.siteName = db.getCurrentSite(session.username)
            session.currentServices = db.getServices(session.username, session.siteID)
            return render.services()
        if 'reset' in inputData:
            return render.services()
class DeleteServices:
    def GET(self):
        if session.get('username'):
            return render.delete_service()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()
        session.siteID, session.siteName = db.getCurrentSite(session.username)
        if 'fpDelete' in inputData:
            db.deleteFoodPantry(session.siteID)
            raise web.seeother('/services/')
        if 'skDelete' in inputData:
            db.deleteSoupKitchen(session.siteID)
            raise web.seeother('/services/')
        if 'shDelete' in inputData:
            db.deleteShelter(session.siteID)
            raise web.seeother('/services/')
        if 'fbDelete' in inputData:
            db.deleteFoodBank(session.siteID)
            raise web.seeother('/services/')

class addsoupkitchen:
    def GET(self):
        if session.get('username'):
            return render.addsoupkitchen()
        else:
            raise web.seeother('/')
    def POST(self):
        inputData = web.input()
        session.siteID, session.siteName = db.getCurrentSite(session.username)
        db.addSoupKitchen(session.siteID, inputData.Name, inputData.Address, inputData.Hours, inputData.Conditions, inputData.SeatCapacity, inputData.SeatsAvailable)
        raise web.seeother('/services/')


class addshelter:
    def GET(self):
        if session.get('username'):
            return render.addshelter()
        else:
            raise web.seeother('/')
    def POST(self):
        inputData = web.input()
        session.siteID, session.siteName = db.getCurrentSite(session.username)
        msg = db.addShelter(session.siteID, inputData.Name, inputData.Address, inputData.Hours, inputData.Conditions, inputData.Number)
        session.addShelterMsg = msg
        if msg is None:
            raise web.seeother('/services/')
        else:
            return render.addshelter()

class addfoodbank:
    def GET(self):
        if session.get('username'):
            return render.addfoodbank()
        else:
            raise web.seeother('/')
    def POST(self):
        inputData = web.input()
        session.siteID, session.siteName = db.getCurrentSite(session.username)
        db.addFoodBank(session.siteID)
        raise web.seeother('/services/')

class addfoodpantry:
    def GET(self):
        if session.get('username'):
            return render.addfoodpantry()
        else:
            raise web.seeother('/')
    def POST(self):
        inputData = web.input()
        session.siteID, session.siteName = db.getCurrentSite(session.username)
        db.addFoodPantry(session.siteID, inputData.Name, inputData.Address, inputData.Hours, inputData.Conditions)
        raise web.seeother('/services/')

class addbunkroom:
    def GET(self):
        if session.get('username'):
            return render.addbunkroom()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()
        session.siteID, session.siteName = db.getCurrentSite(session.username)
        db.addbunkroom(session.siteID, inputData.RoomNumber, inputData.BunksAvailable, inputData.BunkCapacity,
                       inputData.bunktype)
        raise web.seeother('/services/')

class addfamilyroom:
    def GET(self):
        if session.get('username'):
            return render.addfamilyroom()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()
        session.siteID, session.siteName = db.getCurrentSite(session.username)
        db.addfamilyroom(session.siteID, inputData.RoomNumber)
        raise web.seeother('/services/')


class Client:
    def GET(self):
        if session.get('username'):
            return render.client()
        else:
            raise web.seeother('/')

class Inventory:
    def GET(self):
        if session.get('username'):
            return render.inventory(db.getSiteServices(session.get('username')))
        else:
            raise web.seeother('/')

class ClientAdd:
    def GET(self):
        if session.get('username'):
            return render.client_add()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()
        db.addClient(
            inputData.first_name, inputData.last_name, inputData.id_number, inputData.phone_number, inputData.description)
        return render.client_add()

class ClientCheckIn:
    def GET(self):
        if session.get('username'):
            session.siteID, session.siteName = db.getCurrentSite(session.username)
            session.currentServices = db.getServices(session.username, session.siteID)
            return render.client_check_in()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()
        print inputData
        session.siteID, session.siteName = db.getCurrentSite(session.username)
        session.currentServices = db.getServices(session.username, session.siteID)
        return render.client_check_in()

class CheckIntoRoom:
    def GET(self):
        if session.get('username'):
            session.current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            return render.check_into_room()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()
        db.addServicesLog(session.clientid, inputData.date_timestamp, inputData.site, inputData.description, inputData.notes)
        session.returnToClient = True
        raise web.seeother('/client/viewedit/')

class ServiceLog:
    def GET(self):
        if session.get('username'):
            session.current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            return render.servicelog()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()
        db.addServicesLog(session.clientid, inputData.date_timestamp, inputData.site, inputData.description, inputData.notes)
        raise web.seeother('/client/viewedit/')

class ClientSearch:
    def GET(self):
        if session.get('username'):
            return render.client_search()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()
        results = db.searchClient(inputData.first_name, inputData.last_name, inputData.id_number)

        if results is None:
            return render.client_search_failed()
        else:
            session.clients = results
            return render.client_search_success()

class ClientViewEdit:
    def GET(self):
        if session.get('username'):
            # update existing client
            if session.get('clientid'):
                clientid = int(session.get('clientid'))
                results_client_info, results_log_services, results_waitlist = db.viewEditClient(clientid)
                session.clientid = clientid
                session.client = results_client_info
                session.log_services = results_log_services
                session.client_waitlist = results_waitlist
            return render.client_view_edit()
        else:
            raise web.seeother('/')

    def POST(self):
        print("I GET HERE")
        inputData = web.input()
        print(inputData)
        clientid = int(inputData.ClientID)
        results_client_info, results_log_services, results_waitlist = db.viewEditClient(clientid)
        session.clientid = clientid
        session.client = results_client_info
        session.log_services = results_log_services
        session.client_waitlist = results_waitlist
        return render.client_view_edit()

class ClientEdit:
    def GET(self):
        if session.get('username'):
            session.current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            return render.client_edit()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()
        prev_client_information, x, y = db.viewEditClient(session.clientid)
        prev_first_name = prev_client_information[0]['FirstName']
        prev_last_name = prev_client_information[0]['LastName']
        prev_id = prev_client_information[0]['IDNumber']
        prev_phone = prev_client_information[0]['PhoneNumber']
        prev_description = prev_client_information[0]['IDDescription']
        db.editClient(
            inputData.first_name, inputData.last_name, inputData.id_number,
            inputData.phone_number, inputData.description, session.clientid)

        results_client_info, results_log_services, results_waitlist = db.viewEditClient(session.clientid)
        results_first_name = results_client_info[0]['FirstName']
        results_last_name = results_client_info[0]['LastName']
        results_id = results_client_info[0]['IDNumber']
        results_phone = results_client_info[0]['PhoneNumber']
        results_description = results_client_info[0]['IDDescription']
        session.client = results_client_info
        session.log_services = results_log_services
        session.client_waitlist = results_waitlist

        if (prev_first_name != results_first_name or prev_last_name != results_last_name):
            db.addServicesLog(session.clientid, inputData.date_timestamp,
                              session.siteName, 'Field Modified',
                              'Previously Logged Name: %s %s' %
                              (prev_first_name, prev_last_name))
        if (prev_id != results_id or prev_description != results_description):
            db.addServicesLog(session.clientid, inputData.date_timestamp,
                              session.siteName, 'Field Modified',
                              'Previously Logged ID: %s %s' %
                              (prev_id, prev_description))
        if (prev_phone != results_phone):
            db.addServicesLog(session.clientid, inputData.date_timestamp,
                              session.siteName, 'Field Modified',
                              'Previously Logged Phone Number: %s' %
                              (prev_phone))


        raise web.seeother('/client/viewedit/')
        #return render.client_view_edit()

class ClientAddWaitlist:
    def GET(self):
        if session.get('username'):
            return render.client_search()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()
        if session.get('username') and session.get('clientid'):
            db.addToWaitlist(session.get('username'), session.get('clientid'))
            raise web.seeother('/client/viewedit/')
        else:
            raise web.seeother('/')

class ModifySeats:
    def GET(self):
        if session.get('username'):
            session.siteID, session.siteName = db.getCurrentSite(session.username)
            seatsInfo = db.getSeats(session.siteID)
            if seatsInfo is None:
                raise web.seeother('/services/')
            else:
                session.seatsInfo = seatsInfo
                return render.modify_seats()
        else:
            raise web.seeother('/')
    def POST(self):
        inputData = web.input()
        serviceID = inputData['serviceID']
        seatsnum = inputData['seatsnum']
        session.modifySeatsMsg = db.modifySeats(serviceID, seatsnum)
        raise web.seeother('/services/modifyseats/')



class ModifyBunks:
    def GET(self):
        if session.get('username'):
            session.siteID, session.siteName = db.getCurrentSite(session.username)
            bunksInfo = db.getBunks(session.siteID)
            if bunksInfo is None:
                raise web.seeother('/services/')
            else:
                session.bunksInfo = bunksInfo
                return render.modify_bunks()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()
        BunksAvailable = {}
        for key in inputData.keys():
            if key == 'serviceID':
                serviceID = inputData[key]
            else:
                BunksAvailable[key] = inputData[key]

        db.modifyBunks(serviceID, BunksAvailable)
        if session.get('returnToClient') is not None:
            session.returnToClient = None
            raise web.seeother('/client/viewedit/')
        else:
            raise web.seeother('/services/modifybunks/')


class ModifyRooms:
    def GET(self):
        if session.get('username'):
            session.siteID, session.siteName = db.getCurrentSite(session.username)
            roomsInfo = db.getRooms(session.siteID)
            if roomsInfo is None:
                raise web.seeother('/services/')
            else:
                session.roomsInfo = roomsInfo
                return render.modify_rooms()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()

        # Get occupied rooms from input form
        # (non-occupied rooms are not passed)
        rnumOccupied = []
        for key in inputData.keys():
            if key=='serviceID':
                serviceID = inputData[key]
            else:
                rnumOccupied.append(key)
        db.modifyRooms(serviceID, rnumOccupied)

        raise web.seeother('/services/modifyrooms/')

class CheckAvailableRooms:
    def GET(self):
        if session.get('username'):
            session.siteID, session.siteName = db.getCurrentSite(session.username)
            bunksInfo = db.getBunks(session.siteID)
            if bunksInfo is None:
                raise web.seeother('/services/')
            else:
                session.bunksInfo = bunksInfo
                return render.check_available_rooms()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()
        BunksAvailable = {}
        for key in inputData.keys():
            if key == 'serviceID':
                serviceID = inputData[key]
            else:
                BunksAvailable[key] = inputData[key]

        db.modifyBunks(serviceID, BunksAvailable)
        if session.get('returnToClient') is not None:
            session.returnToClient = None
            raise web.seeother('/client/viewedit/')
        else:
            raise web.seeother('/services/checkintoroom/')

class ViewEditWaitlist:
    def GET(self):
        if session.get('username'):
            session.siteID, session.siteName = db.getCurrentSite(session.username)
            waitlistInfo = db.getWaitlist(session.siteID)
            if waitlistInfo is None:
                raise web.seeother('/services/')
            else:
                session.waitlistInfo = waitlistInfo
                return render.view_edit_waitlist()
        else:
            raise web.seeother('/')

    def POST(self):
        inputData = web.input()
        session.waitlistErrorMsg = None

        if 'add' in inputData:
            raise web.seeother('/client/search/')
        elif 'delete' in inputData and 'clientSelect' in inputData:
            db.deleteFromWaitlist(inputData['serviceID'],
                                  inputData['clientSelect'])
        elif 'up' in inputData and 'clientSelect' in inputData:
            db.moveUpWaitlist(inputData['serviceID'],
                              inputData['clientSelect'])
        elif 'down' in inputData and 'clientSelect' in inputData:
            db.moveDownWaitlist(inputData['serviceID'],
                              inputData['clientSelect'])
        else:
            session.waitlistErrorMsg = 'No client selected.'

        raise web.seeother('/services/waitlist/')

class PublicReports:
    def GET(self):
        return render.public_reports()

class BedsReport:
    def GET(self):
        session.bedsInfo = db.getBedsReport()
        return render.beds_report()

class MealsReport:
    def GET(self):
        session.mealsInfo = db.getMealsReport()
        return render.meals_report()

class ReorderReport:
    def GET(self):
        session.reorderInfo = db.getReorderReport()
        return render.reorder_report()

class SearchItem:
    def GET(self):
        username = session.get('username')

        if username:
            return render.search_item(
                db.getFoodBank(),
                db.getAllItemNames(),
                None,
                None,
                None,
                db.getSiteIDByUser(username),
                None
            )
        else:
            raise web.seeother('/')

    def POST(self):
        username = session.get('username')

        if username:
            inputData = web.input()

            return render.search_item(
                db.getFoodBank(),
                db.getAllItemNames(),
                inputData,
                db.getItemByForm(inputData),
                db.getSiteServices(username),
                db.getSiteIDByUser(username),
                None
            )
        else:
            raise web.seeother('/')

class AddInventory:
    def GET(self):
        username = session.get('username')

        if username:
            services = db.getSiteServices(username)

            if services['FoodBank']:
                return render.add_inventory(None)
            else:
                raise web.seeother('/')
        else:
            raise web.seeother('/')

    def POST(self):
        username = session.get('username')

        if username:
            services = db.getSiteServices(username)

            if services['FoodBank']:
                inputData = web.input()
                items = db.addInventory(username, inputData)
                return render.add_inventory(items)
            else:
                raise web.seeother('/')
        else:
            raise web.seeother('/')

class Requests:
    def GET(self):
        username = session.get('username')

        if username:
            services = db.getSiteServices(username)

            if services['FoodBank']:
                requestsToFill = db.getRequestToFulfill(username, None)
                highRequests = db.getHighOutstandingRequests(username)
                return render.requests(requestsToFill, None, highRequests)
            else:
                raise web.seeother('/')
        else:
            raise web.seeother('/')

class RequestsBySort:
    def GET(self, pid):
        username = session.get('username')

        if username:
            services = db.getSiteServices(username)

            if services['FoodBank']:
                requestsToFill = db.getRequestToFulfill(username, pid)
                highRequests = db.getHighOutstandingRequests(username)
                return render.requests(requestsToFill, None, highRequests)
            else:
                raise web.seeother('/')
        else:
            raise web.seeother('/')

class ViewRequest:
    def GET(self):
        username = session.get('username')

        if username:
            services = db.getSiteServices(username)

            if services['Shelter'] or services['FoodPantry'] or services['SoupKitchen']:
                return render.view_request(db.getRequests(username), None, db.getHighRequests(username))
            else:
                raise web.seeother('/')
        else:
            raise web.seeother('/')

    def POST(self):
        username = session.get('username')

        if username:
            services = db.getSiteServices(username)

            if services['Shelter'] or services['FoodPantry'] or services['SoupKitchen']:
                inputData = web.input(RequestDateTime=[], ItemID=[], CountRequested=[], OldCountRequested=[], delRequest=[])
                updates = db.updateRequest(username, inputData)
                return render.view_request(db.getRequests(username), updates, db.getHighRequests(username))
            else:
                raise web.seeother('/')
        else:
            raise web.seeother('/')

class AddRequest:
    def GET(self):
        raise web.seeother('/')

    def POST(self):
        username = session.get('username')

        if username:
            inputData = web.input(ItemID=[], CountRequested=[], AvailableCount=[], OldCount=[])
            return render.search_item(db.getFoodBank(), db.getAllItemNames(), None, None, None, db.getSiteIDByUser(username), db.addRequest(username, inputData))

class FulFillRequest:
    def GET(self):
        raise web.seeother('/')

    def POST(self):
        username = session.get('username')

        if username:
            inputData = web.input(Requestor=[], RequestDateTime=[], ItemID=[], CountToProvide=[], Status=[])
            fulfillRequests = db.fulFillRequest(inputData)
            requestsToFill = db.getRequestToFulfill(username, None)
            highRequests = db.getHighOutstandingRequests(username)
            return render.requests(requestsToFill, fulfillRequests, highRequests)

class ClearDataInput:
    def GET(self):
        if session.get('username'):
            raise web.seeother('/inventory/searchItem/')
        else:
            raise web.seeother('/')

if __name__ == "__main__":
    app.run()
