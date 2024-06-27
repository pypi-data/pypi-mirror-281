from .common import remove_duplicate_symbols, remove_unmatched_quotes, remove_commas_in_num, default_trs_table, normalize_symbol

def ko_filter(text) :
    text = normalize_symbol(text)
    text = remove_duplicate_symbols(text)
    text = remove_unmatched_quotes(text)
    text = remove_commas_in_num(text)
    return text


