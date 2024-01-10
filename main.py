from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
from rdkit import Chem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import Draw
from rdkit import Chem
from rdkit.Chem import Draw
import datetime
import os
from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image
import io
import hashlib

async def save(path,png_buffer):
    with open(path, 'wb') as f:
        f.write(png_buffer.getvalue())
    return path

async def render(smiles=""):
    path = f"./images/{hashlib.md5(smiles.encode()).hexdigest()}.png"
    if Path(path).is_file():
        return path
    # 创建分子结构
    mol = Chem.MolFromSmiles(smiles)  # 例如，苯

    # 将分子绘制为PNG图像
    png_image = Draw.MolToImage(mol)

    # 将PNG图像保存到字节缓冲区
    png_buffer = io.BytesIO()
    png_image.save(png_buffer, format='PNG')
    path = await save(path=path,png_buffer=png_buffer)
    return path


app = FastAPI()
@app.get("/smilesRender")
async def get_image(smiles=""):
    if smiles == '':
        return {"error": "Please provide a valid SMILES"}

    image_path = await render(smiles=smiles)
    image_path = Path(image_path)
    if not image_path.is_file():
        return {"error": "Image not found on the server"}
    return FileResponse(image_path)
