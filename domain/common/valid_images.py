def valid_screens_size(screens, max_size: int, error_message: str) -> dict[str, str]:
    errors = {}
    for i, screen in enumerate(screens):
        if screen.size > max_size:
            errors[f"file{i + 1}"] = [error_message]

    return errors
