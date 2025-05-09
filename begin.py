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
def pc( message: str, color: str ):
    """For `rich` printing: Surround a `message` in `color`."""
    return f"[{color}]{message}[/{color}]"
CD = "bright_cyan"
"""For `rich` printing: Default color for normal messages."""
CH = "bright_yellow"
"""For `rich` printing: Default color for help messages."""
CC = "gold1"
"""For `rich` printing: Default color for action column."""
LINE = WIDTH * "-"
R_LINE = pc( LINE, CD )
"""For `rich` printing."""
HEADER = mid( f"< < <   {TITLE.upper()}   > > >", False )
R_HEADER = mid( f"< < <   {pc(TITLE.upper(), CD)}   > > >", True )
"""For `rich` printing."""
QUIT = f"* Quitting app...\n\n{HEADER}\n{BORDER}\n"
R_QUIT = pc( f"* Quitting app...\n\n\n{R_HEADER}\n{BORDER}\n", "blue1" )
"""For `rich` printing."""
R_ENTER = pc( f"{BORDER}\n{R_HEADER}", "green1" )
"""For `rich` printing."""


# Set directories.
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
# Set command(s) based on OS.
dict_od = { "Windows": "explorer", "Darwin": "open" }
OPENER = dict_od[system()] if system() in dict_od.keys() else "xdg-open"
"""Command to open a file or directory."""
# Other variables.
GITHUB_URL = "https://github.com/jaredhidalgo/venmito-cyvu37"


# Package check: Offline check.
with open(FILE_REQ, "r") as r:
    req_pkgs = [line.strip().lower().split("[")[0] for line in r.readlines()]
curr_pkgs = [ "-".join( dist.metadata["Name"].lower().split("_") ) for dist in distributions() ]
miss_pkgs = [ x for x in req_pkgs if x not in curr_pkgs ]


# Package check: If any packages are missing.
if len(miss_pkgs) > 0:
    # Attempt online download.
    print("* WARNING | There are missing packages.\n* Attempting online download...\n")
    call( f"{sys.executable} -m pip install -U pip", shell=True )
    call( f"{sys.executable} -m pip install -r \"{FILE_REQ}\"", shell=True )
    # Check again.
    curr_pkgs = [ "-".join( dist.metadata["Name"].lower().split("_") ) for dist in distributions() ]
    miss_pkgs = [ x for x in req_pkgs if x not in curr_pkgs ]
    if len(miss_pkgs) > 0:
        tmp = "package" if len(miss_pkgs) == 1 else "packages"
        sys.exit( f"\n\n* ERROR! Missing {tmp}: {",".join(miss_pkgs)}\n{QUIT}" )
    print("\n* Packages installed successfully.")


# Import `rich` features.
# > Console print formatting.
from rich.theme import Theme
from rich.console import Console
CONSOLE = Console( record=True, log_time=True, 
                   theme=Theme({"repr.background": "black"}) )
CONSOLE_HTML_FORMAT = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
{stylesheet}
body {{
    color: #ffffff;
    background-color: #000000;
}}
</style>
</head>
<body>
    <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><code style="font-family:inherit">{code}</code></pre>
</body>
</html>
"""
from rich.text import Text
from rich.prompt import IntPrompt
# > Error handling.
from rich.traceback import install
install( show_locals=True, console=CONSOLE )
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
import chime, matplotlib, xmltodict, yaml
import pandas as pd
import sqlalchemy.engine
chime.theme( "material" )
matplotlib.use('Agg')
import matplotlib.pyplot as plt
DPI = 200
plt.rcParams.update({
    "font.size": 5,
    "figure.dpi": DPI,
    "xtick.labelsize": 4,
    "ytick.labelsize": 4
})


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
B_CAN_ADD_DATA_FILES = any( B_DATA_EXISTS.values() )
DEVICES = ['android', 'iphone', 'desktop']


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
        f.write( CONSOLE.export_html( code_format=CONSOLE_HTML_FORMAT ) )
        ### DEV NOTE: How do I make the background black!?
    
    CONSOLE.print(f"\n\n\n")
    if message:
        CONSOLE.print( pc( "* CUSTOM ERROR", "bold red" ) + " | " + pc( message, CD ) )
    # Handle error file and exit.
    err_exit = pc( Text(fp_err, style=Style(link=fp_err)), "gold1" ) + f"\n{R_QUIT}"
    if os.path.exists(fp_err):
        CONSOLE.print( pc( "* Above traceback saved to file ", CD ) + err_exit )
        Popen( [OPENER, fp_err] ) 
        sleep(1)
    else:
        CONSOLE.print( pc( "* Error saving traceback to file ", "bold red" ) + err_exit )
    sys.exit()


# Setup formatting objects with `rich`.
# > Function for common tables.
def FUNC_table_data( t: str, columns: dict[str, str], content: pd.DataFrame, bc: str ) -> Table:
    """Generic function to make a multi-section Table.

    Args:
        t (str): Table title
        columns (dict[str, str]): The column names and respective colors.
        dictionary (dict): Each dict entry is a row. If `list`, then each dict is a section.
        bc (str): Border and title color.

    Returns:
        Table: The table to print on the CMD.
    """    
    table = Table( title=Text( t, justify="center", style=Style( color=bc, bold=True ) ), border_style=bc, show_lines=True )
    for k, v in columns.items():
        table.add_column( k, style=v, header_style=v )
    for i in range( content.shape[0] ):
        table.add_row( *content.iloc[i].astype(str).to_list() )
    return table


# > Function for common tables.
def FUNC_table_system( t: str, columns: dict[str, str], rows: dict | list[dict], bc: str ) -> Table:
    """Function to make an action table.

    Args:
        t (str): Table title
        columns (dict[str, str]): The column names and respective colors.
        rows (dict | list[dict]): Each dict entry is a row. If `list`, then each dict is a section.
        bc (str): Border and title color.

    Returns:
        Table: The table to print on the CMD.
    """    
    table = Table( title=Text( t, justify="center", style=Style( color=bc, bold=True ) ), border_style=bc )
    for k, v in columns.items():
        table.add_column( k, style=v, header_style=v )
    if type(rows) == dict:
        for k, v in rows.items():
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
"""Help + Quit"""
D_PQ = {
    "p / previous": "Return to Previous Menu",
    "q / quit": f"Quit {TITLE}"
}
"""Previous + Quit"""
D_PHQ = {
    "p / previous": "Return to Previous Menu",
    "h / help": "Open Help Menu",
    "q / quit": f"Quit {TITLE}"
}
"""Previous + Help + Quit"""

# > TABLE: The main menu.
prefab_name = "Hot-N-Ready View"
"""A more exciting name for "prefab views". Must be singular."""
#prefab_abbr = "HNR"
"""A more exciting abbreviation for "prefab views". Used as `f"{prefab_abbr} View"`."""
K_MENU = {
    "1": f"{prefab_name}s",
    "2": "Create SQL Report",
    "3": "*Create DeepSeek Prompt"
}
"""Dictionary for main menu selection."""
R_MENU = FUNC_table_system( "MAIN MENU", { "Enter": CC, "Task": "bright_cyan" }, [K_MENU, D_HQ], CD )
"""Printed table for main menu selection."""

# > TABLE: Select Output
D_OUTPUT_EXPORT = {
    "1": "Export Table: CSV",
    "2": "*Export Density Graph"
}
D_OUTPUT_PREVIEW = {
    "3": "Print 1st N Entries",
    "4": "*Print Density Statistics"
}
K_OUTPUT = ChainMap( D_OUTPUT_EXPORT, D_OUTPUT_PREVIEW )
"""Dictionary for output selection."""
R_OUTPUT = FUNC_table_system( "OUTPUT MENU", { "Enter": CC, "Output Type": "bright_cyan" }, [*K_OUTPUT.maps, D_PHQ], CD )
"""Printed table for output selection."""

# > TABLE: Task 1, Step 1 - Prefab Reports
PFR_QUERIES = {
    "view_promotions_metadata": """
        SELECT
            pr.promotion_date,
            pe.first_name || ' ' || pe.last_name AS customer_name,
            pd.name AS product_name,
            pr.has_responded
        FROM promotions AS pr
        LEFT JOIN products AS pd ON pr.product_id = pd.id
        LEFT JOIN people AS pe ON pr.customer_id = pe.id
        """,

    "view_store_products": """
        SELECT 
            st.name AS store_name,
            pd.name AS product_name,
            SUM(tp.quantity) AS total_sold
        FROM transaction_products AS tp
        LEFT JOIN transaction_ids AS ti ON tp.transaction_id = ti.id
        LEFT JOIN products AS pd ON tp.product_id = pd.id
        LEFT JOIN stores AS st ON ti.store_id = st.id
        GROUP BY st.name, pd.name
        ORDER BY st.name, pd.name;
        """,

    "view_transactions_metadata": """
        SELECT
            ti.id AS transaction_id,
            ti.date, 
            st.name AS store_name, 
            pe.first_name || ' ' || pe.last_name AS customer_name,
            SUM(tp.price) AS price_sum
        FROM transaction_products AS tp 
        LEFT JOIN transaction_ids AS ti ON ti.id = tp.transaction_id
        LEFT JOIN people AS pe ON ti.customer_id = pe.id
        LEFT JOIN stores AS st ON ti.store_id = st.id
        GROUP BY ti.id, ti.date, st.name, customer_name
        ORDER BY ti.id;
        """,

    "view_transactions_full": """
        SELECT
            tp.transaction_id AS id, 
            ti.date, 
            st.name AS store_name, 
            pe.first_name || ' ' || pe.last_name AS customer_name, 
            pr.name AS product_name, 
            tp.price, 
            tp.price_per_item, 
            tp.quantity
        FROM transaction_products AS tp 
        LEFT JOIN transaction_ids AS ti ON ti.id = tp.transaction_id 
        LEFT JOIN people AS pe ON pe.id = ti.customer_id 
        LEFT JOIN stores AS st ON st.id = ti.store_id 
        LEFT JOIN products AS pr ON pr.id = tp.product_id
        ORDER BY tp.transaction_id, st.name, pr.name;
        """,

    "view_transfers_metadata": """
        SELECT 
            tr.date, 
            tr.amount, 
            sender.first_name || ' ' || sender.last_name AS sender_name, 
            recipient.first_name || ' ' || recipient.last_name AS recipient_name 
        FROM transfers AS tr, people AS sender, people AS recipient
        WHERE tr.sender_id = sender.id
        AND tr.recipient_id = recipient.id
        ORDER BY tr.date
        """
}
"""The prefab queries."""
K_PFR = { "1": "Single Table Output" } # Scalable from the top.
"""Dictionary for prefab report selection."""
PFR_KEYS = list(PFR_QUERIES.keys())
"""Key list of prefab report from `PFR_QUERIES`."""
tmp = len( list(K_PFR.keys()) ) + 1
PFR_USER = [ str(i) for i in range( tmp, len(PFR_KEYS) + tmp ) ]
"""Key list of prefab report user selection from `K_PFR`."""
K_PFR.update({ i : " ".join(k.split("_")).title()
               for i, k in zip( PFR_USER, PFR_KEYS ) })
R_PFR = FUNC_table_system( f"{prefab_name.upper()} MENU", { "Enter": CC, prefab_name: "bright_cyan" }, [K_PFR, D_PHQ], CD )
"""Printed table for prefab report selection."""

# > TABLE LIST
R_PFR_LIST = FUNC_table_system( 
    f"SQL SCRIPTS FOR {prefab_name.upper()}S", { prefab_name: CC, "Script": "bright_cyan" },
    [{ " ".join(k.split("_")).title() : v } for k, v in PFR_QUERIES.items()], CD
)

# > Input: Select Database Tables
K_INPUT: dict[str, str]
"""Dictionary for table selection."""
R_INPUT: Table

# > Help Desk
D_HD_LEARN = {
    "1": "*About & Features",
    "2": "*Menu Hierarchy & Current Position",
    "3": "Print SQL Scripts for Hot-N-Ready Views"
}
D_HD_ACTION = {
    "4": Text( "Open README.md. Fallback: [5]" ),
    "5": Text( "Open Browser to GitHub Repo. Fallback: [4]", 
               style=Style( link=GITHUB_URL ) )
}
K_HELP_DESK = ChainMap( D_HD_LEARN, D_HD_ACTION )
"""Dictionary for help selection."""
R_HELP_DESK = FUNC_table_system( "HELP DESK", { "Enter": CC, "Action": "bright_cyan" }, [*K_HELP_DESK.maps, D_PQ], CH )
"""Printed table for help selection."""

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
        """
        The class to import files into the database.
        """

        def __init__( self, engine: sqlalchemy.engine.Engine, conn: sqlalchemy.PoolProxiedConnection, if_exists: str ):
            
            with Progress() as progress:
                n_p = len([v for v in B_DATA_EXISTS.values() if v]) + 3
                task = progress.add_task( f"[{CD}]* Importing data...", total=n_p )
                tmp1 = {}; tmp2 = {}
                DATA_PEOPLE = None
                DJ = None
                DY = None
                TRANSFERS = None
                PROMOTIONS = None
                TRANS_PRODUCTS = None
                
                # PEOPLE: Process JSON file.
                if B_DATA_EXISTS["people.json"]:
                    DJ = {}
                    # Process data.
                    with open( os.path.join( DIR_DATA, "people.json" ), 'r' ) as f:
                        DJ = json_load( f )
                    for person in DJ:
                        tmp1[ int(person["id"]) ] = self._func_process_people_json( person )
                    # Handle database.
                    DJ = pd.DataFrame.from_dict( tmp1, orient='index' )
                    DJ = DJ.astype({"id":int})
                    progress.update( task, advance=1 )
                
                # PEOPLE: Process YAML file.
                if B_DATA_EXISTS["people.yml"]:
                    DY = {}
                    # Process data.
                    with open( os.path.join( DIR_DATA, "people.yml" ), 'r' ) as f:
                        DY = yaml.safe_load( f )
                    for person in DY:
                        tmp2[ int(person["id"]) ] = self._func_process_people_yml( person )
                    # Handle database.
                    DY = pd.DataFrame.from_dict( tmp2, orient='index' )
                    DY = DY.astype({"id":int})
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
                
                # TRANSFERS: Process CSV file.
                if B_DATA_EXISTS["transfers.csv"]:
                    TRANSFERS = pd.read_csv( os.path.join( DIR_DATA, "transfers.csv" ) )
                    TRANSFERS.columns = [ h.lower() for h in TRANSFERS.columns ]
                    progress.update( task, advance=1 )
                
                # PROMOTIONS: Process CSV file.
                if B_DATA_EXISTS["promotions.csv"]:
                    PROMOTIONS = pd.read_csv( os.path.join( DIR_DATA, "promotions.csv" ) )
                    PROMOTIONS.columns = [ h.lower() for h in PROMOTIONS.columns ]
                    if "responded" in PROMOTIONS.columns:
                        PROMOTIONS["has_responded"] = PROMOTIONS["responded"].map({ "Yes": True, "No": False })
                        PROMOTIONS = PROMOTIONS.drop( columns=["responded"] )
                    progress.update( task, advance=1 )
                
                # TRANSACTIONS: Split into IDS and PRODUCTS.
                if B_DATA_EXISTS["transactions.xml"]:
                    # Create `transaction_ids`
                    with open( os.path.join( DIR_DATA, "transactions.xml" ), 'rb' ) as f:
                        TRANS_IDS = pd.read_xml(f)
                    TRANS_IDS = TRANS_IDS.drop( columns=["items"] )
                    if "dob" in TRANS_IDS.columns:
                        TRANS_IDS["dob"] = [ datetime.strftime( parse(v), "%Y-%m-%d" ) for v in TRANS_IDS["dob"] ]
                    # Create `transaction_products`
                    with open( os.path.join( DIR_DATA, "transactions.xml" ), 'rb' ) as f:
                        TRANS_PRODUCTS = xmltodict.parse(f)["transactions"]["transaction"]
                    
                    TRANS_PRODUCTS = self._func_process_transactions_xml( TRANS_PRODUCTS )
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
                    tmp1 = TRANS_IDS["store"].drop_duplicates().values
                    STORES = pd.DataFrame( tmp1, columns=["name"], index=range(1, len(tmp1)+1) )

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
                    cur.execute( """
                        ALTER TABLE people
                            ADD CONSTRAINT unique_person PRIMARY KEY (id);
                        ALTER TABLE transfers 
                            ADD FOREIGN KEY (sender_id) REFERENCES people(id),
                            ADD FOREIGN KEY (recipient_id) REFERENCES people(id);
                        ALTER TABLE products 
                            ADD CONSTRAINT unique_product PRIMARY KEY (id);
                        ALTER TABLE stores 
                            ADD CONSTRAINT unique_store PRIMARY KEY (id);
                        ALTER TABLE promotions 
                            ADD CONSTRAINT unique_promotion PRIMARY KEY (id), 
                            ADD FOREIGN KEY (customer_id) REFERENCES people(id), 
                            ADD FOREIGN KEY (product_id) REFERENCES products(id);
                        ALTER TABLE transaction_ids 
                            ADD CONSTRAINT unique_transaction PRIMARY KEY (id), 
                            ADD FOREIGN KEY (customer_id) REFERENCES people(id);
                        ALTER TABLE transaction_products 
                            ADD FOREIGN KEY (transaction_id) REFERENCES transaction_ids(id), 
                            ADD FOREIGN KEY (product_id) REFERENCES products(id);
                    """ )
                    cur.execute("ALTER TABLE people ALTER COLUMN dob TYPE DATE USING dob::date")
                    cur.execute("ALTER TABLE promotions ALTER COLUMN promotion_date TYPE DATE USING promotion_date::date")
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
                            output[k] = datetime.strftime( parse(v), "%Y-%m-%d" )
                        except:
                            output[k] = v
                    case "devices":
                        # Get `"devices": [...]`.
                        output["has_android"] = "Android" in v
                        output["has_iphone"] = "Iphone" in v
                        output["has_desktop"] = "Desktop" in v
                    case _:
                        output[k] = v
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
                    case _ if k in DEVICES:
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

        
        def _func_process_item( self, item_info: dict, id: int ) -> dict:
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
                    res.append( self._func_process_item( items, int(transaction["@id"]) ) )
                elif isinstance(items, list):
                    res.extend( [ self._func_process_item( item, int(transaction["@id"]) ) for item in items ] )
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
            "mid_color": "bright_white",
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
        n_print = 10
        """Number of rows to print in preview (default: N=10)."""

        def __init__( self ):
            try:
                self.engine = sqlalchemy.engine.create_engine( "postgresql+psycopg://postgres:Space!3742@localhost:5432/postgres" )
                self.conn = self.engine.raw_connection()
            except:
                FUNC_capture_app_error("Can't connect to database.")

            # Check if tables exist.
            tmp = pc( "* Would you like to start from scratch? ([green]y[/green]/[red]OTHER[/red])\n: " , CD )
            b_first_time = CONSOLE.input(tmp)
            if b_first_time.lower() == "y":
                CONSOLE.print(pc("* Starting from scratch...", CD))
                self._func_first_time()
            
            CONSOLE.print(
                pc("* All prerequisites satisfied!\n* Future output saved to directory ", CD) + 
                pc(f"\"{DIR_OUTPUT}\"", "gold1") + f"\n\n\n{R_ENTER}"
            )
            self.func_l1_menu_loop()


        def _func_quit( self ):
            try: VE.conn.close()
            except: pass
            CONSOLE.print(R_QUIT)
            sys.exit()


        def _func_UNDER_CONSTRUCTION( self, option: str ):
            self.msg.update({ "bot": f"DEV NOTE | {option}: Under construction.",
                              "bot_color": "purple3", "border_color": "purple3" })


        def _func_first_time( self ):
            self._func_reset_database()
            if self.b_can_add_data_files:
                Process_Files( self.engine, self.conn, "replace" )
            else:
                CONSOLE.print( f"{pc("* ERROR", "bold red")} | {pc("No valid files detected in `data` folder. Can't continue.", CD)}\n{R_QUIT}" )
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
            cur.execute( "DROP VIEW IF EXISTS view_transaction_metadata CASCADE" )
            cur.execute( "DROP VIEW IF EXISTS view_transaction_full CASCADE" )
            cur.execute( "DROP VIEW IF EXISTS view_store_products CASCADE" )
            self.conn.commit()
            cur.close()

        
        def _func_MSG_BUBBLE( self, default_msg: dict ):
            """
            The function to print the message bubble.

            Args:
                default_msg (dict): The message and format to 1) print when no changes are made (`self.b_msg_change = False`), or 2) set after changes are made (`self.b_msg_change = True`).
            """            
            if not self.b_msg_change:
                self.msg.update({ "top_color": CD, "mid_color": "bright_white", "bot_color": CD, "border_color": CD })
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
            if self.b_msg_change:
                self.b_msg_change = False
                self.msg.update({ "top_color": CD, "mid_color": "bright_white", "bot_color": CD, "border_color": CD })
                self.msg.update( default_msg )
        

        def _func_OTHER_ENTRIES( self, inp: str ):
            """
            Handle all other input values here.

            Args:
                inp (str): The input value.
            """            
            match inp:
                case "q" | "quit":
                    self._func_quit()
                case "":
                    self.b_msg_change = True
                    self.msg.update({"bot": "No input. Try again.", 
                                     "bot_color": "dark_orange", "border_color": "dark_orange"})
                case _:
                    self.b_msg_change = True
                    self.msg.update({"bot": f"Invalid input: {inp}. Try again.", 
                                     "bot_color": "dark_orange", "border_color": "dark_orange"})
        

        def func_l1_menu_loop( self ):
            """
            Loop to allow user to keep using this program after finishing a task.

            The Level 1 command for nested loop handling.
            """
            default_msg = deepcopy( self.msg )
            while True:
                self._func_MSG_BUBBLE( default_msg )
                # Print menu + get input.
                CONSOLE.print(R_MENU)
                self.i_menu = CONSOLE.input(": ").lower()
                match self.i_menu:
                    case "1":
                        self.func_l2_t1s1_output()
                    case "2":
                        self.func_l2_t2s1_output()
                    case "3":
                        ### DEV NOTE: Dead end right now.
                        self.b_msg_change = True
                        self._func_UNDER_CONSTRUCTION( K_MENU[self.i_menu] )
                    case "p" | "previous":
                        self.b_msg_change = True
                        self.msg.update({"bot": "This is the top level. :)", "bot_color": "dark_orange"})
                    case "h" | "help":
                        self.func_helpdesk( R_MENU.title, K_MENU )
                    case _:
                        self._func_OTHER_ENTRIES( self.i_menu )

        
        def func_helpdesk( self, menu_title: str, menu: dict[str, str] ):
            """
            Open the HELP DESK menu.

            A Level 1 command for nested loop handling.
            """
            default_msg = {
                "top": f"{T} Help Lvl 1 | Prev: {menu_title}", "top_color": CH,
                "mid": "What would you like to know or do?",
                "bot": "VE Status", "bot_color": CH, "border_color": CH
            }
            self.msg.update( default_msg )
            CONSOLE.print(f"\n\n{R_LINE}\n")
            while True:
                self._func_MSG_BUBBLE( default_msg )
                # Print menu + get input.
                CONSOLE.print(R_HELP_DESK)
                self.i_help = CONSOLE.input(": ").lower()
                match self.i_help:
                    case "1":
                        ### DEV NOTE: Dead end right now.
                        self.b_msg_change = True
                        self._func_UNDER_CONSTRUCTION( K_HELP_DESK[self.i_help] )
                    
                    case "2":
                        ### DEV NOTE: Dead end right now.
                        self.b_msg_change = True
                        self._func_UNDER_CONSTRUCTION( K_HELP_DESK[self.i_help] )
                    
                    case "3":
                        self.b_msg_change = True
                        self.msg.update({ 
                            "top": f"Output View", "top_color": CD,
                            "mid": "SQL Scripts for Hot-N-Ready Views", "border_color": "bright_white",
                            "bot": "Output printed. Press Enter to return to previous menu.", "bot_color": "green1"
                            })
                        self._func_MSG_BUBBLE( default_msg )
                        CONSOLE.print(R_PFR_LIST)
                        inp = CONSOLE.input( pc("Scroll up for table. Press Enter to continue (or q to quit). ", CD) )
                        match inp:
                            case "q" | "quit":
                                self._func_quit()
                            case _:
                                pass
                    
                    case "4":
                        self.b_msg_change = True
                        try:
                            Popen([OPENER, os.path.join(DIR_PROGRAM, "README.md")])
                            self.msg.update({"bot": "README.md opened.", "bot_color": "bright_green"})
                        except:
                            try:
                                open_new_tab( GITHUB_URL )
                                self.msg.update({
                                    "bot": "Couldn't open README.md, but GitHub repo opened in local browser.",
                                    "bot_color": "bright_green"})
                            except:
                                self.msg.update({"bot": "Couldn't open README.md or GitHub repo. Huh.", "bot_color": "dark_orange"})
                    
                    case "5":
                        self.b_msg_change = True
                        try:
                            open_new_tab( GITHUB_URL )
                            self.msg.update({"bot": "GitHub repo opened in local browser.", "bot_color": "bright_green"})
                        except:
                            try:
                                Popen([OPENER, os.path.join(DIR_PROGRAM, "README.md")])
                                self.msg.update({"bot": "Couldn't open GitHub repo, but README.md opened.", "bot_color": "bright_green"})
                            except:
                                self.msg.update({"bot": "Couldn't open GitHub repo or README.md. Huh.", "bot_color": "dark_orange"})
                    
                    case "p" | "previous":
                        break
                    case _:
                        self._func_OTHER_ENTRIES( self.i_help )

        
        def func_l2_t1s1_output( self ):
            """
            Loop for Step 1 of Task 1: Prefab Reports
            > Step 1: Select Output type.
            * Step 2: Select Prefab report.
            * Step 3, if applicable: Select Input type.
            
            A Level 2 command for nested loop handling.
            """
            default_msg = { 
                "top": f"{T} Menu Lvl 2 | {K_MENU[self.i_menu]}",
                "mid": "Step 1: Select an output type.",
                "bot": "Report: N/A >> Output: N/A"
            }
            self.msg.update( default_msg )
            while True:
                self._func_MSG_BUBBLE( default_msg )
                CONSOLE.print(R_OUTPUT)
                self.i_output = CONSOLE.input(": ").lower()
                if self.i_output in K_OUTPUT.keys():
                    self.b_msg_change = True
                    if K_OUTPUT[self.i_output] == "Print 1st N Entries":
                        self.n_print = IntPrompt.ask( pc("* Input N, the number of rows to preview. Range: [1, 20]. Default: 10.\n", CD),
                                                      console=CONSOLE, choices=[str(i) for i in range(1, 21)], show_choices=False )
                    self.func_l3_t1s2_report()
                else:
                    match self.i_output:
                        case "p" | "previous":
                            break
                        case "h" | "help":
                            self.func_helpdesk( R_OUTPUT.title, K_OUTPUT )
                        case _:
                            self._func_OTHER_ENTRIES( self.i_output )

        
        def func_l3_t1s2_report( self ):
            """
            Loop for Step 2 of Task 1: Prefab Reports
            * Step 1: Select Output type.
            > Step 2: Select Prefab report.
            * Step 3, if applicable: Select Input type.
            
            A Level 3 command for nested loop handling.
            """
            txt = K_OUTPUT[self.i_output]
            if txt == "Print 1st N Entries":
                txt = str(self.n_print).join(txt.split("N"))
            default_msg = { 
                "top": f"{T} Menu Lvl 3 | {K_MENU[self.i_menu]}",
                "mid": "Step 2: Select a report type.",
                "bot": f"Report: N/A >> Output: {txt}"
            }
            self.msg.update( default_msg )
            while True:
                self._func_MSG_BUBBLE( default_msg )
                CONSOLE.print(R_PFR)
                self.i_pfr = CONSOLE.input(": ").lower()
                match self.i_pfr:
                    case "1":
                        self.b_msg_change = True
                        self.func_l4_t1c1_input()
                    case _ if self.i_pfr in PFR_USER:
                        self.b_msg_change = True
                        view = PFR_KEYS[ int(self.i_pfr)-2 ]
                        df = pd.read_sql_query( PFR_QUERIES[view], self.engine )
                        self._func_EXPORT( df, default_msg, K_PFR[self.i_pfr] )
                    case "p" | "previous":
                        break
                    case "h" | "help":
                        self.func_helpdesk( R_PFR.title, K_PFR )
                    case _:
                        self._func_OTHER_ENTRIES( self.i_pfr )

        
        def func_l4_t1c1_input( self ):
            """
            Loop for Step 3 of Task 1: Prefab Reports
            * Step 1: Select Output type.
            * Step 2: Select Single Table Output.
            > Step 3: Select Input type.
            
            A Level 4 command for nested loop handling.
            """
            txt = K_OUTPUT[self.i_output]
            if txt == "Print 1st N Entries":
                txt = str(self.n_print).join(txt.split("N"))
            default_msg = { 
                "top": f"{T} Menu Lvl 4 | {K_MENU[self.i_menu]}",
                "mid": "Step 3: Select an input type.",
                "bot": f"Input: N/A >> Report: {K_PFR[self.i_pfr]} >> Output: {txt}"
            }
            self.msg.update( default_msg )
            while True:
                self._func_MSG_BUBBLE( default_msg )
                CONSOLE.print( pc("* Fetching table list...", CD), end="\r" )
                # Access and print list.
                D_INPUT = pd.read_sql_query( "SELECT table_name FROM information_schema.tables WHERE table_schema='public'", self.engine, dtype=str )
                D_INPUT = { str(i+1):c for i, c in enumerate(D_INPUT["table_name"]) }
                R_INPUT = FUNC_table_system( "INPUT MENU", { "Enter": CC, "Database Table": "bright_cyan" }, [D_INPUT, D_PHQ], CD )
                CONSOLE.print(R_INPUT)
                # Capture input.
                self.i_input = CONSOLE.input(": ").lower()
                if self.i_input in D_INPUT.keys():
                    self.b_msg_change = True
                    df = pd.read_sql_query( f"SELECT * FROM {D_INPUT[self.i_input]}", self.engine, dtype=str )
                    self._func_EXPORT( df, default_msg, D_INPUT[self.i_input].title() )
                else:
                    match self.i_input:
                        case "p" | "previous":
                            break
                        case "h" | "help":
                            self.func_helpdesk( R_INPUT.title, D_INPUT )
                        case _:
                            self._func_OTHER_ENTRIES( self.i_input )

        
        def _func_EXPORT( self, df: pd.DataFrame, default_msg: dict, fname: str ):
            """Universal function to export the desired output based on OUTPUT MENU: `K_OUTPUT[self.i_output]`

            Args:
                df (pd.DataFrame): DataFrame to handle.
                default_msg (dict): The default message pack of the parent function.
                fname (str): The filename or table title.
            """
            if "Density" in K_OUTPUT[self.i_output]:
                can_graph = True
                try:    # Get one or more number columns.
                    rs = df.select_dtypes( include=[int, float] )
                    rs = rs[rs.columns[0]].drop_duplicates( ignore_index=True )
                except: # Can't graph any density.
                    can_graph = False
                    self.msg.update({ "bot": "ERROR: Can't graph. Try printing or CSV.", "bot_color": "red", "border": "red" })
                #self._func_UNDER_CONSTRUCTION( K_OUTPUT[self.i_output] )

            match self.i_output:    # Check `K_OUTPUT[self.i_output]` = ...
                case "1":           # "Export Table: CSV"
                    fpath = os.path.join( DIR_OUTPUT, f"{fname}.csv" )
                    df.to_csv( fpath )
                    fsplt = fpath.split(os.sep)
                    fshrt = fpath if len(fsplt) < 5 else fsplt[0] + f"{os.sep}...{os.sep}" + os.sep.join(fsplt[-3:])
                    self.msg.update({ "bot": f"Exported to {fshrt}", "bot_color": "green1" })
                    Popen([OPENER, fpath])
                case "2":           # "Export Density Graph"
                    if can_graph:
                        fpath = os.path.join( DIR_OUTPUT, f"{fname} density.png" )
                        fig = plt.figure( fname, dpi=DPI, tight_layout=True, figsize=(3200/DPI, 1800/DPI) )
                        fig.add_axes( rs.plot.density(), label=rs.name )
                        fig.savefig( fpath )
                        fsplt = fpath.split(os.sep)
                        fshrt = fsplt[0] + f"{os.sep}...{os.sep}" + os.sep.join(fsplt[-3:])
                        self.msg.update({ "bot": f"Exported to {fshrt}", "bot_color": "green1" })
                        Popen([OPENER, fpath])
                case "3":           # "Print 1st N Entries"
                    # Get 1st N or less entries.
                    res = df.head( self.n_print )
                    if res.shape[0] == self.n_print and res.shape[0] != df.shape[0]:
                        num = self.n_print
                        res = pd.concat([ res, 
                                        pd.DataFrame( [[f"[{df.shape[0]-self.n_print} more entries]"]*df.shape[1]], columns=df.columns )
                                        ], ignore_index=True)
                    else:
                        num = res.shape[0]
                    # Print all.
                    self.msg.update({ 
                        "top": f"Output View | Preview 1st {num} Entries", "top_color": CD,
                        "mid": fname, "border_color": "bright_white",
                        "bot": "Output printed. Press Enter to return to previous menu.", "bot_color": "green1"
                        })
                    self._func_MSG_BUBBLE( default_msg )
                    CONSOLE.print(FUNC_table_data( 
                        fname, dict.fromkeys( df.columns, "bright_white" ), res, "bright_white" 
                        ))
                    inp = CONSOLE.input( pc("Scroll up for table. Press Enter to continue (or q to quit). ", CD) )
                    match inp:
                        case "q" | "quit":
                            self._func_quit()
                        case _:
                            pass
                case "4":           # "Print Density Statistics"
                    if can_graph:
                        pass
                    self._func_UNDER_CONSTRUCTION( K_OUTPUT[self.i_output] )
                    ### Statistics on rs.
                    '''self.msg.update({ 
                        "top": "Output View | Density Statistics", "top_color": CD,
                        "mid": fname, "border_color": "bright_white",
                        "bot": "Output printed. Press Enter to continue.", "bot_color": "green1"
                        })
                    self._func_msg_bubble( default_msg )
                    CONSOLE.print(FUNC_table_data( 
                        fname, dict.fromkeys( df.columns, "bright_white" ), table, "bright_white" 
                        ))'''
                    #inp = CONSOLE.input( pc("Scroll up for table. Press Enter to continue (or q to quit). ", CD) )
            #

        
        def func_l2_t2s1_output( self ):
            """
            Loop for getting output for Task 2: Create SQL Report
            > Step 1: Select Output type.
            * Step 2: Write SQL command. 

            A Level 2 command for nested loop handling.
            """
            default_msg = {
                "top": f"{T} Menu Lvl 2 | {K_MENU[self.i_menu]}",
                "mid": "Step 1/2: Select an output type for your SQL report.",
                "bot": "Output: N/A"
            }
            self.msg.update( default_msg )
            while True:
                self._func_MSG_BUBBLE( default_msg )
                CONSOLE.print(R_OUTPUT)
                self.i_output = CONSOLE.input(": ").lower()
                if self.i_output in K_OUTPUT.keys():
                    self.b_msg_change = True
                    if K_OUTPUT[self.i_output] == "Print 1st N Entries":
                        self.n_print = IntPrompt.ask( pc("* Input N, the number of rows to preview. Range: [1, 20]. Default: 10.\n", CD),
                                                      console=CONSOLE, choices=[str(i) for i in range(1, 21)], show_choices=False )
                    self.func_l3_sql()
                else:
                    match self.i_output:
                        case "p" | "previous":
                            break
                        case "h" | "help":
                            self.func_helpdesk( R_OUTPUT.title, K_OUTPUT )
                        case _:
                            self._func_OTHER_ENTRIES( self.i_output )

        
        def func_l3_sql( self ):
            """
            Loop for getting output for Task 2: Create SQL Report
            * Step 1: Select Output type.
            > Step 2: Write SQL command. 

            A Level 3 command for nested loop handling.
            """
            txt = K_OUTPUT[self.i_output]
            if txt == "Print 1st N Entries":
                txt = str(self.n_print).join(txt.split("N"))
            default_msg = {
                "top": f"{T} Menu Lvl 3 | {K_MENU[self.i_menu]}",
                "mid": "Step 2/2: Write SQL query in one line, then Enter. 'previous', 'quit' available.",
                "bot": f"Output: {txt}. 'p', 'q' available."
            }
            self.msg.update( default_msg )
            while True:
                self._func_MSG_BUBBLE( default_msg )
                query = CONSOLE.input("SQL Query: ")
                match query:
                    case "p" | "previous":
                        break
                    case "q" | "quit":
                        self._func_quit()
                    case _:
                        fname = f"sql {datetime.strftime( datetime.now(), "%Y %m %d, %H %M %S %f" )}"
                        self.b_msg_change = True
                        try:
                            df = pd.read_sql_query( query, self.engine, dtype=str )
                            self._func_EXPORT( df, default_msg, fname )
                        except:
                            self.msg.update({ 
                                "bot": f"WARNING! Invalid query. Try again. | Output: {txt}",
                                "bot_color": "orange1", "border_color": "orange1"
                                })



    if __name__ == "__main__":
        VE = Venmito_Evaluator()



except Exception as e:
    FUNC_capture_app_error()