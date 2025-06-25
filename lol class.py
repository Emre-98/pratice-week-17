class Champion:

    def __init__(self, type, location, name):
        self.type = type
        self.location = location
        self.name = name
        

    def print_champion(self):
        print(self.name, self.type, self.location)


    
    
    

champion_annie = Champion(
    type = "mage",
    location = "midlaner",
    name = "Annie"
)

champion_veigar = Champion(
    type = "mage",
    location = "midlaner",
    name = "Veigar"
)

champion_Sett = Champion(
    type = "fighter",
    location = "toplaner",
    name = "Sett"
)

champion_Aphelios = Champion(
    type = "ADC",
    location = "Botlaner",
    name = "Aphelios"    
)

# champion_Aphelios.print_champion()
# champion_annie.print_champion()
# champion_Sett.print_champion()
# champion_veigar.print_champion()

champion_list = [champion_Aphelios, champion_annie, champion_Sett, champion_veigar]

for champion in champion_list:
    champion.print_champion()



# print(champion_annie.type, champion_annie.location, champion_annie.name , champion_veigar.type)
# print(champion_Sett.type, champion_Sett.location, champion_Sett.name)
# print(champion_Aphelios.name, champion_Aphelios.location, champion_Aphelios.type)