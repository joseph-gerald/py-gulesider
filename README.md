# py-gulesider
Python api to fetch data from gulesider

> [!IMPORTANT]
> This project will most likely not be maintained and will break over time

> [!NOTE]
> Code open-sourced from the private repo for [api.jooo.tech](https://api.jooo.tech/)

### Screenshot
![image](https://github.com/joseph-gerald/py-gulesider/assets/73967013/a7f9a398-e3e9-489e-bae6-9b22e9e68415)

## Example (examples.py)
```py
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
pages = gule_sider.search("Benk Moe", False)

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
Information (Benk Moe):
-------------------------------------------------------
FLN : Benk Moe
TLF : 947 85 488
DOB : 1999-11-16
ADR : Langskårveien 131 7100 Rissa
-------------------------------------------------------
Address Information (Langskårveien 131 7100 Rissa):
-------------------------------------------------------
LAT 63.5554934, LON 9.9382168

Tenants (3):

FLN : Parisa Moe
TLF : 474 85 388

FLN : Benk Moe ~TARGET~
TLF : 947 85 488

FLN : Terje Olav Moe
TLF : 416 95 104
-------------------------------------------------------
"""
```
