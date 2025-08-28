from PIL import Image
from pathlib import Path
import pytesseract

class OCR():
    def __init__(self, maps = [
        "hillofswords", "crystalchapel", 
        "doubledungeon", "driedlake", "antisland", "edgeofheaven", "goldencastle",
        "kuinshipalace", "landofthegods", "planetnamak", "ruinedcity", 
        "sandvillage", "shibuyaaftermath", "shibuyastation",
        "shiningcastle", "spiderforest", "spiritsociety", 
        "suntemple", "tracksattheedgeoftheworlda", "tracksattheedgeoftheworldb",
        "undergroundchurch"
        ], ):
        self.maps = maps

    def normalize(self, text: str) -> str:
        return "".join(text.lower().split())

    def ocrMatch(self):
        img_folder = Path("Sect/Images")
        text = pytesseract.image_to_string(Image.open(f'{img_folder}/OCR_TEST.jpg'), lang="eng") # THIS IS JUST A TEST
        norm_text = self.normalize(text)
        for i in self.maps:
            if (i in norm_text):
                print("Match!")
        return norm_text