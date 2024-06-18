

# File: oik_autosaver.py - **** YOU BLENDER AUTOSAVE
# Author: itsOiK
# Date: 02/06-22
# v0.0.3: 30/11-22
# v0.0.4: 13/04-23
# v0.0.5: 17/08-23

import atexit
import bpy  # Import blender library
# Import persistent for Add-on persistence
from bpy.app.handlers import persistent
from typing import Union, Any  # Importing typing for type-hinting
import datetime as dt  # Importing DateTime for timetracking
import atexit  # Import atexit for triggering save prompt on exit


SAVE_INTERVAL: float = 120.0  # how long to wait between saves
# how long to wait after Blender has started or loaded a new file
INITIAL_WAIT: float = 15.0
CONTINUE: bool = True  # boolean for disabling
PATH: Union[None, str] = None  # variable to track filepath
last_saved = dt.datetime.now  # variable to track last time save happened
bl_info = {
    "name": "Oik's AutoSaver for Blender",
    "blender": (3, 0, 2),
    "category": "Object",
    "author": "ItsOik",
    "version": (0, 0, 4),
    "description": "Because blender autosave can go **** a donkey!"
}  # Blender Add-on metadata


# TODO add info popup when saving
# class InfoTextOutput(bpy.types.Operator):
#     bl_idname = "oikautosave.infotextoutput"
#     bl_label = "Testing Things"

#     def execute(self, context):
#         _print(context)
#         self.report({'INFO'}, "test")
#         return {'FINISHED'}


def on_exit():
    if check_if_dirty():
        global last_saved

        _print("last saved: " + last_saved)
        # if isDirty + (lastSaved > someAmount), prompt user for save
        path = bpy.data.filepath
        # bpy.ops.wm.save_mainfile('INVOKE_AREA')
        # _print("Prompted user for save before exit")
        # if not isDirty BUT (lastSaved > someGreaterAmount), prompt user for save

    ...


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

    # bpy.ops.oikautosave.infotextoutput()

    path = bpy.data.filepath

    if check_if_dirty():
        # is dirty
        if path:
            # is exsisting project
            filename = path.split("\\")[-1]
            location = "\\".join(path.split("\\")[:-1])
            bpy.ops.wm.save_as_mainfile(
                filepath=location + "\\_" + filename, copy=True)
            _print(f"SAVING: '{filename}' - **** YOU BLENDER AUTOSAVE!")
            _print(f"Location: '{location}'")
            #TODO attempted setting back to dirty to not interfere with how "dirty" should work
            #bpy.data.is_dirty = True
        else:
            # is not exsisting project
            bpy.ops.wm.save_mainfile('INVOKE_AREA')
            _print("Prompted user for initial save")
        if not check_if_dirty():
            # was dirty and is not dirty anymore
            global last_saved
            last_saved = dt.datetime.now
    else:
        # is not dirty
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
    global last_saved
    set_timer(SAVE_INTERVAL)
    last_saved = dt.datetime.now


@persistent
def load_handler(dummy: Any) -> None:
    """Handler for what to do after blender completely loads

    Args:
        dummy (Any): dont be a dummy!
    """
    global INITIAL_WAIT
    global SAVE_INTERVAL
    global last_saved
    path = "New File: Untitled.blend"
    wait = INITIAL_WAIT
    if bpy.data.filepath:
        path = bpy.data.filepath
        wait = SAVE_INTERVAL
    set_timer(wait)
    last_saved = dt.datetime.now
    _print(f"Load Handler Loaded: {path}")


def register() -> None:
    """Register handlers"""
    global CONTINUE
    _print("Enabled: Oik's AutoSaver for Blender")
    _print("Setting load-handlers")
    bpy.app.handlers.load_post.append(load_handler)
    _print("Setting save-handlers")
    bpy.app.handlers.save_post.append(save_handler)

    # TODO add info popup when saving
    # _print("Setting info output")
    # bpy.utils.register_class(InfoTextOutput)

    _print("Setting on-exit")
    atexit.register(on_exit)
    set_timer(INITIAL_WAIT)
    CONTINUE = True


def unregister() -> None:
    """Un-register handlers"""
    global CONTINUE
    _print("Removing load-handlers")
    bpy.app.handlers.load_post.remove(load_handler)
    _print("Removing save-handlers")
    bpy.app.handlers.save_post.remove(save_handler)

    # TODO add info popup when saving
    # _print("Removing info output")
    # bpy.utils.unregister_class(InfoTextOutput)

    if bpy.app.timers.is_registered(auto_save):
        _print("Removing AutoSave timer")
        bpy.app.timers.unregister(auto_save)
    _print("Removing on-exit")
    atexit.unregister(on_exit)
    _print("Disabled: Oik's AutoSaver for Blender")
    CONTINUE = False


def _print(string: str) -> None:
    """i got bored...

    Args:
        string (str): string to print
    """
    now = dt.datetime.now().strftime(("%H:%M:%S"))
    print(f"[Oik's AutoSaver]: {now} - {string}")


if __name__ == "__main__":
    register()
