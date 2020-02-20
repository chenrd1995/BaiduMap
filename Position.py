import requests, re, time
import geopandas as gpd
import pandas as pd
import shapely
from GCJ20WGS84 import bd09_to_wgs84


def BaiduMapQuery(region, city, key):
    """
    通过百度地图API查询某城市某区域的经纬度坐标
    :param region: 区域名
    :param city: 所在城市
    :param key: 百度地图API的开发者key
    :return:
    如果有返回：
    [0, [区域名, 百度地图所查询到的地址, longitude, latitude]]
    如果没有返回
    [1, "百度地图未找到这个地点"]
    """
    # https://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi 开发文档
    coordinate_url = "http://api.map.baidu.com/place/v2/search?query={}&region={}&page_size=1&ak={}".format(
        region, city, key)
    request = requests.get(coordinate_url)
    status = int(re.findall('<status>\s*(\d?)</status>', request.text)[0])
    if (status == 0):
        longitude = re.findall('<lng>\s*(.+?)</lng>', request.text)
        latitude = re.findall('<lat>\s*(.+?)</lat>', request.text)
        if (longitude != []):
            pos = bd09_to_wgs84(float(longitude[0]), float(latitude[0]))
            longitude = pos[0]
            latitude = pos[1]
        else:
            print("没有坐标信息!")
            return [1, "没有坐标信息!"]
        address = re.findall('<address>\s*(.+?)</address>', request.text)
        if (address != []):
            address = address[0]
        else:
            print("没有位置信息!")
            return [1, [region, "没有位置信息!", longitude, latitude]]
        print([region, address, longitude, latitude])
        time.sleep(0.1)
        return ([status, [region, address, longitude, latitude]])
    else:
        message = re.findall('<message>\s*(.+?)</message>', request.text)[0]
        print(message)
        time.sleep(0.05)
        return ([status, "百度地图未找到这个地点"])


def Query2Shp(query_list, out_path):
    """

    :param query_list: 查询到的列表
    :param out_path: 输出位置
    :return: geopandas 格式的shp文件属性表
    """
    df = pd.DataFrame(query_list)
    df.rename(columns={0: '名称', 1: 'address', 2: 'longitude', 3: 'latitude'}, inplace=True)
    geom = [shapely.geometry.Point(xy) for xy in zip(df.longitude.astype(float), df.latitude.astype(float))]
    gdf = gpd.GeoDataFrame(df, geometry=geom)
    gdf.to_file(out_path, encoding="UTF-8")
    return gdf


if __name__ == '__main__':
    ## excel的路径
    excel_path = "./工业园区列表.xlsx"
    ## 需要用到的表名
    sheet_name = "筛选出区域"
    ## 所在城市的列名
    city_name = "城市"
    ## 厂区的列名
    region_name = "名称"
    ## 百度地图开放平台所得到的key
    key = ""
    ## 输出的shp文件名
    out_path = "./result.shp"

    excel_df = pd.read_excel(excel_path, sheet_name=sheet_name)
    query_list = []
    for i in range(len(excel_df)):
        region = excel_df[region_name][i]
        city = excel_df[city_name][i]
        query_result = BaiduMapQuery(region, city, key)
        if (query_result[0] == 0):
            query_list.append(query_result[1])

    point_position_shp = Query2Shp(query_list, out_path)
