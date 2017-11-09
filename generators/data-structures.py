import csv
import argparse
import inflection

LANG_GO = "go"
LANG_HAKSELL = "haskell"

TYPE_STRING = "string"
TYPE_INT = "int"
TYPE_FLOAT = "float"


def define_parameters(parser):
    """Creates the support command line options"""
    parser.add_argument("--input", help="the path to the input CSV file",type=str, required=True )
    parser.add_argument("--go", help="create a Go datastructure", action="store_true")
    parser.add_argument("--haskell", help="create a Haskell datastructure", action="store_true")
    parser.add_argument("--name", help="name of the datastructure being created", type=str)
    parser.add_argument("--verbose", help="more output during the parsing and creation of the datastructures", action="store_true")

def get_data_type(col_val):
    """Deterimes if the current value is numeric or a string"""
    dtype = TYPE_STRING

    if col_val.replace('.', '',1).replace ('-', '',1).replace(',', '', -1).isdigit():
        if '.' in col_val:
            dtype = TYPE_FLOAT
        else:
            dtype = TYPE_INT

    return dtype

def parse_file(args):
    """Parses the CSV file and tracks the datatypes of each column

    this will be a map with the column name and the data type of the col
    all cols will default to a empty string so that I will know if a column has already
    been declared a string, once a string always string.  If after all lines
    have been read and a column still has an empty string it will be set as 
    a string.  Currently the values for data types are string, int or float"""

    data_types = []
    headers = []

    with open(args.input, "r") as csvfile:
        reader = csv.reader(csvfile)
        have_columns = False

        for line in reader:
            if have_columns:
                index = 0
                for col in line:
                    if col != "" and data_types[index] != TYPE_STRING:
                        data_types[index] = get_data_type(col)
                    index += 1

            else:
                headers = line   
                for col in line:
                    data_types.append("")
                have_columns = True 

    return headers, data_types

def col_name_cleaner(col_name):
    if col_name[0].isdigit():
        if col_name == "2B":
            return "doubles"
        if col_name == "3B":
            return "triples"
    
    return col_name

def convert_to_lang_specific_type(typeMap, type):
    if type in typeMap:
        return typeMap[type]

    return type

def create_haskell_datastructure(args, headers, data_types):
    name = "CsvObj"
    comma = ""
    index = 0
    if args.name != None:
        name = args.name 
    
    print "data", name, "=", name , "{"
    for raw_col in headers:
        if index > 0:
            comma=","
        
        col = col_name_cleaner(raw_col).lower()
        print "  ", comma, col[:1].lower() + col[1:], "::", data_types[index].title()
        index += 1
    print "} deriving (Show)"

def create_go_datastructure(args, headers, data_types):
    types = {
        "float" : "float64"
    }
    name = "CsvObj"
    index = 0

    if args.name != None:
        name = args.name 
     
    print "type", name, "struct {"
    for raw_col in headers:
        col = col_name_cleaner(raw_col).lower()
        print "  ", col.title(), " ", convert_to_lang_specific_type(types, data_types[index]), "\t`json:\"" +inflection.camelize(col,False) +"\"`"
        index += 1
    print "}"

def main():
    parser = argparse.ArgumentParser(description="Test the SMS notification Service.")
    define_parameters(parser)
    args = parser.parse_args()

    LANGUAGE_FUNCS = {
        LANG_HAKSELL: create_haskell_datastructure,
        LANG_GO: create_go_datastructure
    }

    if args.go:
        language = LANG_GO

    if args.haskell:
        language = LANG_HAKSELL

    if language == None:
        print "ERROR: Please select a language\n"
        parser.print_usage()
        parser.exit()
    
    headers, data_types = parse_file(args)
    if args.verbose:
        print "Data types\n------------------------------------------------------------------"
        index = 0
        for field in headers:
            print field, " ", data_types[index]
            index += 1

    LANGUAGE_FUNCS[language](args, headers, data_types)


if __name__ == "__main__":
    main()