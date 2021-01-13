import sqlite3
import sys
import time
import getpass
from cryptography.fernet import Fernet
from tqdm import tqdm
from password_strength import PasswordStats

def updateUser(db_file, userInformation):
		query = "UPDATE USER SET userMail = ?, userPassword = ? WHERE  userMail = userMail;"
		connection = sqlite3.connect(db_file)
		cursor = connection.cursor()
		cursor.execute(query, list(userInformation))
		connection.commit()
		cursor.close()
		connection.close()

def userLogin(db_file,username, password):
		connection = sqlite3.connect(db_file)
		cursor = connection.cursor()
		cursor.execute("SELECT userMail, userPassword FROM USER;")
		result = cursor.fetchall()
		cursor.close()
		connection.close()

		if(username == result[0][0] and password == result[0][1]):
				askUpdate()
				return homePage()
		else:
				print("Wrong username or password!")

def askUpdate():
		print("DO YOU WANT TO UPDATE YOUR LOGIN PASSWORD?")
		answer = input("y/n:")
		if(answer == "y" or answer == "Y"):
				username = input("new username: ")
				"""password = input("new password: ")"""
				password = getpass.getpass(prompt = "new password: ")
				updateUser("pythonCryptography.db",(username, password))
				print(" ")
				print("UPDATING USER DATABASE")
				for i in tqdm(range(100)):
					time.sleep(0.02)
					pass
		elif(answer == "n" or answer == "N"):
			print(" ")
			print("LOADING...")
			print(" ")
			for i in tqdm(range(100)):
				time.sleep(0.005)
				pass

def loginPage():
		
		print("""
IF YOU LOGIN FIRST TIME

user name: admin
user password: admin

YOU CAN LOGIN THIS INFORMATION
		""")
				
		print("Please enter username and password")
		userNameInput = input("username: ")
		"""userNamePassword = input("password: ")"""
		userNamePassword = getpass.getpass(prompt = "password: ", stream=None)
		
		userLogin("pythonCryptography.db", userNameInput, userNamePassword)

def allWebsites(db_file):

		print(" ")
		print("LOADING...")
		print(" ")
		for i in tqdm(range(100)):
			time.sleep(0.005)
			pass

		try:
				sqliteConnection = sqlite3.connect(db_file)
				cursor = sqliteConnection.cursor()

				query = "SELECT * FROM WEBSITE_INFO"
				cursor.execute(query)
				records = cursor.fetchall()
				
				for i in records:
						print("")
						print("Website id: ",i[0])
						print("Website Name: ",i[1])
						print("Website Adress: ",i[2])
						print("Website Password: ",i[3])
						print("")

				cursor.close()

		except sqlite3.Error as error:
				print("SOMETING WENT WRONG")
		finally:
				if (sqliteConnection):
					sqliteConnection.close()
					homePage()
					print("The SQLite connection is closed")

def showPassword(db_file):
		try:
				sqliteConnection = sqlite3.connect(db_file)
				cursor = sqliteConnection.cursor()
				showPassInput = input("Enter ID: ")
				cursor.execute("SELECT * FROM WEBSITE_INFO WHERE id = ?;", [showPassInput])
				records = cursor.fetchall()
				
				for i in records:
					print("")
					print("Website id: ",i[0])
					print("Website Name: ",i[1])
					print("Website Adress: ",i[2])
					a = decryptPassword(i[3])
					print("Website Password: ",a)
					print("")

				cursor.close()

		except sqlite3.Error as error:
				print("SOMETING WENT WRONG")
		finally:
				if (sqliteConnection):
					sqliteConnection.close()
					homePage()
					print("The SQLite connection is closed")


def addWebsites(db_file):

		print("ADD WEBSITE")
		websiteNameInput = input("Website Name: ")
		websiteAddressInput = input("Website Address: ")
		websitePasswordInput = getpass.getpass(prompt = "Website password: ")
		websitePasswordInput = bytes(websitePasswordInput , encoding="utf-8")
		websitePasswordInput = encryptPassword(websitePasswordInput)
		addData = (websiteNameInput, websiteAddressInput, websitePasswordInput)
		sqliteConnection = sqlite3.connect(db_file)
		cursor = sqliteConnection.cursor()
		cursor.execute("""INSERT INTO WEBSITE_INFO (
							websiteName, websiteAdress, websitePassword
						 )
						 VALUES (
							 ?,?,?
						 );""", addData)
		sqliteConnection.commit()
		cursor.close()
		sqliteConnection.close()
		homePage()

def deleteWebsites(db_file):
	print("REMOVE WEBSITE")
	websiteDeleteId= input("Enter website Id: ")
	sqliteConnection = sqlite3.connect(db_file)
	cursor = sqliteConnection.cursor()
	cursor.execute("""DELETE FROM WEBSITE_INFO WHERE id = ?;""", [websiteDeleteId])
	sqliteConnection.commit()
	cursor.close()
	sqliteConnection.close()
	homePage()

def updateWebsites(db_file):
	print("UPDATE WEBSITE")
	websiteUpdateId = input("Enter website Id: ")
	websiteNameUpdate = input("Website Name: ")
	websiteAddressUpdate = input("Website Address: ")
	websitePasswordUpdate = getpass.getpass(prompt = "Website password: ")
	websitePasswordUpdate = bytes(websitePasswordUpdate , encoding="utf-8")
	websitePasswordUpdate = encryptPassword(websitePasswordUpdate)
	updateData = (websiteNameUpdate, websiteAddressUpdate, websitePasswordUpdate, websiteUpdateId)
	sqliteConnection = sqlite3.connect(db_file)
	cursor = sqliteConnection.cursor()
	cursor.execute("""UPDATE WEBSITE_INFO SET  websiteName = ?, websiteAdress = ?, websitePassword = ? WHERE id = ?;""", updateData)
	sqliteConnection.commit()
	cursor.close()
	sqliteConnection.close()
	homePage()

def homePage():
		print("""WELCOME TO CRYPTOLG

CHOOSE STATUS

1.ALL WEBSITES
2.ADD WEBSITE
3.DELETE WEBSITE
4.UPDATE WEBSITE
5.SHOW PASSWORDS
6.EXIT
""")

		choose = input("Chose: ")

		if(choose == "1"):
				allWebsites("pythonCryptography.db")
		elif(choose == "2"):
				addWebsites("pythonCryptography.db")
		elif(choose == "3"):
				deleteWebsites("pythonCryptography.db")
		elif(choose == "4"):
				updateWebsites("pythonCryptography.db")
		elif(choose == "5"):
				showPassword("pythonCryptography.db")
		elif(choose == "6"):
				sys.exit()
"""
def generateKey():
    key=Fernet.generate_key()
    with open("cryptoKey","wb") as keyFile:
        keyFile.write(key)
"""

def loadKey():
    return open("cryptoKey","rb").read()

def encryptPassword(password):
	key = loadKey()
	encoded_text = Fernet(key).encrypt(password)
	return encoded_text

def decryptPassword(password):
	key = loadKey()
	decoded_text = Fernet(key).decrypt(password)
	return decoded_text

def main():
	loginPage()

if __name__ == '__main__':
	main()
