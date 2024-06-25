def get_comma_separated_values(arr, *keys):
    values = []
    for item in arr:
        current_value = item
        for key in keys:
            if isinstance(current_value, dict) and key in current_value:
                current_value = current_value[key]
            else:
                current_value = None
                break
        if current_value is not None:
            values.append(str(current_value))
    return ', '.join(values)