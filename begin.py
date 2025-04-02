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
# PREREQUISITES Part 1: Check Packages
#
TITLE = "Venmito Evaluator"
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


# Set formatting features.
WIDTH = 100
"""Width of printing borders and aligned text."""
BORDER = "<"*(WIDTH//2) + ">"*(WIDTH//2)
def mid( input: str, has_color: bool = False ):
    """Aligns text to the middle of the CMD by `WIDTH`."""
    l = len(re.sub( r"\[.*?\]", "", input )) if has_color else len(input)
    spaces = " "*(( WIDTH-l )//2)
    return spaces + input + spaces
def fcolor( message: str, color: str ):
    """Sets a `message` in `color`."""
    return f"[{color}]{message}[/{color}]"
C = "bright_cyan"
LINE = fcolor( WIDTH * "-", C )
HEADER = mid( f"< < <   {fcolor(TITLE.upper(), C)}   > > >", True )
QUIT1 = f"* Quitting app...\n\n{HEADER}\n{BORDER}\n"
"""Default color for normal messages."""
YN = f"[{C}]([/{C}][green]y[/green][{C}]/[/{C}][red]n[/red][{C}])[/{C}]"
"""Default yes/no prompt."""
ENTER = fcolor( f"{BORDER}\n{HEADER}", "green1" )
QUIT2 = fcolor( f"* Quitting app...\n\n\n{HEADER}\n{BORDER}\n", "blue1" )


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


# Check required files.
missing_req = [ f for f in [FILE_REQ, FILE_LISTS] if not os.path.exists(f) ]
if len(missing_req) > 0:
    tmp = "file" if len(missing_req) == 1 else "files"
    sys.exit( f"* ERROR | Missing {tmp}: {",".join(missing_req)}\n{QUIT1}" )
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


# Package check: Offline check.
cutoff_symbols = ["==", "["]
with open(FILE_REQ, "r") as r:
    req_pkgs = [ i.split( next(( s for s in cutoff_symbols if s in i ), None) )[0].lower() for i in r.readlines() ]
curr_pkgs = [ "-".join( dist.metadata["Name"].lower().split("_") ) for dist in distributions() ]
miss_pkgs = [ x for x in req_pkgs if x not in curr_pkgs ]


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
        sys.exit( f"\n\n* ERROR | Missing {tmp}: {",".join(miss_pkgs)}\n{QUIT1}" )
    print("\n* Packages installed successfully.")


# Import `rich` features.
# > Console formatting.
from rich.console import Console
CONSOLE = Console( record=True )
from rich.text import Text
# > Error handling.
from rich.traceback import install
install( show_locals=False, console=CONSOLE )
# > Progress bars.
from rich.progress import Progress
progress = Progress( console=CONSOLE )
# > Tables and panels.
from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.style import Style


# Import other external packages.
import chime, xmltodict, yaml
import pandas as pd
import sqlalchemy.engine
chime.theme( "material" )


# Define function to handle VE errors.
VE = None
def capture_app_error( message: str = None ):
    """Print and save the traceback to an HTML file in the Venmito Output folder.

    Args:
        message (str, optional): A custom message to print out. Defaults to None.
    """
    # Close connection to server if possible.
    try:    VE.conn.close()
    except: pass
    # Print the traceback to save.
    CONSOLE.print()
    CONSOLE.print_exception( show_locals=True )
    # Save the traceback to an HTML file.
    f_err = f"traceback {datetime.strftime( datetime.now(), "%Y %m %d, %H %M %S %f" )}.html"
    fp_err = os.path.join( DIR_ERR, f_err )
    with open( fp_err, "w+", encoding="utf-8" ) as f:
        f.write( CONSOLE.export_html() )
    CONSOLE.print(f"\n\n\n")
    if message:
        CONSOLE.print(fcolor( "* CUSTOM ERROR", "bold red" ) + " | " + fcolor( message, C ))
    CONSOLE.print(fcolor( "* Above traceback saved to", C ) + " " + fcolor( f"\"{fp_err}\"", "gold1" ) + f"\n{QUIT2}")
    Popen( [OPENER, fp_err] ) 
    sleep(1)
    sys.exit()


# Setup formatting objects with `rich`.
# > Function for common tables.
def make_cmd_table( t: str, columns: dict[str], rows: list[dict[str]] ) -> Table:
    """Generic function to make a 2-section action table of up to 4 columns.

    Args:
        t (str): Table title
        columns (dict[str]): The column names and respective colors.
        rows (list[dict[str]]): Each dictionary is a section. Each dict entry is a row.

    Returns:
        Table: The CMD table.
    """
    table = Table( title=Text( t, justify="center", style="sea_green2" ) )
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

# > The main menu.
prefab_name = "Prefab Report"
prefab_abbr = "Prefab" # Ends with " Report"
D_MENU = {
    "1": f"{prefab_name}s",
    "2": "Create SQL Report",
    "3": "Create DeepSeek Prompt"
}
P_MENU = make_cmd_table(
    "MAIN MENU", { "Enter": "gold1", "Task": "bright_cyan" }, 
    [D_MENU,
    {
        "h / help": "Open Help Menu",
        "q / quit": f"Quit {TITLE}"
    }]
)

# > Select Output
D_OUTPUT = {
    "1": "Table Preview",
    "2": "Table Export (CSV)",
    "3": "Summary Preview",
    "4": "Summary Export",
    "5": "Graph Export"
}
P_OUTPUT = make_cmd_table(
    "SELECT OUTPUT", { "Enter": "gold1", "Output Type": "bright_cyan" }, 
    [D_OUTPUT, 
    {
        "p / previous": "Return to Main Menu",
        "h / help": "Open Help Menu",
        "q / quit": f"Quit {TITLE}"
    }]
)

# > Task 1
D_HNRR = {
    "1": "Single Table Output",
    "2": "View of Store Products",
    "3": "View of Transactions"
}
P_HNRR = make_cmd_table(
    f"SELECT {prefab_name.upper()}", { "Enter": "gold1", prefab_name: "bright_cyan" }, 
    [D_HNRR, 
    {
        "p / previous": "Return to Previous Menu",
        "h / help": "Open Help Menu",
        "q / quit": f"Quit {TITLE}"
    }]
)

# > Select Tables, Views, Etc.
D_INPUT = {
    "1": "People",
    "2": "Transfers",
    "3": "Promotions",
    "4": "Transaction IDs",
    "5": "Transaction Products"
}
P_INPUT = make_cmd_table(
    "SELECT INPUT", { "Enter": "gold1", "Table": "bright_cyan" }, 
    [D_INPUT, 
    {
        "p / previous": "Return to Previous Menu",
        "h / help": "Open Help Menu",
        "q / quit": f"Quit {TITLE}"
    }]
)

# > The Help Menu
P_HELP_MENU = Table( 
    title=Text( "HELP MENU [TBF]", justify="center", style="sea_green2" ), 
    show_lines=True, width=WIDTH, box=box.DOUBLE
    )
"""The Help Menu."""
P_HELP_MENU.add_column( "Task", style="gold1", header_style="gold1" )
P_HELP_MENU.add_column( "Meaning", style="bright_cyan", header_style="bright_cyan" )
tmp = """Prefabricated scripts to generate reports.
X
X"""
P_HELP_MENU.add_row( f"{prefab_name}s", tmp )
tmp = """X
X
X"""
P_HELP_MENU.add_row( "Create SQL Report", tmp )
tmp = """X
X
X"""
P_HELP_MENU.add_row( "Create DeepSeek Prompt", tmp )

# > The Help Desk
P_HELP_DESK = make_cmd_table(
    "HELP DESK", { "Enter": "gold1", "Action": "bright_cyan" },
    [{
        "g / github": "Open the GitHub Repository & Return to Previous Menu",
        "p / prev": "Return to Previous Menu",
        "q / quit": f"Quit {TITLE}"
    }]
)




#
# PREREQUISITES Part 2: Set Up Class
#
try:

    class Venmito_Evaluator():
        """
        Master class for handling database and commands in the CLI.
        """

        b_can_add_data_files = any( B_DATA_EXISTS.values() )
        b_new_devices = False
        devices = ["android", "desktop", "iphone"]
        engine: sqlalchemy.engine.Engine
        conn: sqlalchemy.PoolProxiedConnection
    
        bubble_txt = ""
        bubble_sty = ""
        b_change_lH = False
        b_change_l1 = False
        b_change_l2 = False
        b_change_l3 = False
        b_change_l4 = False
        """Must the default message be changed or not, including errors?"""

        i_menu = ""
        i_output = ""
        i_hnrr = ""
        i_input = ""

        def __init__( self ):
            CONSOLE.print(f"[orange1]* DEV MODE: Skipping database connection and setup...[/orange1]")
            try:
                self.engine = sqlalchemy.engine.create_engine( "postgresql+psycopg://postgres:Space!3742@localhost:5432/postgres" )
                self.conn = self.engine.raw_connection()
            except:
                # TO DO: Set up server from scratch here??
                capture_app_error("Can't connect to database.")

            # Check if tables exist.
            b_first_time = CONSOLE.input(f"[{C}]* Would you like to start from scratch?[/{C}] {YN}\n> ")
            if b_first_time.lower() == "y":
                CONSOLE.print(f"[{C}]* Starting from scratch...[/{C}]")
                self._func_first_time()
            
            CONSOLE.print(fcolor("* All prerequisites satisfied!", C) + "\n" + 
                          fcolor("* Output saved to ", C ) + fcolor(f"\"{DIR_OUTPUT}\"", "gold1") +
                          f"\n\n\n{ENTER}")
            #CONSOLE.print(f"[{C}]* All prerequisites satisfied![/{C}]\n\n\n{ENTER}")
            self.func_l1_menu_loop()


        def _func_first_time( self ):
            self._func_reset_database()
            #self._func_create_tables()
            if self.b_can_add_data_files:
                self._func_process_master()
                #self._func_handle_views()
            else:
                CONSOLE.print( f"[bold red]* ERROR[/bold red] | [{C}]No valid files detected in `data` folder.[/{C}]\n{QUIT2}" )
                sys.exit()


        def _func_reset_database( self ):
            cur = self.conn.cursor()
            cur.execute( "DROP TABLE IF EXISTS people CASCADE" )
            cur.execute( "DROP TABLE IF EXISTS transfers CASCADE" )
            cur.execute( "DROP TABLE IF EXISTS promotions CASCADE" )
            cur.execute( "DROP TABLE IF EXISTS transaction_ids CASCADE" )
            cur.execute( "DROP TABLE IF EXISTS transaction_products CASCADE" )
            cur.execute( "DROP VIEW IF EXISTS view_store_products CASCADE" )
            cur.execute( "DROP VIEW IF EXISTS view_transactions CASCADE" )
            self.conn.commit()
            cur.close()


        def _func_create_tables( self ):
            """
            Create tables with foreign key attributes and other features. 
            
            If tables exist and are broken, run `self._func_reset_database()` first.
            """
            cur = self.conn.cursor()
            cur.execute( """
                        CREATE TABLE people ( 
                            id INTEGER PRIMARY KEY, 
                            first_name TEXT, 
                            last_name TEXT, 
                            phone TEXT UNIQUE, 
                            email TEXT UNIQUE, 
                            city TEXT, 
                            country TEXT, 
                            android BOOLEAN, 
                            iphone BOOLEAN, 
                            desktop BOOLEAN 
                        )""" )
            cur.execute( """
                        CREATE TABLE transfers ( 
                            sender_id INTEGER REFERENCES people(id), 
                            recipient_id INTEGER REFERENCES people(id), 
                            amount FLOAT, 
                            date DATE
                        )""" )
            cur.execute( """
                        CREATE TABLE promotions ( 
                            id INTEGER PRIMARY KEY, 
                            customer_id INTEGER, 
                            promotion TEXT, 
                            responded BOOLEAN, 
                            FOREIGN KEY(customer_id) REFERENCES people(id) 
                        )""" )
            cur.execute( """
                        CREATE TABLE transaction_ids ( 
                            id INTEGER PRIMARY KEY, 
                            customer_id INTEGER, 
                            store TEXT, 
                            FOREIGN KEY(customer_id) REFERENCES people(id)
                        )""" )
            cur.execute( """
                        CREATE TABLE transaction_products ( 
                            transaction_id INTEGER, 
                            item TEXT, 
                            price FLOAT, 
                            price_per_item FLOAT, 
                            quantity INTEGER, 
                            FOREIGN KEY(transaction_id) REFERENCES transaction_ids(id) 
                        )""" )
            self.conn.commit()
            cur.close()


        def _func_handle_views( self ):
            """
            Create or replace views. 
            
            If views exist and are broken, run `self._func_reset_database()` first.
            """
            cur = self.conn.cursor()
            cur.execute( """
                        CREATE OR REPLACE VIEW view_store_products AS 
                            SELECT t1.store, t2.item 
                            FROM transaction_ids as t1 
                            LEFT JOIN transaction_products as t2 ON t1.id = t2.transaction_id
                        """ ) # DEV NOTE: Test and edit.
            cur.execute( """
                        CREATE OR REPLACE VIEW view_transactions AS 
                            SELECT t1.id, t1.customer_id, t1.store, t2.item, t2.price, t2.price_per_item, t2.quantity 
                            FROM transaction_ids as t1 
                            LEFT JOIN transaction_products as t2 ON t1.id = t2.transaction_id
                        """ ) # DEV NOTE: Test and edit.
            self.conn.commit()
            cur.close()


        def _func_process_master( self ):
            """
            Can only run when there are any files to process.
            """
            with Progress() as progress:
                n_p = len([v for v in B_DATA_EXISTS.values() if v]) + 2
                DATA_PEOPLE = None
                DJ = None
                DY = None
                TRANSFERS = None
                PROMOTIONS = None
                TRANS_PRODUCTS = None
                task = progress.add_task( f"[{C}]*Processing files...", total=n_p )
                
                # PEOPLE: Process files.
                if B_DATA_EXISTS["people.json"]:
                    DJ = {}; dj = {}
                    # Process data.
                    with open( os.path.join( DIR_DATA, "people.json" ), 'r' ) as f:
                        DJ = json_load( f )
                    for person in DJ:
                        dj[ int(person["id"]) ] = self._func_process_people_json( person )
                    # Handle database.
                    DJ = pd.DataFrame.from_dict( dj, orient='index' )
                    del dj
                    progress.update( task, advance=1 )
                
                if B_DATA_EXISTS["people.yml"]:
                    DY = {}; dy = {}
                    # Process data.
                    with open( os.path.join( DIR_DATA, "people.yml" ), 'r' ) as f:
                        DY = yaml.safe_load( f )
                    for person in DY:
                        dy[ int(person["id"]) ] = self._func_process_people_yml( person )
                    # Handle database.
                    DY = pd.DataFrame.from_dict( dy, orient='index' )
                    del dy
                    progress.update( task, advance=1 )
                
                '''# DEV NOTE: This is for handling loss of files.
                if DATA_PEOPLE == None and b_first_time:
                    # > HAPPENS WHEN `people.json` and `people.yml` don't exist while there IS NO usable data.
                    # TO DO: Rewrite code below based on changes for temporary tables mentioned above.
                    # - User must be prompted to find the right files to get rid of temporary tables.
                    sys.exit(">> [bold red]ERROR[/bold red] | Insufficient data for proper process.\nQuitting app...")
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
                    '''if "date" in TRANSFERS.columns:
                        TRANSFERS["date"] = [ datetime.strftime( datetime.strptime( e, "%Y-%m-%d" ), "%d-%m-%Y" ) for e in TRANSFERS["date"] ]'''
                    progress.update( task, advance=1 )
                
                # PROMOTIONS: Process file.
                if B_DATA_EXISTS["promotions.csv"]:
                    PROMOTIONS = pd.read_csv( os.path.join( DIR_DATA, "promotions.csv" ) )
                    PROMOTIONS.columns = [ h.lower() for h in PROMOTIONS.columns ]
                    PROMOTIONS["responded"] = PROMOTIONS["responded"].map({ "Yes":True, "No":False })
                    progress.update( task, advance=1 )
                
                # TRANSACTIONS: Split into UNIQUE and PRODUCTS.
                if B_DATA_EXISTS["transactions.xml"]:
                    with open( os.path.join( DIR_DATA, "transactions.xml" ), 'rb' ) as f:
                        TRANS_UNIQUE = pd.read_xml(f)
                    if "items" in TRANS_UNIQUE.columns:
                        TRANS_UNIQUE = TRANS_UNIQUE.drop( columns=["items"] )
                    with open( os.path.join( DIR_DATA, "transactions.xml" ), 'rb' ) as f:
                        DT = xmltodict.parse(f)["transactions"]["transaction"]
                    TRANS_PRODUCTS = self._func_process_transactions_xml( DT )
                    progress.update( task, advance=1 )
                
                # Filter and organzie. DEV NOTE: Assume all files exist for now.
                if all( B_DATA_EXISTS.values() ):
                    # Make DATA_PEOPLE.
                    DATA_PEOPLE = pd.concat( [DJ, DY], ignore_index=True )
                    del DJ, DY
                    DATA_PEOPLE = DATA_PEOPLE.astype({ "id": "int", "android": "bool", "iphone": "bool", "desktop": "bool" })
                    # Change phones + emails to id in TRANS_UNIQUE, PROMOTIONS
                    lookup_email = {e:i for e, i in zip(DATA_PEOPLE["email"], DATA_PEOPLE["id"])}
                    lookup_phone = {p:i for p, i in zip(DATA_PEOPLE["phone"], DATA_PEOPLE["id"])}
                    PROMOTIONS["customer_id"] = PROMOTIONS["client_email"].map( lookup_email ).fillna( 
                        PROMOTIONS["telephone"].map( lookup_phone )
                        ).astype(int)
                    PROMOTIONS = PROMOTIONS.drop( columns=["client_email", "telephone"] )
                    TRANS_UNIQUE["customer_id"] = [ lookup_phone[v] for v in TRANS_UNIQUE["phone"] ]
                    TRANS_UNIQUE = TRANS_UNIQUE.drop( columns=["phone"] )
                    progress.update( task, advance=1 )

                    # Send to database + handle variables.
                    # TO DO???: Replace `if_exists` with `method` to ignore duplicates and [...]
                    DATA_PEOPLE.to_sql( "people", self.engine, index=False, if_exists='append' )
                    TRANSFERS.to_sql( "transfers", self.engine, index=False, if_exists='append' )
                    PROMOTIONS.to_sql( "promotions", self.engine, index=False, if_exists='append' )
                    TRANS_UNIQUE.to_sql( "transaction_ids", self.engine, index=False, if_exists='append' )
                    TRANS_PRODUCTS.to_sql( "transaction_products", self.engine, index=False, if_exists='append' )
                    progress.update( task, advance=1 )


        def _func_process_people_json( self, input: dict ) -> dict:
            """
            Function to process all parts of `people.json`. Tested to be 50% faster than for-loops on a DataFrame.
            
            FEATURE: Scalable for new exceptions!
            """
            output = {}
            for k, v in input.items():
                match k:
                    case "location":
                        # Get `{'City': ..., 'Country': ...}`.
                        output.update({ key.lower():value for key, value in v.items() })
                    case "telephone":
                        # Change "telephone" to "phone".
                        output["phone"] = v
                    case "devices":
                        # Get `"devices": [...]`.
                        output["android"] = "Android" in v
                        output["iphone"] = "Iphone" in v
                        output["desktop"] = "Desktop" in v
                        '''
                        # TO DO: This is a draft for a loop to keep track of new devices.
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
                                output[f'has_{device}'] = False'''
                    case _:
                        output[k.lower()] = v
            if self.b_new_devices:
                # TO DO: Open `FILE_LISTS` and update `self.devices` list.
                self.b_new_devices = False
            return output


        def _func_process_people_yml( self, input: dict ) -> dict:
            """
            Function to process all parts of `people.yml`. FEATURE: Scalable for new exceptions!
            """
            output = {}
            for k, v in input.items():
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
                    case _:
                        output[k.lower()] = v
            return output


        def _func_process_transfers_csv( self, input: pd.DataFrame ) -> dict:
            """
            Function to process all parts of `transfers.csv`. FEATURE: Scalable for new exceptions!
            """
            output = {}
            for k, v in input.items():
                match k:
                    # FEATURE: Add exceptions here.
                    case _:
                        output[k.lower()] = v
            return output

        
        def _func_process_item( self, item: dict, id ) -> dict:
            """
            Function to process each nested item of a transaction in `transactions.xml`. FEATURE: Scalable for new exceptions!
            """
            item_row = {"transaction_id":id}
            for k, v in item.items():
                match k:
                    # FEATURE: Add cases here.
                    case _:
                        item_row[k.lower()] = v
            return item_row


        def _func_process_transactions_xml( self, DT: dict ):
            """
            Function to process the items of each transaction of `transactions.xml`.
            """
            res = []
            for transaction in DT:
                items = transaction["items"]["item"]
                if isinstance(items, dict):
                    res.append( self._func_process_item( items, transaction["@id"] ) )
                elif isinstance(items, list):
                    res.extend( [ self._func_process_item( item, transaction["@id"] ) for item in items ] )
            return pd.DataFrame( res )


        def _func_process_universal( self, input: dict ) -> dict:
            """
            Function to process all data when no exceptions are found.
            """
            return { k.lower():v for k, v in input.items() }

        
        def _func_msg_bubble( self, b_change: bool = True, default_msg: str = None ):
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
                title=Text( "VE Status", style=Style(italic=True) ),
                width=WIDTH, border_style=self.bubble_sty
            ) )
            CONSOLE.print("\n")
            return False # Revert back to default message.

        
        def func_l1_menu_loop( self ):
            """
            Loop to allow user to keep using this program after finishing a task.

            The Level 1 command for loop handling.
            """
            self.b_change_l1 = False
            """Must the default message be changed or not, including errors?"""
            while True:
                self.b_change_l1 = self._func_msg_bubble( self.b_change_l1, "What would you like to do today?" )
                CONSOLE.print(P_MENU)
                self.i_menu = CONSOLE.input("> ").lower()
                match self.i_menu:
                    case "1":
                        self.func_l2_input_t1()
                    case "2":
                        self.func_l2_input_t2()
                    case "3":
                        ### DEV NOTE:
                        CONSOLE.print(fcolor("DEV NOTE: Not available yet. Try a different option.", "bold red"))
                    case "h" | "help":
                        self.func_help()
                    case "q" | "quit":
                        CONSOLE.print(f"{QUIT2}")
                        sys.exit()
                    case "":
                        self.b_change_l1 = True
                        self.bubble_txt = "No input. Try again."
                        self.bubble_sty = "bold yellow"
                    case _:     # Error input.c
                        self.b_change_l1 = True
                        self.bubble_txt = "Invalid input. Try again."
                        self.bubble_sty = "bold yellow"
                self.i_menu = ""

        
        def func_help( self ):
            """
            Present help menu.
            """
            self.b_change_lH = False
            CONSOLE.print(f"\n\n{LINE}\n")
            CONSOLE.print(P_HELP_MENU)
            while True:
                self.b_change_lH = self._func_msg_bubble( self.b_change_lH,
                                                         "Read the HELP MENU above. Take action with the HELP DESK below." )
                CONSOLE.print(P_HELP_DESK)
                i = CONSOLE.input(fcolor("> ", C))
                match i:
                    case "g" | "github":
                        try:
                            open_new_tab( "https://github.com/cyvu37/venmito-cyvu37" )
                            self.b_change_lH = False
                            break
                        except:
                            self.b_change_lH = True
                            self.bubble_txt = "Error in connection."
                            self.bubble_sty = "bold red"
                    case "p" | "prev":
                        break
                    case "q" | "quit":
                        CONSOLE.print(f"{QUIT2}")
                        sys.exit()
                    case "":
                        self.b_change_lH = True
                        self.bubble_txt = "No input. Try again."
                        self.bubble_sty = "bold yellow"
                    case _:
                        self.b_change_lH = True
                        self.bubble_txt = "Invalid input. Try again."
                        self.bubble_sty = "bold yellow"
            CONSOLE.print(f"\n\n{LINE}\n")

        
        def func_l2_input_t1( self ):
            """
            Loop for Step 1 of Task 1: Prefab Reports
            > Step 1: Select Output type.
            > Step 2: Select HNR report.
            > Step 3: Select Input type. 
            
            A Level 2 command for loop handling.
            """
            self.b_change_l2 = False
            while True:
                self.b_change_l2 = self._func_msg_bubble( self.b_change_l2, f"{prefab_abbr} Report, Step 1" )
                CONSOLE.print(P_OUTPUT)
                self.i_output = CONSOLE.input("> ").lower()
                if self.i_output in D_OUTPUT.keys():
                    self.func_l3_list_hnr_t1()
                else:
                    match self.i_output:
                        case "p" | "previous":
                            break
                        case "h" | "help":
                            self.func_help()
                        case "q" | "quit":
                            CONSOLE.print(f"{QUIT2}")
                            sys.exit()
                        case "":
                            self.b_change_l2 = True
                            self.bubble_txt = "No input. Try again."
                            self.bubble_sty = "bold yellow"
                        case _:
                            self.b_change_l2 = True
                            self.bubble_txt = "Invalid input. Try again."
                            self.bubble_sty = "bold yellow"
                self.i_output = ""

        
        def func_l3_list_hnr_t1( self ):
            """
            Loop for Step 2 of Task 1: Prefab Reports
            > Step 1: Select Output type.
            > Step 2: Select HNR report.
            > Step 3: Select Input type. 
            
            A Level 3 command for loop handling.
            """
            self.b_change_l3 = False
            while True:
                self.b_change_l3 = self._func_msg_bubble( self.b_change_l3, f"{prefab_abbr} Report, Step 2 | Output: {D_OUTPUT[self.i_output]}" )
                CONSOLE.print( P_HNRR )
                self.i_hnrr = CONSOLE.input("> ").lower()
                match self.i_hnrr:
                    case "1":
                        self.func_l4_input_t1()
                    case "2":
                        # self.func_l4_t1_view_store_products()
                        CONSOLE.print(fcolor("DEV NOTE: Not available yet. Try [1].", "bold red"))
                    case "3":
                        # self.func_l4_t1_view_transactions()
                        CONSOLE.print(fcolor("DEV NOTE: Not available yet. Try [1].", "bold red"))
                    case "p" | "previous":
                        break
                    case "h" | "help":
                        self.func_help()
                    case "q" | "quit":
                        CONSOLE.print(f"{QUIT2}")
                        sys.exit()
                    case "":
                        self.b_change_l3 = True
                        self.bubble_txt = "No input. Try again."
                        self.bubble_sty = "bold yellow"
                    case _:
                        self.b_change_l3 = True
                        self.bubble_txt = "Invalid input. Try again."
                        self.bubble_sty = "bold yellow"
                self.i_hnrr = ""

        
        def func_l4_t1_view_store_products( self ):
            """
            Prefab Report w/ Output: View of Store Products
            
            A Level 4 command for loop handling.
            """
            pass

        
        def func_l4_t1_view_transactions( self ):
            """
            Prefab Report w/ Output: View Transactions
            
            A Level 4 command for loop handling.
            """
            pass

        
        def func_l4_input_t1( self ):
            """
            Loop for Step 3 of Task 1: Prefab Reports
            > Step 1: Select Output type.
            > Step 2: Select HNR report.
            > Step 3: Select Input type. 
            
            A Level 4 command for loop handling.
            """
            self.b_change_l4 = False
            while True:
                self.b_change_l4 = self._func_msg_bubble( self.b_change_l4, 
                    f"{prefab_abbr} Report, Step 3 | Output: {D_OUTPUT[self.i_output]}; Report: {D_HNRR[self.i_hnrr]}"
                )
                CONSOLE.print( P_INPUT )
                self.i_input = CONSOLE.input("> ").lower()
                if self.i_input in D_INPUT:
                    ### DEV NOTE: This is when the processing starts.
                    CONSOLE.print(fcolor("DEV NOTE: Not available yet. Applies to all such options.", "bold red"))
                else:
                    match self.i_input:
                        case "p" | "previous":
                            break
                        case "h" | "help":
                            self.func_help()
                        case "q" | "quit":
                            CONSOLE.print(f"{QUIT2}")
                            sys.exit()
                        case "":
                            self.b_change_l4 = True
                            self.bubble_txt = "No input. Try again."
                            self.bubble_sty = "bold yellow"
                        case _:
                            self.b_change_l4 = True
                            self.bubble_txt = "Invalid input. Try again."
                            self.bubble_sty = "bold yellow"

        
        def func_l2_input_t2( self ):
            """
            Loop for getting input for Task 2: Create SQL Report
            > Step 1: Select Output type.
            > Step 2: Write SQL command. 

            A Level 2 command for loop handling.
            """
            self.b_change_l2 = False
            while True:
                self.b_change_l2 = self._func_msg_bubble( self.b_change_l2, "SQL Report 1/2: Select your output type." )
                CONSOLE.print( P_OUTPUT )
                self.i_output = CONSOLE.input("> ").lower()
                if self.i_output in D_OUTPUT.keys():
                    ### DEV NOTE:
                    CONSOLE.print(fcolor("DEV NOTE: Not available yet. Applies to all such options.", "bold red"))
                else:
                    match self.i_output:
                        case "p" | "previous":
                            break
                        case "h" | "help":
                            self.func_help()
                        case "q" | "quit":
                            CONSOLE.print(f"{QUIT2}")
                            sys.exit()
                        case "":
                            self.b_change_l2 = True
                            self.bubble_txt = "No input. Try again."
                            self.bubble_sty = "bold yellow"
                        case _:
                            self.b_change_l2 = True
                            self.bubble_txt = "Invalid input. Try again."
                            self.bubble_sty = "bold yellow"



    if __name__ == "__main__":
        VE = Venmito_Evaluator()

except Exception as e:
    capture_app_error()