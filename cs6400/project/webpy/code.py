"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Name: Team 010
Date: 03/10/2017
Purpose: Sample webpy app
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import web
web.config.debug = False # Needed for session to work

session = None

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
urls: pages in our Web App (based on regular regression)

left side = url pages, right side = related class names to run

(i.e. left side  = /, /pages/(.*), /db/, /session_end/, /login/
      right side = Index, Page, DB, SessionEnd, LogIn)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
urls = (
    '/', 'Index',
    '/page/(.*)', 'Page',
    '/db/', 'DB',
    '/session_end/', 'SessionEnd',
    '/login/', 'LogIn'
)



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
app: our webpy app
-globals(): tells app to look for classes in the global namespace
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
app = web.application(urls, globals())



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
session: our session object
-DiskStore: stores session on the hard drive
-DBStore (not used): stores session in the DB back-end
-initializer (not used): to store intial session's attribute:value
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
session = web.session.Session(app, web.session.DiskStore('session')) #, initializer={'username':'team010'})



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
globals: contains the session variable object

web.template.render():
 -used to render pages with the templating system
 -notice globals is passed into the render function so the templates
  can access it
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
globals = {'session':session}
render = web.template.render('templates/', globals=globals)



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Below are classes to run when related URLs are opened on the browser.

NOTE: Need to login before you can see page's content.
      See class LogIN below for more info.

      If not logged in, message 'User is not logged in!'

      In real app, we can redirect to a different page.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Default root URL for app is:
http://0.0.0.0:8080 (same as / for Index)

-session.get('username') is to get the value of the session variable
-render.index() is to render the index page. other_pages would used
 render.other_pages()

-Optional: hasattr() can be used to check if needed session
           attributes exists
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Index:
    def GET(self):
        # if hasattr(session, 'username'):
        if session.get('username'):
            return render.index()
        else:
            html = """
                <p>User is not logged in!</p>
                <br/><br/>
                <a href="/login/">Click to login as 'team010'</a>
            """

            return html



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Open with:
http://0.0.0.0:8080/page/
or
http://0.0.0.0:8080/page/{number here}
(i.e. http://0.0.0.0:8080/page/123)

This demonstrates the use of regular expression for url paging.
The URLs that class Page will process is set to '/page/(.*)' in the
'urls' variable near the very top. This is good for something like:

http://0.0.0.0:8080/getAccountNumberFor/Khanh/
http://0.0.0.0:8080/getAccountNumberFor/Melanie/
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Page:
    def GET(self, pid):
        if session.get('username'):
            # pid here is the number after /page/
            # pid is being passed to the template page for processing
            return render.page(pid)
        else:
            html = """
                <p>User is not logged in!</p>
                <br/><br/>
                <a href="/login/">Click to login as 'team010'</a>
            """

            return html



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
NOTE: As is, this will most likely not work in your environment.
      -Need to be updated your schema name, username and password

Open with:
http://0.0.0.0:8080/db/

Look at the Databases section of http://webpy.org/cookbook/
for info on how to create queries
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class DB:
    def GET(self):
        if session.get('username'):
            # DB connection
            dbh = web.database(dbn='mysql', db='cs6400_sp17_team010', user='developer', pw='stardust4') ######## NEED TO PUT IN user and pw

            # A SELECT statement, returning a DICTIONARY object
            # results = dbh.query("SELECT * FROM User WHERE UserName = 'khanh'") ### Regular SQL
            results = dbh.query("SELECT * FROM User WHERE UserName = $UserName", vars={'UserName':'khanh'}) ### SQL Injection prevention
            return render.db(results)
        else:
            html = """
                <p>User is not logged in!</p>
                <br/><br/>
                <a href="/login/">Click to login as 'team010'</a>
            """

            return html



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Open with:
http://0.0.0.0:8080/session_end/

This kills the session (which logs out the user),
deleting the session data stored on hard drive
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class SessionEnd:
    def GET(self):
        html = """
            <p>Session Ended!</p>
            <br/><br/>
            <a href="/">Go Home</a>
        """

        if session:
            session.kill()
            return html



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Open with:
http://0.0.0.0:8080/login/

An extremely simple way of logging in a hard-coded user.

Will need to create a form input field for username input instead.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class LogIn:
    def GET(self):
        session.username = 'team010'

        html = """
            <p>Log in as %s</p>
            <br/><br/>
            <a href="/">Go Home</a>
        """ % session.username

        return html



if __name__ == "__main__":
    app.run()
