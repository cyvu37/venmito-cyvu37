"""
Venmito Data
===

About
---
begin.py: Runs the entire program.

Author
---
Code by Jared Hidalgo.
"""


#
# PREREQUISITES Part 1: Package and Definition Check
#
TITLE = "Venmito Evaluator"
"""Title of the program."""
T = "VE"
"""Abbreviation of the program."""
print(f"\nBooting {TITLE}...\n\n* Checking prerequisites...")


# Import internal packages.
import os, re, sys
from platform import system
from subprocess import call, Popen
from importlib.metadata import distributions
from json import load as json_load
from pickle import load as pickle_load, dump as pickle_dump
from datetime import datetime
from time import sleep
from webbrowser import open_new_tab
from copy import deepcopy
from collections import ChainMap
from dateutil.parser import parse


# Set basic formatting features.
WIDTH = 100
"""Width of printing borders and aligned text."""
BORDER = "<"*(WIDTH//2) + ">"*(WIDTH//2)
def mid( input: str, has_color: bool = False ):
    """Aligns text to the middle of the CMD by `WIDTH`."""
    l = len(re.sub( r"\[.*?\]", "", input )) if has_color else len(input)
    spaces = " "*(( WIDTH-l )//2)
    return spaces + input + spaces
def fcolor( message: str, color: str ):
    """For `rich` printing: Surround a `message` in `color`."""
    return f"[{color}]{message}[/{color}]"
CD = "bright_cyan"
"""For `rich` printing: Default color for normal messages."""
CH = "bright_yellow"
"""For `rich` printing: Default color for help messages."""
CC = "gold1"
"""For `rich` printing: Default color for action column."""
LINE = WIDTH * "-"
R_LINE = fcolor( LINE, CD )
"""For `rich` printing."""
HEADER = mid( f"< < <   {TITLE.upper()}   > > >", False )
R_HEADER = mid( f"< < <   {fcolor(TITLE.upper(), CD)}   > > >", True )
"""For `rich` printing."""
QUIT = f"* Quitting app...\n\n{HEADER}\n{BORDER}\n"
R_QUIT = fcolor( f"* Quitting app...\n\n\n{R_HEADER}\n{BORDER}\n", "blue1" )
"""For `rich` printing."""
R_YN = f"[{CD}]([/{CD}][green]y[/green][{CD}]/[/{CD}][red]n[/red][{CD}])[/{CD}]"
"""For `rich` printing: Default `(yes/no)` prompt."""
R_ENTER = fcolor( f"{BORDER}\n{R_HEADER}", "green1" )
"""For `rich` printing."""


# Set directories.
EXE_GLOBAL = f"{sys.executable}"
DIR_PROGRAM = os.getcwd()
DIR_DATA = os.path.join( DIR_PROGRAM, "data" )
DIR_PARENT = os.sep.join( DIR_PROGRAM.split(os.sep)[:-1] )
DIR_OUTPUT = os.path.join( DIR_PARENT, "Venmito Output" )
DIR_ERR = os.path.join( DIR_OUTPUT, "errors" )
# Temporarily import program directory to PATH to import program files from any directory.
sys.path.append( DIR_PROGRAM )
# Add directories.
if not os.path.exists( DIR_OUTPUT ):
    os.mkdir( DIR_OUTPUT )
if not os.path.exists( DIR_ERR ):
    os.mkdir( DIR_ERR )
# Set filepaths
FILE_REQ = os.path.join( DIR_PROGRAM, "requirements.txt" )
FILE_LISTS = os.path.join( DIR_PROGRAM, "default_lists.p" )
FILES_DATA = [ 
    "people.json",
    "people.yml",
    "transfers.csv",
    "promotions.csv",
    "transactions.xml"
]


# Package check: Offline check.
cutoff_symbols = ["==", "["]
with open(FILE_REQ, "r") as r:
    req_pkgs = [ i.split( next(( s for s in cutoff_symbols if s in i ), None) )[0].lower() for i in r.readlines() ]
curr_pkgs = [ "-".join( dist.metadata["Name"].lower().split("_") ) for dist in distributions() ]
miss_pkgs = [ x for x in req_pkgs if x not in curr_pkgs ]


# Package check: If any packages are missing.
if len(miss_pkgs) > 0:
    # Attempt online download.
    print("* WARNING | There are missing packages.\n* Attempting online download...\n")
    call( f"{EXE_GLOBAL} -m pip install -U pip", shell=True )
    call( f"{EXE_GLOBAL} -m pip install -r \"{FILE_REQ}\"", shell=True )
    # Check again.
    curr_pkgs = [ "-".join( dist.metadata["Name"].lower().split("_") ) for dist in distributions() ]
    miss_pkgs = [ x for x in req_pkgs if x not in curr_pkgs ]
    if len(miss_pkgs) > 0:
        tmp = "package" if len(miss_pkgs) == 1 else "packages"
        sys.exit( f"\n\n* ERROR | Missing {tmp}: {",".join(miss_pkgs)}\n{QUIT}" )
    print("\n* Packages installed successfully.")


# Import `rich` features.
# > Console formatting.
from rich.theme import Theme
from rich.console import Console
CONSOLE = Console( record=True, log_time=True, 
                   theme=Theme({"repr.background": "black"}) )
from rich.text import Text
# > Error handling.
from rich.traceback import install
install( show_locals=False, console=CONSOLE )
# > Progress bars.
from rich.progress import Progress
progress = Progress( console=CONSOLE )
# > Tables and panels.
from rich.panel import Panel
from rich.table import Table
from rich.style import Style
from rich.tree import Tree
from rich.markdown import Markdown


# Import other external packages.
import chime, xmltodict, yaml
import pandas as pd
import sqlalchemy.engine
chime.theme( "material" )


# Check required files.
missing_req = [ f for f in [FILE_REQ, FILE_LISTS] if not os.path.exists(f) ]
if len(missing_req) > 0:
    tmp = "file" if len(missing_req) == 1 else "files"
    CONSOLE.print( f"[bold red]* ERROR[/bold red] | [{CD}]Missing {tmp}: {",".join(missing_req)}[/{CD}]\n{R_QUIT}" )
    exit()
# Check data files.
FILES_DATA = [ 
    "people.json",
    "people.yml",
    "transfers.csv",
    "promotions.csv",
    "transactions.xml"
]
B_DATA_EXISTS = { f : os.path.exists(os.path.join(DIR_DATA, f)) for f in FILES_DATA }
b_can_add_data_files = any( B_DATA_EXISTS.values() )
# Get list of devices. FEATURE: Scalable with permanent changes!
with open( FILE_LISTS, 'rb' ) as f:
    tmp = pickle_load(f)
    DEVICES = list(tmp[0])


# Set command(s) based on OS.
dict_od = {
    "Windows": "explorer", 
    "Darwin": "open"
}
OPENER = dict_od[system()] if system() in dict_od else "xdg-open"
"""Command to open a file or directory."""


# Define function to handle VE errors.
def FUNC_capture_app_error( message: str = None ):
    """Print and save the traceback to an HTML file in the Venmito Output folder.

    Args:
        message (str, optional): A custom message to print out. Defaults to None.
    """
    # Close connection to server if possible.
    try:    VE.conn.close()
    except: pass
    # Set output and time of error.
    f_err = f"traceback {datetime.strftime( datetime.now(), "%Y %m %d, %H %M %S %f" )}.html"
    fp_err = os.path.join( DIR_ERR, f_err )
    # Print the traceback to save.
    CONSOLE.print()
    CONSOLE.print_exception( show_locals=True )
    # Save the traceback to an HTML file.
    with open( fp_err, "w+", encoding="utf-8" ) as f:
        f.write( CONSOLE.export_html() )
    
    CONSOLE.print(f"\n\n\n")
    if message:
        CONSOLE.print( fcolor( "* CUSTOM ERROR", "bold red" ) + " | " + fcolor( message, CD ) )
    # Handle error file and exit.
    err_exit = fcolor( Text(fp_err, style=Style(link=fp_err)), "gold1" ) + f"\n{R_QUIT}"
    if os.path.exists(fp_err):
        CONSOLE.print( fcolor( "* Above traceback saved to file ", CD ) + err_exit )
        Popen( [OPENER, fp_err] ) 
        sleep(1)
    else:
        CONSOLE.print( fcolor( "* Error saving traceback to file ", "bold red" ) + err_exit )
    sys.exit()


# Setup formatting objects with `rich`.
# > Function for common tables.
def FUNC_make_cmd_table( t: str, columns: dict[str, str], rows: dict[str, str] | list[dict[str, str]], bc: str ) -> Table:
    """Generic function to make a multi-section Table.

    Args:
        t (str): Table title
        columns (dict[str, str]): The column names and respective colors.
        rows (dict[str, str] | list[dict[str, str]]): Each dict entry is a row. If `list`, then each dict is a section.
        bc (str): Border and title color.

    Returns:
        Table: The table to print on the CMD.
    """    
    table = Table( title=Text( t, justify="center", style=bc ), border_style=bc )
    for k, v in columns.items():
        table.add_column( k, style=v, header_style=v )
    if len(rows) == 1:
        for k, v in rows[0].items():
            table.add_row( k, v )
    else:
        for sec in rows:
            for k, v in sec.items():
                table.add_row( k, v )
            table.add_section()
    return table

# > TABLE: Common dictionaries.
D_HQ = {
    "h / help": "Open Help Menu",
    "q / quit": f"Quit {TITLE}"
}
D_PQ = {
    "p / previous": "Return to Previous Menu",
    "q / quit": f"Quit {TITLE}"
}
D_PHQ = {
    "p / previous": "Return to Previous Menu",
    "h / help": "Open Help Menu",
    "q / quit": f"Quit {TITLE}"
}

# > TABLE: The main menu.
prefab_name = "Hot-N-Ready Report" # Must be singular.
prefab_abbr = "HNR" # Use: f"{prefab_abbr} Report"
D_MENU = {
    "1": f"{prefab_name}s",
    "2": "Create SQL Report",
    "3": "Create DeepSeek Prompt"
}
R_MENU = FUNC_make_cmd_table(
    "MAIN MENU", { "Enter": CC, "Task": "bright_cyan" }, [ D_MENU, D_HQ ], CD
)

# > TABLE: Select Output
D_OUTPUT = {
    "1": "Table Preview",
    "2": "Table Export (CSV)",
    "3": "Summary Preview",
    "4": "Summary Export",
    "5": "Graph Export"
}
R_OUTPUT = FUNC_make_cmd_table(
    "OUTPUT MENU", { "Enter": CC, "Output Type": "bright_cyan" }, [ D_OUTPUT, D_PHQ ], CD
)

# > TABLE: Task 1, Step 1 - Prefab Reports
D_PFR = {
    "1": "Single Table Output",
    "2": "View of Store Products",
    "3": "View of Transactions"
}
R_PFR = FUNC_make_cmd_table(
    f"{prefab_name.upper()} MENU", { "Enter": CC, prefab_name: "bright_cyan" }, [ D_PFR, D_PHQ ], CD
)

# > Input: Select Database Tables
D_INPUT = {
    "1": "People",
    "2": "Transfers",
    "3": "Promotions",
    "4": "Transaction IDs",
    "5": "Transaction Products"
}
R_INPUT = FUNC_make_cmd_table(
    "INPUT MENU", { "Enter": CC, "Database Table": "bright_cyan" }, [ D_INPUT, D_PHQ ], CD
)

# > Help Desk
D_HD_LEARN = {
    "1": "About & Features",
    "2": "Menu Hierarchy & Current Position",
    "3": "Print Current File Directory"
}
D_HD_ACTION = {
    "4": "Open README.md",
    "5": Text( "Open Browser to GitHub Repository (& Return to Previous Menu)", 
               style=Style( link="https://github.com/cyvu37/venmito-cyvu37" ) )
}
C_HELP_DESK = ChainMap( D_HD_LEARN, D_HD_ACTION )
R_HELP_DESK = FUNC_make_cmd_table(
    "HELP DESK", { "Enter": CC, "Action": "bright_cyan" }, [ *C_HELP_DESK.maps, D_PQ ], CH
)

# > Help 1: Program Directory Tree
#R_VE_TREE = 

# > Help 2: About & Features
#R_ABOUT = 

# > Help 3: File Directory Status
#R_VE_DIR = 




#
# PREREQUISITES Part 2: Set Up Class
#
try:

    class Process_Files():

        #

        def __init__( self, engine: sqlalchemy.engine.Engine, conn: sqlalchemy.PoolProxiedConnection, if_exists: str ):
            
            with Progress() as progress:
                n_p = len([v for v in B_DATA_EXISTS.values() if v]) + 4
                tmp1 = {}; tmp2 = {}
                DATA_PEOPLE = None
                DJ = None
                DY = None
                TRANSFERS = None
                PROMOTIONS = None
                TRANS_PRODUCTS = None
                task = progress.add_task( f"[{CD}]* Importing data...", total=n_p )
                
                # PEOPLE: Process files.
                if B_DATA_EXISTS["people.json"]:
                    DJ = {}
                    # Process data.
                    with open( os.path.join( DIR_DATA, "people.json" ), 'r' ) as f:
                        DJ = json_load( f )
                    for person in DJ:
                        tmp1[ int(person["id"]) ] = self._func_process_people_json( person )
                    # Handle database.
                    DJ = pd.DataFrame.from_dict( tmp1, orient='index' )
                    DJ["id"] = DJ["id"].astype(int)
                    progress.update( task, advance=1 )
                
                if B_DATA_EXISTS["people.yml"]:
                    DY = {}
                    # Process data.
                    with open( os.path.join( DIR_DATA, "people.yml" ), 'r' ) as f:
                        DY = yaml.safe_load( f )
                    for person in DY:
                        tmp2[ int(person["id"]) ] = self._func_process_people_yml( person )
                    # Handle database.
                    DY = pd.DataFrame.from_dict( tmp2, orient='index' )
                    DY["id"] = DY["id"].astype(int)
                    progress.update( task, advance=1 )
                
                '''# DEV NOTE: This is for handling loss of files.
                if DATA_PEOPLE == None and b_first_time:
                    # > HAPPENS WHEN `people.json` and `people.yml` don't exist while there IS NO usable data.
                    # TO DO: Rewrite code below based on changes for temporary tables mentioned above.
                    # - User must be prompted to find the right files to get rid of temporary tables.
                    sys.exit(">> [bold red]ERROR[/bold red] | Insufficient data for proper process.\nheaderting app...")
                elif DATA_PEOPLE == None and not b_first_time:
                    # > HAPPENS WHEN `people.json` and `people.yml` don't exist while there IS usable data.
                    # TO DO: Create `self._func_get_lookups()` to extract ids, emails, and phones from complete database.
                    # - `lookup_email`: `SELECT id, email FROM people`
                    # - `lookup_phone`: `SELECT id, phone FROM people`
                    pass'''
                
                # TRANSFERS: Process file.
                if B_DATA_EXISTS["transfers.csv"]:
                    TRANSFERS = pd.read_csv( os.path.join( DIR_DATA, "transfers.csv" ) )
                    TRANSFERS.columns = [ h.lower() for h in TRANSFERS.columns ]
                    progress.update( task, advance=1 )
                
                # PROMOTIONS: Process file.
                if B_DATA_EXISTS["promotions.csv"]:
                    PROMOTIONS = pd.read_csv( os.path.join( DIR_DATA, "promotions.csv" ) )
                    PROMOTIONS.columns = [ h.lower() for h in PROMOTIONS.columns ]
                    if "responded" in PROMOTIONS.columns:
                        PROMOTIONS["has_responded"] = PROMOTIONS["responded"].map({ "Yes": True, "No": False })
                        PROMOTIONS = PROMOTIONS.drop( columns=["responded"] )
                    progress.update( task, advance=1 )
                
                # TRANSACTIONS: Split into UNIQUE and PRODUCTS.
                if B_DATA_EXISTS["transactions.xml"]:
                    # Create `transaction_ids`
                    with open( os.path.join( DIR_DATA, "transactions.xml" ), 'rb' ) as f:
                        TRANS_IDS = pd.read_xml(f)
                    TRANS_IDS = TRANS_IDS.drop( columns=["items"] )
                    # Create `transaction_products`
                    with open( os.path.join( DIR_DATA, "transactions.xml" ), 'rb' ) as f:
                        TRANS_PRODUCTS = xmltodict.parse(f)["transactions"]["transaction"]
                    TRANS_PRODUCTS = self._func_process_transactions_xml( TRANS_PRODUCTS )
                    TRANS_PRODUCTS["transaction_id"] = TRANS_PRODUCTS["transaction_id"].astype(int)
                    progress.update( task, advance=1 )
                
                # Filter and organzie. DEV NOTE: Assume all files exist for now.
                if all( B_DATA_EXISTS.values() ):
                    # Merge for `people` database.
                    DATA_PEOPLE = DJ.combine_first( DY )
                    del DJ, DY
                    DATA_PEOPLE.insert(0, "id", DATA_PEOPLE.pop("id"))
                    DATA_PEOPLE.insert(1, "first_name", DATA_PEOPLE.pop("first_name"))
                    DATA_PEOPLE.insert(2, "last_name", DATA_PEOPLE.pop("last_name"))
                    
                    # Make table for products.
                    tmp1 = TRANS_PRODUCTS["item"].drop_duplicates().values
                    tmp2 = PROMOTIONS["promotion"].drop_duplicates().values
                    PRODUCTS = pd.DataFrame( list(set(tmp1) | set(tmp2)), columns=["name"] )

                    # Make table for stores.
                    STORES = pd.DataFrame( TRANS_IDS["store"].drop_duplicates().values, columns=["name"] )

                    # Create dictionaries for replacements.
                    lookup_products = {v:k for k, v in PRODUCTS.to_dict()["name"].items()}
                    lookup_emails = dict(zip( DATA_PEOPLE["email"], DATA_PEOPLE["id"] ))
                    lookup_phones = dict(zip( DATA_PEOPLE["phone"], DATA_PEOPLE["id"] ))
                    lookup_stores = {v:k for k, v in STORES.to_dict()["name"].items()}

                    # Update
                    TRANS_IDS["store_id"] = TRANS_IDS["store"].map( lookup_stores )
                    TRANS_IDS["customer_id"] = TRANS_IDS["phone"].map( lookup_phones )
                    TRANS_IDS["customer_id"] = TRANS_IDS["customer_id"].astype(int)
                    TRANS_IDS = TRANS_IDS.drop( columns=["phone", "store"] )

                    # Update
                    PROMOTIONS["product_id"] = PROMOTIONS["promotion"].map( lookup_products )
                    tmp1 = PROMOTIONS["client_email"].map( lookup_emails )
                    tmp2 = PROMOTIONS["telephone"].map( lookup_phones )
                    PROMOTIONS["customer_id"] = tmp1.fillna(tmp2)
                    PROMOTIONS["customer_id"] = PROMOTIONS["customer_id"].astype(int)
                    PROMOTIONS = PROMOTIONS.drop( columns=["client_email", "telephone", "promotion"] )
                    
                    # Update
                    TRANS_PRODUCTS["product_id"] = TRANS_PRODUCTS["item"].map( lookup_products )
                    TRANS_PRODUCTS = TRANS_PRODUCTS.drop(columns=["item"])
                    TRANS_PRODUCTS.insert(0, "transaction_id", TRANS_PRODUCTS.pop("transaction_id"))
                    TRANS_PRODUCTS.insert(1, "product_id", TRANS_PRODUCTS.pop("product_id"))

                    progress.update( task, advance=1 )
                    # Send to database + handle variables.
                    DATA_PEOPLE.to_sql( "people", engine, index=False, if_exists=if_exists )
                    TRANSFERS.to_sql( "transfers", engine, index=False, if_exists=if_exists )
                    PROMOTIONS.to_sql( "promotions", engine, index=False, if_exists=if_exists )
                    TRANS_IDS.to_sql( "transaction_ids", engine, index=False, if_exists=if_exists )
                    TRANS_PRODUCTS.to_sql( "transaction_products", engine, index=False, if_exists=if_exists )
                    PRODUCTS.to_sql( "products", engine, index=True, index_label="id", if_exists=if_exists )
                    STORES.to_sql( "stores", engine, index=True, index_label="id", if_exists=if_exists )
                    del DATA_PEOPLE, TRANSFERS, PROMOTIONS, TRANS_IDS, TRANS_PRODUCTS
                    progress.update( task, advance=1 )
                
                    # Update all tables in database.
                    cur = conn.cursor()
                    cur.execute("ALTER TABLE people " + 
                                "ADD CONSTRAINT unique_person PRIMARY KEY (id)")
                    cur.execute("ALTER TABLE transfers " + 
                                "ADD FOREIGN KEY (sender_id) REFERENCES people(id), " + 
                                "ADD FOREIGN KEY (recipient_id) REFERENCES people(id)")
                    cur.execute("ALTER TABLE products " + 
                                "ADD CONSTRAINT unique_product PRIMARY KEY (id)")
                    cur.execute("ALTER TABLE stores " + 
                                "ADD CONSTRAINT unique_store PRIMARY KEY (id)")
                    cur.execute("ALTER TABLE promotions " + 
                                "ADD CONSTRAINT unique_promotion PRIMARY KEY (id), " + 
                                "ADD FOREIGN KEY (customer_id) REFERENCES people(id), " + 
                                "ADD FOREIGN KEY (product_id) REFERENCES products(id)")
                    cur.execute("ALTER TABLE transaction_ids " + 
                                "ADD CONSTRAINT unique_transaction PRIMARY KEY (id), " + 
                                "ADD FOREIGN KEY (customer_id) REFERENCES people(id)")
                    cur.execute("ALTER TABLE transaction_products " + 
                                "ADD FOREIGN KEY (transaction_id) REFERENCES transaction_ids(id), " + 
                                "ADD FOREIGN KEY (product_id) REFERENCES products(id)")
                    cur.execute("ALTER TABLE people ALTER COLUMN dob TYPE DATE USING dob::date")
                    cur.execute("ALTER TABLE promotions ALTER COLUMN promotion_date TYPE DATE USING promotion_date::date")
                    conn.commit()
                    cur.close()
                    progress.update( task, advance=1 )
                    
                    cur = conn.cursor()
                    cur.execute( """
                                CREATE OR REPLACE VIEW view_transaction_info AS 
                                    SELECT t1.id, t1.date, t2.first_name, t2.last_name, t3.name "store"
                                    FROM transaction_ids as t1 
                                    LEFT JOIN people as t2 ON t1.customer_id = t2.id
                                    LEFT JOIN stores as t3 ON t1.store_id = t3.id
                                """ ) # DEV NOTE: Merge first and last names.
                    cur.execute( """
                                CREATE OR REPLACE VIEW view_transaction_full AS 
                                    SELECT t1.transaction_id, t2.date, t4.name "store", t3.first_name, t3.last_name, t5.name "product", t1.price, t1.price_per_item, t1.quantity
                                    FROM transaction_products as t1 
                                    LEFT JOIN transaction_ids as t2 on t1.transaction_id = t2.id  
                                    LEFT JOIN people as t3 ON t2.customer_id = t3.id 
                                    LEFT JOIN stores as t4 ON t2.store_id = t4.id 
                                    LEFT JOIN products as t5 ON t1.product_id = t5.id
                                    ORDER BY transaction_id, store, product
                                """ )
                    cur.execute( """
                                CREATE OR REPLACE VIEW view_store_products AS 
                                    SELECT DISTINCT t4.name "store", t3.name "product" 
                                    FROM transaction_products as t1
                                    LEFT JOIN transaction_ids as t2 on t1.transaction_id = t2.id
                                    LEFT JOIN products as t3 on t1.product_id = t3.id
                                    LEFT JOIN stores as t4 on t2.store_id = t4.id
                                    ORDER BY store, product
                                """ ) # DEV NOTE: Test and edit.
                    # DEV NOTE: If working, then create trigger function to auto-update.
                    conn.commit()
                    cur.close()
                    progress.update( task, advance=1 )


        def _func_process_people_json( self, input: dict ) -> dict:
            """
            Function to reorganize all parts of `people.json`. FEATURE: Scalable for new exceptions!
            """
            output = {}
            for k, v in input.items():
                k = k.lower()
                match k:
                    case "location":
                        # Get `{'City': ..., 'Country': ...}`.
                        output.update({ key.lower():value for key, value in v.items() })
                    case "telephone":
                        # Change "telephone" to "phone".
                        output["phone"] = v
                    case "dob":
                        try:
                            output["dob"] = datetime.strftime( parse(v), "%Y-%m-%d" )
                        except:
                            output["dob"] = v
                    case "devices":
                        # Get `"devices": [...]`.
                        output["has_android"] = "Android" in v
                        output["has_iphone"] = "Iphone" in v
                        output["has_desktop"] = "Desktop" in v
                        
                        """# TO DO: This is a draft for a loop to keep track of new devices.
                        for device in v:
                            device = device.lower()
                            # The device in the list exists.
                            output[f'has_{device}'] = True
                            # Add any new device.
                            if device not in self.devices:
                                self.b_new_devices = True
                                self.devices.append(device)
                        # Any devices from default list `self.devices` not in `v` don't exist.
                        for device in self.devices:
                            if device not in v:
                                output[f'has_{device}'] = False"""
                    case _:
                        output[k.lower()] = v
            '''if self.b_new_devices:
                # TO DO: Open `FILE_LISTS` and update `self.devices` list.
                self.b_new_devices = False'''
            return output


        def _func_process_people_yml( self, input: dict ) -> dict:
            """
            Function to reorganize all parts of `people.yml`. FEATURE: Scalable for new exceptions!
            """
            output = {}
            for k, v in input.items():
                k = k.lower()
                match k:
                    case "name":
                        # Split "name" into first and last names.
                        spl = v.split(" ")
                        output["first_name"] = spl[0]
                        if len(spl) == 2:
                            output["last_name"] = spl[1]
                    case "city":
                        vs = v.split(", ")
                        output["city"] = vs[0]
                        output["country"] = vs[1]
                    case "dob":
                        try:
                            output["dob"] = datetime.strftime( parse(v), "%Y-%m-%d" )
                        except:
                            output["dob"] = v
                    case "android":
                        output[f"has_{k}"] = bool(v)
                    case "iphone":
                        output[f"has_{k}"] = bool(v)
                    case "desktop":
                        output[f"has_{k}"] = bool(v)
                    case _:
                        output[k] = v
            return output


        def _func_process_transfers_csv( self, input: pd.DataFrame ) -> dict:
            """
            Empty function to reorganize all parts of `transfers.csv`. FEATURE: Scalable for new exceptions!
            """
            output = {}
            for k, v in input.items():
                k = k.lower()
                match k:
                    # FEATURE: Add exceptions here.
                    case _:
                        output[k] = v
            return output

        
        def _func_process_item( self, item_info: dict, id ) -> dict:
            """
            Function to process each nested item of a transaction in `transactions.xml` for `transactions_products`.
            
            FEATURE: Scalable for new exceptions!
            """
            item_row = {"transaction_id":id}
            for k, v in item_info.items():
                k = k.lower()
                match k:
                    case "price":
                        item_row[k] = int(v)
                    case "price_per_item":
                        item_row[k] = int(v)
                    case "quantity":
                        item_row[k] = int(v)
                    case _:
                        item_row[k] = v
            return item_row


        def _func_process_transactions_xml( self, DT: dict ):
            """
            Function to process the items of each transaction of `transactions.xml` for `transactions_products`.
            """
            res = []
            for transaction in DT:
                items = transaction["items"]["item"]
                if isinstance(items, dict):
                    res.append( self._func_process_item( items, transaction["@id"] ) )
                elif isinstance(items, list):
                    res.extend( [ self._func_process_item( item, transaction["@id"] ) for item in items ] )
            return pd.DataFrame( res )
            





    class Venmito_Evaluator():
        """
        Master class for handling database and commands in the CLI.
        """

        b_can_add_data_files = any( B_DATA_EXISTS.values() )
        b_new_devices = False
        devices = ["android", "desktop", "iphone"]
        engine: sqlalchemy.engine.Engine
        conn: sqlalchemy.PoolProxiedConnection

        msg = {
            "top": f"{T} Menu Lvl 1",
            "top_color": CD,
            "mid": "What would you like to do?",
            "mid_color": CD,
            "bot": f"{T} Status",
            "bot_color": CD,
            "border_color": CD
        }
        b_msg_change = False

        i_menu = ""
        """Current index of MAIN MENU selection."""
        i_help = ""
        """Current index of HELP DESK selection."""
        i_output = ""
        """Current index of OUTPUT selection."""
        i_pfr = ""
        """Current index of PREFAB REPORT selection."""
        i_input = ""
        """Current index of INPUT selection."""

        def __init__( self ):
            #CONSOLE.print(f"[orange1]* DEV MODE: Skipping database connection and setup...[/orange1]")
            try:
                self.engine = sqlalchemy.engine.create_engine( "postgresql+psycopg://postgres:Space!3742@localhost:5432/postgres" )
                self.conn = self.engine.raw_connection()
            except:
                # TO DO: Set up server from scratch here??
                FUNC_capture_app_error("Can't connect to database.")

            # Check if tables exist.
            b_first_time = CONSOLE.input(f"[{CD}]* Would you like to start from scratch? {R_YN}\n> [/{CD}]")
            if b_first_time.lower() == "y":
                CONSOLE.print(f"[{CD}]* Starting from scratch...[/{CD}]")
                self._func_first_time()
            
            CONSOLE.print(
                fcolor("* All prerequisites satisfied!", CD) + "\n" + 
                fcolor("* Output saved to directory ", CD ) + fcolor(f"\"{DIR_OUTPUT}\"", "gold1") +
                f"\n\n\n{R_ENTER}"
            )
            self.func_l1_menu_loop()


        def _func_quit( self ):
            try: VE.conn.close()
            except: pass
            CONSOLE.print(R_QUIT)
            sys.exit()


        def _func_first_time( self ):
            self._func_reset_database()
            if self.b_can_add_data_files:
                Process_Files( self.engine, self.conn, "replace" )
            else:
                CONSOLE.print( f"[bold red]* ERROR[/bold red] | [{CD}]No valid files detected in `data` folder. Can't continue.[/{CD}]\n{R_QUIT}" )
                sys.exit()


        def _func_reset_database( self ):
            cur = self.conn.cursor()
            cur.execute( "DROP TABLE IF EXISTS people CASCADE" )
            cur.execute( "DROP TABLE IF EXISTS transfers CASCADE" )
            cur.execute( "DROP TABLE IF EXISTS products CASCADE" )
            cur.execute( "DROP TABLE IF EXISTS stores CASCADE" )
            cur.execute( "DROP TABLE IF EXISTS promotions CASCADE" )
            cur.execute( "DROP TABLE IF EXISTS transaction_ids CASCADE" )
            cur.execute( "DROP TABLE IF EXISTS transaction_products CASCADE" )
            cur.execute( "DROP VIEW IF EXISTS view_transaction_info CASCADE" )
            cur.execute( "DROP VIEW IF EXISTS view_transaction_full CASCADE" )
            cur.execute( "DROP VIEW IF EXISTS view_store_products CASCADE" )
            self.conn.commit()
            cur.close()

        
        def _func_msg_bubble( self, default_msg: dict ):
            if not self.b_msg_change:
                self.msg.update({ "top_color": CD, "mid_color": CD, "bot_color": CD, "border_color": CD })
                self.msg.update( default_msg )
            # Print message bubble.
            CONSOLE.print("\n")
            CONSOLE.print( Panel(
                Text( self.msg["mid"], justify="center", style=Style( color=self.msg["mid_color"], italic=True ) ), 
                title=Text( self.msg["top"], style=Style( color=self.msg["top_color"] ) ),
                subtitle=Text( self.msg["bot"], style=Style( color=self.msg["bot_color"] ) ),
                border_style=self.msg["border_color"], width=WIDTH, padding=(1,1)
            ) )
            CONSOLE.print("\n")
            # Reset default variables.
            self.b_msg_change = False
        

        def _func_other_entries( self, inp: str ):
            match inp:
                case "q" | "quit":
                    self._func_quit()
                case "":
                    self.b_msg_change = True
                    self.msg.update({"bot": "No input. Try again.", 
                                     "bot_color": "orange1", "border_color": "orange1"})
                case _:
                    self.b_msg_change = True
                    self.msg.update({"bot": f"Invalid input: {inp}. Try again.", 
                                     "bot_color": "orange1", "border_color": "orange1"})
        

        def func_l1_menu_loop( self ):
            """
            Loop to allow user to keep using this program after finishing a task.

            The Level 1 command for nested loop handling.
            """
            default_msg = deepcopy( self.msg )
            while True:
                self._func_msg_bubble( default_msg )
                # Print menu + get input.
                CONSOLE.print(R_MENU)
                self.i_menu = CONSOLE.input("> ").lower()
                match self.i_menu:
                    case "1":
                        self.func_l2_t1s1_output()
                    case "2":
                        self.func_l2_t2s1_output()
                    case "3":
                        ### DEV NOTE: Dead end right now.
                        self.b_msg_change = True
                        self.msg.update({
                            "bot": f"DEV NOTE | {D_MENU[self.i_menu]}: Under construction.",
                            "bot_color": "orange1", "border_color": "orange1"
                            })
                    case "h" | "help":
                        self.func_helpdesk( R_MENU.title, D_MENU )
                    case _:
                        self._func_other_entries( self.i_menu )

        
        def func_helpdesk( self, menu_title: str, menu: dict[str, str] ):
            """
            Open the HELP DESK menu.

            A Level 1 command for nested loop handling.
            """
            default_msg = {
                "top": f"{T} Help Lvl 1 | From {menu_title}", "top_color": CH,
                "mid": "What would you like to know or do?",
                "bot": "VE Status", "bot_color": CH, "border_color": CH
            }
            self.msg.update( default_msg )
            CONSOLE.print(f"\n\n{R_LINE}\n")
            while True:
                self._func_msg_bubble( default_msg )
                # Print menu + get input.
                CONSOLE.print(R_HELP_DESK)
                self.i_help = CONSOLE.input("> ").lower()
                match self.i_help:
                    case "1" | "2" | "3" | "4":
                        ### DEV NOTE: Dead end right now.
                        self.b_msg_change = True
                        self.msg.update({
                            "bot": f"DEV NOTE | {D_MENU[self.i_menu]}: Under construction.",
                            "bot_color": "orange1", "border_color": "orange1"
                            })
                    case "5":
                        self.b_msg_change = True
                        try:
                            open_new_tab( "https://github.com/cyvu37/venmito-cyvu37" )
                            self.msg.update({"bot": "Website opened in local browser.", "bot_color": "bright_green"})
                        except:
                            self.msg.update({"bot": "Couldn't open GitHub.", "bot_color": "orange1"})
                    case "p" | "previous":
                        break
                    case _:
                        self._func_other_entries( self.i_help )

        
        def func_l2_t1s1_output( self ):
            """
            Loop for Step 1 of Task 1: Prefab Reports
            > Step 1: Select Output type.
            * Step 2: Select Prefab report.
            * Step 3, if applicable: Select Input type.
            
            A Level 2 command for nested loop handling.
            """
            default_msg = { 
                "top": f"{T} Menu Lvl 2 | {D_MENU[self.i_menu]}",
                "mid": "Step 1: Select an output type.",
                "bot": "Output: N/A, Report: N/A"
            }
            self.msg.update( default_msg )
            while True:
                self._func_msg_bubble( default_msg )
                CONSOLE.print(R_OUTPUT)
                self.i_output = CONSOLE.input("> ").lower()
                if self.i_output in D_OUTPUT.keys():
                    self.func_l3_t1s2_report()
                else:
                    match self.i_output:
                        case "p" | "previous":
                            break
                        case "h" | "help":
                            self.func_helpdesk( R_OUTPUT.title, D_OUTPUT )
                        case _:
                            self._func_other_entries( self.i_output )

        
        def func_l3_t1s2_report( self ):
            """
            Loop for Step 2 of Task 1: Prefab Reports
            * Step 1: Select Output type.
            > Step 2: Select Prefab report.
            * Step 3, if applicable: Select Input type.
            
            A Level 3 command for nested loop handling.
            """
            default_msg = { 
                "top": f"{T} Menu Lvl 3 | {D_MENU[self.i_menu]}",
                "mid": "Step 2: Select a report type.",
                "bot": f"Output: {D_OUTPUT[self.i_output]}, Report: N/A"
            }
            self.msg.update( default_msg )
            while True:
                self._func_msg_bubble( default_msg )
                CONSOLE.print(R_PFR)
                self.i_pfr = CONSOLE.input("> ").lower()
                match self.i_pfr:
                    case "1":
                        self.func_l4_t1c1_input()
                    case "2":
                        self.func_l4_t1c2_view_store_products()
                        ### DEV NOTE: Dead end right now.
                        self.b_msg_change = True
                        self.msg.update({
                            "bot": f"DEV NOTE | {D_PFR[self.i_pfr]}: Under construction. Try [1].",
                            "bot_color": "orange1", "border_color": "orange1"
                            })
                    case "3":
                        self.func_l4_t1c3_view_transactions()
                        ### DEV NOTE: Dead end right now.
                        self.b_msg_change = True
                        self.msg.update({
                            "bot": f"DEV NOTE | {D_PFR[self.i_pfr]}: Under construction. Try [1].",
                            "bot_color": "orange1", "border_color": "orange1"
                            })
                    case "p" | "previous":
                        break
                    case "h" | "help":
                        self.func_helpdesk( R_PFR.title, D_PFR )
                    case _:
                        self._func_other_entries( self.i_pfr )

        
        def func_l4_t1c1_input( self ):
            """
            Loop for Step 3 of Task 1: Prefab Reports
            * Step 1: Select Output type.
            * Step 2: Select single table output.
            > Step 3: Select Input type.
            
            A Level 4 command for nested loop handling.
            """
            default_msg = { 
                "top": f"{T} Menu Lvl 4 | {D_MENU[self.i_menu]}",
                "mid": "Step 3: Select an input type.",
                "bot": f"Output: {D_OUTPUT[self.i_output]}, Report: {D_PFR[self.i_pfr]}, Input: N/A"
            }
            self.msg.update( default_msg )
            while True:
                self._func_msg_bubble( default_msg )
                CONSOLE.print(R_INPUT)
                self.i_input = CONSOLE.input("> ").lower()
                print(self.i_input)
                print(self.i_input in D_INPUT.keys())
                if self.i_input in D_INPUT.keys():
                    ### DEV NOTE: Dead end right now.
                    self.b_msg_change = True
                    self.msg.update({
                        "bot": f"DEV NOTE | {D_INPUT[self.i_input]}: Under construction.",
                        "bot_color": "orange1", "border_color": "orange1"
                        })
                else:
                    match self.i_input:
                        case "p" | "previous":
                            break
                        case "h" | "help":
                            self.func_helpdesk( R_INPUT.title, D_INPUT )
                        case _:
                            self._func_other_entries( self.i_input )

        
        def func_l4_t1c2_view_store_products( self ):
            """
            Prefab Report w/ Output: View of Store Products
            
            A Level 4 command for nested loop handling.
            """
            pass

        
        def func_l4_t1c3_view_transactions( self ):
            """
            Prefab Report w/ Output: View Transactions
            
            A Level 4 command for nested loop handling.
            """
            pass

        
        def func_l2_t2s1_output( self ):
            """
            Loop for getting output for Task 2: Create SQL Report
            > Step 1: Select Output type.
            > Step 2: Write SQL command. 

            A Level 2 command for nested loop handling.
            """
            default_msg = {
                "top": f"{T} Menu Lvl 2 | {D_MENU[self.i_menu]}",
                "mid": "Step 1/2: Select an output type for your SQL report.",
                "bot": "Output: N/A"
            }
            self.msg.update( default_msg )
            while True:
                self._func_msg_bubble( default_msg )
                CONSOLE.print(R_OUTPUT)
                self.i_output = CONSOLE.input("> ").lower()
                if self.i_output in D_OUTPUT.keys():
                    ### DEV NOTE: Make function to let user write SQL command.
                    self.b_msg_change = True
                    self.msg.update({
                        "bot": f"DEV NOTE | {D_OUTPUT[self.i_output]}: Under construction.",
                        "bot_color": "orange1", "border_color": "orange1"
                        })
                else:
                    match self.i_output:
                        case "p" | "previous":
                            break
                        case "h" | "help":
                            self.func_helpdesk( R_OUTPUT.title, D_OUTPUT )
                        case _:
                            self._func_other_entries( self.i_output )



    if __name__ == "__main__":
        VE = Venmito_Evaluator()



except Exception as e:
    FUNC_capture_app_error()