-- for regression purposes only, to be removed with testing system
library STD;
use STD.standard.all;

library IEEE;
use IEEE.std_logic_1164.all;

package standard is

    -- Predefined enumeration types

    type BOOLEAN is ( FALSE, TRUE );

    -- The predefined operators for this type are as follows:

    function "and" (_opL, _opR: BOOLEAN) return BOOLEAN;
    function "or" (_opL, _opR: BOOLEAN) return BOOLEAN;
    function "nand" (_opL, _opR: BOOLEAN) return BOOLEAN;
    function "nor" (_opL, _opR: BOOLEAN) return BOOLEAN;
    function "xor" (_opL, _opR: BOOLEAN) return BOOLEAN;
    function "xnor" (_opL, _opR: BOOLEAN) return BOOLEAN;

    function "not" (_op: BOOLEAN) return BOOLEAN;

    function "=" (_opL, _opR: BOOLEAN) return BOOLEAN;
    function "/=" (_opL, _opR: BOOLEAN) return BOOLEAN;
    function "<" (_opL, _opR: BOOLEAN) return BOOLEAN;
    function "<=" (_opL, _opR: BOOLEAN) return BOOLEAN;
    function ">" (_opL, _opR: BOOLEAN) return BOOLEAN;
    function ">=" (_opL, _opR: BOOLEAN) return BOOLEAN;


    type BIT is ( '0', '1' );

    -- The predefined operators for this type are as follows:

    function "and" (_opL, _opR: BIT) return BIT;
    function "or" (_opL, _opR: BIT) return BIT;
    function "nand" (_opL, _opR: BIT) return BIT;
    function "nor" (_opL, _opR: BIT) return BIT;
    function "xor" (_opL, _opR: BIT) return BIT;
    function "xnor" (_opL, _opR: BIT) return BIT;

    function "not" (_op: BIT) return BIT;

    function "=" (_opL, _opR: BIT) return BOOLEAN;
    function "/=" (_opL, _opR: BIT) return BOOLEAN;
    function "<" (_opL, _opR: BIT) return BOOLEAN;
    function "<=" (_opL, _opR: BIT) return BOOLEAN;
    function ">" (_opL, _opR: BIT) return BOOLEAN;
    function ">=" (_opL, _opR: BIT) return BOOLEAN;


    type CHARACTER is (
        NUL, SOH, STX, ETX, EOT, ENQ, ACK, BEL,
        BS, HT, LF, VT, FF, CR, SO, SI,
        DLE, DC1, DC2, DC3, DC4, NAK, SYN, ETB,
        CAN, EM, SUB, ESC, FSP, GSP, RSP, USP,
        ' ', '!', '"', '#', '$', '%', '&', ''',
        '(', ')', '*', '+', ',', '-', '.', '/',
        '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', ':', ';', '<', '=', '>', '?',
        '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
        'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
        'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
        'X', 'Y', 'Z', '[', '\', ']', '^', '_',
        '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
        'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
        'x', 'y', 'z', '{', '|', '}', '~', DEL,
        C128, C129, C130, C131, C132, C133, C134, C135,
        C136, C137, C138, C139, C140, C141, C142, C143,
        C144, C145, C146, C147, C148, C149, C150, C151,
        C152, C153, C154, C155, C156, C157, C158, C159,
        ' ', '¡', '¢', '£', '€', '¥', '|', '§',     -- 1st column is non-breaking space
        '¨', '©', 'ª', '«', '¬', '­', '®', '¯',      -- 6th column appears empty, contains non-rendered soft-hyphen
        '°', '±', '²', '³', '´', 'µ', '¶', '•',
        '¸', '¹', 'º', '»', '¼', '½', '¾', '¿',
        'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç',
        'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï',
        'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', '◊',
        'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß',
        'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç',
        'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï',
        '∂', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', '÷',
        'ø', 'ù', 'ú', 'û', 'ü', 'y', 'þ', 'ÿ');

    -- The predefined operators for this type are as follows:

    function "=" (_opL, _opR: CHARACTER) return BOOLEAN;
    function "/=" (_opL, _opR: CHARACTER) return BOOLEAN;
    function "<" (_opL, _opR: CHARACTER) return BOOLEAN;
    function "<=" (_opL, _opR: CHARACTER) return BOOLEAN;
    function ">" (_opL, _opR: CHARACTER) return BOOLEAN;
    function ">=" (_opL, _opR: CHARACTER) return BOOLEAN;


    type SEVERITY_LEVEL is ( NOTE, WARNING, ERROR, FAILURE );

    -- The predefined operators for this type are as follows:

    function "=" (_opL, _opR: SEVERITY_LEVEL) return BOOLEAN;
    function "/=" (_opL, _opR: SEVERITY_LEVEL) return BOOLEAN;
    function "<" (_opL, _opR: SEVERITY_LEVEL) return BOOLEAN;
    function "<=" (_opL, _opR: SEVERITY_LEVEL) return BOOLEAN;
    function ">" (_opL, _opR: SEVERITY_LEVEL) return BOOLEAN;
    function ">=" (_opL, _opR: SEVERITY_LEVEL) return BOOLEAN;


    type _universal_integer; -- is range 16#8000_0000_0000_0000# to 16#7fff_ffff_ffff_ffff#;

    -- The predefined operators for this type are as follows:

    function "=" (_opL, _opR: _universal_integer) return BOOLEAN;
    function "/=" (_opL, _opR: _universal_integer) return BOOLEAN;
    function "<" (_opL, _opR: _universal_integer) return BOOLEAN;
    function "<=" (_opL, _opR: _universal_integer) return BOOLEAN;
    function ">" (_opL, _opR: _universal_integer) return BOOLEAN;
    function ">=" (_opL, _opR: _universal_integer) return BOOLEAN;

    function "+" (_op: _universal_integer) return _universal_integer;
    function "-" (_op: _universal_integer) return _universal_integer;
    function "abs" (_op: _universal_integer) return _universal_integer;

    function "+" (_opL, _opR: _universal_integer) return _universal_integer;
    function "-" (_opL, _opR: _universal_integer) return _universal_integer;
    function "*" (_opL, _opR: _universal_integer) return _universal_integer;
    function "/" (_opL, _opR: _universal_integer) return _universal_integer;
    function "mod" (_opL, _opR: _universal_integer) return _universal_integer;
    function "rem" (_opL, _opR: _universal_integer) return _universal_integer;
    function "**" (_opL, _opR: _universal_integer) return _universal_integer;


    type _universal_real; -- is range -3.4E+38 to 3.4E+38;

    -- The predefined operators for this type are as follows:

    function "=" (_opL, _opR: _universal_real) return BOOLEAN;
    function "/=" (_opL, _opR: _universal_real) return BOOLEAN;
    function "<" (_opL, _opR: _universal_real) return BOOLEAN;
    function "<=" (_opL, _opR: _universal_real) return BOOLEAN;
    function ">" (_opL, _opR: _universal_real) return BOOLEAN;
    function ">=" (_opL, _opR: _universal_real) return BOOLEAN;

    function "+" (_op: _universal_real) return _universal_real;
    function "-" (_op: _universal_real) return _universal_real;
    function "abs" (_op: _universal_real) return _universal_real;

    function "+" (_opL, _opR: _universal_real) return _universal_real;
    function "-" (_opL, _opR: _universal_real) return _universal_real;
    function "*" (_opL, _opR: _universal_real) return _universal_real;
    function "*" (_opL: _universal_real; _opR: _universal_integer) return _universal_real;
    function "*" (_opL: _universal_integer; _opR: _universal_real) return _universal_real;
    function "/" (_opL, _opR: _universal_real) return _universal_real;
    function "/" (_opL: _universal_real; _opR: _universal_integer) return _universal_real;


    -- Predefined numeric types

    type INTEGER is range -2_147_483_648 to 2_147_483_647;

    -- The predefined operators for this type are as follows:

    function "=" (_opL, _opR: INTEGER) return BOOLEAN;
    function "/=" (_opL, _opR: INTEGER) return BOOLEAN;
    function "<" (_opL, _opR: INTEGER) return BOOLEAN;
    function "<=" (_opL, _opR: INTEGER) return BOOLEAN;
    function ">" (_opL, _opR: INTEGER) return BOOLEAN;
    function ">=" (_opL, _opR: INTEGER) return BOOLEAN;

    function "+" (_op: INTEGER) return INTEGER;
    function "-" (_op: INTEGER) return INTEGER;
    function "abs" (_op: INTEGER) return INTEGER;

    function "+" (_opL, _opR: INTEGER) return INTEGER;
    function "-" (_opL, _opR: INTEGER) return INTEGER;
    function "*" (_opL, _opR: INTEGER) return INTEGER;
    function "/" (_opL, _opR: INTEGER) return INTEGER;
    function "mod" (_opL, _opR: INTEGER) return INTEGER;
    function "rem" (_opL, _opR: INTEGER) return INTEGER;
    function "**" (_opL, _opR: INTEGER) return INTEGER;
    function "**" (_opL: _universal_integer; _opR: INTEGER) return _universal_integer;
    function "**" (_opL: _universal_real; _opR: INTEGER) return _universal_real;


    type REAL is range _universal_real'range;

    -- The predefined operators for this type are as follows:

    function "=" (_opL, _opR: REAL) return BOOLEAN;
    function "/=" (_opL, _opR: REAL) return BOOLEAN;
    function "<" (_opL, _opR: REAL) return BOOLEAN;
    function "<=" (_opL, _opR: REAL) return BOOLEAN;
    function ">" (_opL, _opR: REAL) return BOOLEAN;
    function ">=" (_opL, _opR: REAL) return BOOLEAN;

    function "+" (_op: REAL) return REAL;
    function "-" (_op: REAL) return REAL;
    function "abs" (_op: REAL) return REAL;

    function "+" (_opL, _opR: REAL) return REAL;
    function "-" (_opL, _opR: REAL) return REAL;
    function "*" (_opL, _opR: REAL) return REAL;
    function "/" (_opL, _opR: REAL) return REAL;
    function "**" (_opL: REAL; _opR: INTEGER) return REAL;

    
    -- Predefined type TIME:

    type TIME is range _universal_integer'range units
        fs;             -- femtosecond
        ps = 1000 fs;   -- picosecond
        ns = 1000 ps;   -- nanosecond
        us = 1000 ns;   -- microsecond
        ms = 1000 us;   -- millisecond
        sec = 1000 ms;  -- second
        min = 60 sec;   -- minute
        hr = 60 min;    -- hour
    end units;

    -- The predefined operators for this type are as follows:

    function "=" (_opL, _opR: TIME) return BOOLEAN;
    function "/=" (_opL, _opR: TIME) return BOOLEAN;
    function "<" (_opL, _opR: TIME) return BOOLEAN;
    function "<=" (_opL, _opR: TIME) return BOOLEAN;
    function ">" (_opL, _opR: TIME) return BOOLEAN;
    function ">=" (_opL, _opR: TIME) return BOOLEAN;

    function "+" (_op: TIME) return TIME;
    function "-" (_op: TIME) return TIME;
    function "abs" (_op: TIME) return TIME;

    function "+" (_opL, _opR: TIME) return TIME;
    function "-" (_opL, _opR: TIME) return TIME;
    function "*" (_opL: TIME; _opR: INTEGER) return TIME;
    function "*" (_opL: TIME; _opR: REAL) return TIME;
    function "*" (_opL: INTEGER; _opR: TIME) return TIME;
    function "*" (_opL: REAL; _opR: TIME) return TIME;
    function "/" (_opL: TIME; _opR: INTEGER) return TIME;
    function "/" (_opL: TIME; _opR: REAL) return TIME;
    function "/" (_opL, _opR: TIME) return _universal_integer;


    subtype DELAY_LENGTH is TIME range 0 fs to TIME'HIGH;


    -- A function that returns universal_to_physical_time ( T[c] ), (see 1076-200 12.6.4)

    impure function NOW return DELAY_LENGTH;


    -- Predefined numeric subtypes:

    subtype NATURAL is INTEGER range 0 to INTEGER'HIGH;
    subtype POSITIVE is INTEGER range 1 to INTEGER'HIGH;


    -- Predefined array types:

    type STRING is array (POSITIVE range <>) of CHARACTER;

    -- The predefined operators for this type are as follows:

    function "=" (_opL, _opR: STRING) return BOOLEAN;
    function "/=" (_opL, _opR: STRING) return BOOLEAN;
    function "<" (_opL, _opR: STRING) return BOOLEAN;
    function "<=" (_opL, _opR: STRING) return BOOLEAN;
    function ">" (_opL, _opR: STRING) return BOOLEAN;
    function ">=" (_opL, _opR: STRING) return BOOLEAN;

    function "&" (_opL, _opR: STRING) return STRING;
    function "&" (_opL: STRING; _opR: CHARACTER) return STRING;
    function "&" (_opL: CHARACTER; _opR: STRING) return STRING;
    function "&" (_opL, _opR: CHARACTER) return STRING;


    type BIT_VECTOR is array (NATURAL range <>) of BIT;

    -- The predefined operators for this type are as follows:

    function "and" (_opL, _opR: BIT_VECTOR) return BIT_VECTOR;
    function "or" (_opL, _opR: BIT_VECTOR) return BIT_VECTOR;
    function "nand" (_opL, _opR: BIT_VECTOR) return BIT_VECTOR;
    function "nor" (_opL, _opR: BIT_VECTOR) return BIT_VECTOR;
    function "xor" (_opL, _opR: BIT_VECTOR) return BIT_VECTOR;
    function "xnor" (_opL, _opR: BIT_VECTOR) return BIT_VECTOR;

    function "not" (_op: BIT_VECTOR) return BIT_VECTOR;

    function "sll" (_opL, _opR: BIT_VECTOR) return BIT_VECTOR;
    function "srl" (_opL, _opR: BIT_VECTOR) return BIT_VECTOR;
    function "sla" (_opL, _opR: BIT_VECTOR) return BIT_VECTOR;
    function "sra" (_opL, _opR: BIT_VECTOR) return BIT_VECTOR;
    function "ror" (_opL, _opR: BIT_VECTOR) return BIT_VECTOR;
    function "rol" (_opL, _opR: BIT_VECTOR) return BIT_VECTOR;

    function "=" (_opL, _opR: BIT_VECTOR) return BOOLEAN;
    function "/=" (_opL, _opR: BIT_VECTOR) return BOOLEAN;
    function "<" (_opL, _opR: BIT_VECTOR) return BOOLEAN;
    function "<=" (_opL, _opR: BIT_VECTOR) return BOOLEAN;
    function ">" (_opL, _opR: BIT_VECTOR) return BOOLEAN;
    function ">=" (_opL, _opR: BIT_VECTOR) return BOOLEAN;

    function "&" (_opL, _opR: BIT_VECTOR) return BIT_VECTOR;
    function "&" (_opL: BIT_VECTOR; _opR: BIT) return BIT_VECTOR;
    function "&" (_opL: BIT; _opR: BIT_VECTOR) return BIT_VECTOR;
    function "&" (_opL, _opR: BIT) return BIT_VECTOR;


    -- The predefined types for opening files:

    type FILE_OPEN_KIND is (
        READ_MODE,      -- Resulting access mode is read-only.
        WRITE_MODE,     -- Resulting access mode is write-only.
        APPEND_MODE);   -- Resulting access mode is write-only; information 
                        -- is appended to the end of the existing file.

    -- The predefined operators for this type are as follows                        

    function "=" (_opL, _opR: FILE_OPEN_KIND) return BOOLEAN;
    function "/=" (_opL, _opR: FILE_OPEN_KIND) return BOOLEAN;
    function "<" (_opL, _opR: FILE_OPEN_KIND) return BOOLEAN;
    function "<=" (_opL, _opR: FILE_OPEN_KIND) return BOOLEAN;
    function ">" (_opL, _opR: FILE_OPEN_KIND) return BOOLEAN;
    function ">=" (_opL, _opR: FILE_OPEN_KIND) return BOOLEAN;


    type FILE_OPEN_STATUS is (
        OPEN_OK,        -- File open was successful.
        STATUS_ERROR,   -- File object was already open.
        NAME_ERROR,     -- External file not found or inaccessible.
        MODE_ERROR);    -- Could not open file with requested access mode

    -- The predefined operators for this type are as follows                        

    function "=" (_opL, _opR: FILE_OPEN_STATUS) return BOOLEAN;
    function "/=" (_opL, _opR: FILE_OPEN_STATUS) return BOOLEAN;
    function "<" (_opL, _opR: FILE_OPEN_STATUS) return BOOLEAN;
    function "<=" (_opL, _opR: FILE_OPEN_STATUS) return BOOLEAN;
    function ">" (_opL, _opR: FILE_OPEN_STATUS) return BOOLEAN;
    function ">=" (_opL, _opR: FILE_OPEN_STATUS) return BOOLEAN;


    -- The 'FOREIGN attribute:

    attribute FOREIGN: STRING;

end package standard;
