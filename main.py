# import files from assets folder - turn assets into module?
import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "assets/")

from GUI import *


# is the user logged into an account that exists
isLoggedin = False

# the current and previous page
navPage = "Login page"
prevPage = "Login page"

# change default font
ChangeFontName("RedHatMono.ttf")

# customer storage file and currently selected customer
customersFile = "customers.json"
currentCustomerID = None


# login page
class Login:
	def __init__(self, rect, colors):
		self.rect = pg.Rect(rect)
		self.backgroundColor = colors[0]
		self.borderColor = colors[1]
		self.activeColor = colors[2]
		self.inactiveColor = colors[3]
		# where user accounts are stored
		self.userDetails = "userDetails.json"

		self.userNameForgroundColor = self.inactiveColor
		self.passwordForgroundColor = self.inactiveColor

		self.title = Label((self.rect.x + 300, self.rect.y + 10, self.rect.w - 600, self.rect.h // 2 - 60), (self.backgroundColor, self.borderColor), text="Login", textData={"fontSize": 90}, lists=[])

		self.userNameInput = TextInputBox((self.rect.x + 10, self.rect.y + self.rect.h // 2 - 35, self.rect.w - 20, 55), (self.backgroundColor, self.borderColor, self.activeColor), drawData={"replaceSplashText": False}, textData={"alignText": "left", "fontSize": 30}, splashText="User name: ", inputData={"charLimit": 50, "allowedKeysFile": "userNameKeys.txt"}, lists=[])
		self.passwordInput = TextInputBox((self.rect.x + 10, self.rect.y + self.rect.h // 2 + 35, self.rect.w - 20, 55), (self.backgroundColor, self.borderColor, self.activeColor), drawData={"replaceSplashText": False}, textData={"alignText": "left", "fontSize": 30}, splashText="Password: ", inputData={"charLimit": 50, "allowedKeysFile": "passwordKeys.txt"}, lists=[])

		self.submitButton = Button((self.rect.x + self.rect.w - 210, self.rect.y + self.rect.h // 2 + 110, 200,  55), (self.backgroundColor, self.borderColor, self.activeColor), onClick=self.Submit, text="Log in", textData={"fontSize": 30}, lists=[])

		self.messageBox = Label((self.rect.x + 10, self.rect.y + self.rect.h // 2 + 110, self.rect.w - 230,  55), (self.backgroundColor, self.borderColor), text="Please enter a user name and password.", textData={"fontSize": 30, "alignText": "left"}, lists=[])

		self.userName = None
		self.password = None
		self.ID = None

	def Draw(self):
		pg.draw.rect(screen, self.backgroundColor, self.rect)
		DrawRectOutline(self.borderColor, self.rect, 2)

		self.title.Draw()
		self.userNameInput.Draw()
		self.passwordInput.Draw()
		self.submitButton.Draw()
		self.messageBox.Draw()

	def HandleEvent(self, event):
		self.userNameInput.HandleEvent(event)
		self.passwordInput.HandleEvent(event)
		self.submitButton.HandleEvent(event)

	def Submit(self):
		with open(self.userDetails, "r") as file:
			data = json.load(file)
			file.close()

		for key in data:
			user = data[key]
			if user["userName"] == self.userNameInput.input and user["password"] == self.passwordInput.input:
				self.LoginUser(user["userName"], user["password"], user["ID"])
			else:
				self.messageBox.UpdateText(f"User name or password is incorrect!")

	def LoginUser(self, userName, password, ID):
		global isLoggedin, navPage, prevPage
		isLoggedin = True
		prevPage = "Home"
		navPage = "Home"
		self.userName = userName
		self.password = password
		self.ID = ID
		self.time = NowFormatted()

	def LogoutUser(self):
		global isLoggedin, navPage, prevPage
		isLoggedin = False
		prevPage = navPage
		navPage = "Login page"
		self.userName = None
		self.password = None
		self.time = None
		self.ID = None
		self.userNameInput.ClearText()
		self.passwordInput.ClearText()
		self.messageBox.UpdateText(f"Please enter a user name and password.")

	def ChangeUserName(self):
		with open(self.userDetails, "r") as file:
			data = json.load(file)
			file.close()

		self.userName = userNameEditPage.textInput.input
		userNameEditPage.UpdateMessage(f"User name: {self.userName}")
		data[str(self.ID)]["userName"] = self.userName

		with open(self.userDetails, "w") as file:
			json.dump(data, fp=file, indent=2)
			file.close()

	def ChangePassword(self):
		with open(self.userDetails, "r") as file:
			data = json.load(file)
			file.close()

		self.password = userPasswordPage.textInput.input
		userPasswordPage.UpdateMessage(f"Password: {self.password}")
		data[str(self.ID)]["password"] = self.password

		with open(self.userDetails, "w") as file:
			json.dump(data, fp=file, indent=2)
			file.close()

	def CreateUser(self, userName, password):
		with open(self.userDetails, "r") as file:
			data = json.load(file)
			file.close()

		maxID = 0
		for key in data:
			maxID = max(int(key), maxID)

		maxID += 1
		data[str(maxID)] = {"userName": userName, "password": password, "ID": maxID}

		with open(self.userDetails, "w") as file:
			data = json.dump(data, fp=file, indent=2)
			file.close()

	def DeleteUser(self):
		with open(self.userDetails, "r") as file:
			data = json.load(file)
			file.close()

		del data[str(self.ID)]

		self.LogoutUser()

		with open(self.userDetails, "w") as file:
			json.dump(data, fp=file, indent=2)
			file.close()


# navigation object used in a navigation menu
class NavItem(Button):
	def __init__(self, index, text, action=None):
		self.index = index
		self.text = text
		self.action = action

	def Create(self, rect, colors, onClick, text="", name=""):
		super().__init__(rect, colors, onClick=onClick, text=text, name=name, textData={"fontSize": 20, "alignText": "top" if "\n" in text else "center"}, lists=[])


class NavigationMenu:
	def __init__(self, rect, colors, navItems=[]):
		self.rect = pg.Rect(rect)

		self.backgroundColor = colors[0]
		self.borderColor = colors[1]

		self.navItems = navItems
		self.CreateNavItems()

	# give navItems a rect and color
	def CreateNavItems(self):
		xCounter = 0
		yCounter = 0
		for item in self.navItems:

			if item.index % 5 == 0 and item.index != 0:
				xCounter = 0
				yCounter += 1

			h = 68
			xOffset = 3
			rect = ((xCounter * (self.rect.w // 5) + xOffset), self.rect.y + ((xOffset * 2) * (yCounter + 1)) + (yCounter * h), (self.rect.w // 5) - (xOffset * 2), h)
			xCounter += 1

			item.Create(rect, (self.backgroundColor, self.borderColor, lightBlue), item.action, item.text, str(item.index))

	def Draw(self):
		pg.draw.rect(screen, self.backgroundColor, self.rect)
		DrawRectOutline(self.borderColor, self.rect, 2)

		for item in self.navItems:
			item.Draw()

	def HandleEvent(self, event):
		for item in self.navItems:
			item.HandleEvent(event)


# show details about an object
class DetailsPage:
	def __init__(self, rect, colors, titleText="", messageText="", messageBoxRect=None):
		self.rect = pg.Rect(rect)
		self.backgroundColor = colors[0]
		self.borderColor = colors[1]

		self.title = Label((self.rect.x + 30, self.rect.y + 10, self.rect.w - 60, self.rect.h // 2 - 120), (self.backgroundColor, self.borderColor), text=titleText, textData={"fontSize": 45}, lists=[])

		if messageBoxRect == None:
			rect = (self.rect.x + 10, self.rect.y + 100, self.rect.w - 20, self.rect.h - 110)
		else:
			rect = messageBoxRect

		self.messageBox = Label(rect, (self.backgroundColor, self.borderColor), text=messageText, textData={"fontSize": 30, "alignText": "left-top", "multiline": True}, lists=[])

	def Draw(self):
		pg.draw.rect(screen, self.backgroundColor, self.rect)
		DrawRectOutline(self.borderColor, self.rect, 2)

		self.title.Draw()
		self.messageBox.Draw()

	def UpdateMessage(self, text):
		self.messageBox.UpdateText(text)


# edit details of an object
class EditPage(DetailsPage):
	def __init__(self, rect, colors, titleText="", messageText="", action=None, inputData={}):
		super().__init__(rect, colors, titleText, messageText, (rect[0] + 10, rect[1] + 100, rect[2] - 20, 60))
		self.textInput = TextInputBox((self.rect.x + 10, self.rect.y + 170, self.rect.w - 20, 60), colors, inputData=inputData, textData={"alignText": "left"}, drawData={"replaceSplashText": False}, lists=[])
		self.submit = Button((self.rect.x + self.rect.w - 120, self.rect.y + self.rect.h - 60, 105, 45), colors, text="Submit", onClick=action, lists=[])

	def Draw(self):
		pg.draw.rect(screen, self.backgroundColor, self.rect)
		DrawRectOutline(self.borderColor, self.rect, 2)
		self.title.Draw()
		self.messageBox.Draw()
		self.textInput.Draw()
		self.submit.Draw()

	def HandleEvent(self, event):
		self.textInput.HandleEvent(event)
		self.submit.HandleEvent(event)


# create a new user
class CreateUserPage(DetailsPage):
	def __init__(self, rect, colors, titleText="", messageText="", userInputData={}, passwordInputData={}):
		super().__init__(rect, colors, titleText, messageText, messageBoxRect=(rect[0] + 10, rect[1] + 250, rect[2] - 135, 135))

		self.userName = TextInputBox((self.rect.x + 10, self.rect.y + 100, self.rect.w - 20, 60), colors, inputData=userInputData, textData={"alignText": "left"}, drawData={"replaceSplashText": False}, lists=[])
		self.password = TextInputBox((self.rect.x + 10, self.rect.y + 170, self.rect.w - 20, 60), colors, inputData=passwordInputData, textData={"alignText": "left"}, drawData={"replaceSplashText": False}, lists=[])
		self.submit = Button((self.rect.x + self.rect.w - 120, self.rect.y + self.rect.h - 60, 105, 45), colors, text="Submit", onClick=self.Submit, lists=[])

	def Draw(self):
		pg.draw.rect(screen, self.backgroundColor, self.rect)
		DrawRectOutline(self.borderColor, self.rect, 2)

		self.title.Draw()
		self.messageBox.Draw()
		self.userName.Draw()
		self.password.Draw()
		self.submit.Draw()

	def HandleEvent(self, event):
		self.userName.HandleEvent(event)
		self.password.HandleEvent(event)
		self.submit.HandleEvent(event)

	def Submit(self):
		if self.userName.input != "" and self.password.input != "":
			self.UpdateMessage("User created.\nYou can now login.")
			login.CreateUser(self.userName.input, self.password.input)
		else:
			self.UpdateMessage("User name or password is not filled.")


# create a new customer
class CreateCustomerPage(DetailsPage):
	def __init__(self, rect, colors, titleText="", messageText="", nameInputData={}, balanceInputData={}):
		super().__init__(rect, colors, titleText, messageText, messageBoxRect=(rect[0] + 10, rect[1] + 250, rect[2] - 135, 135))

		self.name = TextInputBox((self.rect.x + 10, self.rect.y + 100, self.rect.w - 20, 60), colors, inputData=nameInputData, textData={"alignText": "left"}, drawData={"replaceSplashText": False}, lists=[])
		self.balance = TextInputBox((self.rect.x + 10, self.rect.y + 170, self.rect.w - 20, 60), colors, inputData=balanceInputData, textData={"alignText": "left"}, drawData={"replaceSplashText": False}, lists=[])
		self.submit = Button((self.rect.x + self.rect.w - 120, self.rect.y + self.rect.h - 60, 105, 45), colors, text="Submit", onClick=self.Submit, lists=[])

	def Draw(self):
		pg.draw.rect(screen, self.backgroundColor, self.rect)
		DrawRectOutline(self.borderColor, self.rect, 2)

		self.title.Draw()
		self.messageBox.Draw()
		self.name.Draw()
		self.balance.Draw()
		self.submit.Draw()

	def HandleEvent(self, event):
		self.name.HandleEvent(event)
		self.balance.HandleEvent(event)
		self.submit.HandleEvent(event)

	def Submit(self):
		if self.name.input != "" and self.balance.input != "":
			self.UpdateMessage(f"Customer account created.")
			self.CreateCustomer(self.name.input, int(self.balance.input))
		else:
			self.UpdateMessage(f"Name or balance is empty.")

	def CreateCustomer(self, name, bal):
		global currentCustomerID
		with open(customersFile, "r") as file:
			data = json.load(file)
			file.close()

		maxID = -1
		for key in data:
			maxID = max(int(key), maxID)

		maxID += 1

		data[str(maxID)] = {"name": name, "balance": bal, "ID": maxID}
		currentCustomerID = maxID

		with open(customersFile, "w") as file:
			json.dump(data, fp=file, indent=2)
			file.close()

		customerBrowserPage.GetCustomers()

	def DeleteCustomer(self):
		global currentCustomerID
		if currentCustomerID == None:
			return

		Back()
		with open(customersFile, "r") as file:
			data = json.load(file)
			file.close()

		del data[str(currentCustomerID)]
		currentCustomerID = None

		with open(customersFile, "w") as file:
			json.dump(data, fp=file, indent=2)
			file.close()

		customerBrowserPage.GetCustomers()

	def ChangeName(self):
		with open(customersFile, "r") as file:
			data = json.load(file)
			file.close()

		self.name = customerNameEditPage.textInput.input
		customerNameEditPage.UpdateMessage(f"Name: {self.name}")
		data[str(currentCustomerID)]["name"] = self.name

		with open(customersFile, "w") as file:
			json.dump(data, fp=file, indent=2)
			file.close()

		customerBrowserPage.GetCustomers()

	def ChangeBalance(self):
		with open(customersFile, "r") as file:
			data = json.load(file)
			file.close()

		self.balance = customerBalancePage.textInput.input
		customerBalancePage.UpdateMessage(f"Balance: £{self.balance}")
		data[str(currentCustomerID)]["balance"] = int(self.balance)

		with open(customersFile, "w") as file:
			json.dump(data, fp=file, indent=2)
			file.close()

		customerBrowserPage.GetCustomers()


# view all customers - add scrolling?
class CustomerBrowserPage(DetailsPage):
	def __init__(self, rect, colors, titleText="", messageText="", inputData={}):
		super().__init__(rect, colors, titleText, messageText, (rect[0] + 10, rect[1] + 100, rect[2] - 20, rect[3] - 180))
		self.textInput = TextInputBox((self.rect.x + 10, self.rect.y + self.rect.h - 70, self.rect.w - 135, 60), colors, inputData=inputData, textData={"alignText": "left"}, drawData={"replaceSplashText": False}, lists=[])
		self.submit = Button((self.rect.x + self.rect.w - 120, self.rect.y + self.rect.h - 70, 110, 60), colors, text="Submit", onClick=self.Submit, lists=[])
		self.GetCustomers()

	def Draw(self):
		pg.draw.rect(screen, self.backgroundColor, self.rect)
		DrawRectOutline(self.borderColor, self.rect, 2)
		self.title.Draw()
		self.messageBox.Draw()
		self.textInput.Draw()
		self.submit.Draw()

		for customer in self.customers:
			customer.Draw()

	def GetCustomers(self):
		self.customers = []
		self.ids = []
		with open(customersFile, "r") as file:
			data = json.load(file)
			file.close()

		xCounter = 0
		yCounter = 0
		for i, key in enumerate(data):
			if i % 6 == 0 and i != 0:
				xCounter = 0
				yCounter += 1
			rect = (self.messageBox.rect.x + (xCounter * 203) + (xCounter * 2) + 4, self.messageBox.rect.y + (yCounter * 70) + (yCounter * 2) + 4, 203, 70)
			xCounter += 1
			if data[key]["ID"] == currentCustomerID:
				self.customers.append(Customer(rect, (lightBlack, lightBlue), data[key]["name"], data[key]["balance"], data[key]["ID"]))
			else:
				self.customers.append(Customer(rect, (lightBlack, darkWhite), data[key]["name"], data[key]["balance"], data[key]["ID"]))

			self.ids.append(data[key]["ID"])

	def HandleEvent(self, event):
		self.textInput.HandleEvent(event)
		self.submit.HandleEvent(event)

	def Submit(self):
		global currentCustomerID
		if int(self.textInput.input) in self.ids:
			currentCustomerID = int(self.textInput.input)

		self.GetCustomers()


# customer stores name and balance for a customer
class Customer(Label):
	def __init__(self, rect, colors, name, balance, ID):
		super().__init__(rect, colors, f"Name:{name}\nBal:{balance}\nID:{ID}", textData={"multiline": True, "alignText": "left-top", "fontSize": 15}, lists=[])


class HelpPage(Label):
	def __init__(self, rect, colors, helpFiles=[], text="", name="", drawData={}, textData={"alignText": "top"}, lists=[]):
		super().__init__(rect, colors, text, name, screen, drawData, textData, lists)
		self.ogRect = self.rect
		self.helpFilesText = []

		for file in helpFiles:
			self.helpFilesText.append(OpenFile(file))

		self.inexpHelp = Button((self.rect.x + 10, self.rect.y + (self.textHeight * len(self.textObjs)) + 10, self.rect.w - 20, self.rect.h / 3 - 25), colors, text="Help 1", onClick=self.ShowInexpHelp, lists=[])
		self.expHelp = Button((self.rect.x + 10, self.rect.y + (self.textHeight * len(self.textObjs)) + 145, self.rect.w - 20, self.rect.h / 3 - 25), colors, text="Help 2", onClick=self.ShowExpHelp, lists=[])
		self.expertHelp = Button((self.rect.x + 10, self.rect.y + (self.textHeight * len(self.textObjs)) + 280, self.rect.w - 20, self.rect.h / 3 - 25), colors, text="Help 3", onClick=self.ShowExpertHelp, lists=[])
		
		self.helpPage = None
		self.scrollBar = None

	def Draw(self):
		if isLoggedin:
			self.rect.y = self.ogRect.y
			self.rect.h = self.ogRect.h
			self.inexpHelp.UpdateRect((self.rect.x + 10, self.rect.y + (self.textHeight * len(self.textObjs)) + 10, self.rect.w - 20, self.rect.h / 3 - 25))
			self.expHelp.UpdateRect((self.rect.x + 10, self.rect.y + (self.textHeight * len(self.textObjs)) + 145, self.rect.w - 20, self.rect.h / 3 - 25))
			self.expertHelp.UpdateRect((self.rect.x + 10, self.rect.y + (self.textHeight * len(self.textObjs)) + 280, self.rect.w - 20, self.rect.h / 3 - 25))
		else:
			self.rect.y = 10
			self.rect.h = 630
			self.inexpHelp.UpdateRect((self.rect.x + 10, self.rect.y + (self.textHeight * len(self.textObjs) + 10), self.rect.w - 20, self.rect.h / 3 - 25))
			self.expHelp.UpdateRect((self.rect.x + 10, self.rect.y + (self.textHeight * len(self.textObjs) + self.rect.h / 3 - 25 + 20), self.rect.w - 20, self.rect.h / 3 - 25))
			self.expertHelp.UpdateRect((self.rect.x + 10, self.rect.y + (self.textHeight * len(self.textObjs) + (self.rect.h / 3 - 25 + 15) * 2), self.rect.w - 20, self.rect.h / 3 - 25))

		self.inexpHelp.UpdateText(self.inexpHelp.text)
		self.expHelp.UpdateText(self.expHelp.text)
		self.expertHelp.UpdateText(self.expertHelp.text)
		self.UpdateText(self.text)

		self.DrawBackground()
		self.DrawBorder()
		self.DrawText()

		if self.helpPage != None:
			self.helpPage.Draw()
			self.scrollBar.Draw()
		else:
			self.inexpHelp.Draw()
			self.expHelp.Draw()
			self.expertHelp.Draw()

	def HandleEvent(self, event):
		if self.helpPage == None:
			self.inexpHelp.HandleEvent(event)
			self.expHelp.HandleEvent(event)
			self.expertHelp.HandleEvent(event)
		else:
			self.scrollBar.HandleEvent(event)

	def ShowInexpHelp(self):
		global prevPage
		prevPage = "Help Page"
		self.helpPage = Label((self.rect.x + 10, self.rect.y + (self.textHeight * len(self.textObjs)) + 10, self.rect.w - 50, self.rect.h - (self.textHeight * len(self.textObjs) + 20)), (self.backgroundColor, self.foregroundColor), text=self.helpFilesText[0], lists=[], textData={"alignText": "left-top"})
		self.scrollBar = ScollBar((self.helpPage.rect.x + self.helpPage.rect.w, self.helpPage.rect.y, 30, self.helpPage.rect.h), (self.inexpHelp.backgroundColor, self.inexpHelp.inactiveColor), self.helpPage, buttonData={"backgroundColor": lightBlack, "inactiveColor": darkWhite, "activeColor": lightRed}, lists=[])

	def ShowExpHelp(self):
		global prevPage
		prevPage = "Help Page"
		self.helpPage = Label((self.rect.x + 10, self.rect.y + (self.textHeight * len(self.textObjs)) + 10, self.rect.w - 50, self.rect.h - (self.textHeight * len(self.textObjs) + 20)), (self.backgroundColor, self.foregroundColor), text=self.helpFilesText[1], lists=[], textData={"alignText": "left-top"})
		self.scrollBar = ScollBar((self.helpPage.rect.x + self.helpPage.rect.w, self.helpPage.rect.y, 30, self.helpPage.rect.h), (self.expHelp.backgroundColor, self.expHelp.inactiveColor), self.helpPage, buttonData={"backgroundColor": lightBlack, "inactiveColor": darkWhite, "activeColor": lightRed}, lists=[])

	def ShowExpertHelp(self):
		global prevPage
		prevPage = "Help Page"
		self.helpPage = Label((self.rect.x + 10, self.rect.y + (self.textHeight * len(self.textObjs)) + 10, self.rect.w - 50, self.rect.h - (self.textHeight * len(self.textObjs) + 20)), (self.backgroundColor, self.foregroundColor), text=self.helpFilesText[2], lists=[], textData={"alignText": "left-top"})
		self.scrollBar = ScollBar((self.helpPage.rect.x + self.helpPage.rect.w, self.helpPage.rect.y, 30, self.helpPage.rect.h), (self.expertHelp.backgroundColor, self.expertHelp.inactiveColor), self.helpPage, buttonData={"backgroundColor": lightBlack, "inactiveColor": darkWhite, "activeColor": lightRed}, lists=[])

	def Back(self):
		global prevPage
		if isLoggedin:
			prevPage = "Home"
		else:
			prevPage = "Login page"
		self.helpPage = None
		self.scrollBar = None


# get a customer with only the ID of the customer
def GetCustomer(ID):
	with open(customersFile, "r") as file:
		data = json.load(file)
		file.close()

	if str(ID) in data:
		return data[str(ID)]
	else:
		return None


def Quit():
	global running
	running = False


# go to the previous page / home page
def Back():
	global navPage
	navPage = prevPage
	if prevPage == "Help Page":
		hp.Back()


def DrawLoop():
	screen.fill(darkGray)

	# only draw for current page

	if navPage == "Login page":
		login.Draw()
		createUserButton.Draw()

	if isLoggedin:
		if navPage == "User details":
			userDetailsPage.Draw()
			if login.ID != 0:
				deleteAccount.Draw()

		elif navPage == "Edit user name":
			userNameEditPage.Draw()

		elif navPage == "Edit password":
			userPasswordPage.Draw()

		elif navPage == "Change current customer":
			customerBrowserPage.Draw()

		elif navPage == "Customer details":
			customerDetailsPage.Draw()

		elif navPage == "Edit customer name":
			customerNameEditPage.Draw()

		elif navPage == "Edit customer balance":
			customerBalancePage.Draw()

		elif navPage == "Create user page":
			createUserPage.Draw()

		elif navPage == "Create customer page":
			createCustomerPage.Draw()

		if navPage != "Login page":
			back.Draw()
			if navPage != "Create user page":
				navMenu.Draw()

	if navPage == "Help Page":
		hp.Draw()
		back.Draw()


	DrawAllGUIObjects()

	pg.display.update()


def HandleEvents(event):
	HandleGui(event)

	# only handle events for current page - change to active surfaces?

	if navPage == "Login page":
		login.HandleEvent(event)
		createUserButton.HandleEvent(event)

	if isLoggedin:
		if navPage == "User details":
			if login.ID != 0:
				deleteAccount.HandleEvent(event)

		elif navPage == "Edit user name":
			userNameEditPage.HandleEvent(event)

		elif navPage == "Edit password":
			userPasswordPage.HandleEvent(event)

		elif navPage == "Change current customer":
			customerBrowserPage.HandleEvent(event)

		elif navPage == "Edit customer name":
			customerNameEditPage.HandleEvent(event)

		elif navPage == "Edit customer balance":
			customerBalancePage.HandleEvent(event)

		elif navPage == "Create user page":
			createUserPage.HandleEvent(event)

		elif navPage == "Create customer page":
			createCustomerPage.HandleEvent(event)

		if navPage != "Login page":
			back.HandleEvent(event)
			if navPage != "Create user page":
				navMenu.HandleEvent(event)

	if navPage == "Help Page":
		hp.HandleEvent(event)
		back.HandleEvent(event)


# change to a different page

def NewUserPage():
	global navPage, prevPage
	prevPage = "Login page"
	navPage = "Create user page"


def NewCustomerPage():
	global navPage, prevPage
	prevPage = "Home"
	navPage = "Create customer page"


def UserDetailsPage():
	global navPage, prevPage
	prevPage = "Home"
	navPage = "User details"
	userDetailsPage.UpdateMessage(f"User name: {login.userName}\nPassword: {login.password}\nLogged in at: {login.time}")


def EditUserNamePage():
	global navPage, prevPage
	prevPage = "Home"
	navPage = "Edit user name"
	userNameEditPage.UpdateMessage(f"User name: {login.userName}")


def EditPasswordPage():
	global navPage, prevPage
	prevPage = "Home"
	navPage = "Edit password"
	userPasswordPage.UpdateMessage(f"Password: {login.password}")


def ChangeCurrentCustomerPage():
	global navPage, prevPage
	prevPage = "Home"
	navPage = "Change current customer"
	customerBrowserPage.UpdateMessage("")


def CustomerDetailsPage():
	global navPage, prevPage
	prevPage = "Home"
	navPage = "Customer details"
	customer = GetCustomer(currentCustomerID)
	if customer != None:
		customerDetailsPage.UpdateMessage(f"Name: {customer['name']}\nBalance: £{customer['balance']}\nID: {customer['ID']}")
	else:
		customerDetailsPage.UpdateMessage(f"No customer selected.")


def ChangeHelpPage():
	global navPage, prevPage
	if isLoggedin:
		prevPage = "Home"
	else:
		prevPage = "Login page"
	navPage = "Help Page"


def EditCustomerNamePage():
	global navPage, prevPage
	prevPage = "Home"
	navPage = "Edit customer name"
	customer = GetCustomer(currentCustomerID)
	if customer != None:
		customerNameEditPage.UpdateMessage(f"Name: {customer['name']}")
	else:
		customerNameEditPage.UpdateMessage(f"No customer selected.")


def EditCustomerBalancePage():
	global navPage, prevPage
	prevPage = "Home"
	navPage = "Edit customer balance"
	customer = GetCustomer(currentCustomerID)
	if customer != None:
		customerBalancePage.UpdateMessage(f"Balance: £{customer['balance']}")
	else:
		customerBalancePage.UpdateMessage(f"No customer selected.")


# create gui objects

# exit program
exit = Button((width - 210, height - 60, 200, 50), (lightBlack, darkWhite, lightBlue), onClick=Quit, text="Quit")

# previous page
back = Button((width - 420, height - 60, 200, 50), (lightBlack, darkWhite, lightBlue), onClick=Back, text="Back", lists=[])


# login page
login = Login((10, 100, width - 20, 400), (lightBlack, darkWhite, lightBlue, darkWhite))
# new user page
createUserButton = Button((width - 410, height - 200, 400, 50), (lightBlack, darkWhite, lightBlue), onClick=NewUserPage, text="Create new user", lists=[])
createUserPage = CreateUserPage((10, 100, width - 20, 400), (lightBlack, darkWhite, lightBlue), "Create new user", "Please enter a user name and password.", userInputData={"splashText": "User name: ", "charLimit": 50, "allowedKeysFile": "userNameKeys.txt"}, passwordInputData={"splashText": "Password: ", "charLimit": 50, "allowedKeysFile": "passwordKeys.txt"})

# new customer page
createCustomerPage = CreateCustomerPage((10, 180, width - 20, 400), (lightBlack, darkWhite, lightBlue), "Create new customer", "Please enter a name and balance.", nameInputData={"splashText": "Customer name:", "charLimit": 50, "allowedKeysFile": "userNameKeys.txt"}, balanceInputData={"splashText": "Balance: £", "charLimit": 50, "allowedKeysFile": "numberKeys.txt"})
customerBrowserPage = CustomerBrowserPage((10, 180, width - 20, 400), (lightBlack, darkWhite, lightBlue), "Choose a customer", inputData={"splashText": "ID: ", "charLimit": 3, "allowedKeysFile": "numberKeys.txt"})


# navigation options
navs = [
	NavItem(0, "Log out", login.LogoutUser),
	NavItem(1, "Get user details", UserDetailsPage),
	NavItem(2, "Edit user name", EditUserNamePage),
	NavItem(3, "Edit user password", EditPasswordPage),
	NavItem(4, "New customer", NewCustomerPage),
	NavItem(5, "Change current\ncustomer", ChangeCurrentCustomerPage),
	NavItem(6, "Customer details", CustomerDetailsPage),
	NavItem(7, "Edit customer name", EditCustomerNamePage),
	NavItem(8, "Edit customer\nbalance", EditCustomerBalancePage),
	NavItem(9, "Delete current user", createCustomerPage.DeleteCustomer)
]

navMenu = NavigationMenu((0, 0, width, 160), (lightBlack, darkWhite), navs)


# user details
userDetailsPage = DetailsPage((10, 180, width - 20, 400), (lightBlack, darkWhite), "Your details")
deleteAccount = Button((width - 430, height - 210, 400, 50), (lightBlack, darkWhite, lightBlue), onClick=login.DeleteUser, text="Delete account", lists=[])

# customer details
customerDetailsPage = DetailsPage((10, 180, width - 20, 400), (lightBlack, darkWhite), "Customer details")

# change user details
userNameEditPage = EditPage((10, 180, width - 20, 400), (lightBlack, darkWhite, lightBlue), "Edit user name", action=login.ChangeUserName, inputData={"splashText": "New user name: ", "charLimit": 50, "allowedKeysFile": "userNameKeys.txt"})
userPasswordPage = EditPage((10, 180, width - 20, 400), (lightBlack, darkWhite, lightBlue), "Edit password", action=login.ChangePassword, inputData={"splashText": "New password: ", "charLimit": 50, "allowedKeysFile": "passwordKeys.txt"})

# change customer details
customerNameEditPage = EditPage((10, 180, width - 20, 400), (lightBlack, darkWhite, lightBlue), "Edit customer name", action=createCustomerPage.ChangeName, inputData={"splashText": "New customer name: ", "charLimit": 50, "allowedKeysFile": "userNameKeys.txt"})
customerBalancePage = EditPage((10, 180, width - 20, 400), (lightBlack, darkWhite, lightBlue), "Edit customer balance", action=createCustomerPage.ChangeBalance, inputData={"splashText": "New customer balance: £", "charLimit": 50, "allowedKeysFile": "numberKeys.txt"})

openHp = Button((10, height - 60, 200, 50), (lightBlack, darkWhite, lightBlue), text="Help", onClick=ChangeHelpPage)
hp = HelpPage((10, 180, width - 20, 450), (lightBlack, darkWhite, lightBlue), ["help1.txt", "help2.txt", "help3.txt"], text="Help")


while running:
	clock.tick_busy_loop(fps)
	deltaTime = clock.get_time()
	for event in pg.event.get():
		if event.type == pg.QUIT:
			Quit()

		HandleEvents(event)

	DrawLoop()


