from enum import Enum


class Log(str, Enum):
    browser = "browser"
    get_facts = "get_facts"
    update_fact = "update_fact"
    study = "study"
    suspend = "suspend"
    delete = "delete"
    report = "report"
    mark = "mark"
    undo_suspend = "undo_suspend"
    undo_delete = "undo_delete"
    undo_report = "undo_report"
    undo_study = "undo_study"  # currently unimplemented
    undo_mark = "undo_mark"
    resolve_report = "resolve_report"
    clear_report_or_suspend = "clear_report_or_suspend"
    assign_viewer = "assign_viewer"
    reassign_model = "reassign_model"
