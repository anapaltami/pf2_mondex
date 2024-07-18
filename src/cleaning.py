import pandas as pd
import re


def clean_trailing_commas(text):
    if isinstance(text, str):
        return text.rstrip(', ')
    return text


def ensure_semicolon_after_numbers(text):
    if pd.isna(text):
        return text
    return re.sub(r'(\+\d+)(?![\d;])', r'\1;', text)


def fill_empty_parentheses(perception_text, precise_ids, imprecise_ids, monster_id):
    if pd.isna(perception_text):
        return perception_text
    empty_paren_variations = ['()', '( )', '() ', '( ) ']
    for variation in empty_paren_variations:
        if variation in perception_text:
            if monster_id in precise_ids:
                perception_text = perception_text.replace(variation, '(precise)')
            elif monster_id in imprecise_ids:
                perception_text = perception_text.replace(variation, '(imprecise)')
    return perception_text


def correct_perception_entries(df, corrections):
    for monster_id, correct_text in corrections.items():
        df.loc[df['ID'] == monster_id, 'Perception'] = correct_text
    return df


def remove_comma_before_semicolon(text):
    if isinstance(text, str):
        return re.sub(r',\s*;', ';', text)
    return text


def clean_data(df):
    # drop duplicate entries
    df.drop_duplicates(subset=['Name'], keep='first', inplace=True)

    # fill null values
    df['Alignment'] = df['Alignment'].fillna('None')
    df['Traits'] = df['Traits'].fillna('None')

    # remove trailing commas
    columns_to_clean = ['Traits', 'Perception', 'Languages', 'Skills', 'Resistances', 'Speed']
    for column in columns_to_clean:
        df[column] = df[column].apply(clean_trailing_commas)

    # clean Perception column
    df['Perception'] = df['Perception'].apply(ensure_semicolon_after_numbers)

    # fill empty parentheses in perception column
    imprecise_ids = [
        47, 80, 90, 102, 117, 118, 119, 120, 121, 122, 123, 124, 125, 159, 160, 161, 163, 164, 175, 182, 183, 185, 186,
        193, 201, 202, 208, 209, 213, 215, 224, 228, 236, 245, 248, 249, 259, 265, 266, 267, 268, 269, 270, 271, 276,
        284, 285, 286, 287, 289, 290, 294, 303, 329, 335, 336, 341, 342, 343, 347, 356, 365, 366, 369, 371, 379, 380,
        381, 382, 393, 397, 402, 403, 410, 411, 416, 421
    ]
    precise_ids = [320]
    df['Perception'] = df.apply(
        lambda row: fill_empty_parentheses(row['Perception'], precise_ids, imprecise_ids, row['ID']), axis=1)

    # fix special case perception entries
    perception_corrections = {
        47: "+10; low-light vision, scent (imprecise) 30 feet",
        57: "+18; darkvision, thoughtsense 60 feet",
        80: "+16; darkvision, scent (imprecise) 30 feet",
        90: "+20; darkvision, plaguesense (imprecise) 60 feet",
        91: "+28; darkvision, lifesense 30 feet, truesight",
        102: "+30; darkvision, scent (imprecise) 60 feet, truesight",
        117: "+6; low-light vision, scent (imprecise) 30 feet",
        118: "+7; low-light vision, scent (imprecise) 30 feet",
        119: "+12; low-light vision, scent (imprecise) 30 feet",
        120: "+15; low-light vision, scent (imprecise) 30 feet",
        121: "+16; low-light vision, scent (imprecise) 30 feet",
        122: "+16; low-light vision, scent (imprecise) 30 feet",
        123: "+19; low-light vision, scent (imprecise) 30 feet",
        124: "+6; low-light vision, scent (imprecise) 30 feet",
        125: "+7; low-light vision, scent (imprecise) 30 feet",
        159: "+9; darkvision, scent (imprecise) 30 feet",
        160: "+12; darkvision, scent (imprecise) 30 feet, smoke vision",
        161: "+13; darkvision, scent (imprecise) 30 feet",
        163: "+14; darkvision, scent (imprecise) 30 feet, snow vision",
        164: "+15; darkvision, sandstorm sight, scent (imprecise) 30 feet",
        175: "+11; low-light vision, scent (imprecise) 30 feet",
        183: "+12; darkvision, tremorsense (imprecise) 60 feet",
        185: "+16; darkvision, tremorsense (imprecise) 80 feet",
        186: "+20; darkvision, tremorsense (imprecise) 90 feet",
        187: "+9; darkvision, smoke vision",
        188: "+10; darkvision, smoke vision",
        190: "+16; darkvision, smoke vision",
        192: "+3; darkvision, fog vision",
        193: "+3; darkvision, tremorsense (imprecise) 30 feet",
        194: "+3; darkvision, smoke vision",
        201: "+13; low-light vision, scent (imprecise) 30 feet",
        202: "+18; low-light vision, scent (imprecise) 30 feet",
        213: "+15; darkvision, tremorsense (imprecise) 60 feet",
        215: "+16; (18 to Sense Motive) darkvision, wavesense (imprecise) 60 feet",
        224: "+22; cloudsight, low-light vision, scent (imprecise) 30 feet",
        236: "+6; low-light vision, scent (imprecise) 30 feet",
        245: "+4; darkvision, scent (imprecise) 30 feet",
        248: "+13; darkvision, scent (imprecise) 60 feet",
        249: "+29; darkvision, manifold vision, tremorsense (imprecise) 30 feet",
        250: "+41; darkvision, see the unseen, status sight, truesight",
        251: "+32; darkvision, see the unseen, status sight, truesight",
        259: "+9; darkvision, scent (imprecise) 60 feet",
        265: "+4; low-light vision, scent (imprecise) 30 feet",
        266: "+5; low-light vision, scent (imprecise) 30 feet",
        267: "+5; low-light vision, scent (imprecise) 30 feet",
        268: "+6; low-light vision, scent (imprecise) 30 feet",
        269: "+17; low-light vision, scent (imprecise) 30 feet",
        270: "+6; low-light vision, scent (imprecise) 30 feet",
        271: "+9; low-light vision, scent (imprecise) 30 feet",
        276: "+16; low-light vision, scent (imprecise) 60 feet",
        284: "+26; darkvision, scent (imprecise) 60 feet, truesight",
        285: "+29; darkvision, scent (imprecise) 60 feet, truesight",
        286: "+35; darkvision, scent (imprecise) 60 feet, truesight",
        287: "+37; darkvision, scent (imprecise) 60 feet, truesight",
        289: "+7; low-light vision, scent (imprecise) 30 feet",
        290: "+11; low-light vision, scent (imprecise) 30 feet",
        294: "+14; darkvision, scent (imprecise) 30 feet",
        303: "+24; darkvision, tremorsense (imprecise) 60 feet",
        329: "+12; darkvision, scent (imprecise) 30 feet",
        339: "+6; darkvision, lifesense 60 feet",
        340: "+28; darkvision, lifesense 60 feet",
        341: "+8; low-light vision, scent (imprecise) 30 feet",
        342: "+15; low-light vision, scent (imprecise) 30 feet",
        343: "+29; tremorsense (imprecise) 60 feet",
        347: "+5; low-light vision, scent (imprecise) 30 feet",
        356: "+9; darkvision, tremorsense (imprecise) 60 feet",
        371: "+10; darkvision, sin scent (imprecise) 30 feet",
        379: "+5; low-light vision, scent (imprecise) 30 feet",
        380: "+6; low-light vision, scent (imprecise) 30 feet",
        381: "+7; low-light vision, scent (imprecise) 30 feet",
        382: "+17; low-light vision, scent (imprecise) 60 feet",
        386: "+7; darkvision, web sense",
        388: "+22; darkvision, web sense",
        393: "+31; darkvision, tremorsense (imprecise) 120 feet",
        397: "+13; darkvision, scent (imprecise) 30 feet",
        402: "+8; darkvision, scent (imprecise) 30 feet",
        403: "+14; darkvision, scent (imprecise) 30 feet",
        410: "+8; low-light vision, scent (imprecise) 30 feet",
        411: "+9; low-light vision, scent (imprecise) 30 feet",
        416: "+10; low-light vision, scent (imprecise) 30 feet",
        421: "+15; darkvision, scent (imprecise) 30 feet"
    }
    df = correct_perception_entries(df, perception_corrections)

    # clean Languages column
    df['Languages'] = df['Languages'].replace('UNKNOWN', 'None')
    df['Languages'] = df['Languages'].apply(remove_comma_before_semicolon)

    return df
