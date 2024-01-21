def get_min(arr):
    min_index = 0
    for i in range(1, len(arr)):
        if arr[i] < arr[min_index]:
            min_index = i
    return min_index

def get_max(arr):
    max_index = 0
    for i in range(1, len(arr)):
        if arr[i] > arr[max_index]:
            max_index = i
    return max_index

def min_of_2(x, y):
    return x if x < y else y

def min_cash_flow_rec(amount, data_to_return, users):
    mxCredit = get_max(amount)
    mxDebit = get_min(amount)

    if amount[mxCredit] == 0 and amount[mxDebit] == 0:
        return

    min_amount = min_of_2(-amount[mxDebit], amount[mxCredit])
    amount[mxCredit] -= min_amount
    amount[mxDebit] += min_amount

    if mxDebit not in data_to_return:
        data_to_return[mxDebit] = {}

    data_to_return[mxDebit][mxCredit] = min_amount
    min_cash_flow_rec(amount, data_to_return, users)

def min_cash_flow(amount, users):
    data_to_return = {}
    min_cash_flow_rec(amount, data_to_return, users)
    return convert_to_user_data(data_to_return, users)

def convert_to_user_data(data_to_return, users):
    new_dict = {}
    for key, value in data_to_return.items():
        if isinstance(value, dict):
            new_dict[users[key]] = convert_to_user_data(value, users)
        else:
            new_dict[users[key]] = value
    return new_dict

def simplify_expenses(user_balances):
    amount = list(user_balances.values())
    users = list(user_balances.keys())
    return min_cash_flow(amount, users)