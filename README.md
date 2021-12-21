# TDDD97

Labs for the course Web Programming - TDDD97 given by Linköping University.

## Questions Lab 1

1. We don’t want to send unnecessary data to the server. We save traffic by doing this, but lose development time.
2. Not very, in theory a user could manually put an access token in the browser to gain access.
3. Unsure, however this is a real threat and must be taken seriously. In the worst case scenario the code could execute and delete or share vital data.
4. As the current implementation Twidder is a single page application and pushing the back button does nothing or takes you back to the previous page unrelated to Twidder. The solution is to implement routes.
5. When refreshing the Twidder goes back to its default state. This could be the expected behavior in some apps. We are getting this behavior because all information is stored in css and the single html page. Upon refreshing the code gets reset.
6. Server-side rendering is a good idea. The obvious advantage is removing stress from the client
7. A much better approach is to use http status codes. They can tell you exactly what went wrong.
8. It is fairly reliable. A great solution is to double check everything! This could be done on the server.
9. CSS is better. This is because tables are bigger (memory wise), may break text coping (on some browsers), they describe presentation not layout.
10. They definitely have a place. Nowadays single page applications are expected behavior. In my opinion they are great to display systems but can a bit frustrating when navigating.

## Questions Lab 2

1. The obvious answer is that storing it as plain text makes it possible to read right out of the database. This can be prevented by for example hashing and salting the password.
2. The communication should be subject to encryption. This ensures that even if a third party gets access to the communication stream, they can’t read it.
3. Flask could use the `render_template` method to display different pages. This could be used to show information to the user. In other words the current return statement with status and data and so on, could be replaced with actual html code.
4. According to IBM “A database management system (or DBMS) is essentially nothing more than a computerized data-keeping system.” SQLite is in a sense a scaled down system, containing a lot less functionality than other systems. This is both good and bad. In this project SQLite is definitely enough.
5. Telnet has both advantages and shortcomings. For example, it includes authentication support. The shortcomings are that no encryption is used in communication, it’s very ineffective protocol and it’s expensive due to slow typing speed.
