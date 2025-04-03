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
C = "bright_cyan"
"""For `rich` printing: Default color for normal messages."""
LINE = WIDTH * "-"
R_LINE = fcolor( LINE, C )
"""For `rich` printing."""
HEADER = mid( f"< < <   {TITLE.upper()}   > > >", False )
R_HEADER = mid( f"< < <   {fcolor(TITLE.upper(), C)}   > > >", True )
"""For `rich` printing."""
QUIT = f"* Quitting app...\n\n{HEADER}\n{BORDER}\n"
R_QUIT = fcolor( f"* Quitting app...\n\n\n{R_HEADER}\n{BORDER}\n", "blue1" )
"""For `rich` printing."""
R_YN = f"[{C}]([/{C}][green]y[/green][{C}]/[/{C}][red]n[/red][{C}])[/{C}]"
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


# Check required files.
missing_req = [ f for f in [FILE_REQ, FILE_LISTS] if not os.path.exists(f) ]
if len(missing_req) > 0:
    tmp = "file" if len(missing_req) == 1 else "files"
    CONSOLE.print( f"[bold red]* ERROR[/bold red] | [{C}]Missing {tmp}: {",".join(missing_req)}[/{C}]\n{R_QUIT}" )
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
        CONSOLE.print( fcolor( "* CUSTOM ERROR", "bold red" ) + " | " + fcolor( message, C ) )
    # Handle error file and exit.
    err_exit = fcolor( f"\"{fp_err}\"", "gold1" ) + f"\n{R_QUIT}"
    if os.path.exists(fp_err):
        CONSOLE.print( fcolor( "* Above traceback saved to ", C ) + err_exit )
        Popen( [OPENER, fp_err] ) 
        sleep(1)
    else:
        CONSOLE.print( fcolor( "* Error saving traceback to ", "bold red" ) + err_exit )
    sys.exit()


# Setup formatting objects with `rich`.
# > Function for common tables.
def FUNC_make_cmd_table( t: str, columns: dict[str], rows: list[dict[str]] ) -> Table:
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
prefab_abbr = "Prefab" # Use: f"{prefab_abbr} Report"
D_MENU = {
    "1": f"{prefab_name}s",
    "2": "Create SQL Report",
    "3": "Create DeepSeek Prompt"
}
R_MENU = FUNC_make_cmd_table(
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
R_OUTPUT = FUNC_make_cmd_table(
    "OUTPUT MENU", { "Enter": "gold1", "Output Type": "bright_cyan" }, 
    [D_OUTPUT, 
    {
        "p / previous": "Return to Main Menu",
        "h / help": "Open Help Menu",
        "q / quit": f"Quit {TITLE}"
    }]
)

# > Prefab Reports: Task 1
D_PFR = {
    "1": "Single Table Output",
    "2": "View of Store Products",
    "3": "View of Transactions"
}
R_PFR = FUNC_make_cmd_table(
    f"{prefab_name.upper()} MENU", { "Enter": "gold1", prefab_name: "bright_cyan" }, 
    [D_PFR, 
    {
        "p / previous": "Return to Previous Menu",
        "h / help": "Open Help Menu",
        "q / quit": f"Quit {TITLE}"
    }]
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
    "INPUT MENU", { "Enter": "gold1", "Database Table": "bright_cyan" }, 
    [D_INPUT, 
    {
        "p / previous": "Return to Previous Menu",
        "h / help": "Open Help Menu",
        "q / quit": f"Quit {TITLE}"
    }]
)

# > Help Desk: Take 2 [DEV NOTES]
'''D_HELP_DESK = {
    "1": "About Features",
    "2": "Program Outline",
    "3": "File Directory Status",
    "4": "Open Browser to GitHub Repository (& Return to Previous Menu)"
}
R_HELP_DESK = FUNC_make_cmd_table(
    "HELP DESK", { "Enter": "gold1", "Action": "bright_cyan" },
    [D_HELP_DESK,
    {
        "p / prev": "Return to Previous Menu",
        "q / quit": f"Quit {TITLE}"
    }]
)'''

# > The Help Menu
R_HELP_MENU = Table( 
    title=Text( "HELP MENU [TBF]", justify="center", style="sea_green2" ), 
    show_lines=True, width=WIDTH, box=box.DOUBLE
    )
"""The Help Menu."""
R_HELP_MENU.add_column( "Task", style="gold1", header_style="gold1" )
R_HELP_MENU.add_column( "Meaning", style="bright_cyan", header_style="bright_cyan" )
tmp = """Prefabricated scripts to generate reports.
X
X"""
R_HELP_MENU.add_row( f"{prefab_name}s", tmp )
tmp = """X
X
X"""
R_HELP_MENU.add_row( "Create SQL Report", tmp )
tmp = """X
X
X"""
R_HELP_MENU.add_row( "Create DeepSeek Prompt", tmp )

# > The Help Desk
R_HELP_DESK = FUNC_make_cmd_table(
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

        msg = {
            "title": "What would you like to do?",
            "title_color": C,
            "header": "VE Status: Level 1",
            "header_color": C,
            "border_color": C
        }
        pointer_menu = R_MENU.title

        bubble_txt = ""
        bubble_sty = ""
        b_change_lH = False
        b_change_l1 = False
        b_change_l2 = False
        b_change_l3 = False
        b_change_l4 = False
        """Must the default message be changed or not, including errors?"""

        i_menu = ""
        """Current index of MAIN MENU selection."""
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
            b_first_time = CONSOLE.input(f"[{C}]* Would you like to start from scratch? {R_YN}\n> [/{C}]")
            if b_first_time.lower() == "y":
                CONSOLE.print(f"[{C}]* Starting from scratch...[/{C}]")
                self._func_first_time()
            
            CONSOLE.print(
                fcolor("* All prerequisites satisfied!", C) + "\n" + 
                fcolor("* Output saved to ", C ) + fcolor(f"\"{DIR_OUTPUT}\"", "gold1") +
                f"\n\n\n{R_ENTER}"
            )
            self.func_l1_menu_loop_v2()


        def _func_quit( self ):
            try: VE.conn.close()
            except: pass
            CONSOLE.print(R_QUIT)
            sys.exit()


        def _func_first_time( self ):
            if self.b_can_add_data_files:
                self._func_process_master( "replace" )
                #self._func_handle_views() # DEV NOTE: TEST
            else:
                CONSOLE.print( f"[bold red]* ERROR[/bold red] | [{C}]No valid files detected in `data` folder. Can't continue.[/{C}]\n{R_QUIT}" )
                sys.exit()


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


        def _func_process_master( self, if_exists: str ):
            """
            Can only run when there are any files to process.
            """
            with Progress() as progress:
                n_p = len([v for v in B_DATA_EXISTS.values() if v]) + 3
                tmp1 = {}; tmp2 = {}
                DATA_PEOPLE = None
                DJ = None
                DY = None
                TRANSFERS = None
                PROMOTIONS = None
                TRANS_PRODUCTS = None
                task = progress.add_task( f"[{C}]* Importing data...", total=n_p )
                
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
                    
                    # Make table for products.
                    tmp1 = TRANS_PRODUCTS["item"].drop_duplicates().values
                    tmp2 = PROMOTIONS["promotion"].drop_duplicates().values
                    PRODUCTS = pd.DataFrame( list(set(tmp1) | set(tmp2)), columns=["product"] )

                    # Make table for stores.
                    STORES = pd.DataFrame( TRANS_IDS["store"].drop_duplicates(), columns=["store"] )

                    # Create dictionaries for replacements.
                    lookup_products = {v:k for k, v in PRODUCTS.to_dict()["product"].items()}
                    lookup_emails = dict(zip( DATA_PEOPLE["email"], DATA_PEOPLE["id"] ))
                    lookup_phones = dict(zip( DATA_PEOPLE["phone"], DATA_PEOPLE["id"] ))
                    lookup_stores = {v:k for k, v in STORES.to_dict()["store"].items()}

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
                    DATA_PEOPLE.to_sql( "people", self.engine, index=False, if_exists=if_exists )
                    TRANSFERS.to_sql( "transfers", self.engine, index=False, if_exists=if_exists )
                    PROMOTIONS.to_sql( "promotions", self.engine, index=False, if_exists=if_exists )
                    TRANS_IDS.to_sql( "transaction_ids", self.engine, index=False, if_exists=if_exists )
                    TRANS_PRODUCTS.to_sql( "transaction_products", self.engine, index=False, if_exists=if_exists )
                    PRODUCTS.to_sql( "products", self.engine, index=True, index_label="id", if_exists=if_exists )
                    progress.update( task, advance=1 )
                
                    # Update all tables in database.
                    cur = self.conn.cursor()
                    cur.execute("ALTER TABLE people " + 
                                "ADD CONSTRAINT unique_person PRIMARY KEY (id)")
                    cur.execute("ALTER TABLE transfers " + 
                                "ADD FOREIGN KEY (sender_id) REFERENCES people(id), " + 
                                "ADD FOREIGN KEY (recipient_id) REFERENCES people(id)")
                    cur.execute("ALTER TABLE products " + 
                                "ADD CONSTRAINT unique_product PRIMARY KEY (id)")
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
                    self.conn.commit()
                    cur.close()
                    del DATA_PEOPLE, TRANSFERS, PROMOTIONS, TRANS_IDS, TRANS_PRODUCTS
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
                            output["dob"] = datetime.strftime( datetime.strptime( v, "%m/%d/%Y" ), "%Y-%m-%d" )
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
            if self.b_new_devices:
                # TO DO: Open `FILE_LISTS` and update `self.devices` list.
                self.b_new_devices = False
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

        
        def _func_msg_bubble_v2( self, default_msg: dict ):
            # Print message bubble.
            CONSOLE.print("\n")
            CONSOLE.print( Panel(
                Text( self.msg["title"], justify="center", style=Style( color=self.msg["title_color"] ) ), 
                title=Text( self.msg["header"], style=Style( color=self.msg["header_color"], italic=True, dim=True ) ),
                border_style=self.msg["border_color"], width=WIDTH
            ) )
            CONSOLE.print("\n")
            # Reset default variables.
            self.msg.update({ "title_color": C, "header_color": C, "border_color": C })
            self.msg.update( default_msg )

        
        def _func_msg_bubble_v1( self, b_change: bool = True, default_msg: str = None ):
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

        
        def func_l1_menu_loop_v2( self ):
            """
            Loop to allow user to keep using this program after finishing a task.

            The Level 1 command for nested loop handling.
            """
            default_msg = { 
                "header": "VE Status: Level 1",
                "title": "What would you like to do?"
            }
            self.msg.update( default_msg )
            while True:
                self._func_msg_bubble_v2( default_msg )
                # Print menu + get input.
                CONSOLE.print(R_MENU)
                self.i_menu = CONSOLE.input("> ").lower()
                match self.i_menu:
                    case "1":
                        self.func_l2_input_t1()
                    case "2":
                        self.func_l2_input_t2()
                    case "3":
                        self.msg.update({
                            "header": f"WARNING | {D_MENU[self.i_menu]}: Not available yet.",
                            "header_color": "orange1", "border_color": "orange1"
                            })
                    case "h" | "help":
                        self.func_help_v1()
                    case "q" | "quit":
                        self._func_quit()
                    case "":
                        self.msg.update({
                            "header": "No input. Try again.", 
                            "header_color": "yellow", "border_color": "yellow"
                            })
                    case _:
                        self.msg.update({
                            "header": f"Invalid input: {self.i_menu}. Try again.", 
                            "header_color": "yellow", "border_color": "yellow"
                            })

        
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
                        self.func_l2_input_t1()
                    case "2":
                        self.func_l2_input_t2()
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

        
        def func_help_loop( self ):
            """
            Open the HELP DESK menu.

            A Level 1 command for nested loop handling.
            """
            default_msg = {
                "header": "Help Desk: Level 1",
                "title": "What would you like to know or do?"
            }
            self.msg.update( default_msg )
            CONSOLE.print(f"\n\n{R_LINE}\n")
            CONSOLE.print(R_HELP_MENU)
            while True:
                self._func_msg_bubble_v2( default_msg )
                # Print menu + get input.
                CONSOLE.print(R_MENU)
                self.i_menu = CONSOLE.input("> ").lower()
                ###

        
        def func_help_v1( self ):
            """
            Present help menu.
            """
            self.b_change_lH = False
            CONSOLE.print(f"\n\n{R_LINE}\n")
            CONSOLE.print(R_HELP_MENU)
            while True:
                self.b_change_lH = self._func_msg_bubble_v1( self.b_change_lH,
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

        
        def func_l2_input_t1( self ):
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

        
        def func_l3_list_hnr_t1( self ):
            """
            Loop for Step 2 of Task 1: Prefab Reports
            > Step 1: Select Output type.
            > Step 2: Select HNR report.
            > Step 3: Select Input type. 
            
            A Level 3 command for nested loop handling.
            """
            self.b_change_l3 = False
            while True:
                self.b_change_l3 = self._func_msg_bubble_v1( self.b_change_l3, f"{prefab_abbr} Report, Step 2 | Output: {D_OUTPUT[self.i_output]}" )
                CONSOLE.print( R_PFR )
                self.i_pfr = CONSOLE.input("> ").lower()
                match self.i_pfr:
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
                        self.func_help_v1()
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

        
        def func_l4_t1_view_store_products( self ):
            """
            Prefab Report w/ Output: View of Store Products
            
            A Level 4 command for nested loop handling.
            """
            pass

        
        def func_l4_t1_view_transactions( self ):
            """
            Prefab Report w/ Output: View Transactions
            
            A Level 4 command for nested loop handling.
            """
            pass

        
        def func_l4_input_t1( self ):
            """
            Loop for Step 3 of Task 1: Prefab Reports
            > Step 1: Select Output type.
            > Step 2: Select HNR report.
            > Step 3: Select Input type. 
            
            A Level 4 command for nested loop handling.
            """
            self.b_change_l4 = False
            while True:
                self.b_change_l4 = self._func_msg_bubble_v1( self.b_change_l4, 
                    f"{prefab_abbr} Report, Step 3 | Output: {D_OUTPUT[self.i_output]}; Report: {D_PFR[self.i_pfr]}"
                )
                CONSOLE.print( R_INPUT )
                self.i_input = CONSOLE.input("> ").lower()
                if self.i_input in D_INPUT:
                    ### DEV NOTE: This is when the processing starts.
                    CONSOLE.print(fcolor("DEV NOTE: Not available yet. Applies to all such options.", "bold red"))
                else:
                    match self.i_input:
                        case "p" | "previous":
                            break
                        case "h" | "help":
                            self.func_help_v1()
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

        
        def func_l2_input_t2( self ):
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



    if __name__ == "__main__":
        VE = Venmito_Evaluator()



except Exception as e:
    FUNC_capture_app_error()