import os

from pxr import Usd, UsdGeom, UsdLux

dir_path = os.path.dirname(__file__)
stage_file_path = os.path.join(dir_path, './assets/first_stage.usda')
stage = None

def init_default():
    os.makedirs(os.path.dirname(stage_file_path), exist_ok=True)

    stage: Usd.Stage = Usd.Stage.CreateNew(stage_file_path)

    # Create cube geometry
    geom_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, '/Geometry')
    xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, geom_scope.GetPath().AppendPath('GroupTransform')) 
    cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, xform.GetPath().AppendPath('Box'))

    # Create lights
    light_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, '/Lights')
    UsdLux.DomeLight.Define(stage, light_scope.GetPath().AppendPath('DomeLight')) 
    UsdLux.DistantLight.Define(stage, light_scope.GetPath().AppendPath('Sun'))

    stage.Save()

    print(f'Stage created: {stage.ExportToString()}')

def traverse_all_path():
    global stage
    # Traverses in a DFS approach
    for prim in stage.Traverse():
        print(prim.GetPath())

def list_cube_attrs(cube):
    # Get list of default attributes
    cube_attrs = cube.GetSchemaAttributeNames()
    for attr in cube_attrs:
        print(attr)

def change_cube_color(cube):
    cube_attr_color: Usd.Attribute = cube.GetDisplayColorAttr()
    cube_attr_color.Set([(1.0, 0.0, 0.0)]) # Sets an opinion

def change_cube_size(cube):
    # Get 'size' attribute
    cube_size_attr: Usd.Attribute = cube.GetSizeAttr()
    cube_size_attr.Set(cube_size_attr.Get()*2)

def add_child_to_prim():
    global stage
    geom_scope: UsdGeom.Scope = stage.GetPrimAtPath('/Geometry/GroupTransform')
    small_box: UsdGeom.Cube = UsdGeom.Cube.Define(stage, geom_scope.GetPath().AppendPath('Small_Box'))
    UsdGeom.XformCommonAPI(small_box).SetTranslate((4 , 5, 4))

def check_prim_exist():
    global stage
    prim: Usd.Prim = stage.GetPrimAtPath('/Geometry')
    child_prim: Usd.Prim

    if child_prim := prim.GetChild('Box'):
        print('Box child prim exist')
    else:
        # Prints DOES NOT EXIST cause it checks only direc children of prim
        print('Child prim Box DOES NOT EXIST')

def main():
    if not os.path.exists(stage_file_path):
        init_default()
    
    global stage
    
    stage = Usd.Stage.Open(stage_file_path)

    # Get cube by prim path
    cube: UsdGeom.Cube = UsdGeom.Cube(stage.GetPrimAtPath('/Geometry/GroupTransform/Box'))

    list_cube_attrs(cube)
    change_cube_color(cube)
    change_cube_size(cube)
    add_child_to_prim()
    traverse_all_path()
    check_prim_exist()

    stage.Save()


if __name__ == '__main__':
    main()