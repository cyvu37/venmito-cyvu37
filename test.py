"""
Always end test code with `exit()`.
"""






"""from platform import system
dict_od = { "Windows": "explorer", "Darwin": "open" }
print(system() in dict_od)
print(system() in dict_od.keys())
exit()"""


'''import contextlib
import json
import time
from pathlib import Path
from rich.console import Console
from rich.live import Live
from rich.table import Table

console = Console()

def make_table(coin_list):
    """Generate a Rich table from a list of coins"""
    table = Table(
        title=f"Crypto Data - {time.asctime()}",
        style="black on grey66",
        header_style="white on dark_blue",
    )
    table.add_column("Symbol")
    table.add_column("Name", width=30)
    table.add_column("Price (USD)", justify="right")
    table.add_column("Volume (24h)", justify="right", width=16)
    table.add_column("Percent Change (7d)", justify="right", width=8)
    for coin in coin_list:
        symbol, name, price, volume, pct_change = (
            coin["symbol"],
            coin["name"],
            coin["price_usd"],
            f"{coin['volume24']:.2f}",
            float(coin["percent_change_7d"]),
        )
        pct_change_str = f"{pct_change:2.1f}%"
        if pct_change > 5.0:
            pct_change_str = f"[white on dark_green]{pct_change_str:>8}[/]"
        elif pct_change < -5.0:
            pct_change_str = f"[white on red]{pct_change_str:>8}[/]"
        table.add_row(symbol, name, price, volume, pct_change_str)
    return table

# Load the coins data
raw_data = json.loads(Path("C://Users//jared//Downloadscrypto_data.json").read_text(encoding="utf-8"))
num_coins = len(raw_data)
coins = raw_data + raw_data
num_lines = 20

with Live(make_table(coins[:num_lines]), screen=True) as live:
    index = 0
    with contextlib.suppress(KeyboardInterrupt):
        while True:
            live.update(make_table(coins[index : index + num_lines]))
            time.sleep(0.5)
            index = (index + 1) % num_coins'''



'''
#
# FUNCTION ARCHIVE 
#
        
        def func_help_OLD( self ):
            """
            Present help menu.
            """
            self.b_change_lH = False
            CONSOLE.print(f"\n\n{R_LINE}\n")
            CONSOLE.print(R_HELP_MENU)
            while True:
                self.b_change_lH = self._func_msg_bubble_OLD( self.b_change_lH,
                                                         "Read the HELP MENU above. Take action with the HELP DESK below." )
                CONSOLE.print(R_HELP_DESK)
                i = CONSOLE.input(fcolor("> ", C))
                match i:
                    case "g" | "github":
                        try:
                            open_new_tab( "https://github.com/cyvu37/venmito-cyvu37" )
                            self.b_change_lH = False
                            break
                        except:
                            self.b_change_lH = True
                            self.bubble_txt = "Couldn't open GitHub."
                            self.bubble_sty = "bold red"
                    case "p" | "prev":
                        break
                    case "q" | "quit":
                        self._func_quit()
                    case "":
                        self.b_change_lH = True
                        self.bubble_txt = "No input. Try again."
                        self.bubble_sty = "bold yellow"
                    case _:
                        self.b_change_lH = True
                        self.bubble_txt = "Invalid input. Try again."
                        self.bubble_sty = "bold yellow"
            CONSOLE.print(f"\n\n{R_LINE}\n")
        
            

        def _func_msg_bubble_OLD( self, b_change: bool = True, default_msg: str = None ):
            """Template to make the message bubble.

            Args:
                b_change (bool, optional): Internal boolean tracking deviation from default message. Defaults to True.
                default_msg (str, optional): The default message. Defaults to "".
            """
            if not b_change:
                self.bubble_txt = default_msg
                self.bubble_sty = C
            CONSOLE.print("\n")
            CONSOLE.print( Panel(
                Text( self.bubble_txt, justify="center", style=self.bubble_sty ), 
                title=Text( "VE Status", style=Style(italic=True, color=self.bubble_sty) ),
                width=WIDTH, border_style=self.bubble_sty
            ) )
            CONSOLE.print("\n")
            return False # Revert back to default message.


        
        def func_l1_menu_loop_v1( self ):
            """
            Loop to allow user to keep using this program after finishing a task.

            The Level 1 command for nested loop handling.
            """
            self.b_change_l1 = False
            """Must the default message be changed or not, including errors?"""
            while True:
                self.b_change_l1 = self._func_msg_bubble_v1( self.b_change_l1, "What would you like to do?" )
                CONSOLE.print(R_MENU)
                self.i_menu = CONSOLE.input("> ").lower()
                match self.i_menu:
                    case "1":
                        self.func_l2_t1_1report()
                    case "2":
                        self.func_l2_input_t2_v1()
                    case "3":
                        self.b_change_l1 = True
                        self.bubble_txt = f"{D_MENU[self.i_menu]}: Under construction. No DeepSeek model available yet."
                        self.bubble_sty = "bold orange1"
                    case "h" | "help":
                        self.func_help_v1()
                    case "q" | "quit":
                        self._func_quit()
                    case "":
                        self.b_change_l1 = True
                        self.bubble_txt = "No input. Try again."
                        self.bubble_sty = "bold yellow"
                    case _:     # Error input.c
                        self.b_change_l1 = True
                        self.bubble_txt = "Invalid input. Try again."
                        self.bubble_sty = "bold yellow"

        
        def func_l2_input_t1_v1( self ):
            """
            Loop for Step 1 of Task 1: Prefab Reports
            > Step 1: Select Output type.
            > Step 2: Select HNR report.
            > Step 3: Select Input type. 
            
            A Level 2 command for nested loop handling.
            """
            self.b_change_l2 = False
            while True:
                self.b_change_l2 = self._func_msg_bubble_v1( self.b_change_l2, f"{prefab_abbr} Report, Step 1" )
                CONSOLE.print(R_OUTPUT)
                self.i_output = CONSOLE.input("> ").lower()
                if self.i_output in D_OUTPUT.keys():
                    self.func_l3_list_hnr_t1()
                else:
                    match self.i_output:
                        case "p" | "previous":
                            break
                        case "h" | "help":
                            self.func_help_v1()
                        case "q" | "quit":
                            self._func_quit()
                        case "":
                            self.b_change_l2 = True
                            self.bubble_txt = "No input. Try again."
                            self.bubble_sty = "bold yellow"
                        case _:
                            self.b_change_l2 = True
                            self.bubble_txt = "Invalid input. Try again."
                            self.bubble_sty = "bold yellow"
                self.i_output = ""


        
        def func_l2_input_t2_v1( self ):
            """
            Loop for getting input for Task 2: Create SQL Report
            > Step 1: Select Output type.
            > Step 2: Write SQL command. 

            A Level 2 command for nested loop handling.
            """
            self.b_change_l2 = False
            while True:
                self.b_change_l2 = self._func_msg_bubble_v1( self.b_change_l2, "SQL Report 1/2: Select your output type." )
                CONSOLE.print( R_OUTPUT )
                self.i_output = CONSOLE.input("> ").lower()
                if self.i_output in D_OUTPUT.keys():
                    ### DEV NOTE:
                    CONSOLE.print(fcolor("DEV NOTE: Not available yet. Applies to all such options.", "bold red"))
                else:
                    match self.i_output:
                        case "p" | "previous":
                            break
                        case "h" | "help":
                            self.func_help_v1()
                        case "q" | "quit":
                            self._func_quit()
                        case "":
                            self.b_change_l2 = True
                            self.bubble_txt = "No input. Try again."
                            self.bubble_sty = "bold yellow"
                        case _:
                            self.b_change_l2 = True
                            self.bubble_txt = "Invalid input. Try again."
                            self.bubble_sty = "bold yellow"


        
        def func_l3_list_hnr_t1_OLD( self ):
            """
            Loop for Step 2 of Task 1: Prefab Reports
            > Step 1: Select Output type.
            > Step 2: Select HNR report.
            > Step 3: Select Input type. 
            
            A Level 3 command for nested loop handling.
            """
            self.b_change_l3 = False
            while True:
                self.b_change_l3 = self._func_msg_bubble_OLD( self.b_change_l3, f"{prefab_abbr} Report, Step 2 | Output: {D_OUTPUT[self.i_output]}" )
                CONSOLE.print( R_PFR )
                self.i_pfr = CONSOLE.input("> ").lower()
                match self.i_pfr:
                    case "1":
                        self.func_l4_input_t1_OLD()
                    case "2":
                        self.func_l4_t1c2_view_store_products()
                        ### DEV NOTE: Dead end right now.
                        self.msg.update({
                            "bot": f"DEV NOTE | {D_OUTPUT[self.i_output]}: Under construction. Try [1].",
                            "bot_color": "orange1", "border_color": "orange1"
                            })
                    case "3":
                        self.func_l4_t1c3_view_transactions()
                        ### DEV NOTE: Dead end right now.
                        self.msg.update({
                            "bot": f"DEV NOTE | {D_OUTPUT[self.i_output]}: Under construction. Try [1].",
                            "bot_color": "orange1", "border_color": "orange1"
                            })
                    case "p" | "previous":
                        break
                    case "h" | "help":
                        self.func_help_OLD()
                    case "q" | "quit":
                        self._func_quit()
                    case "":
                        self.b_change_l3 = True
                        self.bubble_txt = "No input. Try again."
                        self.bubble_sty = "bold yellow"
                    case _:
                        self.b_change_l3 = True
                        self.bubble_txt = "Invalid input. Try again."
                        self.bubble_sty = "bold yellow"
                self.i_pfr = ""

        
        def func_l4_input_t1_OLD( self ):
            """
            Loop for Step 3 of Task 1: Prefab Reports
            > Step 1: Select Output type.
            > Step 2: Select HNR report.
            > Step 3: Select Input type. 
            
            A Level 4 command for nested loop handling.
            """
            self.b_change_l4 = False
            while True:
                self.b_change_l4 = self._func_msg_bubble_OLD( self.b_change_l4, 
                    f"{prefab_abbr} Report, Step 3 | Output: {D_OUTPUT[self.i_output]}; Report: {D_PFR[self.i_pfr]}"
                )
                CONSOLE.print( R_INPUT )
                self.i_input = CONSOLE.input("> ").lower()
                if self.i_input in D_INPUT:
                    ### DEV NOTE: This is when the processing starts.
                    CONSOLE.print(fcolor("DEV NOTE: Under construction. Applies to all such options.", "bold red"))
                else:
                    match self.i_input:
                        case "p" | "previous":
                            break
                        case "h" | "help":
                            self.func_help_OLD()
                        case "q" | "quit":
                            self._func_quit()
                        case "":
                            self.b_change_l4 = True
                            self.bubble_txt = "No input. Try again."
                            self.bubble_sty = "bold yellow"
                        case _:
                            self.b_change_l4 = True
                            self.bubble_txt = "Invalid input. Try again."
                            self.bubble_sty = "bold yellow"
'''




'''from rich import print
from rich.panel import Panel
from rich.text import Text
panel = Panel(Text("Hello", justify="right"), width=100)
print(panel)
exit()



from time import sleep
from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn
text_column = TextColumn("{task.description}", table_column=Column(ratio=1))
bar_column = BarColumn(bar_width=None, table_column=Column(ratio=2))
progress = Progress(text_column, bar_column, expand=True)
with progress:
    for n in progress.track(range(30)):
        progress.print(n)
        sleep(0.1)


import time
from rich.progress import Progress
with Progress() as progress:
    task1 = progress.add_task("[red]Downloading...", total=1000)
    task2 = progress.add_task("[green]Processing...", total=1000)
    task3 = progress.add_task("[cyan]Cooking...", total=1000)
    while not progress.finished:
        progress.update(task1, advance=0.5)
        progress.update(task2, advance=0.3)
        progress.update(task3, advance=0.9)
        time.sleep(0.02)



import time
from rich.progress import track
for i in track(range(20), description="Processing..."):
    time.sleep(1)  # Simulate work being done
'''

'''import os, pandas as pd
from time import time
from json import load as json_load

DIR_PROGRAM = os.getcwd()
DIR_DATA = os.path.join( DIR_PROGRAM, "data" )
DIR_PARENT = os.sep.join( DIR_PROGRAM.split(os.sep)[:-1] )
DIR_OUTPUT = os.path.join( DIR_PARENT, "Venmito Output" )

b_items = False
DJ = {}; dj = {}

# Method 1
t = time()
with open( os.path.join( DIR_DATA, "people.json" ), 'r' ) as f:
    DJ = pd.read_json(f)
DJ["id"] = DJ["id"].astype(int)
# Organize new columns.
DJ["phone"] = DJ["telephone"]
DJ["city"] = [ i["City"] for i in DJ["location"] ]
DJ["country"] = [ i["Country"] for i in DJ["location"] ]
DJ["has_android"] = [ "Android" in d for d in DJ["devices"] ]
DJ["has_iphone"] = [ "Iphone" in d for d in DJ["devices"] ]
DJ["has_desktop"] = [ "Desktop" in d for d in DJ["devices"] ]
# Drop irrelevant columns.
DJ = DJ.drop(columns=["telephone", "location", "devices"])
print(time() - t)
print(DJ)
# y = x/(1-%)
# x/y = 1-%
# Method 2
def func_process_people_json( input: dict ) -> dict:
    """
    Function to process all parts of `people.json`. FEATURE: Scalable for new exceptions!
    """
    output = {}
    #i2 = { k.lower():v for k, v in input.items() }
    for k, v in input.items():
        match k:
            case "id":
                output[k.lower()] = int(v)
            case "location":
                # Get `{'City': ..., 'Country': ...}`.
                output.update({ key.lower():value for key, value in v.items() })
            case "telephone":
                # Change "telephone" to "phone".
                output["phone"] = v
            case "devices":
                # Get `"devices": [...]`.
                output["has_android"] = "Android" in v
                output["has_iphone"] = "Iphone" in v
                output["has_desktop"] = "Desktop" in v
            case _:
                output[k.lower()] = v
    return output

t = time()
with open( os.path.join( DIR_DATA, "people.json" ), 'r' ) as f:
    DJ = json_load( f )
for person in DJ:
    dj[ int(person["id"]) ] = func_process_people_json( person )
DJ = pd.DataFrame.from_dict( dj, orient='index' )
print(time() - t)
print(DJ)

t = time()
x = {v["phone"]: k for k, v in dj.items()}
print(time() - t)

t = time()
x = dict(reversed(list(dj.items())))
print(time() - t)
exit()'''



'''# BOOKMARK: ChatGPT generated error handling
from typing import List, Tuple
from rich.console import Console
from rich.traceback import install
import sys
import os

# Initialize the Console for rich output
console = Console(record=True)

# Install the global exception handler
install(console=console)

def divide_by(number: float, divisor: float) -> float:
    """Divide a number by the divisor."""
    return number / divisor  # May raise ZeroDivisionError if divisor is 0

def divide_all(divides: List[Tuple[float, float]]) -> None:
    """Attempt to divide pairs of numbers, handling exceptions gracefully."""
    for number, divisor in divides:
        console.print(f"\nDividing {number} by {divisor}")
        try:
            result = divide_by(number, divisor)
        except Exception as e:
            # Print the exception type and message
            console.print(f"[bold red]Error:[/bold red] {e.__class__.__name__}: {e}")

            # Capture and print the most recent traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            console.print_exception(max_frames=1)

            # Save the full traceback to an HTML file
            error_dir = "errors"
            os.makedirs(error_dir, exist_ok=True)
            error_filename = os.path.join(error_dir, f"traceback_{number}_div_{divisor}.html")
            with open(error_filename, "w", encoding="utf-8") as error_file:
                error_file.write(console.export_html(clear=False))
            console.print(f"Full traceback saved to [bold blue]{error_filename}[/bold blue]\n")
        else:
            console.print(f"Result: {result}\n")

# List of number pairs to divide
DIVIDES = [
    (1000, 200),
    (10000, 500),
    (1, 0),
    (0, 1000000),
    (3.1427, 2),
    (888, 0),
    (2**32, 2**16),
]

# Execute the division operations
divide_all(DIVIDES)
'''

'''"""
Basic example to show how to print an traceback of an exception
"""
from typing import List, Tuple
from rich.console import Console

from datetime import datetime
from time import sleep

console = Console()


def divide_by(number: float, divisor: float) -> float:
    """Divide any number by zero."""
    # Will throw a ZeroDivisionError if divisor is 0
    result = number / divisor
    return result


def divide_all(divides: List[Tuple[float, float]]) -> None:
    """Do something impossible every day."""

    for number, divisor in divides:
        console.print(f"dividing {number} by {divisor}")
        try:
            result = divide_by(number, divisor)
        except Exception:
            console.print_exception(extra_lines=8, show_locals=True)
        else:
            console.print(f" = {result}")


DIVIDES = [
    (1000, 200),
    (10000, 500),
    (1, 0),
    (0, 1000000),
    (3.1427, 2),
    (888, 0),
    (2**32, 2**16),
]

divide_all(DIVIDES)
exit()'''


'''import os, pandas as pd

DIR_PROGRAM = os.getcwd()
DIR_DATA = os.path.join( DIR_PROGRAM, "data" )
DIR_PARENT = os.sep.join( DIR_PROGRAM.split(os.sep)[:-1] )
DIR_OUTPUT = os.path.join( DIR_PARENT, "Venmito Output" )

b_items = False
with open(os.path.join(DIR_DATA, "transactions.xml")) as f:
    TRANS_UNIQUE = pd.read_xml(f)
    if "items" in TRANS_UNIQUE.columns:
        TRANS_UNIQUE.drop( columns=["items"] )
        b_items = True
        
if b_items:
    with open(os.path.join(DIR_DATA, "transactions.xml")) as f:
        pass
exit()'''

'''
from time import time

FILE_REQ = os.path.join( DIR_PROGRAM, "requirements.txt" )
ignore_symbols = ["==", "["]
req_pkgs = []
with open(FILE_REQ, "r") as r:
    t = time()
    req_pkgs = [i.split(next((s for s in ignore_symbols if s in i), None))[0] for i in r.readlines()]
    print(time() - t)
    print(req_pkgs)

with open(FILE_REQ, "r") as r:
    t = time()
    req_pkgs = [i.split(next((s for s in ignore_symbols if s in i), i))[0] for i in r.readlines()]
    print(time() - t)
    print(req_pkgs)

with open(FILE_REQ, "r") as r:
    t = time()
    req_pkgs = [next((i.split(s)[0] for s in ignore_symbols if s in i), i) for i in r.readlines()]
    print(time() - t)
    print(req_pkgs)
exit()'''


'''x = """
    TEST 
    TEST"""
print(x)
exit()'''



'''# BOOKMARK: Old function for processing all elements of `transactions.xml`.

TRANS_UNIQUE = [ self._func_process_transactions_xml( transaction, TRANS_PRODUCTS, lookup_phone ) for transaction in DT ]

def _func_process_transactions_xml( self, input: dict, TRAN_PRODUCTS: list, lookup_phone: dict ) -> dict:
    """
    Function to process the items of each transaction of `transactions.xml`. FEATURE: Scalable for new exceptions!
    """
    
    i2 = {}
    b_can_lookup = lookup_phone != {}
    # Make keys lowercase and capture transaction ID.
    for k, v in input.items():
        match k:
            case "@id":
                i2["id"] = v
            case _:
                i2[k.lower()] = v
    # Process data.
    for k, v in i2.items():
        match k:
            case "items":
                # Create one row for each item in table `transaction_products`.
                if isinstance(v["item"], dict):
                    TRAN_PRODUCTS.append( self._func_process_item( v["item"], i2["id"] ) )
                elif isinstance(v["item"], list):
                    TRAN_PRODUCTS.extend( [ self._func_process_item( item, i2["id"] ) for item in v["item"] ] )
            case "phone":
                if b_can_lookup:
                    transaction_row["customer_id"] = lookup_phone[v]
            case _:
                transaction_row[k] = v
    return transaction_row
'''










'''
#
# PREREQUISITES Part 2: Set Up Functions
# > These functions are here to auto-setup the database for the first time.
#


def func_process_people_json( input: dict ) -> dict:
    """
    Function to process all parts of `people.json`. FEATURE: Scalable for new exceptions!
    """
    output = {}
    i2 = { k.lower():v for k, v in input.items() }
    for k, v in i2.items():
        match k:
            case "location":
                # Get `{'City': ..., 'Country': ...}`.
                output.update({ key.lower():value for key, value in v.items() })
            case "telephone":
                # Change "telephone" to "phone".
                output["phone"] = v
            case "devices":
                # Get `"devices": [...]`.
                for device in v:
                    device = device.lower()
                    # The device in the list exists.
                    output[f'has_{device}'] = True
                    # Add any new device.
                    if device not in DEVICES:
                        ANY_NEW_DEVICES = True
                        DEVICES.append(device)
                # Any devices from default list `DEVICES` not in `v` don't exist.
                for device in DEVICES:
                    if device not in v:
                        output[f'has_{device}'] = False
            case _:
                output[k] = v
    if ANY_NEW_DEVICES:
        # TO DO: Open `FILE_LISTS` and update `DEVICES` list.
        ANY_NEW_DEVICES = False
    return output


def func_process_people_yml( input: dict ) -> dict:
    """
    Function to process all parts of `people.yml`. FEATURE: Scalable for new exceptions!
    """
    output = {}
    i2 = { k.lower():v for k, v in input.items() }
    for k, v in i2.items():
        match k:
            case "name":
                # Split "name" into first and last names.
                spl = v.split(" ")
                output["first_name"] = spl[0]
                if len(spl) == 2:
                    output["last_name"] = spl[1]
            case tuple(DEVICES):
                # Individual boolean for each device. 
                output[f"has_{k}"] = bool(v)
            case _:
                output[k] = v
    return output


def func_process_transfers_csv( input: dict ) -> dict:
    """
    Function to process all parts of `transfers.csv`. FEATURE: Scalable for new exceptions!
    """
    output = {}
    i2 = { k.lower():v for k, v in input.items() }
    for k, v in i2.items():
        match k:
            # FEATURE: Add exceptions here.
            case _:
                output[k] = v
    return output


def func_process_transactions_xml( input: dict, TRAN_PRODUCTS: list, lookup_phone: dict ) -> dict:
    """
    Function to process each transaction of `transactions.xml`. FEATURE: Scalable for new exceptions!
    """
    transaction_row = {}
    i2 = {}
    b_can_lookup = lookup_phone != {}
    # Make keys lowercase and capture transaction ID.
    for k, v in input.items():
        match k:
            case "@id":
                i2["id"] = v
            case _:
                i2[k.lower()] = v
    # Process data.
    for k, v in i2.items():
        match k:
            case "items":
                # Create one row for each item in table `transaction_products`.
                if isinstance(v["item"], dict):
                    TRAN_PRODUCTS.append( func_process_item( v["item"], i2["id"] ) )
                elif isinstance(v["item"], list):
                    TRAN_PRODUCTS.extend( [ func_process_item( item, i2["id"] ) for item in v["item"] ] )
            case "phone":
                if b_can_lookup:
                    transaction_row["customer_id"] = lookup_phone[v]
            case _:
                transaction_row[k] = v
    return transaction_row

def func_process_item( item: dict, id ) -> dict:
    """
    Function to process each nested item of a transaction in `transactions.xml`.
    """
    item_row = {"id":id}
    for k, v in item.items():
        match k:
            # FEATURE: Add cases here.
            case _:
                item_row[k] = v
    return item_row


def func_process_universal( input: dict ) -> dict:
    """
    Function to process all data when no exceptions are found.
    """
    return { k.lower():v for k, v in input.items() }


def func_sql_method( table_name, CONN: psycopg.Connection, keys, data_iter ):
    """
    DEV NOTE: DOESN'T WORK. IS IT USEFUL?
    Function to insert data into PostgreSQL using psycopg3,
    while ignoring duplicate primary keys or unique constraints.
    """
    data = [dict(zip(keys, row)) for row in data_iter]  # Convert iterator to list of dictionaries
    columns = ', '.join(keys)  # Column names as CSV
    placeholders = ', '.join([f'%({key})s' for key in keys])  # Named placeholders

    query = f"""
        INSERT INTO {table_name} ({columns}) 
        VALUES ({placeholders})
        ON CONFLICT DO NOTHING
    """

    with CONN.cursor() as cur:
        cur.executemany(query, data)
        CONN.commit()


def func_process_files( b_first_time: bool ):
    """
    Only runs when there are files to process.
    """
    c_p = 1
    n_p = len([v for v in FILE_EXIST.values() if v])
    DATA_PEOPLE = {}
    lookup_email = {}
    lookup_phone = {}
    
    # PEOPLE: Process files.
    if FILE_EXIST["people.json"] or FILE_EXIST["people.yml"]:
        DATA_PEOPLE == {}

        # TO DO: Rewrite code below to allow temporary tables on database.
        if FILE_EXIST["people.json"]:
            print(f">> Processing files [{c_p}/{n_p}]...")
            c_p += 1
            DJ = {}; dj = {}
            # Process data.
            with open( os.path.join( DIR_DATA, "people.json" ), 'r' ) as f:
                DJ = json.load( f )
            for person in DJ:
                dj[ int(person["id"]) ] = func_process_people_json( person )
            # Handle database.
            DJ = pd.DataFrame.from_dict( dj, orient='index' )
            DATA_PEOPLE = DJ
            del DJ, dj
        
        if FILE_EXIST["people.yml"]:
            print(f">> Processing files [{c_p}/{n_p}]...")
            c_p += 1
            DY = {}; dy = {}
            # Process data.
            with open( os.path.join( DIR_DATA, "people.yml" ), 'r' ) as f:
                DY = yaml.safe_load( f )
            for person in DY:
                dy[ int(person["id"]) ] = func_process_people_yml( person )
            # Handle database.
            DY = pd.DataFrame.from_dict( dy, orient='index' )
            if FILE_EXIST["people.json"]:
                DATA_PEOPLE.update( DY )
            else:
                DATA_PEOPLE = DY
            del DY, dy
        
        # Send to database + handle variables.
        # TO DO: Replace `if_exists` with `method` to ignore duplicates and [...].
        DATA_PEOPLE.to_sql( "people", CONN, index=False, if_exists='append' ) 
    
    if DATA_PEOPLE == {} and b_first_time:
        # > HAPPENS WHEN `people.json` and `people.yml` don't exist while there IS NO usable data.
        # TO DO: Rewrite code below based on changes for temporary tables mentioned above.
        # - User must be prompted to find the right files to get rid of temporary tables.
        sys.exit(">> ERROR | Insufficient data for proper process.\nQuitting app...")
    elif DATA_PEOPLE == {} and not b_first_time:
        # > HAPPENS WHEN `people.json` and `people.yml` don't exist while there IS usable data.
        # TO DO: Create `func_get_lookups()` to extract ids, emails, and phones from complete database.
        # - `lookup_email`: `SELECT id, email FROM people`
        # - `lookup_phone`: `SELECT id, phone FROM people`
        pass
    lookup_email = {v: k for k, v in DATA_PEOPLE["email"].to_dict().items()}
    lookup_phone = {v: k for k, v in DATA_PEOPLE["phone"].to_dict().items()}
    b_can_lookup = lookup_phone != {}
    
    # TRANSFERS: Process file.
    if FILE_EXIST["transfers.csv"]:
        print(f">> Processing files [{c_p}/{n_p}]...")
        c_p += 1
        TRANSFERS = pd.read_csv( os.path.join( DIR_DATA, "transfers.csv" ) )
        TRANSFERS.columns = [ h.lower() for h in TRANSFERS.columns ]
        TRANSFERS.to_sql( "transfers", CONN, index=False, if_exists="append" )
    
    # PROMOTIONS: Process file.
    if FILE_EXIST["promotions.csv"]:
        print(f">> Processing files [{c_p}/{n_p}]...")
        c_p += 1
        PROMOTIONS = pd.read_csv( os.path.join( DIR_DATA, "promotions.csv" ) )
        PROMOTIONS.columns = [ h.lower() for h in PROMOTIONS.columns ]
        other_headers = [c for c in PROMOTIONS.columns if c not in ["id", "client_email", "telephone"]]
        if b_can_lookup:
            s1 = PROMOTIONS["client_email"].map( lookup_email )
            s2 = PROMOTIONS["telephone"].map( lookup_phone )
            PROMOTIONS["customer_id"] = s1.fillna( s2 ).astype(int)
            del s1, s2
        else:
            # TO DO: Apply `func_get_lookups()` from previous TO DOs.
            pass
        PROMOTIONS["responded"] = PROMOTIONS["responded"].map({ "Yes":True, "No":False })
        PROMOTIONS = PROMOTIONS[["id", "customer_id", *other_headers]]
    
    # TRANSACTIONS: Split into UNIQUE and PRODUCTS.
    if FILE_EXIST["transactions.xml"]:
        print(f">> Processing files [{c_p}/{n_p}]...")
        with open( os.path.join( DIR_DATA, "transactions.xml" ), 'rb' ) as f:
            DT = xmltodict.parse(f)["transactions"]["transaction"]
        TRAN_PRODUCTS = []
        TRAN_UNIQUE = [ func_process_transactions_xml( transaction, TRAN_PRODUCTS, lookup_phone ) for transaction in DT ]
        db_name = "transactions_unique" if b_can_lookup else "tmp_transactions_unique"
        TRAN_UNIQUE = pd.DataFrame( TRAN_UNIQUE )
        TRAN_UNIQUE.to_sql( db_name, CONN, index=False, if_exists="append" )
        TRAN_PRODUCTS = pd.DataFrame( TRAN_PRODUCTS )
        TRAN_PRODUCTS.to_sql( "transaction_products", CONN, index=False, if_exists="append" )


def func_create_tables():
    """
    Create tables with foreign key attributes and other features. If tables already exist first, run `func_reset_databases()`.
    """
    with CONN.cursor() as cur:
        CONN.set_autocommit(True)
        cur.execute( """
                    CREATE TABLE people ( 
                        id INTEGER PRIMARY KEY, 
                        first_name TEXT, 
                        last_name TEXT, 
                        phone TEXT UNIQUE, 
                        email TEXT UNIQUE, 
                        city TEXT, 
                        country TEXT, 
                        has_android BOOLEAN, 
                        has_iphone BOOLEAN, 
                        has_desktop BOOLEAN 
                    )""" )
        cur.execute( """
                    CREATE TABLE transfers ( 
                        sender_id INTEGER, 
                        recipient_id INTEGER, 
                        amount MONEY, 
                        date DATE, 
                        FOREIGN KEY(sender_id) REFERENCES people(id), 
                        FOREIGN KEY(recipient_id) REFERENCES people(id) 
                    )""" )
        cur.execute( """
                    CREATE TABLE promotions ( 
                        id INTEGER PRIMARY KEY, 
                        customer_id INTEGER, 
                        promotion TEXT, 
                        responded BOOLEAN, 
                        FOREIGN KEY (customer_id) REFERENCES people(id) 
                    )""" )
        cur.execute( """
                    CREATE TABLE transactions_unique ( 
                        id INTEGER PRIMARY KEY, 
                        customer_id INTEGER, 
                        store TEXT, 
                        FOREIGN KEY (customer_id) REFERENCES people(id)
                    )""" )
        cur.execute( """
                    CREATE TABLE transaction_products ( 
                        transaction_id INTEGER, 
                        item TEXT, 
                        price MONEY, 
                        price_per_item MONEY, 
                        quantity INTEGER, 
                        FOREIGN KEY (transaction_id) REFERENCES transactions_unique(id) 
                    )""" )
        cur.execute( """
                    CREATE VIEW view_store_products AS 
                        SELECT t1.store, t2.item 
                        FROM transactions_unique as t1 
                        LEFT JOIN transaction_products as t2 ON t1.id = t2.transaction_id
                    """ ) # DEV NOTE: Test and edit.
        cur.execute( """
                    CREATE VIEW view_transactions AS 
                        SELECT t1.id, t1.customer_id, t1.store, t2.item, t2.price, t2.price_per_item, t2.quantity 
                        FROM transactions_unique as t1 
                        LEFT JOIN transaction_products as t2 ON t1.id = t2.transaction_id
                    """ ) # DEV NOTE: Test and edit.
        CONN.set_autocommit(False)


def func_first_time():
    func_create_tables()
    if CAN_ADD:
        func_process_files( True )
    else:
        print("< ERROR | No files to add.")
        exit()


def func_reset_databases():
    with CONN.cursor() as cur:
        CONN.set_autocommit(True)
        cur.execute( "DROP TABLE IF EXISTS people CASCADE" )
        cur.execute( "DROP TABLE IF EXISTS transfers CASCADE" )
        cur.execute( "DROP TABLE IF EXISTS promotions CASCADE" )
        cur.execute( "DROP TABLE IF EXISTS transactions CASCADE" )
        cur.execute( "DROP TABLE IF EXISTS transaction_products CASCADE" )
        cur.execute( "DROP VIEW IF EXISTS view_store_products CASCADE" )
        CONN.set_autocommit(False)


#
# PREREQUISITES Part 3: Check Database
#
print("> Checking prerequisites [3/3]")

# Check if database exists.
try:
    CONN = psycopg.connect( "dbname=postgres user=postgres password=Space!3742" )
except:
    console.print_exception( show_locals=True )
    print("\n< Can't connect to database.\n> Quitting app...\n")
    exit()
    # TO DO: Set up server from scratch here??

# Check if database is complete.
try:
    with CONN.cursor() as cur:
        # DEV NOTE: Test!
        cur.execute( """SELECT EXISTS ( SELECT 1 FROM people ) AS table_existence""" )
        x = cur.fetchone()
        print(x)
        exit()
except:
    CONN.rollback()
    console.print(">> First time setup...")
    func_reset_databases()
    func_first_time()



#
# PART 2: Introduction
#
print(f"\n< All prerequisites satisfied!\n\n\n{BORDER}\n{mid_txt(TITLE)}\n\n")
print("MAIN MENU\n[0] Import data\n[1]")
'''





'''
import os, xmltodict

DIR_PROGRAM = os.getcwd()
DIR_DATA = os.path.join( DIR_PROGRAM, "data" )
FILES_DATA = [ # Scalable!
    "people.json",
    "people.yml",
    "transfers.csv",
    "promotions.csv",
    "transactions.xml"
]
FILE_EXIST = { f : os.path.exists(os.path.join(DIR_DATA, f)) for f in FILES_DATA }


def func_process_transactions_xml( TRAN_PRODUCTS: list, input: dict ) -> dict:
    """
    Function to process each transaction of `transactions.xml` with scalability for new exceptions.
    """
    transaction_row = {}
    i2 = {}
    # Make keys lowercase and capture transaction ID.
    for k, v in input.items():
        match k:
            case "@id":
                i2["id"] = v
            case _:
                i2[k.lower()] = v
    # Process data.
    for k, v in i2.items():
        match k:
            case "items":
                # Create one row for each item in table `transaction_products`.
                if isinstance(v["item"], dict):
                    TRAN_PRODUCTS.append( func_process_item( v["item"], i2["id"] ) )
                    #TRAN_PRODUCTS[ i2["id"] ] = func_process_item( v, i2["id"] )
                elif isinstance(v["item"], list):
                    TRAN_PRODUCTS.extend( [ func_process_item( item, i2["id"] ) for item in v["item"] ] )
                    #for item in v: TRAN_PRODUCTS[ i2["id"] ] = func_process_item( item, i2["id"] )
            case _:
                transaction_row[k] = v
    return transaction_row

def func_process_item( item: dict, id ) -> dict:
    """
    Function to process each nested item of a transaction in `transactions.xml`.
    """
    item_row = {"id":id}
    for k, v in item.items():
        match k:
            # FEATURE: Add cases here.
            case _:
                item_row[k] = v
    return item_row


if FILE_EXIST["transactions.xml"]:
    #TRAN_UNIQUE = []
    with open( os.path.join( DIR_DATA, "transactions.xml" ), 'rb' ) as f:
        DT = xmltodict.parse(f)["transactions"]["transaction"]
    TRAN_PRODUCTS = []
    TRAN_UNIQUE = [ func_process_transactions_xml( TRAN_PRODUCTS, transaction ) for transaction in DT ]
    #for transaction in DT:
    #    func_process_transactions_xml( TRAN_UNIQUE, TRAN_PRODUCTS, transaction )
    print(TRAN_UNIQUE)
    print(TRAN_PRODUCTS)

exit()'''







'''
### BOOKMARK
def func_one_sql( command: str, *args ):
    """DEV NOTE: Necessary???"""
    with CONN.cursor() as cur:
        if len(args) == 0:
            cur.execute( sql.SQL( command ) )
        else:
            cur.execute( sql.SQL( command ).format( *args ) )
        CONN.commit()
'''



"""### BOOKMARK First time importing to `default_lists.p`
import pickle
DEVICES = ["android", "iphone", "desktop"]
with open("default_lists.p", 'wb') as f:
    pickle.dump(DEVICES, f)
exit()"""


'''"""

Venmito Data
===

About
---
begin.py: Generates GUI and binds commands.

Author
---
Code by Jared Hidalgo.

"""



#
# PREREQUISITES Part 1: Check Packages
#
TITLE = "Venmito Data Processer"
print("\n> Checking prerequisites...")

# Import internal packages.
import os, sys, json, csv
from platform import system
from subprocess import call, Popen
from importlib.metadata import distributions
#import xml.etree.ElementTree as ET

# Set variables.
EXE_GLOBAL = f"{sys.executable}"
DIR_PROGRAM = os.getcwd() #"_".join( os.getcwd().split(" ") )
TXT_REQ = os.path.join( DIR_PROGRAM, "requirements.txt" )
DIR_DATA = os.path.join( DIR_PROGRAM, "data" )
ANY_DATA = False

# Set formatting.
N = 50
BORDER = "-"*N
def mid_txt( input: str ):
    spaces = " "*(( N-len(input) )//2)
    return spaces + input + spaces

# Check dependent files. 
req_files = [ # Scalable!
    "people.json",
    "people.yml",
    "transfers.csv",
    "promotions.csv",
    "transactions.xml"
]
FILE_EXIST = { f : os.path.exists(os.path.join(DIR_DATA, f)) for f in req_files }
WILL_ADD = any( FILE_EXIST.values() )

# Temporarily import program directory to PATH to import program files from any directory.
sys.path.append( DIR_PROGRAM )

# Set command(s) based on OS.
dict_od = {
    "Windows": "explorer", 
    "Darwin": "open"
}
OPEN_DIR = dict_od[system()] if system() in dict_od else "xdg-open"

# Package check: Offline check.
dict_pk = {
    "psycopg[binary]": "psycopg"
}
with open(TXT_REQ, "r") as r:
    req_pkgs = { i.split("==" if "==" in i else "\n")[0] : i for i in r.readlines() }
for k in dict_pk.keys():
    del req_pkgs[k]
req_pkgs = req_pkgs.keys()
for v in dict_pk.values():
    req_pkgs.append( v )
curr_pkgs = [ "-".join(dist.metadata["Name"].lower().split("_")) for dist in distributions() ]
miss_pkgs = [ x for x in req_pkgs if x not in curr_pkgs ]

if len(miss_pkgs) > 0:
    # Attempt online download.
    print()
    call( f"{EXE_GLOBAL} -m pip install -U pip", shell=True )
    call( f"{EXE_GLOBAL} -m pip install -r \"{TXT_REQ}\"", shell=True )
    # Check again.
    curr_pkgs = [ "-".join(dist.metadata["Name"].lower().split("_")) for dist in distributions() ]
    miss_pkgs = [ x for x in req_pkgs if x not in curr_pkgs ]
    if len(miss_pkgs) > 0:
        txt = "package" if len(miss_pkgs) == 1 else "packages"
        sys.exit( f"\n\n< ERROR | Missing {txt}: {",".join(miss_pkgs)}\n--> Can't run program." )
    print()

# Import external packages.
import psycopg, xmltodict, yaml
from psycopg import sql
import pandas as pd
import chime
chime.theme( "material" )
from rich.traceback import install
install( show_locals=True )
from rich.console import Console
console = Console()


#
# PREREQUISITES Part 2: Set Up Functions
# > These functions are here to auto-setup the database for the first time.
#
def func_universal( input: dict ) -> dict:
    """
    Parent function to process all known exceptions. Designed to scale for more exceptions.

    Args:
        input (dict): Original dictionary from the file.

    Returns:
        dict: Processed dictionary.
    """
    tmp = {}
    i2 = { k.lower() : v for k, v in input.items() }
    for k, v in i2.items():
        match k:
            case "location":
                tmp.update(v)
            case "telephone":
                tmp["phone"] = v
            case "name":
                spl = v.split(" ")
                tmp["first_name"] = spl[0]
                if len(spl) == 2:
                    tmp["last_name"] = spl[1]
            case "devices":
                tmp["has_android"] = "Android" in v
                tmp["has_iphone"] = "Iphone" in v
                tmp["has_desktop"] = "Desktop" in v
            case "android" | "desktop" | "iphone":
                tmp[f"has_{k}"] = bool(v)
            case _:
                tmp[k] = v
    return tmp


def func_sql_method(table_name, conn: psycopg.Connection, keys, data_iter):
    """
    Function to insert data into PostgreSQL using psycopg3,
    while ignoring duplicate primary keys or unique constraints.
    """
    data = [dict(zip(keys, row)) for row in data_iter]  # Convert iterator to list of dictionaries
    columns = ', '.join(keys)  # Column names as CSV
    placeholders = ', '.join([f'%({key})s' for key in keys])  # Named placeholders

    query = f"""
        INSERT INTO {table_name} ({columns}) 
        VALUES ({placeholders})
        ON CONFLICT DO NOTHING
    """

    with conn.cursor() as cur:
        cur.executemany(query, data)
        conn.commit()


def func_process_files( cur: psycopg.Cursor, from_scratch: bool ):

    print("> Processing files...")

    # Process people.
    if FILE_EXIST["people.json"] or FILE_EXIST["people.yml"]:
        DATA_PEOPLE = {}
        DJ = {}
        DY = {}

        # Process files.
        if FILE_EXIST["people.json"]:
            with open( os.path.join( DIR_DATA, "people.json" ), 'r' ) as f:
                for person in json.load( f ):
                    DJ[ int(person["id"]) ] = func_universal( person )
            DJ = pd.DataFrame.from_dict( DJ, orient='index' )
            DJ.to_sql( "people", conn, index=False, method=func_sql_method )
        
        if FILE_EXIST["people.yml"]:
            with open( os.path.join( DIR_DATA, "people.yml" ), 'r' ) as f:
                for person in yaml.safe_load( f ):
                    DY[ int(person["id"]) ] = func_universal( person )
            DY = pd.DataFrame.from_dict( DY, orient='index' )
            DY.to_sql( "people", conn, index=False, method=func_sql_method )
        
        #
        #
        
        # Cleanup dictionaries.
        if FILE_EXIST["people.json"] and FILE_EXIST["people.yml"]:
            common = list( set(DJ.keys()) & set(DY.keys()) )
            # DEV NOTE: Handle data overlap here.
        else:
            DATA_PEOPLE = DJ if FILE_EXIST["people.json"] else DY
        DATA_PEOPLE = pd.DataFrame.from_dict( DATA_PEOPLE, orient='index' )

        # Send to database.
        DATA_PEOPLE.to_sql( "people", conn, if_exists="append", index=False )

        # DEV NOTE: If not first_time, then extract full database first.
        if from_scratch:
            lookup_email = {v: k for k, v in DATA_PEOPLE["email"].to_dict().items()}
            lookup_phone = {v: k for k, v in DATA_PEOPLE["phone"].to_dict().items()}
    
    if FILE_EXIST["transfers.csv"]:
        TRANSFERS = pd.read_csv( os.path.join( DIR_DATA, "transfers.csv" ) )
        # DEV NOTE: Cast correct data types here.
        TRANSFERS.to_sql( "tmp_transfers", conn, if_exists="append", index=False )
        cur.execute( """
                     INSERT INTO transfers 
                        (SELECT * FROM tmp_transfers)
                        ON CONFLICT DO NOTHING
                     """ )

    PROMOTIONS = pd.read_csv( os.path.join( DIR_DATA, "promotions.csv" ) )
    headers = [c for c in PROMOTIONS.columns if c not in ["id", "client_email", "telephone"]]
    s1 = PROMOTIONS["client_email"].map( lookup_email )
    s2 = PROMOTIONS["telephone"].map( lookup_phone )
    PROMOTIONS["customer_id"] = s1.fillna( s2 ).astype(int)
    PROMOTIONS["responded"] = PROMOTIONS["responded"].map( {"Yes":True, "No":False} )
    PROMOTIONS = PROMOTIONS[["id", "customer_id", *headers]]

    ### BOOKMARK
    TRANSACTIONS = []
    PRODUCTS = [] # DEV NOTE: Change this to a view within a schema?
    with open( os.path.join( DIR_DATA, "transactions.xml" ), 'r' ) as f:
        tree = ET.parse(f)
    root = tree.getroot()
    for transaction in root.findall("transaction"):
        t_id = transaction.get("id")
        customer_id = lookup_phone[transaction.find("phone").text]
        store = transaction.find("store").text
        # DEV NOTE: Set loop for other variables except for known exceptions. Also split into two databases.
        for item in transaction.find("items").findall("item"):
            TRANSACTIONS.append({
                "transaction_id": int(t_id),
                "customer_id": customer_id,
                "store": store,
                "item": item.find("item").text,
                "price": float(item.find("price").text),
                "price_per_item": float(item.find("price_per_item").text),
                "quantity": int(item.find("quantity").text)
            })
            PRODUCTS.append( {store, item.find("item").text} )

    TRANSACTIONS = pd.DataFrame( TRANSACTIONS )
    TRANSACTIONS["customer_id"] = TRANSACTIONS["customer_id"].astype(int)
    PRODUCTS = pd.DataFrame( PRODUCTS, columns=["Store", "Item"] )


    ### BOOKMARK
    # DATA 4/4: Add to database.
    DATA_PEOPLE.to_sql( "people", conn, if_exists="append", index=False )
    """for person in DATA_PEOPLE:
        cur.execute( 
            "INSERT OR IGNORE INTO people VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            tuple( person.values() )
        )"""
    TRANSFERS.to_sql( "transfers", conn, if_exists="append", index=False )
    PROMOTIONS.to_sql( "promotions", conn, if_exists="append", index=False )
    TRANSACTIONS.to_sql( "transactions", conn, if_exists="append", index=False )
    PRODUCTS.to_sql( "products", conn, if_exists="append", index=False )


def func_create_databases( cur: psycopg.Cursor ):
    
    cur.execute( sql.SQL( "CREATE SCHEMA {}" ).format( sql.Identifier("venmito_evaluator") ) )
    cur.execute( """
                CREATE TABLE venmito_evaluator.people ( 
                    id INTEGER PRIMARY KEY, 
                    first_name TEXT, 
                    last_name TEXT, 
                    phone TEXT, 
                    email TEXT, 
                    city TEXT, 
                    country TEXT, 
                    has_android BOOLEAN, 
                    has_iphone BOOLEAN, 
                    has_desktop BOOLEAN 
                )""" )
    cur.execute( """
                CREATE TABLE venmito_evaluator.transfers ( 
                    sender_id INTEGER, 
                    recipient_id INTEGER, 
                    amount MONEY, 
                    date DATE, 
                    FOREIGN KEY(sender_id) REFERENCES venmito_evaluator.people(id), 
                    FOREIGN KEY(recipient_id) REFERENCES venmito_evaluator.people(id) 
                )""" )
    cur.execute( """
                CREATE TABLE venmito_evaluator.promotions ( 
                    id INTEGER PRIMARY KEY, 
                    customer_id INTEGER, 
                    phone TEXT, 
                    promotion TEXT, 
                    responded BOOLEAN, 
                    FOREIGN KEY (customer_id) REFERENCES venmito_evaluator.people(id) 
                )""" )
    cur.execute( """
                CREATE TABLE venmito_evaluator.transactions ( 
                    id INTEGER PRIMARY KEY, 
                    customer_id TEXT, 
                    store TEXT, 
                    FOREIGN KEY (customer_id) REFERENCES venmito_evaluator.people(id)
                )""" )
    cur.execute( """
                CREATE TABLE venmito_evaluator.transaction_products ( 
                    transaction_id INTEGER, 
                    item TEXT, 
                    price REAL, 
                    price_per_item REAL, 
                    quantity INTEGER, 
                    FOREIGN KEY (transaction_id) REFERENCES venmito_evaluator.transactions(id) 
                )""" )
    cur.execute( """
                CREATE VIEW venmito_evaluator.products AS 
                    SELECT t1.store, t2.item 
                    FROM venmito_evaluator.transactions as t1 
                    LEFT JOIN venmito_evaluator.transaction_products as t2 ON t1.id = t2.transaction_id
                """ )


def func_first_time( cur: psycopg.Cursor ):
    func_create_databases( cur )
    if WILL_ADD:
        func_process_files( cur, True )
    else:
        print("< ERROR | No files to add.")
        exit()


def func_reset_databases( cur: psycopg.Cursor ):
    cur.execute("DROP TABLE IF EXISTS venmito_evaluator.people CASCADE")
    cur.execute("DROP TABLE IF EXISTS venmito_evaluator.transfers CASCADE")
    cur.execute("DROP TABLE IF EXISTS venmito_evaluator.products CASCADE")
    cur.execute("DROP TABLE IF EXISTS venmito_evaluator.promotions CASCADE")
    cur.execute("DROP TABLE IF EXISTS venmito_evaluator.transactions CASCADE")
    cur.execute("DROP SCHEMA IF EXISTS venmito_evaluator CASCADE")


#
# PREREQUISITES Part 3: Check Database
#

# Connect.
try:
    conn = psycopg.connect( "dbname=postgres user=postgres password=Space!3742" )
    cur = conn.cursor()
    func_reset_databases(cur)
except:
    console.print_exception( show_locals=True )
    print("\n< Can't continue.\n> Quitting app...\n")
    exit()
    # DEV NOTE: Set up server from scratch here?

# Check if database exists.
try:
    cur.execute( "SELECT * FROM people" )
    text = input( "Before we begin, would you like to reset existing databases? (y/n)" )
    from_scratch = text.lower() == "y"
    if from_scratch:
        func_reset_databases( cur )
        func_first_time( cur )
except:
    # DEV NOTE: Ignore intentional error.
    print("< First time setup!")
    func_first_time( cur )



#
# PART 2: Introduction
#
print(f"< Prerequisites satisfied!\n\n\n{BORDER}\n{mid_txt(TITLE)}\n\n")
print("CLI Menu\n[0] Import data\n[1]")
exit()
'''


'''
#
# ChatGPT suggestions
#

# 1: Best-selling Items
conn = sqlite3.connect("business_data.db")
best_selling = pd.read_sql_query("""
    SELECT item, SUM(quantity) as total_sold 
    FROM transactions 
    GROUP BY item 
    ORDER BY total_sold DESC 
    LIMIT 5
""", conn)
print(best_selling)

# 2: Store with Most Profit
most_profitable_store = pd.read_sql_query("""
    SELECT store, SUM(price) as total_profit 
    FROM transactions 
    GROUP BY store 
    ORDER BY total_profit DESC 
    LIMIT 1
""", conn)
print(most_profitable_store)

# 3: Identify Clients with Promotions
clients_promotions = pd.read_sql_query("""
    SELECT p.client_email, p.promotion, ppl.first_name, ppl.last_name
    FROM promotions p
    JOIN people ppl ON p.client_email = ppl.email
""", conn)
print(clients_promotions)
'''



#req_pkgs = [i.split("==" if "==" in i else "\n")[0] for i in r.readlines()]


"""TITLE = "Venmito Data Processer"
print("\n> Checking requirements...\n")

# Import internal packages.
import os, sys
from platform import system
from subprocess import call, Popen
from importlib.metadata import distributions
import xml.etree.ElementTree as ET

# Set variables.
EXE_GLOBAL = f"{sys.executable}"
DIR_PROGRAM = os.getcwd() #"_".join( os.getcwd().split(" ") )
TXT_REQ = os.path.join( DIR_PROGRAM, "requirements.txt" )
DIR_DATA = os.path.join( DIR_PROGRAM, "data" )
DB_INFO = {"name": "postgres", "user": "postgres", "password": "Space!3742"}
DATA_ORG = {}
IS_READY = True

# Check dependent files.
req_files = [ "people.json", "people.yml", "transfers.csv", "promotions.csv", "transactions.xml" ]
curr_files = [ os.path.join(DIR_DATA, f) for f in req_files ]
miss_files = [ x for x in req_files if x not in curr_files ]
WILL_ADD = len(miss_files) != len(req_files)

# Temporarily import program directory to PATH to import program files from any directory.
sys.path.append( DIR_PROGRAM )

# Set commands based on OS.
dict_od = {
    "Windows": "explorer", 
    "Darwin": "open"
}
OPEN_DIR = dict_od[system()] if system() in dict_od else "xdg-open"

# Package check: Offline check.
with open(TXT_REQ, "r") as r:
    req_pkgs = [i.split("==" if "==" in i else "\n")[0] for i in r.readlines()]
curr_pkgs    = ["-".join(dist.metadata["Name"].lower().split("_")) for dist in distributions()]
miss_pkgs = [x for x in req_pkgs if x not in curr_pkgs]

if len(miss_pkgs) > 0:
    # Attempt online download.
    call( f"{EXE_GLOBAL} -m pip install -U pip", shell=True )
    call( f"{EXE_GLOBAL} -m pip install -r \"{TXT_REQ}\"", shell=True )
    # Check again.
    curr_pkgs    = [dist.metadata["Name"] for dist in distributions()]
    miss_pkgs = [x for x in req_pkgs if x not in curr_pkgs]
    if len(miss_pkgs) > 0:
        txt = "package" if len(miss_pkgs) == 1 else "packages"
        sys.exit( f"\n\nERROR: Missing {txt}: {",".join(miss_pkgs)}\n--> Can't run program." )
print(">> Importing external packages...")

# Import external packages.
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import chime
chime.theme("material")
from rich.traceback import install
install(show_locals=True)
from rich.console import Console
console = Console()
import yaml, json, csv
import pandas as pd


#
# PART 2: Setup pgAdmin 4.
#

print(">> Checking database...")
try:
    conn = psycopg2.connect( database = DB_INFO["name"],
                            host = "",
                            user = DB_INFO["user"],
                            password = DB_INFO["password"],
                            port = 5432 )
    del conn
except:
    pass"""







'''import os, csv, json, yaml, psycopg
import pandas as pd
import xml.etree.ElementTree as ET

import xmltodict
from rich.traceback import install
install(show_locals=True)

DATA_ORG = {}
DIR_PROGRAM = "_".join( os.getcwd().split(" ") )
DIR_DATA = os.path.join( DIR_PROGRAM, "data" )

conn = psycopg.connect( "dbname=postgres user=postgres password=Space!3742" )
cur = conn.cursor()

# DATA 1: Process people.
DATA_PEOPLE = {}
with open( os.path.join( DIR_DATA, "people.json" ), 'r' ) as f:
    dataPJ = json.load(f)
for person in dataPJ:
    DATA_PEOPLE[ person["id"] ] = { k:v for k,v in person.items() if not( isinstance(v, (list, dict)) ) }
    if "devices" in person.keys():
        DATA_PEOPLE[ person["id"] ]["has_android"] = "Android" in person["devices"]
        DATA_PEOPLE[ person["id"] ]["has_iphone"] = "Iphone" in person["devices"]
        DATA_PEOPLE[ person["id"] ]["has_desktop"] = "Desktop" in person["devices"]
    if "location" in person.keys():
        DATA_PEOPLE[ person["id"] ]["city"] = person["location"]["City"]
        DATA_PEOPLE[ person["id"] ]["country"] = person["location"]["Country"]
    # Other version
    """for k, v in person.items():
        if isinstance(v, dict):
            DATA_PEOPLE[ person["id"] ]["city"] = v["City"]
            DATA_PEOPLE[ person["id"] ]["country"] = v["Country"]
        elif k == "devices":
            DATA_PEOPLE[ person["id"] ]["has_android"] = "Android" in v
            DATA_PEOPLE[ person["id"] ]["has_iphone"] = "Iphone" in v
            DATA_PEOPLE[ person["id"] ]["has_desktop"] = "Desktop" in v
        else:
            DATA_PEOPLE[ person["id"] ][k] = v"""

with open( os.path.join( DIR_DATA, "people.yml" ), 'r' ) as f:
    dataPY = yaml.safe_load( f )
for person in dataPY:
    id = person["id"]
    tmp = {
            #"id": person["id"],
            "first_name": person["name"].split()[0],
            "last_name": person["name"].split()[1] if len(person["name"].split()) > 1 else "",
            "phone": person["phone"],
            "email": person["email"],
            "city": person["city"].split(",")[0],
            "country": person["city"].split(",")[-1].strip(),
            "has_android": person["Android"],
            "has_iphone": person["Iphone"],
            "has_desktop": person["Desktop"],
        }
    if id in DATA_PEOPLE:
        # [Insert code to decide which info to prioritize.]
        pass
    else:
        DATA_PEOPLE[id] = tmp
DATA_PEOPLE = pd.DataFrame.from_dict( DATA_PEOPLE, orient='index' )
del dataPJ, dataPY
lookup_email = {v: k for k, v in DATA_PEOPLE["email"].to_dict().items()}
lookup_phone = {v: k for k, v in DATA_PEOPLE["phone"].to_dict().items()}

# DATA 2: Get other files.
PROMOTIONS = pd.read_csv( os.path.join( DIR_DATA, "promotions.csv" ) )
headers = [c for c in PROMOTIONS.columns if c not in ["id", "client_email", "telephone"]]
s1 = PROMOTIONS["client_email"].map( lookup_email )
s2 = PROMOTIONS["telephone"].map( lookup_phone )
PROMOTIONS["customer_id"] = s1.fillna( s2 ).astype(int)
PROMOTIONS["responded"] = PROMOTIONS["responded"].map( {"Yes":True, "No":False} )
PROMOTIONS = PROMOTIONS[["id", "customer_id", *headers]]


TRAN_UNIQUE = []
PRODUCTS = []
with open( os.path.join( DIR_DATA, "transactions.xml" ), 'r' ) as f:
    x = xmltodict.parse(f)
    #tree = ET.parse(f)
print(x)
exit()
root = tree.getroot()
for transaction in root.findall("transaction"):
    #standard = 
    t_id = transaction.get("id")
    customer_id = lookup_phone[transaction.find("phone").text]
    store = transaction.find("store").text

    for item in transaction.find("items").findall("item"):
        TRAN_UNIQUE.append({
            "transaction_id": int(t_id),
            "customer_id": customer_id,
            "store": store,
            "item": item.find("item").text,
            "price": float(item.find("price").text),
            "price_per_item": float(item.find("price_per_item").text),
            "quantity": int(item.find("quantity").text)
        })
        PRODUCTS.append( {store, item.find("item").text} )

TRAN_UNIQUE = pd.DataFrame( TRAN_UNIQUE )
TRAN_UNIQUE["customer_id"] = TRAN_UNIQUE["customer_id"].astype(int)
PRODUCTS = pd.DataFrame( PRODUCTS, columns=["Store", "Item"] )
print(TRAN_UNIQUE)'''




"""
# File 2
    with open( os.path.join( DIR_DATA, "people.yml" ), 'r' ) as f:
        dataPY = yaml.safe_load( f )
    for person in dataPY:
        tmp = {}
        for k, v in person.items():
            if k.lower() == "name":
                spl = v.split(" ")
                tmp["first_name"] = spl[0]
                tmp["last_name"] = spl[1]
            else:
                tmp[k] = v
        
        print(person)
        id = person["id"]
        # DEV NOTE: Set loop for other variables except for known exceptions.
        tmp = {
                "id": person["id"],
                "first_name": person["name"].split()[0],
                "last_name": person["name"].split()[1] if len(person["name"].split()) > 1 else "",
                "phone": person["phone"],
                "email": person["email"],
                "city": person["city"].split(",")[0],
                "country": person["city"].split(",")[-1].strip(),
                "has_android": person["Android"],
                "has_iphone": person["Iphone"],
                "has_desktop": person["Desktop"],
            }
        if id in DATA_PEOPLE:
            # [Insert code to decide which info to prioritize.]
            pass
        else:
            DATA_PEOPLE[id] = tmp

    DATA_PEOPLE = pd.DataFrame.from_dict( DATA_PEOPLE, orient='index' )
    del dataPY
"""



"""for FILE in os.listdir( DIR_DATA ):
    fpath = os.path.join( DIR_DATA, FILE )
    fDecode = os.fsdecode( FILE )
    #fspl = fDecode.split(".")
    #fname = ".".join( fspl[:-1] )
    ftype = fDecode.split(".")[-1]
    with open( fpath, 'r', encoding='utf-8-sig' ) as f:
        if ftype == "xml":
            tree = ET.parse(f)
            root = tree.getroot()
            for transaction in root.findall("transaction"):
                transaction_id = transaction.get("id")
                phone = transaction.find("phone").text
                store = transaction.find("store").text

                print(f"Transaction ID: {transaction_id}")
                print(f"Phone: {phone}")
                print(f"Store: {store}")
                print("Items:")

                # Iterate over items in each transaction
                for item in transaction.find("items").findall("item"):
                    item_name = item.find("item").text
                    price = item.find("price").text
                    price_per_item = item.find("price_per_item").text
                    quantity = item.find("quantity").text

                    print(f"  - Item: {item_name}, Price: {price}, Price per item: {price_per_item}, Quantity: {quantity}")

                print("-" * 50)  # Separator for readability"""



"""import os, yaml
from rich.traceback import install
install(show_locals=True)

DIR_PROGRAM = "_".join( os.getcwd().split(" ") )
DIR_DATA = os.path.join( DIR_PROGRAM, "data" )

for FILE in os.listdir( DIR_DATA ):
    fspl = os.fsdecode( FILE ).split(".")
    fname = ".".join( fspl[:-1] )
    ftype = fspl[-1]
    with open( os.path.join(DIR_DATA, FILE), 'r' ) as f:
        if ftype == "yml":
            print("hi")
            dict = yaml.full_load(f)
            print(dict)"""


"""import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE

con = psycopg2.connect(dbname='postgres',
      user=user_name, host='',
      password=password)

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # <-- ADD THIS LINE

cur = con.cursor()

# Use the psycopg2.sql module instead of string concatenation 
# in order to avoid sql injection attacks.
cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(db_name))
    )"""


"""import virtualenv, os
PROJECT_NAME = 'new_project'
virtualenvs_folder = os.path.expanduser("~/.virtualenvs")
venv_dir = os.path.join(virtualenvs_folder, PROJECT_NAME)
virtualenv.create_environment(venv_dir)
command = ". {}/{}/bin/activate && pip install -r requirements.txt".format(virtualenvs_folder, PROJECT_NAME)
os.system(command)"""






#
# ARCHIVED
#
'''exit()



print( f"> Check done!\n{BORDER}\n> Connecting to database..." )

print( f"\n> Connected!\n{BORDER}\n> Booting {TITLE}..." )
#
# [A GUI function]: Process external data.
#


#print( f"\n\nPART 1/3 Done!\n{BORDER}\nPART 2/3: Database Setup\n> Checking connection..." )

# Connect to database.
conn = psycopg_binary.connect( database = DB_INFO["name"],
                         host = "",
                         user = DB_INFO["user"],
                         password = DB_INFO["password"],
                         port = 5432)
conn.set_isolation_level( ISOLATION_LEVEL_AUTOCOMMIT )
cur = conn.cursor()

# CREATE TABLES IF NOT EXIST
print("> Setting up tables...")

# DEV NOTE: Maybe ask user if they want tables to be dropped before running?
cur.execute("DROP TABLE IF EXISTS people CASCADE")
cur.execute("DROP TABLE IF EXISTS transfers CASCADE")
cur.execute("DROP TABLE IF EXISTS products CASCADE")
cur.execute("DROP TABLE IF EXISTS promotions CASCADE")
cur.execute("DROP TABLE IF EXISTS transactions CASCADE")


def process_all( input: dict ) -> dict:
    """
    Parent function to process all known exceptions. Designed to scale for more exceptions.

    Args:
        input (dict): Original data from the file.

    Returns:
        dict: Processed data.
    """
    tmp = {}
    for k, v in input.items():
        k = k.lower()
        match k:
            case "location":
                tmp.update(v)
            case "telephone":
                tmp["phone"] = v
            case "name":
                spl = v.split(" ")
                tmp["first_name"] = spl[0]
                if len(spl) == 2:
                    tmp["last_name"] = spl[1]
            case "devices":
                tmp["has_android"] = "Android" in v
                tmp["has_iphone"] = "Iphone" in v
                tmp["has_desktop"] = "Desktop" in v
            case "android" | "desktop" | "iphone":
                tmp[f"has_{k}"] = bool(v)
            case _:
                tmp[k] = v

        """k = k.lower()
        if k == "location":
            tmp.update(v)
        elif k == "telephone":
            tmp["phone"] = v
        elif k == "name":
            spl = v.split(" ")
            tmp["first_name"] = spl[0]
            if len(spl) == 2:
                tmp["last_name"] = spl[1]
        elif k == "devices":
            tmp["has_android"] = "Android" in v
            tmp["has_iphone"] = "Iphone" in v
            tmp["has_desktop"] = "Desktop" in v
        elif k in ["android", "desktop", "iphone"]:
            tmp[f"has_{k}"] = bool(v)
        else:
            tmp[k] = v"""
    return tmp


if WILL_ADD:
    print("> Processing files from data directory...")
    
    # DATA 2/4: Process people.
    DATA_PEOPLE = {}
    D1 = {}
    with open( os.path.join( DIR_DATA, "people.json" ), 'r' ) as f:
        for person in json.load( f ):
            D1[ int(person["id"]) ] = process_all( person )
    D2 = {}
    with open( os.path.join( DIR_DATA, "people.yml" ), 'r' ) as f:
        for person in yaml.safe_load( f ):
            D2[ int(person["id"]) ] = process_all( person )
    
    common = list( set(D1.keys()) & set(D2.keys()) )
    # DEV NOTE: Handle data overlap here.
    
    DATA_PEOPLE = pd.DataFrame.from_dict( DATA_PEOPLE, orient='index' )
    lookup_email = {v: k for k, v in DATA_PEOPLE["email"].to_dict().items()}
    lookup_phone = {v: k for k, v in DATA_PEOPLE["phone"].to_dict().items()}

    # DATA 3/4: Process other files.
    TRANSFERS = pd.read_csv( os.path.join( DIR_DATA, "transfers.csv" ) )

    PROMOTIONS = pd.read_csv( os.path.join( DIR_DATA, "promotions.csv" ) )
    headers = [c for c in PROMOTIONS.columns if c not in ["id", "client_email", "telephone"]]
    s1 = PROMOTIONS["client_email"].map( lookup_email )
    s2 = PROMOTIONS["telephone"].map( lookup_phone )
    PROMOTIONS["customer_id"] = s1.fillna( s2 ).astype(int)
    PROMOTIONS["responded"] = PROMOTIONS["responded"].map( {"Yes":True, "No":False} )
    PROMOTIONS = PROMOTIONS[["id", "customer_id", *headers]]

    TRAN_UNIQUE = []
    PRODUCTS = [] # DEV NOTE: Change this to a view within a schema?
    with open( os.path.join( DIR_DATA, "transactions.xml" ), 'r' ) as f:
        tree = ET.parse(f)
    root = tree.getroot()
    for transaction in root.findall("transaction"):
        t_id = transaction.get("id")
        customer_id = lookup_phone[transaction.find("phone").text]
        store = transaction.find("store").text
        # DEV NOTE: Set loop for other variables except for known exceptions. Also split into two databases.
        for item in transaction.find("items").findall("item"):
            TRAN_UNIQUE.append({
                "transaction_id": int(t_id),
                "customer_id": customer_id,
                "store": store,
                "item": item.find("item").text,
                "price": float(item.find("price").text),
                "price_per_item": float(item.find("price_per_item").text),
                "quantity": int(item.find("quantity").text)
            })
            PRODUCTS.append( {store, item.find("item").text} )

    TRAN_UNIQUE = pd.DataFrame( TRAN_UNIQUE )
    TRAN_UNIQUE["customer_id"] = TRAN_UNIQUE["customer_id"].astype(int)
    PRODUCTS = pd.DataFrame( PRODUCTS, columns=["Store", "Item"] )


    # DATA 4/4: Add to database.
    DATA_PEOPLE.to_sql( "people", conn, if_exists="append", index=False )
    """for person in DATA_PEOPLE:
        cur.execute( 
            "INSERT OR IGNORE INTO people VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            tuple( person.values() )
        )"""
    TRANSFERS.to_sql( "transfers", conn, if_exists="append", index=False )
    PROMOTIONS.to_sql( "promotions", conn, if_exists="append", index=False )
    TRAN_UNIQUE.to_sql( "transactions", conn, if_exists="append", index=False )
    PRODUCTS.to_sql( "products", conn, if_exists="append", index=False )

    # Add foreign keys.
    cur.execute("""
                ALTER TABLE transfers 
                    FOREIGN KEY (customer_id) REFERENCES people(id) 
                    FOREIGN KEY (recipient_id) REFERENCES people(id)
                """)
    cur.execute("""
                ALTER TABLE promotions 
                    FOREIGN KEY (customer_id) REFERENCES people(id) 
                """)
    cur.execute("""
                ALTER TABLE transactions 
                    FOREIGN KEY (customer_id) REFERENCES people(id) 
                    FOREIGN KEY (recipient_id) REFERENCES people(id)
                """)
    cur.execute("""
                ALTER TABLE products 
                    FOREIGN KEY (customer_id) REFERENCES people(id) 
                    FOREIGN KEY (recipient_id) REFERENCES people(id)
                """)
'''
#