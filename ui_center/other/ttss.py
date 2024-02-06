import json
# import unreal

path = r"D:\temp\ue\ma_json\all.json"


def read_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data


def main():
    actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    if not actors:
        unreal.log_error("Please Select Actor")
        return

    trans_data = read_json(path)

    key_list = []
    for key, value in trans_data.items():
        key_list.append(key)
    
    for actor in actors:
        component_list = actor.get_components_by_class(unreal.StaticMeshComponent)
        for static_mesh_component in component_list:
            static_mesh = static_mesh_component.static_mesh
            print(static_mesh)
            mesh_name = static_mesh.get_name()
            split_index = mesh_name.index("geo")
            ue_mesh_name = "geo_" + mesh_name[split_index + 4:]

            if ue_mesh_name[-1].isdigit():
                _name = ue_mesh_name[:-2]
                master_num = ue_mesh_name[-1]
                result = [item for item in key_list if _name in item]
                for item in result:
                    if item.split(":")[0][-1] == master_num:
                        mesh_value = trans_data.get(item)

            else:
                result = [item for item in key_list if ue_mesh_name in item]
                for item in result:
                    if item.split(":")[0][-1].isalpha() and ue_mesh_name in item:
                        mesh_value = trans_data.get(item)

            transform = mesh_value['transform']
            rotation = mesh_value['rotation']
            scacle = mesh_value['scacle']

            location = unreal.Vector(transform[0], transform[2], transform[1])
            rotation = unreal.Rotator(rotation[0], rotation[2], rotation[1])
            scale = unreal.Vector(scacle[0], scacle[1], scacle[2])

            static_mesh_component.set_editor_property('relative_location', location)
            static_mesh_component.set_editor_property('relative_rotation', rotation)
            static_mesh_component.set_editor_property('relative_scale3d', scale)


        unreal.log("Successful")
