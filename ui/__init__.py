# ui/__init__.py

def bind_enter_navigation(entries, final_action=None):
    """
    Binds Enter key to move focus through entry widgets.
    On the last entry, it runs final_action (if given).
    """
    for i, entry in enumerate(entries):
        def handler(event, idx=i):
            if idx < len(entries) - 1:
                entries[idx + 1].focus_set()
            else:
                if final_action:
                    final_action()
        entry.bind("<Return>", handler)
