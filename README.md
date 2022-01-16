# ShopifyChallenge2022
This is the Shopify challenge in order to apply to Shopify's 2022 summer internships :)
To be honest, I'm not quite experienced in front-end and combining front and back-end, so this is my first attempt and I've learned a lot! Hopefully it meets your expectations :)

## Setup
You will need python for this. A Python 3+ version is required.

All of the setup will be located in the **backend** folder.

First, for either Linux or Windows you need to make a virtual environment. This can be done with the command ```python -m venv venv``` OR ```python3 -m venv venv```. After this, you'll need to install the requirements. You can do this by first activating the virtual environment by ```source venv/Script/activate```, then ```pip install -r requirements.txt``` or ```pip3 install -r requirements.txt```. You may exit the virtual environment after this.

If the db file provided doesn't work, you can delete the file and then do: ```python```, followed by ```from application import db```, then ```db.create_all()``` and exit. (Note: the database will be empty if this is needed.) (Also, in some cases you may need to do python3 or python -i or python3 -i for it to work.)

## Running the Server
To run the server after the setup, you can use the bash scripts I have provided. Either ```./windows.sh``` on windows or ```./linux.sh``` on linux. It will automatically run the virtual environment and setup everything, then proceed to run the server.

In order to access the site, you must have the server running at the same time. Go to the **front-end** folder and open the html file to access the site.

## Site Features

### Displaying the list of Inventory
When first booting up the site, the current inventory will already be loaded. Doing anything else, such as editing/deleting/adding will automatically update the list with the new update.

![image](https://user-images.githubusercontent.com/54968420/149679959-5dd97717-ce91-425f-a389-3d0cdde4f0f5.png)

### Adding an item
To add an item, you must have a name and the amount for the item. The description can be left empty, which will give you an empty string description. Name and amount are mandatory, however. After filling in the name, description, and amount, you hit the add item button in order to add the item to the list. (There is no autoclear so far, so you'll have to manually clear the fields)

![image](https://user-images.githubusercontent.com/54968420/149680078-5d0746ad-4c81-40bc-a229-5c2e7590b789.png)
![image](https://user-images.githubusercontent.com/54968420/149680087-b841655c-3459-4130-bcff-454c8d021dfc.png)

### Editing an item
To edit an item, you must have the ID of the item (from the table). After, you need to have at least one of the name/description/amount fields filled. Following this you can hit the edit button in order to change the field that you requested.

![image](https://user-images.githubusercontent.com/54968420/149680127-9d678f79-f85a-4f8e-a83a-79e3112eefe0.png)
![image](https://user-images.githubusercontent.com/54968420/149680133-4163246e-55a0-48c9-8fd8-a37c0cce9804.png)

### Deleting an item
To delete an item, all you need is the ID of the item. After you input the ID, you hit the delete item button and it'll disappear from the list.

![image](https://user-images.githubusercontent.com/54968420/149680150-cfe03f46-46bd-4183-bf4c-7e6e553588cb.png)
![image](https://user-images.githubusercontent.com/54968420/149680156-a69cf03b-6fce-4834-8d7f-c42b531fbbf4.png)

### Exporting Data
To export data, you press the ```Export Data``` button to download a text file. This text file will be in CVS form, with ID, name, description, amount in that order. These values will just be taken straight from the table.

![image](https://user-images.githubusercontent.com/54968420/149680199-e7284edd-1ca0-4343-beb0-84507107e240.png)
