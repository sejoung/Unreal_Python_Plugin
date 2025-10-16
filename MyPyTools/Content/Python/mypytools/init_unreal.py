import unreal

def _get_viewport_cam():
    loc, rot = unreal.EditorLevelLibrary.get_level_viewport_camera_info()
    return loc, rot

def _get_selected_asset():
    assets = unreal.EditorUtilityLibrary.get_selected_assets()
    return assets[0] if assets else None

def place_from_viewport(distance_cm=120.0, up_offset_cm=0.0):
    world = unreal.EditorLevelLibrary.get_editor_world()
    asset = _get_selected_asset()
    if not asset:
        unreal.log_warning("No asset selected in Content Browser")
        return

    cam_loc, cam_rot = _get_viewport_cam()
    fwd = cam_rot.get_forward_vector()

    spawn_loc = cam_loc + fwd * distance_cm + unreal.Vector(0,0,up_offset_cm)
    spawn_rot = unreal.Rotator(cam_rot.pitch, cam_rot.yaw, 0.0)

    actor = None
    if isinstance(asset, unreal.Blueprint):
        cls = asset.generated_class
        if cls and cls.is_child_of(unreal.Actor):
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, spawn_loc, spawn_rot)
    elif isinstance(asset, unreal.StaticMesh):
        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, spawn_loc, spawn_rot)
        if actor:
            smc = actor.static_mesh_component
            smc.set_static_mesh(asset)
            smc.set_mobility(unreal.ComponentMobility.MOVABLE)

    if actor:
        unreal.GEditor.select_none(False, True, False)
        unreal.GEditor.select_actor(actor, True, True, True)
        unreal.log("Spawned via Python at {}".format(spawn_loc))
    else:
        unreal.log_warning("Unsupported asset type: {}".format(type(asset)))

def _add_toolbar_button():
    menus = unreal.ToolMenus.get()
    toolbar = menus.extend_menu("LevelEditor.LevelEditorToolBar")

    entry = unreal.ToolMenuEntry(
        name="MyPyTools.PyPlace",
        type=unreal.MultiBlockType.TOOL_BAR_BUTTON,
        insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.FIRST)
    )
    entry.set_label("Py Place")
    entry.set_tool_tip("Place selected asset in front of viewport camera")
    entry.set_icon("EditorStyle", "LevelEditor.OpenLevelBlueprint")
    # 버튼을 눌렀을 때 실행할 파이썬 문자열
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type="",
        string="import mypytools.init_unreal as M; M.place_from_viewport()"
    )

    section = toolbar.add_section("MyPyTools", "MyPy Tools")
    section.add_entry(entry)
    menus.refresh_all_widgets()

def _add_context_menu():
    menus = unreal.ToolMenus.get()
    for path in ["ContentBrowser.AssetContextMenu",
                 "ContentBrowser.AssetContextMenu.StaticMesh",
                 "ContentBrowser.AssetContextMenu.SkeletalMesh"]:
        menu = menus.extend_menu(path)
        section = menu.add_section("MyPyToolsCtx", "MyPy Tools")
        entry = unreal.ToolMenuEntry(
            name="MyPyTools.PyPlaceCtx",
            type=unreal.MultiBlockType.MENU_ENTRY
        )
        entry.set_label("Py Place From Camera")
        entry.set_tool_tip("Place selected asset in front of viewport camera")
        entry.set_string_command(
            type=unreal.ToolMenuStringCommandType.PYTHON,
            custom_type="",
            string="import mypytools.init_unreal as M; M.place_from_viewport()"
        )
        section.add_entry(entry)
    menus.refresh_all_widgets()

# 에디터 시작 시 한 번 등록
_add_toolbar_button()
_add_context_menu()
unreal.log("MyPyTools initialized")
