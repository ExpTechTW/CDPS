import os
import zipfile


def pack(args, quiet):
    folder_path = "./plugins/{}".format(args.name)
    output_path = "./plugins/{}.cdps".format(args.name)

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file_path = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, zip_file_path)
    print(f"文件夾 '{folder_path}' 已壓縮為 '{output_path}'")
