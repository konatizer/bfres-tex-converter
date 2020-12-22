import os
import subprocess
from libyaz0 import decompress
import bfres
import bntx


def downscale_all_dds(directory="."):

    dds_files = list()
    for file in os.listdir("./dds/"):
        if os.path.splitext(file)[1] == ".dds":
            dds_files.append(file)

    for dds in dds_files:
        subprocess.call(["convert", "-resize", "512", dds])


def textures_from_sbfres_wiiu(sbfres_path):
    fin = open(sbfres_path, "rb")
    if not fin:
        print("File not found - " + sbfres_path)
        return False
    compressed_texture = fin.read()
    uncompressed_texture = decompress(compressed_texture)
    bfres_file = bfres.read(uncompressed_texture)
    if not bfres_file:
        print("bfres read failed - " + sbfres_path)
        return False

    textures, _ = bfres_file
    return textures


def textures_from_sbfres_switch(sbfres_path):
    fin = open(sbfres_path, "rb")
    if not fin:
        print("File not found - " + sbfres_path)
        return False
    compressed_texture = fin.read()
    uncompressed_texture = decompress(compressed_texture)

    # switch specific
    bntx_file = bntx.bntx_from_bfres(uncompressed_texture)
    name, target, textures, texNames = bntx.read(bntx_file)
    return textures, texNames


def extract_dds_from_bfres(outdir, textures, check=False):
    if not textures:
        return False

    for tex in textures:
        bfres.extract(tex, outdir)

    if check:
        for tex in textures:
            if not (os.path.isfile(str(outdir + tex.name + ".dds"))):
                print("Failed to generate file " + tex.name + ".dds")


def convert_tex(filepath):

    wiiu_modded_textures_path = "./wiiu-textures/"
    switch_original_textures_path = "./dump/botw/romfs/Model/"

    wiiu_tex_ext = ".Tex1.sbfres"
    switch_tex_ext = ".Tex.sbfres"

    if not os.path.isfile(wiiu_modded_textures_path+filepath+wiiu_tex_ext):
        print("invalid wiiu tex - " + filepath)
        return False 

    if not os.path.isfile(switch_original_textures_path + filepath + switch_tex_ext):
        print("switch tex not found - " + filepath)
        return False
        
        

    # ========================== #
    # WII U PORTION
    # ========================== #

    wiiu_textures = textures_from_sbfres_wiiu(
            wiiu_modded_textures_path +
            filepath +
            wiiu_tex_ext
            )

    wiiu_tex_names = []

    for tex in wiiu_textures:
        wiiu_tex_names.append(tex.name)

    switch_textures, switch_tex_names = textures_from_sbfres_switch(
            switch_original_textures_path +
            filepath +
            switch_tex_ext
            )

    # compare wii u and switch tex names
    if not len(wiiu_tex_names) == len(switch_tex_names):
        print("tex count mismatch for " + filepath + 
                " (wiiu tex count: "    + str(len(wiiu_tex_names)) + 
                " | switch tex count: " + str(len(switch_tex_names)) + ")")

    # export all wii u tex to dds
    # scale each wii u tex size down by 0.5 using convert cmd
    # inject new tex back into bntx
    # inject new bntx back into switch bfres
    # recompress switch bfres -> sbfres
    # done

    # clear dds folder after we're done


def get_texname(path):
    while '.' in path:
        path = os.path.splitext(path)[0]
    return path


def main():

    # for each file in given folder
    for f in os.listdir("./wiiu-textures"):
        # extract .dds from wiiu bfres, place in ./dds/
        convert_tex(get_texname(f))

        # downscale

        # acquire SWITCH bfres w/ matching name

        # embed dds files w/ matching names

        # recompress bfres into sbfres


if __name__ == "__main__":
    main()
