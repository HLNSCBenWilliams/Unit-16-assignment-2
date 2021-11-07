import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "assets/")

from GUI import *

isLoggedin = False

navPage = "Login page"
prevPage = "Login page"

ChangeFontName("RedHatMono.ttf")

customersFile = "customers.json"
currentCustomerID = None

class Login:
	def __init__(self, rect, colors):
		self.rect = pg.Rect(rect)
		self.backgroundColor = colors[0]
		self.borderColor = colors[1]
		self.activeColor = colors[2]
		self.inactiveColor = colors[3]
		self.userDetails = "userDetails.json"

		self.userNameForgroundColor = self.inactiveColor
		self.passwordForgroundColor = self.inactiveColor

		self.title = Label((self.rect.x + 300, self.rect.y + 10, self.rect.w - 600, self.rect.h // 2 - 60), (self.backgroundColor, self.borderColor), text="Login", textData={"fontSize": 90}, lists=[])
		self.userNameInput = TextInputBox((self.rect.x + 10, self.rect.y + self.rect.h // 2 - 35, self.rect.w - 20, 55), (self.backgroundColor, self.borderColor, self.activeColor), drawData={"replaceSplashText": False}, textData={"alignText": "left", "fontSize": 30}, inputData={"splashText": "User name: ", "charLimit": 50, "allowedKeysFile": "userNameKeys.txt"}, lists=[])
		self.passwordInput = TextInputBox((self.rect.x + 10, self.rect.y + self.rect.h // 2 + 35, self.rect.w - 20, 55), (self.backgroundColor, self.borderColor, self.activeColor), drawData={"replaceSplashText": False}, textData={"alignText": "left", "fontSize": 30}, inputData={"splashText": "Password: ", "charLimit": 50, "allowedKeysFile": "passwordKeys.txt"}, lists=[])
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


class NavItem(Button):
	def __init__(self, index, text, action=None):
		self.index = index
		self.text = text
		self.action = action

	def Create(self, rect, colors, onClick, text="", name=""):
		super().__init__(rect, colors, onClick=onClick, text=text, name=name, textData={"multiline": True if "\n" in text else False, "fontSize": 20, "alignText": "top" if "\n" in text else "center"}, lists=[])


class NavigationMenu:
	def __init__(self, rect, colors, navItems=[]):
		self.rect = pg.Rect(rect)

		self.backgroundColor = colors[0]
		self.borderColor = colors[1]

		self.navItems = navItems
		self.CreateNavItems()

	def CreateNavItems(self):
		xCounter = 0
		yCounter = 0
		for item in self.navItems:

			if item.index % 5 == 0 and item.index != 0:
				xCounter = 0
				yCounter += 1

			rect = ((xCounter * (self.rect.w // 5) + 3), self.rect.y + (6 * (yCounter + 1)) + (yCounter * 68), (self.rect.w // 5) - 6, 68)

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


class DetailsPage:
	def __init__(self, rect, colors, titleText="", messageText="", messageBoxRect=None):
		self.rect = pg.Rect(rect)
		self.backgroundColor = colors[0]
		self.borderColor = colors[1]

		self.title = Label((self.rect.x + 30, self.rect.y + 10, self.rect.w - 60, self.rect.h // 2 - 120), (self.backgroundColor, self.borderColor), text=titleText, textData={"fontSize": 70}, lists=[])
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
			self.UpdateMessage("Username or password is not filled.")


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


class Customer(Label):
	def __init__(self, rect, colors, name, balance, ID):
		super().__init__(rect, colors, f"Name:{name}\nBal:{balance}\nID:{ID}", textData={"multiline": True, "alignText": "left-top", "fontSize": 15}, lists=[])


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


def Back():
	global navPage
	navPage = prevPage


def DrawLoop():
	screen.fill(darkGray)

	if navPage == "Login page":
		login.Draw()
		createUserButton.Draw()
	elif navPage == "User details":
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

	DrawAllGUIObjects()

	pg.display.update()


def HandleEvents(event):
	HandleGui(event)

	if navPage == "Login page":
		login.HandleEvent(event)
		createUserButton.HandleEvent(event)
	elif navPage == "User details":
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


exit = Button((width - 210, height - 60, 200, 50), (lightBlack, darkWhite, lightBlue), onClick=Quit, text="Quit")

back = Button((width - 420, height - 60, 200, 50), (lightBlack, darkWhite, lightBlue), onClick=Back, text="Back", lists=[])


login = Login((10, 100, width - 20, 400), (lightBlack, darkWhite, lightBlue, darkWhite))
createUserButton = Button((width - 410, height - 200, 400, 50), (lightBlack, darkWhite, lightBlue), onClick=NewUserPage, text="Create new user", lists=[])
createUserPage = CreateUserPage((10, 100, width - 20, 400), (lightBlack, darkWhite, lightBlue), "Create new user", "Please enter a user name and password.", userInputData={"splashText": "User name: ", "charLimit": 50, "allowedKeysFile": "userNameKeys.txt"}, passwordInputData={"splashText": "Password: ", "charLimit": 50, "allowedKeysFile": "passwordKeys.txt"})


createCustomerPage = CreateCustomerPage((10, 180, width - 20, 400), (lightBlack, darkWhite, lightBlue), "Create new customer", "Please enter a name and balance.", nameInputData={"splashText": "Customer name:", "charLimit": 50, "allowedKeysFile": "userNameKeys.txt"}, balanceInputData={"splashText": "Balance: £", "charLimit": 50, "allowedKeysFile": "numberKeys.txt"})
customerBrowserPage = CustomerBrowserPage((10, 180, width - 20, 400), (lightBlack, darkWhite, lightBlue), "Choose a customer", inputData={"splashText": "ID: ", "charLimit": 3, "allowedKeysFile": "numberKeys.txt"})


navs = [NavItem(0, "Log out", login.LogoutUser), NavItem(1, "Get user\ndetails", UserDetailsPage), NavItem(2, "Edit user\nname", EditUserNamePage), NavItem(3, "Edit user\npassword", EditPasswordPage), NavItem(4, "New customer", NewCustomerPage), NavItem(5, "Change current\ncustomer", ChangeCurrentCustomerPage), NavItem(6, "Customer details", CustomerDetailsPage), NavItem(7, "Edit customer\nname", EditCustomerNamePage), NavItem(8, "Edit customer\nbalance", EditCustomerBalancePage), NavItem(9, "Delete current\nuser", createCustomerPage.DeleteCustomer)]
navMenu = NavigationMenu((0, 0, width, 160), (lightBlack, darkWhite), navs)


userDetailsPage = DetailsPage((10, 180, width - 20, 400), (lightBlack, darkWhite), "Your details")
deleteAccount = Button((width - 430, height - 210, 400, 50), (lightBlack, darkWhite, lightBlue), onClick=login.DeleteUser, text="Delete account", lists=[])


customerDetailsPage = DetailsPage((10, 180, width - 20, 400), (lightBlack, darkWhite), "Customer details")


userNameEditPage = EditPage((10, 180, width - 20, 400), (lightBlack, darkWhite, lightBlue), "Edit user name", action=login.ChangeUserName, inputData={"splashText": "New user name: ", "charLimit": 50, "allowedKeysFile": "userNameKeys.txt"})
userPasswordPage = EditPage((10, 180, width - 20, 400), (lightBlack, darkWhite, lightBlue), "Edit password", action=login.ChangePassword, inputData={"splashText": "New password: ", "charLimit": 50, "allowedKeysFile": "passwordKeys.txt"})


customerNameEditPage = EditPage((10, 180, width - 20, 400), (lightBlack, darkWhite, lightBlue), "Edit customer name", action=createCustomerPage.ChangeName, inputData={"splashText": "New customer name: ", "charLimit": 50, "allowedKeysFile": "userNameKeys.txt"})
customerBalancePage = EditPage((10, 180, width - 20, 400), (lightBlack, darkWhite, lightBlue), "Edit customer balance", action=createCustomerPage.ChangeBalance, inputData={"splashText": "New customer balance: £", "charLimit": 50, "allowedKeysFile": "numberKeys.txt"})


while running:
	clock.tick_busy_loop(fps)
	deltaTime = clock.get_time()
	for event in pg.event.get():
		if event.type == pg.QUIT:
			Quit()

		HandleEvents(event)

	DrawLoop()


