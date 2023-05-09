# File: oik_autosaver.py - **** YOU BLENDER AUTOSAVE
# Author: itsOiK
# Date: 02/06-22
# v0.0.3: 30/11-22
# v0.0.4: 13/04-23

import bpy
from bpy.app.handlers import persistent
from typing import Union, Any
import datetime as dt

SAVE_INTERVAL: float = 120.0
INITIAL_WAIT: float = 15.0
CONTINUE: bool = True
PATH: Union[None, str] = None

bl_info = {
    "name": "Oik's AutoSaver for Blender",
    "blender": (3, 0, 2),
    "category": "Object",
    "author": "ItsOik",
    "version": (0, 0, 4),
    "description": "Because blender autosave can go **** a donkey!"
}

# TODO add info popup when saving
# class InfoTextOutput(bpy.types.Operator):
#     bl_idname = "oikautosave.infotextoutput"
#     bl_label = "Testing Things"

#     def execute(self, context):
#         _print(context)
#         self.report({'INFO'}, "test")
#         return {'FINISHED'}


def check_if_dirty() -> bool:
    """Checks if document is dirty
    Returns: bool
    """
    return bpy.data.is_dirty


def auto_save() -> Union[int, None]:
    """Does the saving
    Returns:
        None: ...
    """

    bpy.ops.oikautosave.infotextoutput()
    path = bpy.data.filepath
    if path and check_if_dirty():
        filename = path.split("\\")[-1]
        location = "\\".join(path.split("\\")[:-1])
        bpy.ops.wm.save_as_mainfile(
            filepath=location + "\\_" + filename, copy=True)
        _print(f"SAVING: '{filename}' - **** YOU BLENDER AUTOSAVE!")
        _print(f"Location: '{location}'")
    elif not path and check_if_dirty():
        bpy.ops.wm.save_mainfile('INVOKE_AREA')
        _print("Prompted user for initial save")
    elif not check_if_dirty():
        _print(f"Skipped saving, not dirty, next attempt in: {INITIAL_WAIT}")
        set_timer(INITIAL_WAIT)
    return None


def set_timer(amount_to_wait: float = 0) -> None:
    """Handles setting and or resetting timer

    Args:
        amount_to_wait (float): amount of time to wait before next save
    """
    global CONTINUE
    if CONTINUE:
        extra_string = ""
        if bpy.app.timers.is_registered(auto_save):
            bpy.app.timers.unregister(auto_save)
        extra_string += f"Next save in {amount_to_wait} seconds"
        bpy.app.timers.register(
            auto_save,
            first_interval=amount_to_wait,
            persistent=True
        )
        _print(f"{extra_string}")
    else:
        _print(f"Stopped AutoSaving")


@persistent
def save_handler(dummy: Any) -> None:
    """Handler for what to do after save occurs

    Args:
        dummy (Any): dont be a dummy!
    """
    global SAVE_INTERVAL
    set_timer(SAVE_INTERVAL)


@persistent
def load_handler(dummy: Any) -> None:
    """Handler for what to do after blender completely loads

    Args:
        dummy (Any): dont be a dummy!
    """
    global INITIAL_WAIT
    global SAVE_INTERVAL

    path = "New File: Untitled.blend"
    wait = INITIAL_WAIT
    if bpy.data.filepath:
        path = bpy.data.filepath
        wait = SAVE_INTERVAL
    set_timer(wait)
    _print(f"Load Handler Loaded: {path}")


def register() -> None:
    """Register handlers"""
    global CONTINUE
    CONTINUE = True
    _print("Enabled: Oik's AutoSaver for Blender")
    _print("Setting load-handlers")
    bpy.app.handlers.load_post.append(load_handler)
    _print("Setting save-handlers")
    bpy.app.handlers.save_post.append(save_handler)
    # TODO add info popup when saving
    # _print("Setting info output")
    # bpy.utils.register_class(InfoTextOutput)
    set_timer(INITIAL_WAIT)


def unregister() -> None:
    """Un-register handlers"""
    global CONTINUE
    _print("Removing load-handlers")
    bpy.app.handlers.load_post.remove(load_handler)
    _print("Removing save-handlers")
    bpy.app.handlers.save_post.remove(save_handler)
    _print("Removing info output")
    # TODO add info popup when saving
    # bpy.utils.unregister_class(InfoTextOutput)
    # CONTINUE = False
    if bpy.app.timers.is_registered(auto_save):
        _print("Removing AutoSave timer")
        bpy.app.timers.unregister(auto_save)
    _print("Disabled: Oik's AutoSaver for Blender")


def _print(string: str) -> None:
    """i got bored...

    Args:
        string (str): string to print
    """
    now = dt.datetime.now().strftime(("%H:%M:%S"))
    print(f"[Oik's AutoSaver]: {now} - {string}")


if __name__ == "__main__":
    register()
