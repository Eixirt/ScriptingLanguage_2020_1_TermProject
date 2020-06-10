from tkinter import *
from tkinter import filedialog
import webbrowser
import folium


def OpenBrowerForMap(mapx, mapy, zoom_start_val, title):
    # 위도 경도 지정
    map_osm = folium.Map(location=[mapx, mapy], zoom_start=zoom_start_val)
    # 마커 지정
    folium.Marker([37.3402849, 126.7313189], popup=title).add_to(map_osm)
    # html 파일로 저장
    map_osm.save('osm.html')
    webbrowser.open_new('osm_html')
    pass


# 콘솔에 출력, 테스트용
def ProcessOpenFile(file_path):
    if file_path != "":
        with open(file_path, "r") as testr:
            for line in testr:
                print(line)
    pass

