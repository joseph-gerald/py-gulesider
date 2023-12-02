from api.gulesider import GuleSider
from colorama import init, Fore

yellow = Fore.LIGHTYELLOW_EX
red = Fore.LIGHTRED_EX
dark_red = Fore.BLACK
green = Fore.GREEN
lyellow = Fore.LIGHTYELLOW_EX
cyan = Fore.LIGHTCYAN_EX
blue = Fore.LIGHTBLUE_EX
gray = Fore.LIGHTBLACK_EX
white = Fore.LIGHTWHITE_EX
magenta = Fore.LIGHTMAGENTA_EX
reset = Fore.RESET

gule_sider = GuleSider()
pages = gule_sider.search("Arad Asgari", False)

def display_info(person):
    if (person.birth_date == None): return
    print(f"{gray}-------------------------------------------------------")
    print(f"{blue}Information {gray}({cyan}{person.full_name}{gray}):")
    print("-------------------------------------------------------")
    print(f"{red}FLN{reset} : " + person.full_name)
    print(f"{red}TLF{reset} : " + person.primary_number)
    print(f"{red}DOB{reset} : " + person.birth_date)
    if(person.no_address):return
    print(f"{red}ADR{reset} : " + person.full_address)

    address_dict = person.addresses[0]

    if(person.no_full_address):
        print(f"{dark_red}ERROR: {red}NO ADDRESS")
        return

    tenants = gule_sider.search_address(person.full_address)

    print(f"{gray}-------------------------------------------------------")
    print(f"{blue}Address Information {gray}({cyan}{person.full_address}{gray}):")
    print(f"{gray}-------------------------------------------------------")
    print(f"{red}LAT{reset} {str(address_dict['coordinates'][0]['lat'])}, {red}LON{reset} {str(address_dict['coordinates'][0]['lon'])}")

    print()

    print(f"{blue}Tenants {gray}({cyan}{len(tenants)}{gray}){reset}:")

    for tenant in tenants:
        print()
        print(f"{red}FLN{reset} : " + tenant.name + (f"{yellow} ~TARGET~" if tenant.name == person.full_name else ""))
        print(f"{red}TLF{reset} : " + tenant.phone_number[0])
    print(f"{gray}-------------------------------------------------------")

person = pages[0].persons[0];

display_info(person)

"""
-------------------------------------------------------
Information (Arad Aghalo Asgari):
-------------------------------------------------------
FLN : Arad Aghalo Asgari
TLF : 480 55 039
DOB : 2002-09-30
ADR : Hampengen 34A 1391 Vollen
-------------------------------------------------------
Address Information (Hampengen 34A 1391 Vollen):       
-------------------------------------------------------
LAT 59.7870002, LON 10.4859251

Tenants (3):

FLN : Farzaneh Aghlo
TLF : 977 55 926

FLN : Reza Asgari
TLF : 66 78 59 59

FLN : Arad Aghalo Asgari ~TARGET~
TLF : 480 55 039
-------------------------------------------------------
"""