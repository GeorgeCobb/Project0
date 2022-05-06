import pymongo as pm
import pprint as pp
import datetime

def Menu():
	x = input(" 1 for Orders "
		  "\n 2 for Customers"
		  "\n 3 for Ingredients"
		  "\n 4 for Recipes"
		  "\n 5 for items"
		  "\n x for exit\n")
	if x == "1":
		Orders()
	elif x == "2":
		Customers()
	elif x == "3":
		Ingredients()
	elif x == "4":
		Recipes()
	elif x == "5":
		Items()
	elif x.lower() == "x":
		quit
	else:
		print("Incorrect Input")
		Menu()

def Updating(T_Name, E_Name, E_Value, query):
		Table = db[T_Name]
		NewV = {"$set": {E_Name: E_Value}}
		Table.update_one(query, NewV)

def Reload(T_Name):
	Table = db[T_Name]
	Row = Table.find_one({},{"_id": 0})
	NumberC = str(Row).split(",")
	NumberC = len(NumberC)
	for d in Table.find({},{"_id":0}).limit(10):
		print(d)

def Deleting(E_Name, ID, T_Name):
	Table = db[T_Name]
	sure = input("Are you sure you want to delete this yes (y) or no (n): ")
	if sure.lower() == "y":
		# delete from given table where FK ID equals ID
		query = {E_Name: int(ID)}
		Table.delete_one(query)
		print("Deleted")
		return "Deleted"
	else:
		return " "

def Deleting3(E_Name, F_Name, ID, FKID, T_Name):
	Table = db[T_Name]
	sure = input("Are you sure you want to delete this yes (y) or no (n): ")
	if sure.lower() == "y":
		# delete from given table where FK ID equals FKID and FK2ID = ID or something like that
		query = {"$and":[{E_Name: int(ID)},{F_Name: int(FKID)}]}
		Table.delete_one(query)
		print("Deleted")
		return "Deleted"
	else:
		return " "
def Orders():
	Orders = db["Orders"]
	OI = db["Ordered_Items"]
	Cust = db["Customers"]
	Item = db["Items"]
	x = " "
	Item_ID = " "
	while x.lower() != "x":
		count = Orders.count_documents({})
		if count > 0:
			Max = Orders.find_one({},sort=[("Order_ID",pm.DESCENDING)])
			s1=str(Max).split(",")
			s2 = s1[1].split(" ")
			nextid = int(s2[2])
		else:
			nextid = 0
		#List orders
		for d in Orders.find({},{"_id":0}).limit(10):
			d1 = str(d).split(" ")
			#Grabs Customer ID
			Cust_ID = d1[3]
			size = len(Cust_ID)
			Cust_ID = Cust_ID[0:size-1]
			#Finds the Name
			Customer = Cust.find_one({"Cust_ID": int(Cust_ID)},{"_id": 0})
			name = str(Customer).split(" ")
			F_name = name[3]
			F_size = len(F_name)
			F_name = F_name[1:F_size-2]
			L_name = name[5]
			L_size = len(L_name)
			L_name = L_name[1:L_size-2]
			#Grabs Order ID
			Order_ID = d1[1]
			size = len(Order_ID)
			Order_ID = Order_ID[0:size-1]
			#Print Order Table with Customer Name
			print(str(d)+" Customer Name: "+ F_name+ " "+ L_name)
			#Grabs Order_Item Table Based on Order ID
			for i in OI.find({"Order_ID": int(Order_ID)}, {"_id": 0}):
				i1 = str(i).split(",")
				#Grab Item ID
				Item_ID = i1[1]
				Item_ID = Item_ID.split(" ")
				Item_ID = Item_ID[2]
				#print("Item ID: "+Item_ID)
				size = len(Item_ID)
				Item_ID = Item_ID[0:size-1]
				ItemName = Item.find_one({"Item_ID": int(Item_ID)}, {"_id": 0})
				Item_Name = str(ItemName).split(",")
				Item_Name = Item_Name[3]
				Item_Name = Item_Name.split(":")
				Item_Name = Item_Name[1]
				size = len(Item_Name)
				Item_Name = Item_Name[0:size-1]
				print("\t"+str(i) + ", Item Name"+ Item_Name)
		x = input("New (n), Updating (u) or Deleting (d) if done enter x: ")
		if x.lower() == "n":
			Cust_ID = input("Enter Customer ID: ")
			nextid = nextid + 1
			#insert this and current time to order table and get order_ID
			date = datetime.datetime.now()
			print(date)
			insert = {"Order_ID": nextid,
				  "Cust_ID": int(Cust_ID),
				  "Date": date}
			Orders.insert_one(insert)
			Reload("Orders")
			Reload("Items")
			Item_ID = " "
			while Item_ID.lower() != "x":
				Item_ID = input("Enter Item ID or x if done: ")
				if Item_ID.lower() != "x":
					#insert into order_item talbe using order_id as FK
					Oinsert = {"Order_ID": nextid,
						   "Item_ID":  int(Item_ID)}
					OI.insert_one(Oinsert)
				else:
					x = input("New (n), Updating (u), or Deleting (d) if done enter x: ")
		if x.lower() == "u":
			Order_ID = input("Enter Order ID: ")
			AU = input("Adding (a), Deleteing (d), or Customer ID (c) exit with (x): ")
			Reload("Items")
			if AU.lower() ==  "a":
				while Item_ID.lower() != "x":
					Item_ID = input("Enter Item ID or x if done: ")
					if Item_ID.lower() != "x" or Item_ID != "":
						#insert into order_item table using order_id as FK
						Oinsert = {"Order_ID": int(Order_ID),
							   "Item_ID":  int(Item_ID)}
						OI.insert_one(Oinsert)
			if AU.lower() ==  "d":
				Item_ID = " "
				while Item_ID.lower() != "x":
					Item_ID = input("Enter Item ID or x if done: ")
					if Item_ID != "x" or Item_ID != "":
						Deleting3("Item_ID","Order_ID",Item_ID,Order_ID,"Order_Items")
		if x.lower() == "d":
			Order_ID = input("Enter Order ID: ")
			Deleteing("Order_ID", Order_ID, "Order_Items")
			Deleteing("Order_ID", Order_ID, "Orders")
		#if x.lower() == "s":
		elif x.lower() == "x":
			Menu()
		else:
			print("unknown input")
def Customers():
	Cust = db["Customers"]
	x = " "
	Reload("Customers")
	while x.lower() != "x":
		count = Cust.count_documents({})
		if count > 0:
			Max = Cust.find_one({},sort=[("Cust_ID",pm.DESCENDING)])
			s1=str(Max).split(",")
			s2 = s1[1].split(" ")
			nextid = int(s2[2])
		else:
			nextid = 0

		x = input("New (n), Updating (u), or Deleting (d) if done enter x: ")
		if x.lower() == "n":
			Cust_Name = input("Enter Customer Name FL: ")
			name = Cust_Name.split(" ")
			nextid = nextid + 1
			#name[0] will be fname name[1] will be lname
			#Cust_number = input("Enter PhoneNumber: ")
			#Cust_Address = input("Enter Address: ")
			#insert into Customers table
			insert = {"Cust_ID":nextid,
				  "F_name": name[0],
				  "L_name": name[1]}
			Cust.insert_one(insert)
			Reload("Customers")
		elif x.lower() == "u":
			Cust_ID = input("Enter Customer ID: ")
			query = {"Cust_ID": int(Cust_ID)}
			print("Enter a new value or leave blank if not changing")
			Cust_Name = input("Enter Customer Name FL: ")
			if Cust_Name != "":
				name = Cust_Name.split(" ")
				Updating("Customers", "F_name", name[0], query)
				Updating("Customers", "L_name", name[1], query)
			#Cust_number = input("Enter PhoneNumber: ")
			#Cust_Address = input("Enter Address: ")
			#update row based on cust_id
			Reload("Customers")
		elif x.lower() == "d":
			Cust_ID = input("Enter Customer ID ")
			Deleting("Cust_ID", Cust_ID, "Customers")
			Reload("Customers")
		elif x.lower() == "x":
			Menu()
		else:
			print("unknown input")
def Ingredients():
	Ing = db["Ingredients"]
	x = " "
	Reload("Ingredients")
	while x.lower() != "x":
		count = Ing.count_documents({})
		if count > 0:
			Max = Ing.find_one({},sort=[("Ing_ID",pm.DESCENDING)])
			s1=str(Max).split(",")
			s2 = s1[1].split(" ")
			nextid = int(s2[2])
		else:
			nextid = 0
		x = input("New (n), Adding (a), Subtracting (s), or Deleting (d) if done enter x: ")
		if x.lower() == "n":
			nextid = nextid + 1
			Ing_name = input("Enter Name: ")
			Ing_quantity = input("Enter quantity: ")
			# insert new Ingredient into Ingredients table
			insert = {"Ing_ID": nextid,
				  "Name": Ing_name,
				  "Quantity": int(Ing_quantity)}
			Ing.insert_one(insert)
			Reload("Ingredients")
		elif x.lower() == "a":
			Ing_ID = input("Ender ID: ")
			Ing_quantity = input("Enter quatity being added or x to exit: ")
			# update Ingrediens table using 
			if x.lower() != "x":
				s1 = str(Ing.find_one({"Ing_ID": int(Ing_ID)})).split(",")
				s2 = s1[3].split(" ")
				s3 = s2[2]
				size = len(s3)
				CurrentA = s3[0:size-1]
				Sum = int(CurrentA) + int(Ing_quantity)
				query = {"Ing_ID": int(Ing_ID)}
				newV = {"$set": {"Quantity": Sum}}
				Ing.update_one(query, newV)
				Reload("Ingredients")
		elif x.lower() == "s":
			Ing_ID = input("Ender ID: ")
			Ing_quantity = input("Enter quatity being subtracted or x to exit: ")
			# update Ingrediens table using
			if x.lower() != "x":
				s1 = str(Ing.find_one({"Ing_ID": int(Ing_ID)})).split(",")
				s2 = s1[3].split(" ")
				s3 = s2[2]
				size = len(s3)
				CurrentA = s3[0:size-1]
				Sum = int(CurrentA) - int(Ing_quantity)
				query = {"Ing_ID": int(Ing_ID)}
				newV = {"$set": {"Quantity": Sum}}
				Ing.update_one(query, newV)
				Reload("Ingredients")
		elif x.lower() == "d":
			Ing_ID = input("Enter ID of the ingredient you want to delete: ")
			Deleting("Ing_ID", Ing_ID, "Ingredients")
			Reload("Ingredients")
		elif x.lower() == "x":
			Menu()
		else:
			print("unknown input")
def Recipes():
	Rec = db["Recipes"]
	Am = db["Amounts"]
	Ing = db["Ingredients"]
	x = " "
	while x.lower() != "x":
		count = Rec.count_documents({})
		if count > 0:
			Max = Rec.find_one({},sort=[("RED_ID",pm.DESCENDING)])
			s1=str(Max).split(",")
			s2 = s1[1].split(" ")
			nextid = int(s2[2])
		else:
			nextid = 0
		#Shows Table
		#Reload("Recipes")
		for d in Rec.find({},{"_id":0}).limit(10):
			print(d)
		x = input("New (n), Update (u), Deleting (d), or Seeing Ingredients (i) if done enter x: ")
		if x.lower() == "i":
			Rec_ID = input("Enter ID of recipe: ")
			for d in Am.find({"Rec_ID": int(Rec_ID)},{"_id": 0}):
				Ing_ID = str(d).split(" ")
				size = len(Ing_ID[3])
				Ing_ID = Ing_ID[3][0:size-1]
				Name = Ing.find_one({"Ing_ID": int(Ing_ID)},{"_id": 0, "Name": 1})
				Name = str(Name).split(":")
				size =  len(Name[1])
				Name = Name[1][2:size-2]
				print(str(d)+" Ingredient Name: "+str(Name))
		elif x.lower() == "n":
			nextid = nextid + 1
			Rec_Name = input("Enter recipe name: ")
			Rec_Disc = input("Enter recipe discription: ")
			Baking_Time = input("Enter baking time: ")
			Baking_Heat = input("Enter Baking Heat: ")
			How_Many = input ("Enter how many are made per recipe: ")
			# insert into Recipes
			insert = {"Rec_ID": nextid,
				  "Rec_Name": Rec_Name,
				  "Rec_Disc": Rec_Disc,
				  "Baking_Time": Baking_Time,
				  "Backing_Heat": Baking_Heat,
				  "How_Many": How_Many}
			Rec.insert_one(insert)
			#Amounts
			Reload("Ingredients")
			Ing_ID = " "
			while Ing_ID.lower() != "x":
				Ing_ID = input("Enter item ID if done enter x: ")
				if Ing_ID.lower() != "x":
					Amount = input("Enter Amount need: ")
					#insert into Amounts table with highest Rec_ID
					Ainsert = {"Rec_ID": nextid,
						   "Ing_ID": int(Ing_ID),
						   "Amount": float(Amount)}
					Am.insert_one(Ainsert)
		elif x.lower() == "u":
			What = input("Are you udating the Ingredients yes (y) or no (n) if done enter x: ")
			#Updating Recipes Table
			if  What.lower() == "n":
				Rec_ID = input("Enter recipe ID: ")
				query = {"Rec_ID": int(Rec_ID)}
				print("Enter a new value or leave blank if not changing")
				Rec_Name = input("Enter recipe name: ")
				if Rec_Name != "":
					Updating("Recipes", "Rec_Name", Rec_Name, query)
				Rec_Disc = input("Enter recipe discription: ")
				if Rec_Disc != "":
					Updating("Recipes", "Rec_Disc", Rec_Disc, query)
				Baking_Time = input("Enter baking time: ")
				if Baking_Time != "":
					Updating("Recipes", "Baking_Time", Baking_Time, query)
				Baking_Heat = input("Enter baking heat: ")
				if Baking_Heat != "":
					Updating("Recipes", "Baking_Heat", Baking_Heat, query)
				How_Many = input ("Enter how many are made: ")
				if How_Many != "":
					Updating("Recipes", "How_Many", How_Many, query)
			#Updating Amounts Table
			elif What.lower() == "y":
				Q = input("Adding (a) a new ingredient or updating (u) existing one: ")
				Reload("Amounts")
				Reload("Ingredients")
				Rec_ID = input("Enter recipe ID: ")
				if Q.lower() == "u":
					Ing_ID = " "
					while Ing_ID.lower() != "x":
						Ing_ID = input("Enter ingredient ID if done enter x: ")
						if Ing_ID.lower() != "x":
							Amount = input("Enter Amount need: ")
							#update Amounts Based on Ing_ID and Rec_ID
							query = {"$and": [{"Rec_ID": int(Rec_ID)},{"Ing_ID": int(Ing_ID)}]}
							newV = {"$set": {"Amount": float(Amount)}}
							Am.update_one(query, newV)
						else:
							x = input("New (n), Update (u), or Deleting (d) if done enter x: ")
				elif Q.lower() == "a":
					Ing_ID = " "
					while Ing_ID.lower() != "x":
						Ing_ID = input("Enter item ID if done enter x: ")
						if Ing_ID.lower() != "x":
							Amount = input("Enter Amount need: ")
							#insert into Amounts table with highest Rec_ID
							Ainsert = {"Rec_ID": int(Rec_ID),
								   "Ing_ID": int(Ing_ID),
								   "Amount": float(Amount)}
							Am.insert_one(Ainsert)
						else:
							x = input("New (n), Update (u), or Deleting (d) if done enter x: ")
		elif x.lower() == "d":
			Rec_ID = input("Enter recipe ID: ")
			Deleting("Rec_ID",Rec_ID, "Amounts")
			Deleting("Rec_ID",Rec_ID, "Recipes")
		elif x.lower() == "x":
			Menu()
		else:
			print("unknown input")
def Items():
	Items  = db["Items"]
	x = " "
	Reload("Items")
	while x.lower() != "x":
		count = Items.count_documents({})
		if count > 0:
			Max = Items.find_one({},sort=[("Cust_ID",pm.DESCENDING)])
			s1=str(Max).split(",")
			s2 = s1[1].split(" ")
			nextid = int(s2[2])
		else:
			nextid = 0
		x = input("New (n), Update (u), or Deleting (d) if done enter x: ")
		if x.lower() == "n":
			nextid = nextid  + 1
			Item_Name = input("Enter item name: ")
			Item_Disc = input("Enter item disc: ")
			Item_Price = input("Enter item price: ")
			insert = {"Item_ID": nextid,
				  "Item_Name": Item_Name,
				  "Item_Disc": Item_Disc,
				  "Item_Price": float(Item_Price)}
			Items.insert_one(insert)
			Reload("Items")
		if x.lower() == "u":
			Item_ID = input("Enter item ID: ")
			Item_Name = input("Enter item name: ")
			Item_Disc = input("Enter item disc: ")
			Item_Price = input("Enter item price: ")
			#update based off Item_ID
			query = { "Item_ID": int(Item_ID) }
			newV  = {"$set": {"Item_Name": Item_Name,
					  "Item_Disc": Item_Disc,
					  "Item_Price": float(Item_Price)}}
			Items.update_one(query, newV)
			Reload("Items")
		if x.lower() == "d":
			Item_ID = input("Enter item ID: ")
			Deleting("Item_ID", Item_ID, "Items")
			Reload("Items")
		elif x.lower() == "x":
			Menu()
		else:
			print("unknown input")
def main():
	Menu()

if __name__ == "__main__":
	client = pm.MongoClient('mongodb://localhost:27017/')
	db = client.Bakery
	main()
