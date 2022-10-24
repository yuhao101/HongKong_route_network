#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: zhangyuhao
@file: handle_simulator_animation.py
@time: 2022/8/22 下午11:54
@email: yuhaozhang76@gmail.com
@desc: 
"""
import json
from tqdm import tqdm
import osmnx as ox
# G = ox.load_graphml('./hongkong/hongkong.graphml')
# gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
# lat_list = gdf_nodes['y'].tolist()
# lng_list = gdf_nodes['x'].tolist()
# node_id = gdf_nodes.index.tolist()
# node_id_to_lat_lng = {}
# for i in range(len(lat_list)):
#     node_id_to_lat_lng[node_id[i]] = (lng_list[i], lat_list[i])
#

def split_total_simulator_result():
    raw_data = json.load(open('./hongkong/simulator_animation_adjust.json', 'r'))['data']
    line_trajectory_data = {'data':[]}
    node_trajectory_data = {'data':[]}
    car_trajectory_data = {'data':[]}
    try:
        for item in raw_data:
            if item['time_list'][0]>72000:
                car_trajectory_data['data'].append(item)
            elif item['time_list'][0]>64800:
                node_trajectory_data['data'].append(item)
            else:
                line_trajectory_data['data'].append(item)
    except:
        print(item)
    file = open('./hongkong/simulator_line.json', 'w')
    file.write(json.dumps(line_trajectory_data, indent=1, ensure_ascii=False))
    file = open('./hongkong/simulator_node.json', 'w')
    file.write(json.dumps(node_trajectory_data, indent=1, ensure_ascii=False))
    file = open('./hongkong/simulator_car.json', 'w')
    file.write(json.dumps(car_trajectory_data, indent=1, ensure_ascii=False))


def adjust_route():
    start = [22.320547, 114.126400]
    end = [22.330291, 114.112897]
    x = ox.distance.get_nearest_node(G, start, method=None, return_dist=False)
    y = ox.distance.get_nearest_node(G, end, method=None, return_dist=False)
    print(x)
    print(y)
    ite = ox.shortest_path(G, x, y, weight='length', cpus=16)
    print(ite)
    re = []
    for item in ite:
       re.append(list(node_id_to_lat_lng[item]))
    print(re)

'''
桥3-正方向：[114.181221, 22.3044369], [114.18204, 22.28261]
修正-正方向：[[114.181221, 22.3044369],[114.180221, 22.3024369],[114.181675, 22.293215], [114.182605, 22.287711],[114.183015, 22.284615],[114.18204, 22.28261]];
桥3-反方向：[[114.18234, 22.28306], [114.1807029, 22.3037154]]
修正-反方向：[[114.18234, 22.28306], [114.183085,22.283752], [114.182428,22.289054], [114.181373,22.294889],[114.180808,22.298419],[114.1807029, 22.3037154]]
桥2-正方向：[114.1590512, 22.3036855], [114.142394, 22.2897197]
修正-正方向：[[114.1590512, 22.3036855], [114.152923, 22.297185],[114.148813, 22.292717],[114.146193, 22.289888],[114.143574, 22.289391],[114.142394, 22.2897197]]
桥2-反方向：[[114.14246, 22.28986], [114.1575932, 22.3024532]]
修正-反方向：[[114.14246, 22.28986],[114.144823,22.289325],[114.146142,22.289908], [114.1575932, 22.3024532]]
桥1-正方向：[[114.1297249, 22.3210497], [114.1133518, 22.3295913]]
修正-正方向：[[114.1297249, 22.3210497],[114.127613, 22.320299],[114.125500, 22.320604], [114.123762, 22.321733],[114.117984, 22.326252],[114.1133518, 22.3295913]]
桥1-反方向：[[114.113875, 22.3294957], [114.1296272, 22.3212047]]
修正-反方向：[[114.113875, 22.3294957],[114.117464,22.326388],[114.119872,22.324585],[114.126435,22.320290],[ 114.128384,22.320290], [114.1296272, 22.3212047]]
删除：[[114.1768632, 22.2827101], [114.1933534, 22.2918868]]
'''

bridge3_1 = [[114.181221, 22.3044369],[114.180221, 22.3024369],[114.181675, 22.293215], [114.182605, 22.287711],[114.183015, 22.284615],[114.18204, 22.28261]]
bridge3_2 = [[114.18234, 22.28306], [114.183085,22.283752], [114.182428,22.289054], [114.181373,22.294889],[114.180808,22.298419],[114.1807029, 22.3037154]]
bridge2_1 = [[114.1590512, 22.3036855], [114.152923, 22.297185],[114.148813, 22.292717],[114.146193, 22.289888],[114.143574, 22.289391],[114.142394, 22.2897197]]
bridge2_2 = [[114.14246, 22.28986],[114.144823,22.289325],[114.146142,22.289908], [114.1575932, 22.3024532]]
bridge1_1 = [[114.1297249, 22.3210497],[114.127613, 22.320299],[114.125500, 22.320604], [114.123762, 22.321733],[114.117984, 22.326252],[114.1133518, 22.3295913]]
bridge1_2 = [[114.113875, 22.3294957],[114.117464,22.326388],[114.119872,22.324585],[114.126435,22.320290],[ 114.128384,22.320290], [114.1296272, 22.3212047]]
def handle_route():
    data = json.load(open('./hongkong/simulator_animation.json', 'r'))['data']
    re = {'data':[]}
    for item in tqdm(data):
        judge = True
        temp_re = {'time_list':[],'traj_list':[],'type':item['type']}
        time = item['time_list']
        route = item['traj_list']
        if len(item['time_list']) < 2:
            continue
        if [22.2827101,114.1768632] in route or [22.2918868,114.1933534] in route:
            continue
        # 桥3
        if [22.3044369,114.181221] in route and [22.28261,114.18204] in route:
            for i in range(len(time)):
                temp_re['time_list'].append(time[i])
                temp_re['traj_list'].append(route[i])
                if route[i] == [22.3044369, 114.181221] and i < len(time)-1:
                    time_interval = (time[i+1]-time[i])/(len(bridge3_1)-1)
                    temp_time = time[i]
                    for item2 in bridge3_1[1:-1]:
                        temp_time += time_interval
                        temp_re['time_list'].append(temp_time)
                        temp_re['traj_list'].append([item2[1],item2[0]])
                    temp_re['time_list'] += time[i+1:]
                    temp_re['traj_list'] += route[i+1:]
                    break
            route = temp_re['traj_list']
            time = temp_re['time_list']
        if [22.28306,114.18234] in route and [22.3037154, 114.1807029] in route:
            temp_re = {'time_list': [], 'traj_list': [], 'type': item['type']}
            for i in range(len(time)):
                temp_re['time_list'].append(time[i])
                temp_re['traj_list'].append(route[i])
                if route[i] == [22.28306,114.18234] and i < len(time)-1:
                    time_interval = (time[i+1]-time[i])/(len(bridge3_2)-1)
                    temp_time = time[i]
                    for item2 in bridge3_2[1:-1]:
                        temp_time += time_interval
                        temp_re['time_list'].append(temp_time)
                        temp_re['traj_list'].append([item2[1],item2[0]])
                    temp_re['time_list'] += time[i+1:]
                    temp_re['traj_list'] += route[i+1:]
                    break
            route = temp_re['traj_list']
            time = temp_re['time_list']
        if [22.3036855,114.1590512] in route and [22.2897197,114.142394] in route:
            temp_re = {'time_list': [], 'traj_list': [], 'type': item['type']}
            for i in range(len(time)):
                temp_re['time_list'].append(time[i])
                temp_re['traj_list'].append(route[i])
                if route[i] == [22.3036855,114.1590512] and i < len(time)-1:
                    time_interval = (time[i+1]-time[i])/(len(bridge2_1)-1)
                    temp_time = time[i]
                    for item2 in bridge2_1[1:-1]:
                        temp_time += time_interval
                        temp_re['time_list'].append(temp_time)
                        temp_re['traj_list'].append([item2[1],item2[0]])
                    temp_re['time_list'] += time[i+1:]
                    temp_re['traj_list'] += route[i+1:]
                    break
            route = temp_re['traj_list']
            time = temp_re['time_list']
        if [22.28986,114.14246] in route and [22.3024532,114.1575932] in route:
            temp_re = {'time_list': [], 'traj_list': [], 'type': item['type']}
            for i in range(len(time)):
                temp_re['time_list'].append(time[i])
                temp_re['traj_list'].append(route[i])
                if route[i] == [22.28986,114.14246] and i < len(time)-1:
                    time_interval = (time[i+1]-time[i])/(len(bridge2_2)-1)
                    temp_time = time[i]
                    for item2 in bridge2_2[1:-1]:
                        temp_time += time_interval
                        temp_re['time_list'].append(temp_time)
                        temp_re['traj_list'].append([item2[1],item2[0]])
                    temp_re['time_list'] += time[i+1:]
                    temp_re['traj_list'] += route[i+1:]
                    break
            route = temp_re['traj_list']
            time = temp_re['time_list']
        if [22.3210497,114.1297249] in route and [22.3295913,114.1133518] in route:
            temp_re = {'time_list': [], 'traj_list': [], 'type': item['type']}
            for i in range(len(time)):
                temp_re['time_list'].append(time[i])
                temp_re['traj_list'].append(route[i])
                if route[i] == [22.3210497,114.1297249] and i < len(time)-1:
                    time_interval = (time[i+1]-time[i])/(len(bridge1_1)-1)
                    temp_time = time[i]
                    for item2 in bridge1_1[1:-1]:
                        temp_time += time_interval
                        temp_re['time_list'].append(temp_time)
                        temp_re['traj_list'].append([item2[1],item2[0]])
                    temp_re['time_list'] += time[i+1:]
                    temp_re['traj_list'] += route[i+1:]
                    break
            route = temp_re['traj_list']
            time = temp_re['time_list']
        if [22.3294957,114.113875] in route and [ 22.3212047,114.1296272] in route:
            temp_re = {'time_list': [], 'traj_list': [], 'type': item['type']}
            for i in range(len(time)):
                temp_re['time_list'].append(time[i])
                temp_re['traj_list'].append(route[i])
                if route[i] == [22.3294957,114.113875] and i < len(time)-1:
                    time_interval = (time[i+1]-time[i])/(len(bridge1_2)-1)
                    temp_time = time[i]
                    for item2 in bridge1_2[1:-1]:
                        temp_time += time_interval
                        temp_re['time_list'].append(temp_time)
                        temp_re['traj_list'].append([item2[1],item2[0]])
                    temp_re['time_list'] += time[i+1:]
                    temp_re['traj_list'] += route[i+1:]
                    break
            route = temp_re['traj_list']
            time = temp_re['time_list']
        if temp_re['traj_list'] == []:
            temp_re = {'time_list': [], 'traj_list': [], 'type': item['type']}
            for j in range(len(time)-1):
                if (time[j+1] - time[j]) > 100:
                    judge = False
                    break
            for i in range(len(route)-1):
                temp_re['time_list'].append(time[i])
                temp_re['traj_list'].append(route[i])
                range_num = 0.004
                if abs(route[i][1] - 114.181221) < range_num and abs(route[i+1][1] - 114.18204) < range_num\
                       and abs(route[i][0] - 22.3044369) < range_num and abs(route[i+1][0] - 22.28261) < range_num:
                    time_interval = (time[i + 1] - time[i]) / (len(bridge3_1) + 1)
                    temp_time = time[i]
                    for item2 in bridge3_1:
                        temp_time += time_interval
                        temp_re['time_list'].append(temp_time)
                        temp_re['traj_list'].append([item2[1], item2[0]])
                    temp_re['time_list'] += time[i + 1:]
                    temp_re['traj_list'] += route[i + 1:]
                    print('bridge31')
                    print(temp_re['traj_list'])
                    break
                elif abs(route[i][1] - 114.18234) < range_num and abs(route[i+1][1] - 114.1807029) < range_num\
                        and abs(route[i][0] - 22.28306) < range_num and abs(route[i+1][0] - 22.3037154) < range_num:
                    time_interval = (time[i + 1] - time[i]) / (len(bridge3_2) +1)
                    temp_time = time[i]
                    for item2 in bridge3_2:
                        temp_time += time_interval
                        temp_re['time_list'].append(temp_time)
                        temp_re['traj_list'].append([item2[1], item2[0]])
                    temp_re['time_list'] += time[i + 1:]
                    temp_re['traj_list'] += route[i + 1:]
                    print('bridge32')
                    print(temp_re['traj_list'])
                    break
                elif abs(route[i][1] - 114.1590512) < range_num and abs(route[i+1][1] - 114.142394) < range_num\
                        and abs(route[i][0] - 22.3036855) < range_num and abs(route[i+1][0] - 22.2897197) < range_num:
                    time_interval = (time[i + 1] - time[i]) / (len(bridge2_1) +1)
                    temp_time = time[i]
                    for item2 in bridge2_1:
                        temp_time += time_interval
                        temp_re['time_list'].append(temp_time)
                        temp_re['traj_list'].append([item2[1], item2[0]])
                    temp_re['time_list'] += time[i + 1:]
                    temp_re['traj_list'] += route[i + 1:]
                    print('bridge21')
                    print(temp_re['traj_list'])
                    break
                elif abs(route[i][1] - 114.14246) < range_num and abs(route[i+1][1] - 114.1575932) < range_num\
                        and abs(route[i][0] - 22.28986) < range_num and abs(route[i+1][0] - 22.3024532) < range_num:
                    time_interval = (time[i + 1] - time[i]) / (len(bridge2_2) + 1)
                    temp_time = time[i]
                    for item2 in bridge2_2:
                        temp_time += time_interval
                        temp_re['time_list'].append(temp_time)
                        temp_re['traj_list'].append([item2[1], item2[0]])
                    temp_re['time_list'] += time[i + 1:]
                    temp_re['traj_list'] += route[i + 1:]
                    print('bridge22')
                    print(temp_re['traj_list'])
                    break
                elif abs(route[i][1] - 114.1297249) < range_num and abs(route[i+1][1] - 114.1133518) < range_num\
                        and abs(route[i][0] - 22.3210497) < range_num and abs(route[i+1][0] - 22.3295913) < range_num:
                    time_interval = (time[i + 1] - time[i]) / (len(bridge1_1) + 1)
                    temp_time = time[i]
                    for item2 in bridge1_1:
                        temp_time += time_interval
                        temp_re['time_list'].append(temp_time)
                        temp_re['traj_list'].append([item2[1], item2[0]])
                    temp_re['time_list'] += time[i + 1:]
                    temp_re['traj_list'] += route[i + 1:]
                    print('bridge11')
                    print(temp_re['traj_list'])
                    break
                elif abs(route[i][1] -114.113875) < range_num and abs(route[i+1][1] -114.1296272) < range_num\
                        and abs(route[i][0] -22.3294957) < range_num and abs(route[i+1][0] - 22.3212047) < range_num:
                    time_interval = (time[i + 1] - time[i]) / (len(bridge1_2) + 1)
                    temp_time = time[i]
                    for item2 in bridge1_2:
                        temp_time += time_interval
                        temp_re['time_list'].append(temp_time)
                        temp_re['traj_list'].append([item2[1], item2[0]])
                    temp_re['time_list'] += time[i + 1:]
                    temp_re['traj_list'] += route[i + 1:]
                    print('bridge12')
                    print(temp_re['traj_list'])
                    break
        # if temp_re['time_list'] == []:
        #     temp_re = item
        if judge:
            re['data'].append(temp_re)
    file = open('./hongkong/simulator_animation_adjust.json', 'w')
    file.write(json.dumps(re,indent=1,ensure_ascii=False))
        # for i in range(len(time)):
        #     if route[i]

def handle_route_test():
    data = json.load(open('./hongkong/simulator_animation.json', 'r'))['data']
    re = {'data':[]}
    for item in tqdm(data):
        judge = True
        temp_re = {'time_list':[],'traj_list':[],'type':item['type']}
        time = item['time_list']
        route = item['traj_list']
        if len(item['time_list']) < 2:
            continue
        if [22.2827101,114.1768632] in route or [22.2918868,114.1933534] in route:
            continue
        # 桥3

        22.283424, 114.180725
        22.292167, 114.193352

        temp_re = {'time_list': [], 'traj_list': [], 'type': item['type']}
        # for j in range(len(time)-1):
        #     if (time[j+1] - time[j]) > 100:
        #         judge = False
        #         break
        for i in range(len(route)-1):
            range_num = 0.004
            if abs(route[i][1] - 114.193352) < range_num and abs(route[i + 1][1] - 114.180725) < range_num \
                    and abs(route[i][0] - 22.292167) < range_num and abs(route[i + 1][0] - 22.283424) < range_num:
                judge = False
                break
            temp_re['time_list'].append(time[i])
            temp_re['traj_list'].append(route[i])
            if abs(route[i][1] - 114.181221) < range_num and abs(route[i+1][1] - 114.18204) < range_num\
                   and abs(route[i][0] - 22.3044369) < range_num and abs(route[i+1][0] - 22.28261) < range_num:
                time_interval = (time[i + 1] - time[i]) / (len(bridge3_1) +1)
                temp_time = time[i]
                for item2 in bridge3_1:
                    temp_time += time_interval
                    temp_re['time_list'].append(temp_time)
                    temp_re['traj_list'].append([item2[1], item2[0]])
                print('bridge31')
                print(temp_re['traj_list'])
            elif abs(route[i][1] - 114.18234) < range_num and abs(route[i+1][1] - 114.1807029) < range_num\
                    and abs(route[i][0] - 22.28306) < range_num and abs(route[i+1][0] - 22.3037154) < range_num:
                time_interval = (time[i + 1] - time[i]) / (len(bridge3_2) +1)
                temp_time = time[i]
                for item2 in bridge3_2:
                    temp_time += time_interval
                    temp_re['time_list'].append(temp_time)
                    temp_re['traj_list'].append([item2[1], item2[0]])
                print('bridge32')
                print(temp_re['traj_list'])
            elif abs(route[i][1] - 114.1590512) < range_num and abs(route[i+1][1] - 114.142394) < range_num\
                    and abs(route[i][0] - 22.3036855) < range_num and abs(route[i+1][0] - 22.2897197) < range_num:
                time_interval = (time[i + 1] - time[i]) / (len(bridge2_1) +1)
                temp_time = time[i]
                for item2 in bridge2_1:
                    temp_time += time_interval
                    temp_re['time_list'].append(temp_time)
                    temp_re['traj_list'].append([item2[1], item2[0]])
                print('bridge21')
                print(temp_re['traj_list'])
            elif abs(route[i][1] - 114.14246) < range_num and abs(route[i+1][1] - 114.1575932) < range_num\
                    and abs(route[i][0] - 22.28986) < range_num and abs(route[i+1][0] - 22.3024532) < range_num:
                time_interval = (time[i + 1] - time[i]) / (len(bridge2_2) +1)
                temp_time = time[i]
                for item2 in bridge2_2:
                    temp_time += time_interval
                    temp_re['time_list'].append(temp_time)
                    temp_re['traj_list'].append([item2[1], item2[0]])
                print('bridge22')
                print(temp_re['traj_list'])
            elif abs(route[i][1] - 114.1297249) < range_num and abs(route[i+1][1] - 114.1133518) < range_num\
                    and abs(route[i][0] - 22.3210497) < range_num and abs(route[i+1][0] - 22.3295913) < range_num:
                time_interval = (time[i + 1] - time[i]) / (len(bridge1_1) + 1)
                temp_time = time[i]
                for item2 in bridge1_1:
                    temp_time += time_interval
                    temp_re['time_list'].append(temp_time)
                    temp_re['traj_list'].append([item2[1], item2[0]])

                print('bridge11')
                print(temp_re['traj_list'])
            elif abs(route[i][1] -114.113875) < range_num and abs(route[i+1][1] -114.1296272) < range_num\
                    and abs(route[i][0] -22.3294957) < range_num and abs(route[i+1][0] - 22.3212047) < range_num:
                time_interval = (time[i + 1] - time[i]) / (len(bridge1_2) +1)
                temp_time = time[i]
                for item2 in bridge1_2:
                    temp_time += time_interval
                    temp_re['time_list'].append(temp_time)
                    temp_re['traj_list'].append([item2[1], item2[0]])

                print('bridge12')
                print(temp_re['traj_list'])
        # if temp_re['time_list'] == []:
        #     temp_re = item
        if judge:
            re['data'].append(temp_re)
    file = open('./hongkong/simulator_animation_adjust.json', 'w')
    file.write(json.dumps(re,indent=1,ensure_ascii=False))
        # for i in range(len(time)):
        #     if route[i]

def extract_pickup_cruising_data():
    re = {'data':[]}

    data = json.load(open('./hongkong/simulator_animation_adjust.json','r'))['data']
    temp_data = []
    for item in tqdm(data):
        if item['type'] == 0.0 and len(re['data']) < 500:
            if [22.3044369,114.181221] in item['traj_list'] or [22.28306,114.18234] in item['traj_list'] or [22.3036855,114.1590512] in item['traj_list'] or [ 22.28986,114.14246] in item['traj_list'] or [22.3210497,114.1297249] in item['traj_list'] or [22.3294957,114.1297249] in item['traj_list']:
                temp_data.append(item)
    # data = json.load(open('./hongkong/simulator_car.json', 'r'))['data']
    for item in tqdm(data):
        if len(re['data']) < 5000:
            re['data'].append(item)
        if len(re['data'])%20 == 0 and len(re['data']) > 20 and len(re['data']) < 1000:
            print(len(re['data']))
            re['data'].append(temp_data[int(len(re['data'])/20)])
    print(len(re['data']))
    file = open('./hongkong/simulator_car_adjust.json', 'w')
    file.write(json.dumps(re, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    # adjust_route()
    # handle_route_test()
    # split_total_simulator_result()
    extract_pickup_cruising_data()