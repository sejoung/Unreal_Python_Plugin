import os
from os import mkdir

import unreal

ROOT_PATH = "C:/logs"

# 로그 파일 저장 경로
LOG_FILE = os.path.join(ROOT_PATH, "broken_static_mesh_and_materials.txt")

mkdir(ROOT_PATH)

actors = unreal.EditorLevelLibrary.get_all_level_actors()
# 파일 열기 (쓰기 모드, UTF-8 인코딩)
with open(LOG_FILE, "w", encoding="utf-8") as log_file:
    for actor in actors:
        if not isinstance(actor, unreal.StaticMeshActor):
            continue

        sm_comp = actor.static_mesh_component
        static_mesh = sm_comp.get_editor_property("static_mesh")

        if not static_mesh:
            masssage = f"[MissingMesh] {actor.get_name()} has no StaticMesh"
            log_file.write(masssage + "\n")  # 파일에 저장
            unreal.log(masssage)

        mats = sm_comp.get_materials()
        for i, mat in enumerate(mats):
            if not mat:
                masssage = f"Slot {i} [Miss Materials] {actor.get_name()} has no Materials"
                log_file.write(masssage + "\n")  # 파일에 저장
                unreal.log(masssage)
