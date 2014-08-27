import argparse
import random
import string
from subprocess import call

parser = argparse.ArgumentParser(description='Create a database.')
parser.add_argument('-d', '--database', metavar='DATABASE', dest='database', help="name of the database")
parser.add_argument('-u', '--user', metavar='USERNAME', dest='username', help="username for the database")
parser.add_argument('-p', '--password', metavar='PASSWORD', dest='password', default='',
                    help="password for user to connect to the database")
parser.add_argument('-U', '--auth_user', metavar='AUTH_USER', dest='auth_user', default='root',
                    help="user with rights to create database")
parser.add_argument('-P', '--auth_password', metavar='PASSWORD', dest='auth_password', default='',
                    help="password of auth_user to create database")

args = parser.parse_args()

database = args.database
if not database:
    database = raw_input('name of the database: ')

username = args.username
if not username:
    username = raw_input('username for the database (default={}): '.format(database))
    if not username:
        username = database

password = args.password
if not password:
    password = raw_input('password for user to connect to the database: ')
    if not password:
        password = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(6))

auth_pw = ' -p{}'.format(args.auth_password) if args.auth_password else ''
mysql_command = 'mysql'
mysql_create_db_args = '-u{AUTH_USER}{AUTH_PW} -e "create database {DATABASE};"'.format(
    AUTH_USER=args.auth_user,
    AUTH_PW=auth_pw,
    DATABASE=database)

mysql_grant_privileges_args = '-u{AUTH_USER}{AUTH_PW} -e"grant all privileges on {DATABASE}.* to {USERNAME}@"localhost" ' \
                              'identified by \'{PASSWORD}\';"'.format(AUTH_USER=args.auth_user,
                                                                      AUTH_PW=auth_pw,
                                                                      DATABASE=database,
                                                                      USERNAME=username,
                                                                      PASSWORD=password)
# call([mysql_command, mysql_create_db_args])
# call([mysql_grant_privileges_args])

print ""
print mysql_command + " " + mysql_create_db_args
print mysql_command + " " + mysql_grant_privileges_args
print ""
print "---------------------------------------"

