_next_id = 0


def get_id():  # ik this is a dirty function but i don't want to be passing around a ton of _next_ids everywhere
    global _next_id
    _next_id += 1
    return _next_id - 1
