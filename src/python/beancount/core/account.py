"""Account object.

These account objects are rather simple and dumb; they do not contain the list
of their associated postings. This is achieved by building a realization; see
realization.py for details.
"""
import re
from collections import namedtuple

from beancount.core import account_types


# A type used to represent an account read in.
Account = namedtuple('Account', 'name type')

def account_from_name(account_name):
    """Create a new account solely from its name.

    Args:
      account_name: A string, the name of the account to create.
    Returns:
      An instance of Account, the account to be created.
    """
    assert isinstance(account_name, str)
    atype = account_name_type(account_name)
    assert atype in account_types.ACCOUNT_TYPES, "Invalid account type: {}".format(atype)
    return Account(account_name, atype)

def account_name_parent(account_name):
    """Return the name of the parent account of the given account.

    Args:
      account_name: A string, the name of the account whose parent to return.
    Returns:
      A string, the name of the parent account of this account.
    """
    assert isinstance(account_name, str)
    if not account_name:
        return None
    components = account_name.split(':')
    components.pop(-1)
    return ':'.join(components)

def account_name_leaf(account_name):
    """Get the name of the leaf of this account.

    Args:
      account_name: A string, the name of the account whose leaf name to return.
    Returns:
      A string, the name of the leaf of the account.
    """
    return account_name.split(':')[-1] if name else None

def account_sortkey(account):
    """Sort a list of accounts, taking into account the type of account.
    Assets, Liabilities, Equity, Income and Expenses, in this order, then
    in the order of the account's name.

    Args:
      account: An instance of Account, which we are to sort.
    Returns:
      A tuple which is to be used as the sort key for lists of accounts.
    """
    return (account_types.TYPES_ORDER[account.type], account.name)

def account_name_sortkey(account_name):
    """Sort a list of accounts, taking into account the type of account.
    Assets, Liabilities, Equity, Income and Expenses, in this order, then
    in the order of the account's name.

    Args:
      account_name: A string, the name of the account to sort.
    Returns:
      A tuple which is to be used as the sort key for lists of accounts.
    """
    type_ = account_name_type(account_name)
    return (account_types.TYPES_ORDER[type_], account_name)

def account_name_type(account_name):
    """Return the type of this account's name.

    Args:
      account_name: A string, the name of the account whose type is to return.
    Returns:
      A string, the type of the account in 'account_name'.
    """
    assert isinstance(account_name, str)
    atype = account_name.split(':')[0]
    assert atype in account_types.ACCOUNT_TYPES, (
        account_name, atype, account_types.ACCOUNT_TYPES)
    return atype

def is_account_name(string):
    """Return true if the given string is an account name.

    Args:
      string: A string, to be checked for account name pattern.
    Returns:
      A boolean, true if the string has the form of an account's name.
    """
    return bool(re.match(
        '([A-Z][A-Za-z0-9\-]+)(:[A-Z][A-Za-z0-9\-]+)+$', string))

def is_account_name_root(account_name):
    """Return true if the account name is one of the root accounts.

    Args:
      account_name: A string, the name of the account to check for.
    Returns:
      A boolean, true if the name is the name of a root account (same
      as an account type).
    """
    return account_name in account_types.ACCOUNT_TYPES

def is_balance_sheet_account(account, options):
    """Return true if the given account is a balance sheet account.
    Assets, liabilities and equity accounts are balance sheet accounts.

    Args:
      account: An instance of Account.
      options: The options dictionary of a file.
    Returns:
      A boolean, true if the account is a balance sheet account.
    """
    return account.type in (options[x] for x in ('name_assets',
                                                 'name_liabilities',
                                                 'name_equity'))

def is_income_statement_account(account, options):
    """Return true if the given account is an income statement account.
    Income and expense accounts are income statement accounts.

    Args:
      account: An instance of Account.
      options: The options dictionary of a file.
    Returns:
      A boolean, true if the account is an income statement account.
    """
    return account.type in (options[x] for x in ('name_income',
                                                 'name_expenses'))

def accountify_dict(string_dict):
    """Convert the dictionary items that have values which are account names into
    Account instances. This is a simple core convenience designed to be used by the
    importers, so that configurations can be specified in terms of strings, like this:

       {'asset': 'Assets:US:Checking', <---- See how this is just a string.
        ...}

    Args:
      string_dict: A dictionary of keys (whichever type) to strings.
    Returns:
      A similar dictionary, whose value strings have been converted to instances of
      Account.
    """
    return {key: account_from_name(value)
            if isinstance(value, str) and is_account_name(value) else value
            for key, value in string_dict.items()}



# FIXME: This needs a bit of review, we can very likely do everything more
# consistently and simpler by just using strings with methods instead of Account
# types. In other words, we can get rid of the Account type and just deal with
# strings. Everything else should be simpler. Do this at some point.
